#!/usr/bin/env python3
"""拡張機能の個別ページを一括生成するスクリプト"""
import json, os, re, glob

BASE = "D:/NEXTCLOUD/extensions"
OUT = "P:/GitHub/cityriver/ext"
os.makedirs(OUT, exist_ok=True)

# GitHub リポジトリマッピング
GITHUB_MAP = {
    "amazon-real-review": "amazon-real-review",
    "Automatic_email_classification_prioritization": "gmail-priority-sorter",
    "bookmark_reader": "bookmark_reader",
    "Completely_my_own_mode_for_note": None,
    "Currency_to_Yen": "Currency_to_Yen",
    "Dream_Diary_Assistant": "Dream_Diary_Assistant",
    "ExtensionIdeaAI": None,
    "gemini-exporter-extension": None,
    "ImageGenPrompter": "image-gen-prompter",
    "Keep_Clipper_v3": "Keep_Clipper",
    "Local_Prompt_Library": None,
    "Manus_delete": "ai-chat-bulk-delete",
    "Mindfulness_Browser_Assistant": "Mindfulness_Browser_Assistant",
    "Mini_Stock_Portfolio": "Mini_Stock_Portfolio",
    "News_Article_Bias_Checker": "News_Article_Bias_Checker",
    "Note Markdown Cleaner": None,
    "note-draft-generator_custam": "note-draft-generator_custam",
    "note_custom_browser": None,
    "note_mute_browser": "note-mute-browser",
    "Note_Notification_Text_Strong_Color": "Note_Notification_Text_Strong_Color",
    "note_url_copy": "Clean_URL_Copy",
    "note_viewer": "note_viewer",
    "Sakura_Resale_Detector": None,
    "Screenshot-Annotator": None,
    "screenshot-translator": "screenshot-translator",
    "URL Extractor for NotebookLM": None,
    "websnip-chrome-extension-master": None,
    "x_good_hide": "x_good_hide",
    "X_Offline_Enhancer": "X-Offline-Enhancer",
    "YouTue_Dammy_Killer": "YouTube-Dummy-Killer",
}

# カテゴリマッピング
CATEGORY_MAP = {
    "amazon-real-review": ("ショッピング", "#f59e0b", "#fffbeb"),
    "Automatic_email_classification_prioritization": ("生産性向上", "#10b981", "#ecfdf5"),
    "bookmark_reader": ("生産性向上", "#10b981", "#ecfdf5"),
    "Completely_my_own_mode_for_note": ("note.com", "#6366f1", "#eef2ff"),
    "Currency_to_Yen": ("ショッピング", "#f59e0b", "#fffbeb"),
    "Dream_Diary_Assistant": ("AI・プロンプト", "#8b5cf6", "#f5f3ff"),
    "ExtensionIdeaAI": ("AI・プロンプト", "#8b5cf6", "#f5f3ff"),
    "gemini-exporter-extension": ("ユーティリティ", "#0ea5e9", "#ecfeff"),
    "ImageGenPrompter": ("AI・プロンプト", "#8b5cf6", "#f5f3ff"),
    "Keep_Clipper_v3": ("ユーティリティ", "#0ea5e9", "#ecfeff"),
    "Local_Prompt_Library": ("AI・プロンプト", "#8b5cf6", "#f5f3ff"),
    "Manus_delete": ("ユーティリティ", "#0ea5e9", "#ecfeff"),
    "Mindfulness_Browser_Assistant": ("生産性向上", "#10b981", "#ecfdf5"),
    "Mini_Stock_Portfolio": ("生産性向上", "#10b981", "#ecfdf5"),
    "News_Article_Bias_Checker": ("生産性向上", "#10b981", "#ecfdf5"),
    "Note Markdown Cleaner": ("note.com", "#6366f1", "#eef2ff"),
    "note-draft-generator_custam": ("note.com", "#6366f1", "#eef2ff"),
    "note_custom_browser": ("note.com", "#6366f1", "#eef2ff"),
    "note_mute_browser": ("note.com", "#6366f1", "#eef2ff"),
    "Note_Notification_Text_Strong_Color": ("note.com", "#6366f1", "#eef2ff"),
    "note_url_copy": ("note.com", "#6366f1", "#eef2ff"),
    "note_viewer": ("note.com", "#6366f1", "#eef2ff"),
    "Sakura_Resale_Detector": ("ショッピング", "#f59e0b", "#fffbeb"),
    "Screenshot-Annotator": ("ユーティリティ", "#0ea5e9", "#ecfeff"),
    "screenshot-translator": ("AI・プロンプト", "#8b5cf6", "#f5f3ff"),
    "URL Extractor for NotebookLM": ("note.com", "#6366f1", "#eef2ff"),
    "websnip-chrome-extension-master": ("ユーティリティ", "#0ea5e9", "#ecfeff"),
    "x_good_hide": ("SNS・動画", "#ef4444", "#fef2f2"),
    "X_Offline_Enhancer": ("SNS・動画", "#ef4444", "#fef2f2"),
    "YouTue_Dammy_Killer": ("SNS・動画", "#ef4444", "#fef2f2"),
}

