"""삼중(三重) 중복 업로드 가드.

같은 상품 3종으로 같은 쇼츠를 다시 만들지 않도록 세 겹으로 잠근다.

1단계(로컬)   : daily_state.json 의 used_items_by_theme / published_titles
2단계(원격 도감): gooditem-archive 의 history.json 에 이미 등록된 item_id
3단계(유튜브) : 채널 RSS 에 이미 게시된 영상 제목

2·3단계는 네트워크가 일시적으로 실패해도 작업이 멈추지 않도록
로컬 파일(web/history.json)과 로컬 상태로 안전하게 폴백한다.
폴백이 일어나면 어떤 근거로 판단했는지 로그로 남긴다.
"""

import json
import re
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

import config
from episode_builder import build_episode_title, normalize_title

CHANNEL_ID = "UCuzNtUgtrJyPumZ5HGd-m0g"
RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
REMOTE_ARCHIVE_URL = (
    "https://raw.githubusercontent.com/ehdnsj96/gooditem-archive/main/history.json"
)
LOCAL_ARCHIVE_FILE = config.BASE_DIR / "web" / "history.json"
USER_AGENT = "Mozilla/5.0 (compatible; dongap-lab-guard/1.0)"


def _http_get(url: str, timeout: float = 8.0) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return res.read().decode("utf-8", errors="replace")


# ---------------------------------------------------------------- 유튜브 RSS
def fetch_published_titles(timeout: float = 8.0) -> Tuple[Set[str], bool]:
    """유튜브 채널 RSS 에서 이미 게시된 영상 제목 집합을 읽는다.

    Returns: (정규화된 제목 집합, 성공 여부)
    """
    try:
        xml = _http_get(RSS_URL, timeout=timeout)
    except Exception as e:  # 네트워크·일시 장애 → 호출 측이 로컬 상태로 폴백
        print(f"⚠️ [가드3] 유튜브 RSS 조회 실패 → 로컬 상태로 폴백합니다: {e}")
        return set(), False

    titles: Set[str] = set()
    for entry in re.findall(r"<entry>(.*?)</entry>", xml, re.S):
        m = re.search(r"<title>(.*?)</title>", entry, re.S)
        if m:
            raw = m.group(1)
            raw = (
                raw.replace("&amp;", "&")
                .replace("&lt;", "<")
                .replace("&gt;", ">")
                .replace("&quot;", '"')
                .replace("&#39;", "'")
            )
            titles.add(normalize_title(raw))
    return titles, True


# ------------------------------------------------------- 원격 도감 history.json
def load_archive_items(timeout: float = 8.0) -> Tuple[List[Dict[str, Any]], str]:
    """gooditem-archive 의 history.json 을 읽는다. (원격 우선, 로컬 폴백)

    Returns: (항목 목록, 출처 문자열)
    """
    try:
        items = json.loads(_http_get(REMOTE_ARCHIVE_URL, timeout=timeout))
        if isinstance(items, list):
            return items, "remote"
    except Exception as e:
        print(f"⚠️ [가드2] 원격 도감(history.json) 조회 실패 → 로컬 사본으로 폴백합니다: {e}")

    if LOCAL_ARCHIVE_FILE.exists():
        try:
            items = json.loads(LOCAL_ARCHIVE_FILE.read_text(encoding="utf-8"))
            if isinstance(items, list):
                return items, "local"
        except Exception as e:
            print(f"⚠️ [가드2] 로컬 도감 사본도 읽지 못했습니다: {e}")

    return [], "none"


def archive_item_ids(archive_items: List[Dict[str, Any]]) -> Set[str]:
    """도감에 등록된 item_id 집합 (구버전 도감은 제목으로도 매칭)."""
    ids: Set[str] = set()
    for it in archive_items:
        iid = (it or {}).get("item_id")
        if iid:
            ids.add(str(iid))
    return ids


