#!/usr/bin/env python3
"""Generate windows-apps.html and individual Windows app detail pages."""

import json
import html as html_module
from pathlib import Path

BASE_DIR = Path("P:/GitHub/cityriver")
INDEX_JSON = BASE_DIR / "winapp" / "_index.json"
WINAPP_DIR = BASE_DIR / "winapp"
SOURCE_DIR = Path("D:/NEXTCLOUD/Windows_app")

CATEGORIES = [
    {"name": "AIツール",         "anchor": "ai",          "emoji": "&#x1F916;"},
    {"name": "開発ツール",       "anchor": "dev",         "emoji": "&#x1F6E0;"},
    {"name": "メディア",         "anchor": "media",       "emoji": "&#x1F3AC;"},
    {"name": "システム",         "anchor": "system",      "emoji": "&#x2699;"},
    {"name": "プロダクティビティ", "anchor": "productivity", "emoji": "&#x1F4CB;"},
    {"name": "プライバシー",     "anchor": "privacy",     "emoji": "&#x1F512;"},
    {"name": "ユーティリティ",   "anchor": "utility",     "emoji": "&#x1F527;"},
    {"name": "ライフスタイル",   "anchor": "lifestyle",   "emoji": "&#x1F3E0;"},
]

CAT_ANCHOR = {c["name"]: c["anchor"] for c in CATEGORIES}
CAT_EMOJI = {c["name"]: c["emoji"] for c in CATEGORIES}


def h(text):
    return html_module.escape(str(text)) if text else ""


def generate_feature_bullets(desc, tech):
    bullets = []
    desc_lower = desc.lower() if desc else ""
    keywords = {
        "AI": "AIによるインテリジェントな分析・提案機能",
        "リアルタイム": "リアルタイム処理・監視機能",
        "ドラッグ": "ドラッグ&ドロップ操作に対応",
        "自動": "自動化による効率的なワークフロー",
        "検索": "高速検索機能",
        "管理": "直感的な管理・整理機能",
        "変換": "多フォーマット変換対応",
        "ノイズ": "ノイズ除去・フィルタリング機能",
        "プライバシー": "プライバシー保護機能",
        "セマンティック": "セマンティック検索・分析対応",
        "ホットキー": "グローバルホットキー対応",
        "モニター": "使用量・コストのリアルタイム監視",
        "ウィジェット": "常駐型デスクトップウィジェット",
        "音声": "音声処理・合成機能",
        "画像": "画像処理・変換機能",
        "カンバン": "カンバンボードによるタスク管理",
        "ターミナル": "マルチターミナル環境",
    }
    for keyword, bullet in keywords.items():
        if keyword.lower() in desc_lower or keyword in desc:
            bullets.append(bullet)
        if len(bullets) >= 4:
            break
    if len(bullets) < 2:
        bullets.append("Windowsネイティブの高速動作")
    if len(bullets) < 3:
        bullets.append("シンプルで直感的なインターフェース")
    if "Rust" in (tech or ""):
        bullets.append("Rust製の安全で高速な実装")
    elif "Python" in (tech or "") and len(bullets) < 4:
        bullets.append("Pythonベースの柔軟な拡張性")
    elif len(bullets) < 4:
        bullets.append("Windows環境に最適化された設計")
    return bullets[:5]


def github_icon_svg():
    return '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>'


def github_icon_svg_18():
    return '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>'


def arrow_svg():
    return '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>'


def back_arrow_svg():
    return '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>'


def windows_icon_svg():
    return '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>'


# ─── Generate windows-apps.html ──────────────────────────────────────────────