GITHUB_USER = "sayasaya8039"

def slug(dirname):
    s = dirname.lower().replace(" ", "-").replace("_", "-")
    s = re.sub(r'[^a-z0-9\-]', '', s)
    return s

def read_readme(dirpath):
    readme = os.path.join(dirpath, "README.md")
    if not os.path.exists(readme):
        return None
    with open(readme, encoding="utf-8", errors="replace") as f:
        return f.read()

def md_to_html_sections(md_text):
    """README.mdをHTMLセクションに変換（簡易版）"""
    if not md_text:
        return ""

    lines = md_text.split("\n")
    html_parts = []
    in_list = False
    in_code = False

    for line in lines:
        stripped = line.strip()

        # コードブロック
        if stripped.startswith("```"):
            if in_code:
                html_parts.append("</code></pre>")
                in_code = False
            else:
                lang = stripped[3:].strip()
                html_parts.append(f'<pre><code class="lang-{lang}">')
                in_code = True
            continue

        if in_code:
            html_parts.append(line.replace("<", "&lt;").replace(">", "&gt;"))
            continue

        # 見出し
        if stripped.startswith("# ") and not stripped.startswith("## "):
            continue  # h1はページタイトルで使うのでスキップ
        elif stripped.startswith("## "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f'<h2>{stripped[3:]}</h2>')
            continue
        elif stripped.startswith("### "):
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            html_parts.append(f'<h3>{stripped[4:]}</h3>')
            continue

        # リスト
        if stripped.startswith("- ") or stripped.startswith("* "):
            if not in_list:
                html_parts.append("<ul>")
                in_list = True
            content = stripped[2:]
            # インラインコード
            content = re.sub(r'`([^`]+)`', r'<code>\1</code>', content)
            # 太字
            content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', content)
            html_parts.append(f"<li>{content}</li>")
            continue

        if in_list and not stripped:
            html_parts.append("</ul>")
            in_list = False
            continue

        # 通常の段落
        if stripped:
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            content = stripped
            content = re.sub(r'`([^`]+)`', r'<code>\1</code>', content)
            content = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', content)
            content = re.sub(r'!\[.*?\]\(.*?\)', '', content)  # 画像除去
            content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', content)
            if content.strip():
                html_parts.append(f"<p>{content}</p>")

    if in_list:
        html_parts.append("</ul>")

    return "\n        ".join(html_parts)

