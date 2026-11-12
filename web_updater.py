import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Any
from product_pool import THEMES, ProductItem
import config

WEB_DIR = config.BASE_DIR / "web"
WEB_ASSETS_DIR = WEB_DIR / "assets"
HISTORY_FILE = WEB_DIR / "history.json"
WEB_DIR.mkdir(parents=True, exist_ok=True)
WEB_ASSETS_DIR.mkdir(parents=True, exist_ok=True)

PROFILE_SRC = config.BASE_DIR.parent.parent / "downloads" / "유튜브_프로필_아이콘.png"
if PROFILE_SRC.exists() and not (WEB_ASSETS_DIR / "profile.png").exists():
    shutil.copy(PROFILE_SRC, WEB_ASSETS_DIR / "profile.png")


def copy_product_assets():
    """assets 폴더의 제품 이미지들을 웹 assets로 복사"""
    src_dir = config.ASSETS_DIR
    for p in src_dir.glob("*.png"):
        dst = WEB_ASSETS_DIR / p.name
        if not dst.exists() or dst.stat().st_size != p.stat().st_size:
            shutil.copy(p, dst)


def load_history() -> List[Dict[str, Any]]:
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []


def save_history(history: List[Dict[str, Any]]):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def generate_html(theme_name: str, featured_items: List[ProductItem], history_items: List[Dict[str, Any]]) -> str:
    copy_product_assets()

    # Category mapping
    category_map = {
        "living": ("자취·리빙", "🏠"),
        "kitchen": ("주방·살림", "🍳"),
        "food": ("식비·간편식", "🥗"),
        "desk": ("데스크테리어", "💻"),
    }

    # 동영상 테마별 그룹 빌드
    categories = [
        ("kitchen", "🍳 주방·살림", "🍳 주방 살림 혁명 TOP 3"),
        ("living", "🏠 자취·리빙", "🏠 자취생 삶의 질 떡상 TOP 3"),
        ("food", "🥗 식비·간편식", "🥗 식비 절약 가성비 간편식 TOP 3"),
        ("desk", "💻 데스크", "💻 직장인 데스크테리어 TOP 3"),
    ]

    section_blocks = []
    for cat_key, pill_title, sec_title in categories:
        cat_items = [x for x in history_items if x.get("category_key") == cat_key]
        cat_items.sort(key=lambda x: x.get("item_num", 1))

        cards_html = []
        for it in cat_items:
            badge_class = "rocket-badge" if "로켓" in it.get("tag", "") else "discount-badge"
            c = f"""
        <a class="product-card catalog-card" 
           href="{it['coupang_url']}" 
           target="_blank" 
           rel="noopener noreferrer"
           data-category="{cat_key}"
           data-title="{it['title'].lower()}"
           data-desc="{it.get('desc', '').lower()}">
          <div class="product-thumb-wrap">
            <img class="product-thumb" src="assets/{it['img_name']}" alt="{it['title']}" loading="lazy">
            <div class="item-num-badge">0{it.get('item_num', 1)}번</div>
            <div class="cat-pill-badge">{pill_title}</div>
          </div>
          <div class="product-info">
            <div class="product-tag">{it.get('desc', '')}</div>
            <div class="product-name">{it['title']}</div>
            <div class="product-meta">
              <span class="price-val">{it['price']}</span>
              <span class="{badge_class}">{it.get('tag', '로켓배송')}</span>
            </div>
          </div>
          <div class="btn-buy secondary">
            최저가 ➔
          </div>
        </a>"""
            cards_html.append(c)

        if cards_html:
            sec_html = f"""
    <div class="video-group" data-group="{cat_key}">
      <div class="video-group-header">
        <span class="video-group-title">{sec_title}</span>
        <span class="video-group-tag">영상 3종 추천</span>
      </div>
      <div class="product-list">
        {''.join(cards_html)}
      </div>
    </div>"""
            section_blocks.append(sec_html)

    catalog_body = "\n".join(section_blocks)

    if not section_blocks:
        catalog_body = """
      <div id="catalogEmptyState" style="background: #ffffff; border-radius: 22px; padding: 36px 20px; text-align: center; box-shadow: 0 4px 18px rgba(0,0,0,0.03); margin-top: 4px;">
        <div style="font-size: 36px; margin-bottom: 10px;">🧪</div>
        <div style="font-size: 16px; font-weight: 800; color: #191f28; margin-bottom: 6px;">등록된 꿀템을 준비 중입니다</div>
        <div style="font-size: 13px; color: #8b95a1; line-height: 1.55;">새로운 쇼츠 영상이 업로드되면<br>영상 속 최저가 꿀템 링크가 이곳에 자동으로 등록됩니다!</div>
      </div>"""

    catalog_count = len(history_items)

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>돈값연구소 🧪 | 돈값 하는 쿠팡 꿀템 최저가 &amp; 실시간 검색</title>
  <link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" />
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }}
    body {{
      font-family: "Pretendard", -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
      background-color: #f2f4f6;
      color: #191f28;
      display: flex;
      justify-content: center;
      min-height: 100vh;
      padding: 16px 14px 40px;
    }}
    .container {{
      width: 100%;
      max-width: 440px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    
    /* 프로필 카드 */
    .profile-card {{
      background: #ffffff;
      border-radius: 26px;
      padding: 24px 20px 20px;
      text-align: center;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 10px;
    }}
    .avatar-wrap {{
      position: relative;
      width: 82px;
      height: 82px;
    }}
    .avatar {{
      width: 82px;
      height: 82px;
      border-radius: 26px;
      object-fit: cover;
      box-shadow: 0 8px 20px rgba(255, 184, 0, 0.25);
    }}
    .profile-title {{
      font-size: 22px;
      font-weight: 800;
      letter-spacing: -0.5px;
      color: #191f28;
    }}
    .profile-bio {{
      font-size: 13.5px;
      color: #4e5968;
      line-height: 1.45;
      word-break: keep-all;
    }}
    .disclaimer-badge {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      background: #f8f9fa;
      border: 1px solid #e5e8eb;
      border-radius: 20px;
      padding: 5px 12px;
      font-size: 11px;
      color: #8b95a1;
      font-weight: 500;
    }}

    /* 검색창 & 카테고리 칩 바 */
    .search-filter-card {{
      background: #ffffff;
      border-radius: 22px;
      padding: 16px;
      box-shadow: 0 4px 18px rgba(0, 0, 0, 0.04);
      display: flex;
      flex-direction: column;
      gap: 12px;
      position: sticky;
      top: 10px;
      z-index: 100;
      border: 1px solid rgba(0, 115, 233, 0.15);
    }}
    .search-box {{
      position: relative;
      display: flex;
      align-items: center;
    }}
    .search-icon {{
      position: absolute;
      left: 14px;
      font-size: 16px;
      color: #8b95a1;
      pointer-events: none;
    }}
    .search-input {{
      width: 100%;
      height: 46px;
      background: #f2f4f6;
      border: 1.5px solid transparent;
      border-radius: 14px;
      padding: 0 40px 0 40px;
      font-size: 14.5px;
      font-family: inherit;
      font-weight: 600;
      color: #191f28;
      outline: none;
      transition: all 0.2s ease;
    }}
    .search-input:focus {{
      background: #ffffff;
      border-color: #0073e9;
      box-shadow: 0 0 0 3px rgba(0, 115, 233, 0.15);
    }}
    .clear-btn {{
      position: absolute;
      right: 12px;
      width: 22px;
      height: 22px;
      border-radius: 50%;
      background: #c1c7cd;
      color: #ffffff;
      border: none;
      display: none;
      align-items: center;
      justify-content: center;
      font-size: 12px;
      cursor: pointer;
    }}

    /* 카테고리 칩 필터 */
    .category-pills {{
      display: flex;
      gap: 7px;
      overflow-x: auto;
      padding-bottom: 2px;
      scrollbar-width: none;
      -ms-overflow-style: none;
    }}
    .category-pills::-webkit-scrollbar {{
      display: none;
    }}
    .pill-btn {{
      flex-shrink: 0;
      background: #f2f4f6;
      border: 1px solid transparent;
      border-radius: 12px;
      padding: 7px 12px;
      font-size: 12.5px;
      font-weight: 700;
      color: #4e5968;
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .pill-btn.active {{
      background: #191f28;
      color: #ffffff;
    }}

    /* 섹션 라벨 */
    .section-label {{
      font-size: 13.5px;
      font-weight: 800;
      color: #4e5968;
      padding: 4px 6px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .section-label .badge-new {{
      background: #ff3b30;
      color: #fff;
      font-size: 10px;
      font-weight: 800;
      padding: 2px 7px;
      border-radius: 10px;
    }}
    .count-indicator {{
      font-size: 12px;
      font-weight: 600;
      color: #0073e9;
    }}

    /* 제품 리스트 & 카드 */
    .product-list {{
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}
    .product-card {{
      background: #ffffff;
      border-radius: 20px;
      padding: 14px;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.03);
      display: flex;
      align-items: center;
      gap: 14px;
      text-decoration: none;
      color: inherit;
      transition: transform 0.15s ease, background 0.15s ease;
      border: 1px solid #f2f4f6;
    }}
    .product-card:active {{
      transform: scale(0.98);
      background-color: #fafbfc;
    }}
    .product-thumb-wrap {{
      position: relative;
      width: 78px;
      height: 78px;
      flex-shrink: 0;
      border-radius: 14px;
      overflow: hidden;
      background: #f8f9fa;
      border: 1px solid #edf0f3;
    }}
    .product-thumb {{
      width: 100%;
      height: 100%;
      object-fit: cover;
    }}
    .item-num-badge {{
      position: absolute;
      top: 4px;
      left: 4px;
      background: rgba(0, 115, 233, 0.9);
      color: #ffffff;
      font-size: 9.5px;
      font-weight: 800;
      padding: 2px 6px;
      border-radius: 5px;
      backdrop-filter: blur(4px);
    }}
    .cat-pill-badge {{
      position: absolute;
      bottom: 4px;
      left: 4px;
      background: rgba(25, 31, 40, 0.85);
      color: #ffffff;
      font-size: 8.5px;
      font-weight: 700;
      padding: 2px 5px;
      border-radius: 4px;
      backdrop-filter: blur(4px);
    }}
    .product-info {{
      flex: 1;
      min-width: 0;
      display: flex;
      flex-direction: column;
      gap: 3px;
    }}
    .product-tag {{
      font-size: 11px;
      font-weight: 700;
      color: #0073e9;
    }}
    .product-name {{
      font-size: 14.5px;
      font-weight: 700;
      color: #191f28;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      letter-spacing: -0.3px;
    }}
    .product-meta {{
      display: flex;
      align-items: center;
      gap: 6px;
      margin-top: 1px;
    }}
    .price-val {{
      font-size: 15.5px;
      font-weight: 800;
      color: #191f28;
    }}
    .discount-badge {{
      background: #ffebee;
      color: #e52528;
      font-size: 10.5px;
      font-weight: 800;
      padding: 2px 6px;
      border-radius: 5px;
    }}
    .rocket-badge {{
      background: #e8f3ff;
      color: #0073e9;
      font-size: 10.5px;
      font-weight: 800;
      padding: 2px 6px;
      border-radius: 5px;
    }}
    .btn-buy {{
      background: #0073e9;
      color: #ffffff;
      font-size: 12px;
      font-weight: 700;
      padding: 8px 12px;
      border-radius: 12px;
      white-space: nowrap;
      display: flex;
      align-items: center;
      gap: 3px;
      box-shadow: 0 2px 8px rgba(0, 115, 233, 0.25);
    }}
    .btn-buy.secondary {{
      background: #f2f4f6;
      color: #4e5968;
      box-shadow: none;
    }}

    /* 검색 결과 없음 배너 */
    .no-results {{
      display: none;
      background: #ffffff;
      border-radius: 20px;
      padding: 26px 18px;
      text-align: center;
      box-shadow: 0 4px 14px rgba(0,0,0,0.03);
    }}
    .no-results-icon {{
      font-size: 32px;
      margin-bottom: 8px;
    }}
    .no-results-title {{
      font-size: 15px;
      font-weight: 800;
      color: #191f28;
      margin-bottom: 4px;
    }}
    .no-results-desc {{
      font-size: 12.5px;
      color: #8b95a1;
      margin-bottom: 16px;
    }}
    .btn-coupang-search {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      background: #0073e9;
      color: #ffffff;
      font-size: 13.5px;
      font-weight: 700;
      padding: 12px 18px;
      border-radius: 14px;
      text-decoration: none;
      box-shadow: 0 4px 12px rgba(0, 115, 233, 0.3);
    }}

    .extra-links {{
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-top: 8px;
    }}
    .channel-btn {{
      background: #ffffff;
      border-radius: 18px;
      padding: 15px 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      text-decoration: none;
      color: #191f28;
      font-size: 13.5px;
      font-weight: 700;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.03);
      border: 1px solid #f2f4f6;
    }}
    .channel-left {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .channel-icon {{
      font-size: 18px;
    }}
    .channel-arrow {{
      color: #b0b8c1;
      font-size: 15px;
    }}
    .footer {{
      text-align: center;
      font-size: 11px;
      color: #8b95a1;
      line-height: 1.5;
      padding: 10px 0 0;
    }}
  </style>
</head>
<body>
  <div class="container">
    <!-- 프로필 카드 -->
    <div class="profile-card">
      <div class="avatar-wrap">
        <img class="avatar" src="assets/profile.png" alt="돈값연구소">
      </div>
      <h1 class="profile-title">돈값연구소 🧪</h1>
      <p class="profile-bio">"이건 진짜 돈값 한다!" 싶은 알짜배기 쿠팡 꿀템 &amp; 실시간 최저가</p>
      <div class="disclaimer-badge">
        <span>🔒</span> 쿠팡 파트너스 활동으로 수수료를 제공받습니다
      </div>
    </div>

    <!-- 검색 & 카테고리 필터 카드 -->
    <div class="search-filter-card">
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input type="text" id="searchInput" class="search-input" placeholder="영상 속 꿀템이나 키워드 검색..." autocomplete="off">
        <button id="clearBtn" class="clear-btn" aria-label="검색어 지우기">✕</button>
      </div>
      <div class="category-pills">
        <button class="pill-btn active" data-filter="all">🔥 전체 ({len(history_items)})</button>
        <button class="pill-btn" data-filter="kitchen">🍳 주방·살림</button>
        <button class="pill-btn" data-filter="living">🏠 자취·리빙</button>
        <button class="pill-btn" data-filter="food">🥗 식비·간편식</button>
        <button class="pill-btn" data-filter="desk">💻 데스크</button>
      </div>
    </div>

    <!-- 영상별 추천 꿀템 그룹 -->
    <div id="catalogContainer">
{catalog_body}
    </div>

    <!-- 검색 결과 없음 배너 -->
    <div id="noResults" class="no-results" style="display: none; text-align: center; padding: 40px 20px; background: #f9fafb; border-radius: 16px; margin-top: 10px;">
      <div style="font-size: 32px; margin-bottom: 8px;">🔍</div>
      <div style="font-size: 15px; font-weight: 800; color: #191f28; margin-bottom: 6px;">검색된 꿀템이 없습니다</div>
      <div style="font-size: 13px; color: #8b95a1; margin-bottom: 16px;">다른 키워드로 검색하거나 쿠팡에서 직접 찾아보세요!</div>
      <a id="coupangSearchBtn" href="https://www.coupang.com" target="_blank" rel="noopener noreferrer"
         style="display: inline-block; background: #0073e9; color: #ffffff; padding: 10px 18px; border-radius: 12px; font-size: 13px; font-weight: 800; text-decoration: none;">
        쿠팡에서 최저가 검색 ➔
      </a>
    </div>

    <!-- 채널 링크 -->
    <div class="section-label" style="margin-top: 30px;">
      실시간 핫딜 &amp; 채널
    </div>
    <div class="extra-links">
      <a class="channel-btn" href="https://t.me/ym_hotdeal" target="_blank" rel="noopener noreferrer">
        <div class="channel-left">
          <span class="channel-icon">🚀</span>
          <span>실시간 쿠팡 핫딜 모음 (텔레그램)</span>
        </div>
        <span class="channel-arrow">➔</span>
      </a>
      <a class="channel-btn" href="https://youtube.com/@dongap_lab" target="_blank" rel="noopener noreferrer">
        <div class="channel-left">
          <span class="channel-icon">📺</span>
          <span>유튜브 돈값연구소 채널 바로가기</span>
        </div>
        <span class="channel-arrow">➔</span>
      </a>
    </div>

    <div class="footer">
      돈값연구소 🧪 | 진짜 돈값 하는 가성비 필수템<br>
      © 2026 dongap_lab. All rights reserved.
    </div>
  </div>

  <script>
    const searchInput = document.getElementById("searchInput");
    const clearBtn = document.getElementById("clearBtn");
    const pillBtns = document.querySelectorAll(".pill-btn");
    const videoGroups = document.querySelectorAll(".video-group");
    const noResults = document.getElementById("noResults");
    const coupangSearchBtn = document.getElementById("coupangSearchBtn");

    let currentFilter = "all";

    function filterItems() {{
      const query = searchInput.value.trim().toLowerCase();
      let visibleCards = 0;

      videoGroups.forEach(group => {{
        const groupCat = group.getAttribute("data-group");
        const cards = group.querySelectorAll(".catalog-card");
        let groupVisible = 0;

        const matchesGroupCat = (currentFilter === "all" || groupCat === currentFilter);

        cards.forEach(card => {{
          const title = card.getAttribute("data-title") || "";
          const desc = card.getAttribute("data-desc") || "";
          const matchesQuery = (query === "" || title.includes(query) || desc.includes(query));

          if (matchesGroupCat && matchesQuery) {{
            card.style.display = "flex";
            groupVisible++;
            visibleCards++;
          }} else {{
            card.style.display = "none";
          }}
        }});

        if (groupVisible > 0) {{
          group.style.display = "block";
        }} else {{
          group.style.display = "none";
        }}
      }});

      clearBtn.style.display = query.length > 0 ? "flex" : "none";

      if (visibleCards === 0) {{
        noResults.style.display = "block";
        const searchUrl = "https://www.coupang.com/np/search?q=" + encodeURIComponent(query || "자취꿀템") + "&lptag=AF7086198";
        coupangSearchBtn.href = searchUrl;
        coupangSearchBtn.innerText = "쿠팡에서 '" + (query || "꿀템") + "' 최저가 검색 ➔";
      }} else {{
        noResults.style.display = "none";
      }}
    }}

    searchInput.addEventListener("input", filterItems);

    clearBtn.addEventListener("click", () => {{
      searchInput.value = "";
      filterItems();
      searchInput.focus();
    }});

    pillBtns.forEach(btn => {{
      btn.addEventListener("click", () => {{
        pillBtns.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        currentFilter = btn.getAttribute("data-filter");
        filterItems();
      }});
    }});

    // URL Hash support (#kitchen, #living, #food, #desk)
    const hash = window.location.hash.replace("#", "");
    if (hash && ["kitchen", "living", "food", "desk"].includes(hash)) {{
      const targetBtn = document.querySelector(`.pill-btn[data-filter="${{hash}}"]`);
      if (targetBtn) {{
        targetBtn.click();
      }}
    }}
  </script>
</body>
</html>
"""
    return html


def update_link_page(theme_name: str, items: List[ProductItem], auto_push: bool = True) -> bool:
    history = load_history()

    # Prepend new featured items to history if not present
    for i, item in enumerate(items[:3]):
        img_file = Path(item.image_path).name if getattr(item, "image_path", None) else f"{item.item_id}.png"
        h_entry = {
            "title": item.title,
            "price": item.price,
            "tag": item.tag or item.discount,
            "desc": item.caption1 or item.caption2 or item.header_badge,
            "img_name": img_file,
            "coupang_url": item.coupang_url,
            "category_key": "living" if "living" in item.item_id else ("kitchen" if "kitchen" in item.item_id else ("food" if "food" in item.item_id else "desk")),
            "item_num": i + 1
        }
        # 동일 상품이 있으면 업데이트, 없으면 추가
        existing_idx = next((idx for idx, x in enumerate(history) if x.get("coupang_url") == item.coupang_url or x.get("title") == item.title), None)
        if existing_idx is not None:
            history[existing_idx] = h_entry
        else:
            history.append(h_entry)

    save_history(history)

    # Render HTML using ONLY history items (cumulative)
    html_content = generate_html(theme_name, items, history)
    index_file = WEB_DIR / "index.html"
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"📄 누적형 모바일 링크 페이지 HTML 생성 완료 ({len(history)}개 상품): {index_file}")

    git_dir = WEB_DIR / ".git"

    # Git 저장소가 로컬에 없으면 원격 저장소에서 자동 클론
    if auto_push and not git_dir.exists():
        try:
            print("📦 web 폴더에 Git 저장소가 없어 자동으로 GitHub 저장소 연결 중...")
            subprocess.run(["git", "clone", "https://github.com/ehdnsj96/gooditem-archive.git", "web_repo"], cwd=config.BASE_DIR, check=True)
            temp_git = config.BASE_DIR / "web_repo" / ".git"
            if temp_git.exists():
                shutil.move(str(temp_git), str(git_dir))
                shutil.rmtree(config.BASE_DIR / "web_repo", ignore_errors=True)
                print("🔗 GitHub Pages 저장소 자동 연결 성공!")
        except Exception as e:
            print(f"⚠️ Git 저장소 자동 연결 실패 (SSH 또는 로컬 인증 필요): {e}")

    if auto_push and git_dir.exists():
        try:
            print("🚀 GitHub Pages 저장소로 누적형 링크 페이지 배포 중...")
            # 원격 최신 커밋을 받아와 로컬 HEAD를 맞춤으로써 non-fast-forward 충돌 방지
            subprocess.run(["git", "fetch", "origin", "main"], cwd=WEB_DIR, check=False)
            subprocess.run(["git", "reset", "origin/main"], cwd=WEB_DIR, check=False)
            subprocess.run(["git", "add", "."], cwd=WEB_DIR, check=True)
            status = subprocess.run(["git", "status", "--porcelain"], cwd=WEB_DIR, capture_output=True, text=True)
            if status.stdout.strip():
                subprocess.run(["git", "commit", "-m", f"Update link page: {theme_name} ({len(history)} items)"], cwd=WEB_DIR, check=True)
                push_res = subprocess.run(["git", "push", "origin", "main"], cwd=WEB_DIR, capture_output=True, text=True)
                if push_res.returncode == 0:
                    print("✅ GitHub Pages 배포 완료!")
                else:
                    print(f"⚠️ Git 푸시 실패: {push_res.stderr.strip()}")
            else:
                print("ℹ️ 변경된 상품 내용이 없어 추가 푸시를 건너뜁니다.")
            return True
        except Exception as e:
            print(f"⚠️ Git 푸시 중 오류: {e}")
            return False

    return True


def clear_link_page(auto_push: bool = True) -> bool:
    """웹페이지의 모든 상품을 삭제하고 대기 상태로 초기화"""
    save_history([])
    html_content = generate_html("", [], [])
    index_file = WEB_DIR / "index.html"
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"🧹 모바일 링크 페이지 상품 전체 삭제 완료: {index_file}")

    git_dir = WEB_DIR / ".git"

    if auto_push and not git_dir.exists():
        try:
            print("📦 web 폴더에 Git 저장소가 없어 자동으로 GitHub 저장소 연결 중...")
            subprocess.run(["git", "clone", "https://github.com/ehdnsj96/gooditem-archive.git", "web_repo"], cwd=config.BASE_DIR, check=True)
            temp_git = config.BASE_DIR / "web_repo" / ".git"
            if temp_git.exists():
                shutil.move(str(temp_git), str(git_dir))
                shutil.rmtree(config.BASE_DIR / "web_repo", ignore_errors=True)
                print("🔗 GitHub Pages 저장소 자동 연결 성공!")
        except Exception as e:
            print(f"⚠️ Git 저장소 자동 연결 실패: {e}")

    if auto_push and git_dir.exists():
        try:
            print("🚀 GitHub Pages 저장소로 비우기 배포 중...")
            subprocess.run(["git", "add", "."], cwd=WEB_DIR, check=True)
            subprocess.run(["git", "commit", "-m", "Clear products from link page: ready for new release"], cwd=WEB_DIR, check=True)
            subprocess.run(["git", "push", "origin", "main"], cwd=WEB_DIR, check=True)
            print("✅ GitHub Pages 비우기 배포 완료!")
            return True
        except Exception as e:
            print(f"⚠️ Git 푸시 중 오류: {e}")
            return False
    return True


if __name__ == "__main__":
    import sys
    if "--clear" in sys.argv:
        clear_link_page(auto_push=True)
    else:
        from product_pool import THEMES
        sample_items = THEMES["living"]["products"][:3]
        update_link_page("자취생 삶의 질 떡상", sample_items, auto_push=True)