def generate_list_html(apps):
    cat_groups = {}
    for cat in CATEGORIES:
        cat_groups[cat["name"]] = [a for a in apps if a["category"] == cat["name"]]

    cat_nav = ""
    for cat in CATEGORIES:
        cat_nav += f'      <a href="#{cat["anchor"]}" class="category-btn">{cat["name"]}</a>\n'

    sections = ""
    for cat in CATEGORIES:
        items = cat_groups.get(cat["name"], [])
        if not items:
            continue
        count = len(items)
        sections += f'''
    <section id="{cat["anchor"]}" class="category-section">
      <h2 class="category-title"><span class="emoji">{cat["emoji"]}</span> {h(cat["name"])}</h2>
      <p class="category-count">{count} 件のアプリ</p>
      <div class="product-list">
'''
        for app in items:
            footer_right = ""
            if app.get("github"):
                footer_right += f'            <a href="{h(app["github"])}" class="gh-link" target="_blank" rel="noopener" title="GitHub">{github_icon_svg()}</a>\n'

            sections += f'''        <div class="product-item">
          <div class="product-item-header">
            <h3>{h(app["name"])}</h3>
            <span class="product-item-tag">v{h(app["ver"])}</span>
          </div>
          <p>{h(app["desc"])}</p>
          <div class="product-item-footer">
            <a href="winapp/{h(app["slug"])}.html" class="detail-link">詳細を見る {arrow_svg()}</a>
            <div style="display:flex;align-items:center;gap:8px;">
            {footer_right.strip()}
            </div>
          </div>
        </div>
'''
        sections += '      </div>\n    </section>\n'

    total = len(apps)
    cat_count = len([c for c in CATEGORIES if cat_groups.get(c["name"])])

    # Collect unique tech stacks
    techs = set()
    for app in apps:
        for t in (app.get("tech") or "").split(","):
            t = t.strip().split()[0]  # First word
            if t and len(t) > 1:
                techs.add(t)
    top_techs = sorted(techs)[:5]
    tech_label = "・".join(top_techs[:4])

    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Windowsアプリ一覧 | 合同会社シティーリバー</title>
  <meta name="description" content="合同会社シティーリバーが開発・提供するWindows向けネイティブアプリケーションの一覧。AI、開発、メディア、システムなど{total}種以上。" />
  <link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png" />
  <link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png" />
  <link rel="icon" href="favicon.ico" />
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    :root {{
      --bg-primary: #ffffff;
      --bg-secondary: #f8f9fa;
      --text-primary: #0a0a0a;
      --text-secondary: #6b7280;
      --accent: #f59e0b;
      --accent-light: #fffbeb;
      --border: rgba(0, 0, 0, 0.08);
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", "Hiragino Sans", sans-serif;
      background: var(--bg-primary);
      color: var(--text-primary);
      line-height: 1.7;
      min-height: 100vh;
    }}

    header {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(255, 255, 255, 0.8);
      backdrop-filter: blur(20px) saturate(180%);
      border-bottom: 1px solid var(--border);
    }}

    .nav {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px 40px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .logo-text {{
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 16px;
      font-weight: 600;
      letter-spacing: -0.02em;
      color: var(--text-primary);
      text-decoration: none;
    }}

    .logo-img {{
      height: 40px;
      width: auto;
      object-fit: contain;
    }}

    .nav-link {{
      color: var(--text-secondary);
      text-decoration: none;
      font-weight: 500;
      font-size: 14px;
      transition: color 0.3s ease;
    }}

    .nav-link:hover {{ color: var(--accent); }}

    main {{
      max-width: 1100px;
      margin: 0 auto;
      padding: 80px 40px 120px;
    }}

    .breadcrumb {{
      font-size: 14px;
      color: var(--text-secondary);
      margin-bottom: 32px;
    }}

    .breadcrumb a {{
      color: var(--accent);
      text-decoration: none;
    }}

    .page-header {{
      margin-bottom: 48px;
      text-align: center;
    }}

    .page-badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: var(--accent-light);
      color: var(--accent);
      padding: 8px 16px;
      border-radius: 100px;
      font-size: 13px;
      font-weight: 600;
      margin-bottom: 20px;
    }}

    .page-title {{
      font-size: clamp(2.5rem, 5vw, 3.5rem);
      font-weight: 700;
      letter-spacing: -0.02em;
      margin-bottom: 16px;
    }}

    .page-subtitle {{
      font-size: 18px;
      color: var(--text-secondary);
      line-height: 1.8;
      max-width: 700px;
      margin: 0 auto;
    }}

    .stats-bar {{
      display: flex;
      justify-content: center;
      gap: 40px;
      padding: 24px 0;
      margin-bottom: 48px;
      border-bottom: 1px solid var(--border);
    }}

    .stat {{
      text-align: center;
    }}

    .stat-number {{
      font-size: 28px;
      font-weight: 700;
      color: var(--accent);
    }}

    .stat-label {{
      font-size: 13px;
      color: var(--text-secondary);
      font-weight: 500;
    }}

    .category-nav {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      justify-content: center;
      margin-bottom: 48px;
    }}

    .category-btn {{
      padding: 8px 18px;
      border-radius: 100px;
      border: 1.5px solid var(--border);
      background: white;
      color: var(--text-secondary);
      font-size: 14px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.3s ease;
      text-decoration: none;
    }}

    .category-btn:hover,
    .category-btn.active {{
      background: var(--accent);
      color: white;
      border-color: var(--accent);
    }}

    .category-section {{
      margin-bottom: 56px;
    }}

    .category-title {{
      font-size: 22px;
      font-weight: 700;
      margin-bottom: 8px;
      letter-spacing: -0.01em;
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .category-title .emoji {{
      font-size: 24px;
    }}

    .category-count {{
      font-size: 13px;
      color: var(--text-secondary);
      margin-bottom: 24px;
    }}

    .product-list {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 20px;
    }}

    .product-item {{
      background: white;
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 28px 24px;
      transition: all 0.3s ease;
      display: flex;
      flex-direction: column;
    }}

    .product-item:hover {{
      transform: translateY(-3px);
      box-shadow: 0 12px 40px rgba(245, 158, 11, 0.1);
      border-color: var(--accent);
    }}

    .product-item-header {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 10px;
    }}

    .product-item h3 {{
      font-size: 17px;
      font-weight: 600;
      letter-spacing: -0.01em;
      line-height: 1.4;
    }}

    .product-item-tag {{
      font-size: 11px;
      font-weight: 600;
      padding: 3px 8px;
      border-radius: 100px;
      background: var(--accent-light);
      color: var(--accent);
      white-space: nowrap;
      flex-shrink: 0;
    }}

    .product-item p {{
      color: var(--text-secondary);
      font-size: 14px;
      line-height: 1.7;
      flex: 1;
    }}

    .product-item-footer {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-top: 16px;
      padding-top: 14px;
      border-top: 1px solid var(--border);
    }}

    .detail-link {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 13px;
      font-weight: 600;
      color: var(--accent);
      text-decoration: none;
      transition: gap 0.2s ease;
    }}

    .detail-link:hover {{
      gap: 8px;
    }}

    .gh-link {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 32px;
      height: 32px;
      border-radius: 8px;
      color: var(--text-secondary);
      transition: all 0.2s ease;
    }}

    .gh-link:hover {{
      background: var(--bg-secondary);
      color: var(--text-primary);
    }}

    footer {{
      padding: 40px;
      text-align: center;
      color: var(--text-secondary);
      font-size: 14px;
      border-top: 1px solid var(--border);
    }}

    @media (max-width: 768px) {{
      .nav {{ padding: 16px 24px; }}
      main {{ padding: 60px 24px 80px; }}
      .page-title {{ font-size: 2rem; }}
      .product-list {{ grid-template-columns: 1fr; }}
      .stats-bar {{ gap: 24px; }}
      .stat-number {{ font-size: 22px; }}
    }}
  </style>