def generate_page(dirname, manifest, readme_html, github_url, category_info):
    name = manifest.get("name", dirname)
    desc = manifest.get("description", "")
    ver = manifest.get("version", "")
    mv = manifest.get("manifest_version", 3)
    perms = manifest.get("permissions", [])
    cat_name, cat_color, cat_bg = category_info

    slug_name = slug(dirname)

    github_btn = ""
    if github_url:
        github_btn = f'''<a href="{github_url}" class="btn btn-primary" target="_blank" rel="noopener">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
              GitHub
            </a>'''

    perms_html = ""
    if perms:
        perm_items = "".join(f"<li>{p}</li>" for p in perms[:10])
        perms_html = f'''
        <div class="info-section">
          <h2>使用する権限</h2>
          <ul class="perm-list">{perm_items}</ul>
        </div>'''

    content_html = readme_html if readme_html else f"<p>{desc}</p>"

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
      --accent: {cat_color};
      --accent-light: {cat_bg};
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
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}
    .btn-primary:hover {{
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(0,0,0,0.2);
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
    .content h3 {{
      font-size: 18px; font-weight: 600;
      margin: 28px 0 12px;
    }}
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
    .content code {{
      background: var(--bg-secondary); padding: 2px 6px;
      border-radius: 4px; font-size: 14px;
    }}
    .content pre {{
      background: #1e293b; color: #e2e8f0;
      border-radius: 12px; padding: 20px 24px;
      overflow-x: auto; margin: 16px 0 24px;
      font-size: 14px; line-height: 1.6;
    }}
    .content pre code {{
      background: none; padding: 0; color: inherit;
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
    .perm-list {{
      display: flex; flex-wrap: wrap; gap: 8px;
      list-style: none; margin: 16px 0 0 0;
    }}
    .perm-list li {{
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
      <a href="../index.html">ホーム</a> / <a href="../index.html#products">プロダクト</a> / <a href="../extensions.html">拡張機能</a> / {name}
    </div>

    <div class="page-hero">
      <div class="page-badge">{cat_name}</div>
      <h1 class="page-title">{name}</h1>
      <p class="page-desc">{desc}</p>
      <div class="meta-bar">
        <div class="meta-item">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg>
          <strong>v{ver}</strong>
        </div>
        <div class="meta-item">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
          Chrome / Edge
        </div>
        <div class="meta-item">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
          Manifest V{mv}
        </div>
      </div>
      <div class="actions">
        {github_btn}
        <a href="../extensions.html" class="btn btn-outline">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
          一覧に戻る
        </a>
      </div>
    </div>

    <div class="content">
      {content_html}
    </div>
    {perms_html}

    <a href="../extensions.html" class="back-link">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
      拡張機能一覧に戻る
    </a>
  </main>

  <footer>
    &copy; <span id="year"></span> 合同会社シティーリバー / CityRiver LLC. All rights reserved.
  </footer>
  <script>document.getElementById("year").textContent = new Date().getFullYear();</script>
</body>
</html>'''

# 処理対象（manifest.jsonがあるもの、重複除外）
SKIP = {"Note_Notification_Text_Strong_Color-main", "bypass-paywalls-chrome-clean-master", "Acid-Tabs-Original", "Dream_Diary_Assistant_OR"}

generated = []
for mf in sorted(glob.glob(os.path.join(BASE, "*/manifest.json"))):
    dirpath = os.path.dirname(mf)
    dirname = os.path.basename(dirpath)

    if dirname in SKIP:
        continue

    try:
        with open(mf, encoding="utf-8") as f:
            manifest = json.load(f)
    except:
        continue

    if not manifest.get("name"):
        continue

    readme = read_readme(dirpath)
    readme_html = md_to_html_sections(readme)

    gh_repo = GITHUB_MAP.get(dirname)
    github_url = f"https://github.com/{GITHUB_USER}/{gh_repo}" if gh_repo else None

    cat_info = CATEGORY_MAP.get(dirname, ("その他", "#6b7280", "#f3f4f6"))

    slug_name = slug(dirname)
    html = generate_page(dirname, manifest, readme_html, github_url, cat_info)

    outpath = os.path.join(OUT, f"{slug_name}.html")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(html)

    generated.append({
        "dir": dirname,
        "slug": slug_name,
        "name": manifest.get("name", ""),
        "desc": manifest.get("description", ""),
        "ver": manifest.get("version", ""),
        "github": github_url,
        "category": cat_info[0],
    })
    print(f"  Created: ext/{slug_name}.html ({manifest.get('name','')})")

print(f"\nTotal: {len(generated)} pages generated")

# JSONに保存（extensions.html更新用）
with open(os.path.join(OUT, "_index.json"), "w", encoding="utf-8") as f:
    json.dump(generated, f, ensure_ascii=False, indent=2)