def reconcile_state_with_archive(state: Dict[str, Any], archive_items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """도감에 이미 올라간 상품을 used 로 자동 처리한다.

    daily_state.json 이 유실되거나 git pull 로 되돌아가도, 도감에 등록된 상품은
    다시 사용되지 않도록 상태를 복원한다. (에피소드 회차·게시 제목도 함께 복원)
    """
    from product_pool import THEMES

    used = state.setdefault("used_items_by_theme", {})
    episodes = state.setdefault("episode_counts_by_theme", {})
    titles: List[str] = state.setdefault("published_titles", [])

    title_from_item: Dict[str, str] = {}
    for theme_key, theme in THEMES.items():
        for p in theme["products"]:
            title_from_item[p.item_id] = build_episode_title(theme_key, 1)

    touched_themes: Set[str] = set()
    for it in archive_items:
        iid = str((it or {}).get("item_id") or "")
        if not iid or iid not in title_from_item:
            continue
        theme_key = next(k for k, t in THEMES.items() if any(p.item_id == iid for p in t["products"]))
        bucket = used.setdefault(theme_key, [])
        if iid not in bucket:
            bucket.append(iid)
        touched_themes.add(theme_key)

    for theme_key in touched_themes:
        if episodes.get(theme_key, 0) < 1:
            episodes[theme_key] = 1
        first_title = build_episode_title(theme_key, 1)
        if normalize_title(first_title) not in titles:
            titles.append(normalize_title(first_title))

    return state


# --------------------------------------------------------------- 통합 가드
def collect_guard(
    state: Dict[str, Any],
    check_rss: bool = True,
    check_archive: bool = True,
) -> Dict[str, Any]:
    """세 단계 잠금 정보를 모아 하나의 가드 데이터로 만든다."""
    warnings: List[str] = []

    local_used: Set[str] = set()
    for ids in state.get("used_items_by_theme", {}).values():
        local_used.update(ids)

    local_titles: Set[str] = set(state.get("published_titles", []))

    archive_ids: Set[str] = set()
    archive_items: List[Dict[str, Any]] = []
    archive_source = "skipped"
    if check_archive:
        archive_items, archive_source = load_archive_items()
        archive_ids = archive_item_ids(archive_items)
        if archive_source != "remote":
            warnings.append(f"도감 확인 경로: {archive_source}")

    rss_titles: Set[str] = set()
    rss_ok = False
    if check_rss:
        rss_titles, rss_ok = fetch_published_titles()
        if not rss_ok:
            warnings.append("유튜브 RSS 실패 → 로컬 상태로 폴백")

    return {
        "blocked_item_ids": local_used | archive_ids,
        "published_titles": local_titles | rss_titles,
        "rss_titles": rss_titles,
        "archive_items": archive_items,
        "sources": {
            "local_items": len(local_used),
            "archive_items": len(archive_ids),
            "archive_source": archive_source,
            "rss_titles": len(rss_titles),
            "rss_ok": rss_ok,
            "local_titles": len(local_titles),
        },
        "warnings": warnings,
    }


def prune_unpublished_locks(
    state: Dict[str, Any],
    archive_items: List[Dict[str, Any]],
    rss_titles: Set[str],
    rss_ok: bool,
    archive_source: str,
) -> Tuple[Dict[str, Any], List[str]]:
    """유튜브에도 도감에도 없는(게시되지 않은) 회차의 로컬 잠금을 푼다.

    과거 버그로 업로드가 실패한 회차가 daily_state.json 에 '사용/게시' 로 남으면
    도감에서 되돌려도 그 테마가 영원히 건너뛰어진다. 근거(RSS 게시 제목 + 원격 도감)가
    둘 다 정상적으로 확인된 경우에만, 그 테마의 상품이 도감에 하나도 없고 게시 제목도
    RSS 에 없을 때 잠금을 해제한다. (한쪽이라도 조회 실패면 절대 풀지 않는다 →
    같은 영상 재업로드 방지)

    Returns: (갱신된 state, 잠금 해제된 테마 키 목록)
    """
    from product_pool import THEMES

    if not rss_ok or archive_source != "remote":
        return state, []

    archive_ids = archive_item_ids(archive_items)
    used_map = state.get("used_items_by_theme", {}) or {}
    episode_map = state.get("episode_counts_by_theme", {}) or {}
    titles: List[str] = list(state.get("published_titles", []) or [])

    released: List[str] = []
    for theme_key in list(THEMES.keys()):
        theme_item_ids = [p.item_id for p in THEMES[theme_key]["products"]]
        if any(iid in archive_ids for iid in theme_item_ids):
            continue  # 도감에 올라간 상품이 있으면 게시된 회차 → 유지

        max_ep = max(1, int(episode_map.get(theme_key, 0) or 0))
        theme_titles = {normalize_title(build_episode_title(theme_key, n)) for n in range(1, max_ep + 1)}
        if theme_titles & set(rss_titles):
            continue  # 유튜브에 게시된 제목이 있으면 유지

        if not used_map.get(theme_key) and not episode_map.get(theme_key):
            continue  # 애초에 잠금이 없으면 건드리지 않는다

        used_map.pop(theme_key, None)
        episode_map.pop(theme_key, None)
        titles = [t for t in titles if t not in theme_titles]
        released.append(theme_key)

    state["used_items_by_theme"] = used_map
    state["episode_counts_by_theme"] = episode_map
    state["published_titles"] = titles
    return state, released


def describe_guard(guard: Dict[str, Any]) -> str:
    s = guard.get("sources", {})
    state_word = "정상" if s.get("rss_ok") else "폴백"
    return (
        f"🔒 중복 가드: 로컬 사용 상품 {s.get('local_items', 0)}종 · "
        f"도감 잠금 {s.get('archive_items', 0)}종({s.get('archive_source')}) · "
        f"유튜브 게시 제목 {s.get('rss_titles', 0)}건({state_word})"
    )