</head>
<body>
  <header>
    <nav class="nav">
      <a href="index.html" class="logo-text">
        <img src="Logo.png" alt="CityRiver LLC" class="logo-img">
        合同会社シティーリバー
      </a>
      <a href="index.html#contact" class="nav-link">Contact</a>
    </nav>
  </header>

  <main>
    <div class="breadcrumb">
      <a href="index.html">ホーム</a> / <a href="index.html#products">プロダクト</a> / Windowsアプリ
    </div>

    <div class="page-header">
      <div class="page-badge">
        {windows_icon_svg()}
        Windows Applications
      </div>
      <h1 class="page-title">Windowsアプリ一覧</h1>
      <p class="page-subtitle">Windows向けネイティブアプリケーション。高速で安定した動作を実現。</p>
    </div>

    <div class="stats-bar">
      <div class="stat">
        <div class="stat-number">{total}+</div>
        <div class="stat-label">Windowsアプリ</div>
      </div>
      <div class="stat">
        <div class="stat-number">{cat_count}</div>
        <div class="stat-label">カテゴリ</div>
      </div>
      <div class="stat">
        <div class="stat-number">{tech_label}</div>
        <div class="stat-label">主要テクノロジー</div>
      </div>
    </div>

    <nav class="category-nav">
{cat_nav}    </nav>

{sections}
  </main>

  <footer>
    &copy; <span id="year"></span> 合同会社シティーリバー / CityRiver LLC. All rights reserved.
  </footer>
  <script>document.getElementById("year").textContent = new Date().getFullYear();</script>
</body>
</html>'''


# ─── Generate individual detail page ─────────────────────────────────────────

def generate_detail_page(app):
    name = h(app["name"])
    desc = h(app["desc"])
    ver = h(app["ver"])
    tech = h(app.get("tech", ""))
    category = h(app.get("category", ""))
    github = app.get("github")

    meta_items = f'''        <div class="meta-item">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg>
          <strong>v{ver}</strong>
        </div>
        <div class="meta-item">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>
          {tech}
        </div>
        <div class="meta-item">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
          {category}
        </div>'''

    buttons = ""
    if github:
        buttons += f'''        <a href="{h(github)}" class="btn btn-primary" target="_blank" rel="noopener">
          {github_icon_svg_18()}
          GitHub
        </a>
'''
    buttons += f'''        <a href="../windows-apps.html" class="btn btn-outline">
          {back_arrow_svg()}
          一覧に戻る
        </a>'''

    feature_bullets = generate_feature_bullets(app["desc"], app.get("tech", ""))
    bullets_html = "\n".join(f"        <li>{h(b)}</li>" for b in feature_bullets)

    tech_items = [t.strip() for t in (app.get("tech") or "").split(",") if t.strip()]
    tech_html = "\n".join(f"        <li><strong>{h(t)}</strong></li>" for t in tech_items)

    content_html = f'''      <p>{desc}</p>

      <h2>主な機能</h2>
      <ul>
{bullets_html}
      </ul>

      <h2>技術スタック</h2>
      <ul>
{tech_html}
      </ul>'''

    if github:
        content_html += f'''

      <h2>ソースコード</h2>
      <p>このプロジェクトのソースコードは <a href="{h(github)}" target="_blank" rel="noopener">GitHub</a> で公開されています。Issue・Pull Requestを歓迎します。</p>'''

    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{name} | 合同会社シティーリバー</title>
  <meta name="description" content="{desc}" />
  <link rel="icon" type="image/png" sizes="32x32" href="../favicon-32x32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="../favicon-16x16.png" />
  <link rel="apple-touch-icon" sizes="180x180" href="../apple-touch-icon.png" />
  <link rel="icon" href="../favicon.ico" />
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    :root {{
      --bg-primary: #ffffff;
      --bg-secondary: #f8f9fa;
      --text-primary: #0a0a0a;
      --text-secondary: #6b7280;
      --accent: #f59e0b;
      --accent-light: #fffbeb;
      --border: rgba(0, 0, 0, 0.08);
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", "Hiragino Sans", sans-serif;
      background: var(--bg-primary);
      color: var(--text-primary);
      line-height: 1.7;
      min-height: 100vh;
    }}
    header {{
      position: sticky; top: 0; z-index: 100;
      background: rgba(255,255,255,0.8);
      backdrop-filter: blur(20px) saturate(180%);
      border-bottom: 1px solid var(--border);
    }}
    .nav {{
      max-width: 1200px; margin: 0 auto; padding: 20px 40px;
      display: flex; justify-content: space-between; align-items: center;
    }}
    .logo-text {{
      display: flex; align-items: center; gap: 12px;
      font-size: 16px; font-weight: 600; letter-spacing: -0.02em;
      color: var(--text-primary); text-decoration: none;
    }}
    .logo-img {{ height: 40px; width: auto; object-fit: contain; }}
    .nav-link {{
      color: var(--text-secondary); text-decoration: none;
      font-weight: 500; font-size: 14px; transition: color 0.3s ease;
    }}
    .nav-link:hover {{ color: var(--accent); }}
    main {{
      max-width: 900px; margin: 0 auto; padding: 80px 40px 120px;
    }}
    .breadcrumb {{
      font-size: 14px; color: var(--text-secondary); margin-bottom: 32px;
    }}
    .breadcrumb a {{ color: var(--accent); text-decoration: none; }}
    .page-hero {{
      margin-bottom: 48px;
    }}
    .page-badge {{
      display: inline-flex; align-items: center; gap: 6px;
      background: var(--accent-light); color: var(--accent);
      padding: 6px 14px; border-radius: 100px;
      font-size: 12px; font-weight: 600; margin-bottom: 16px;
    }}
    .page-title {{
      font-size: clamp(2rem, 4vw, 2.8rem);
      font-weight: 700; letter-spacing: -0.02em;
      margin-bottom: 12px;
    }}
    .page-desc {{
      font-size: 18px; color: var(--text-secondary);
      line-height: 1.8; max-width: 700px;
    }}
    .meta-bar {{
      display: flex; gap: 20px; flex-wrap: wrap;
      margin-top: 24px; padding-top: 24px;
      border-top: 1px solid var(--border);
    }}
    .meta-item {{
      display: flex; align-items: center; gap: 6px;
      font-size: 14px; color: var(--text-secondary);
    }}
    .meta-item strong {{
      color: var(--text-primary); font-weight: 600;
    }}
    .actions {{
      display: flex; gap: 12px; flex-wrap: wrap;
      margin-top: 24px;
    }}
    .btn {{
      display: inline-flex; align-items: center; gap: 8px;
      padding: 12px 24px; border-radius: 12px; border: none;
      cursor: pointer; font-weight: 600; font-size: 14px;
      text-decoration: none; transition: all 0.3s ease;
    }}
    .btn-primary {{
      background: var(--accent); color: white;
      box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
    }}
    .btn-primary:hover {{
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(245, 158, 11, 0.4);
    }}
    .btn-outline {{
      background: white; color: var(--text-primary);
      border: 1.5px solid var(--border);
    }}
    .btn-outline:hover {{
      border-color: var(--accent); background: var(--accent-light);
    }}
    .content {{
      margin-top: 48px;
      border-top: 1px solid var(--border);
      padding-top: 48px;
    }}
    .content h2 {{
      font-size: 24px; font-weight: 700;
      margin: 40px 0 16px; letter-spacing: -0.01em;
    }}
    .content h2:first-child {{ margin-top: 0; }}
    .content p {{
      font-size: 16px; line-height: 1.8;
      color: var(--text-secondary); margin-bottom: 16px;
    }}
    .content ul {{
      margin: 12px 0 20px 24px;
      color: var(--text-secondary); font-size: 15px;
    }}
    .content li {{
      margin-bottom: 6px; line-height: 1.7;
    }}
    .content a {{
      color: var(--accent); text-decoration: none;
    }}
    .content a:hover {{ text-decoration: underline; }}
    .info-section {{
      margin-top: 40px; background: var(--bg-secondary);
      border-radius: 16px; padding: 32px;
    }}
    .info-section h2 {{
      margin-top: 0; font-size: 20px;
    }}
    .tech-list {{
      display: flex; flex-wrap: wrap; gap: 8px;
      list-style: none; margin: 16px 0 0 0;
    }}
    .tech-list li {{
      background: white; border: 1px solid var(--border);
      padding: 4px 12px; border-radius: 8px;
      font-size: 13px; color: var(--text-secondary);
    }}
    .back-link {{
      display: inline-flex; align-items: center; gap: 6px;
      margin-top: 48px; padding-top: 32px;
      border-top: 1px solid var(--border);
      color: var(--accent); text-decoration: none;
      font-weight: 600; font-size: 15px;
    }}
    .back-link:hover {{ text-decoration: underline; }}
    footer {{
      padding: 40px; text-align: center;
      color: var(--text-secondary); font-size: 14px;
      border-top: 1px solid var(--border);
    }}
    @media (max-width: 768px) {{
      .nav {{ padding: 16px 24px; }}
      main {{ padding: 60px 24px 80px; }}
      .page-title {{ font-size: 1.8rem; }}
      .meta-bar {{ gap: 12px; }}
    }}
  </style>
</head>
<body>
  <header>
    <nav class="nav">
      <a href="../index.html" class="logo-text">
        <img src="../Logo.png" alt="CityRiver LLC" class="logo-img">
        合同会社シティーリバー
      </a>
      <a href="../index.html#contact" class="nav-link">Contact</a>
    </nav>
  </header>

  <main>
    <div class="breadcrumb">
      <a href="../index.html">ホーム</a> / <a href="../index.html#products">プロダクト</a> / <a href="../windows-apps.html">Windowsアプリ</a> / {name}
    </div>

    <div class="page-hero">
      <div class="page-badge">{category}</div>
      <h1 class="page-title">{name}</h1>
      <p class="page-desc">{desc}</p>
      <div class="meta-bar">
{meta_items}
      </div>
      <div class="actions">
{buttons}
      </div>
    </div>

    <div class="content">
{content_html}
    </div>

    <div class="info-section">
      <h2>使用技術</h2>
      <ul class="tech-list">{"".join(f'<li>{h(t.strip())}</li>' for t in tech_items)}</ul>
    </div>

    <a href="../windows-apps.html" class="back-link">
      {back_arrow_svg()}
      Windowsアプリ一覧に戻る
    </a>
  </main>

  <footer>
    &copy; <span id="year"></span> 合同会社シティーリバー / CityRiver LLC. All rights reserved.
  </footer>
  <script>document.getElementById("year").textContent = new Date().getFullYear();</script>
</body>
</html>'''


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    with open(INDEX_JSON, "r", encoding="utf-8") as f:
        apps = json.load(f)

    print(f"Loaded {len(apps)} apps from _index.json")

    cat_counts = {}
    for app in apps:
        cat = app.get("category", "Unknown")
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
    print("Category counts:")
    for cat, count in cat_counts.items():
        print(f"  {cat}: {count}")

    # 1. Generate windows-apps.html
    list_html = generate_list_html(apps)
    outpath = BASE_DIR / "windows-apps.html"
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(list_html)
    print(f"\nGenerated: {outpath}")

    # 2. Generate individual pages
    WINAPP_DIR.mkdir(parents=True, exist_ok=True)
    generated = []

    for app in apps:
        detail_html = generate_detail_page(app)
        detail_path = WINAPP_DIR / f'{app["slug"]}.html'
        with open(detail_path, "w", encoding="utf-8") as f:
            f.write(detail_html)
        generated.append(detail_path.name)

    print(f"\nGenerated {len(generated)} detail pages in {WINAPP_DIR}/:")
    for name in sorted(generated):
        print(f"  {name}")

    print(f"\nDone! Total files generated: {1 + len(generated)}")


if __name__ == "__main__":
    main()
