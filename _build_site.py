#!/usr/bin/env python3
"""Generate ALL CityRiver pages with modern dynamic design."""
import json, html as html_module, os
from pathlib import Path

BASE = Path(r"P:/GitHub/cityriver")

def h(t):
    return html_module.escape(str(t)) if t else ""

# SVGs
ARROW = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>'
BACK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>'
GH = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>'
UP = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 15l-6-6-6 6"/></svg>'
MOON = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'

CSS = (BASE / "shared.css").read_text(encoding="utf-8") if (BASE / "shared.css").exists() else ""

JS = r"""<script>
const H=document.documentElement,S=localStorage.getItem('theme');
if(S)H.dataset.theme=S;else if(matchMedia('(prefers-color-scheme:dark)').matches)H.dataset.theme='dark';
document.querySelectorAll('.tt').forEach(b=>b.addEventListener('click',()=>{const n=H.dataset.theme==='dark'?'light':'dark';H.dataset.theme=n;localStorage.setItem('theme',n)}));
document.querySelectorAll('.hb').forEach(h=>h.addEventListener('click',()=>{h.classList.toggle('active');document.querySelector('.mm')?.classList.toggle('active')}));
const O=new IntersectionObserver(e=>e.forEach(x=>{if(x.isIntersecting){x.target.classList.add('vis');O.unobserve(x.target)}}),{threshold:.1});
document.querySelectorAll('.rv').forEach(e=>O.observe(e));
function aC(){document.querySelectorAll('[data-count]').forEach(e=>{const t=parseInt(e.dataset.count);let c=0;const s=Math.max(1,Math.floor(t/40));const i=setInterval(()=>{c+=s;if(c>=t){c=t;clearInterval(i)}e.textContent=c+(e.dataset.suffix||'')},30)})}
const CO=new IntersectionObserver(e=>e.forEach(x=>{if(x.isIntersecting){aC();CO.unobserve(x.target)}}),{threshold:.3});
document.querySelectorAll('.sr').forEach(e=>CO.observe(e));
const BT=document.querySelector('.bt');
if(BT){window.addEventListener('scroll',()=>BT.classList.toggle('vis',scrollY>400));BT.addEventListener('click',()=>scrollTo({top:0,behavior:'smooth'}))}
document.querySelectorAll('.yr').forEach(e=>e.textContent=new Date().getFullYear());
const SI=document.querySelector('.si4');
if(SI)SI.addEventListener('input',e=>{const q=e.target.value.toLowerCase();document.querySelectorAll('.cd[data-name]').forEach(c=>{c.style.display=(c.dataset.name.toLowerCase().includes(q)||c.dataset.desc?.toLowerCase().includes(q))?'':'none'})});
document.querySelectorAll('.cb[data-cat]').forEach(b=>b.addEventListener('click',e=>{e.preventDefault();document.querySelectorAll('.cb').forEach(x=>x.classList.remove('act'));b.classList.add('act');const c=b.dataset.cat;document.querySelectorAll('.cd[data-cat]').forEach(x=>x.style.display=(!c||x.dataset.cat===c)?'':'none');document.querySelectorAll('.cs2[data-cat]').forEach(x=>x.style.display=(!c||x.dataset.cat===c)?'':'none')}));
</script>"""

def nav(p=""):
    return f'''<header class="nw"><nav class="nv">
<a href="{p}index.html" class="nl"><img src="{p}Logo.png" alt="CityRiver">合同会社シティーリバー</a>
<div class="nk"><a href="{p}index.html#services">事業内容</a><a href="{p}index.html#products">プロダクト</a><a href="{p}index.html#profile">会社情報</a><a href="{p}index.html#contact" class="nc">お問い合わせ</a><button class="tt" aria-label="テーマ切替">{MOON}</button></div>
<div style="display:flex;gap:8px;align-items:center"><button class="tt" aria-label="テーマ切替">{MOON}</button><button class="hb" aria-label="メニュー"><span></span><span></span><span></span></button></div>
</nav></header>
<div class="mm"><a href="{p}index.html">ホーム</a><a href="{p}index.html#services">事業内容</a><a href="{p}index.html#products">プロダクト</a><a href="{p}extensions.html">拡張機能</a><a href="{p}webapps.html">Webアプリ</a><a href="{p}windows-apps.html">Windowsアプリ</a><a href="{p}index.html#contact">お問い合わせ</a></div>'''

def shell(title, desc, body, p=""):
    return f'''<!DOCTYPE html><html lang="ja"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{h(title)} | 合同会社シティーリバー</title>
<meta name="description" content="{h(desc)}"/>
<link rel="icon" type="image/png" sizes="32x32" href="{p}favicon-32x32.png"/>
<link rel="icon" type="image/png" sizes="16x16" href="{p}favicon-16x16.png"/>
<link rel="apple-touch-icon" sizes="180x180" href="{p}apple-touch-icon.png"/>
<link rel="icon" href="{p}favicon.ico"/>
<style>{CSS}</style></head><body>
<div class="bg-blobs"><span></span><span></span><span></span></div>
{nav(p)}<div class="cw">{body}</div>
<footer><div class="fi"><div class="fc">&copy; <span class="yr"></span> 合同会社シティーリバー / CityRiver LLC</div><div class="fl"><a href="{p}index.html">ホーム</a><a href="{p}extensions.html">拡張機能</a><a href="{p}webapps.html">Webアプリ</a><a href="{p}windows-apps.html">Windowsアプリ</a></div></div></footer>
<button class="bt" aria-label="トップへ戻る">{UP}</button>{JS}</body></html>'''

# ─── INDEX ─────────────────────────────────────────────────────────
print("Generating index.html...")
idx = f'''<section class="hero"><div class="ct">
<div class="hbg"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3l1.5 4.5H18l-3.5 2.8 1.3 4.2L12 12l-3.8 2.5 1.3-4.2L6 7.5h4.5z"/></svg> Flowing With The City</div>
<h1>街に、<span class="gt">ビジネスと創造</span>の<br>新しい流れを描く。</h1>
<p class="hs">投資業・イラスト制作・Webデザイン・note記事作成・コンビニエンスストア運営。<br>多彩な事業を通じ、人と街をつなぐ価値を創造しています。</p>
<div class="ha"><a class="btn bp" href="#services">事業内容を見る {ARROW}</a><a class="btn bs" href="#profile">会社情報</a></div>
</div></section>
<section id="services"><div class="ct">
<div class="sh rv"><div class="sb" style="background:var(--al);color:var(--accent)">事業紹介</div><h2 class="st">事業内容</h2><p class="ss">都市生活をめぐる5つの領域で、投資・クリエイティブ・店舗運営を横断的に支援します。</p></div>
<div class="svg">
<a href="investment.html" class="sc rv rd1"><span class="si2">📈</span><h3>投資業</h3><p>成長分野への戦略投資と、長期的な資産形成のパートナーです。</p></a>
<a href="illustration.html" class="sc rv rd2"><span class="si2">🎨</span><h3>イラスト制作</h3><p>ブランドの世界観を、丁寧なアートワークで印象を最大化します。</p></a>
<a href="webdesign.html" class="sc rv rd3"><span class="si2">💻</span><h3>Webデザイン</h3><p>洗練されたビジュアルと情報設計で成果につながるサイトを構築。</p></a>
<a href="note-writing.html" class="sc rv rd1"><span class="si2">✍️</span><h3>note記事作成</h3><p>読者の心に響く丁寧な文章で、魅力的にブランドを発信します。</p></a>
<a href="convenience-store.html" class="sc rv rd2"><span class="si2">🏪</span><h3>コンビニエンスストア</h3><p>地域に密着した店舗づくりで、暮らしに寄り添うサービス。</p></a>
</div></div></section>
<section id="products" style="background:var(--bg-section)"><div class="ct">
<div class="sh rv"><div class="sb" style="background:var(--cl);color:var(--cyan)">プロダクト</div><h2 class="st">開発プロダクト</h2><p class="ss">ブラウザ拡張機能、Webアプリ、Windowsアプリを開発・提供しています。</p></div>
<div class="sr rv">
<div class="si"><div class="sn" data-count="30" data-suffix="+">0</div><div class="sl">拡張機能</div></div>
<div class="si"><div class="sn" data-count="33" data-suffix="+">0</div><div class="sl">Webアプリ</div></div>
<div class="si"><div class="sn" data-count="36" data-suffix="+">0</div><div class="sl">Windowsアプリ</div></div>
<div class="si"><div class="sn" data-count="99" data-suffix="+">0</div><div class="sl">プロダクト合計</div></div>
</div>
<div class="pg">
<a href="extensions.html" class="pc cd rv rd1"><div class="ci pu"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg></div><h3>ブラウザ拡張機能</h3><p>Chrome・Edge対応。日常のブラウジングをより便利に。</p><span class="cl2">30+の拡張機能を見る {ARROW}</span></a>
<a href="webapps.html" class="pc cd rv rd2"><div class="ci cy"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg></div><h3>Webアプリ</h3><p>インストール不要。ブラウザですぐに利用可能。</p><span class="cl2">33+のWebアプリを見る {ARROW}</span></a>
<a href="windows-apps.html" class="pc cd rv rd3"><div class="ci am"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg></div><h3>Windowsアプリ</h3><p>高速で安定したネイティブアプリケーション。</p><span class="cl2">36+のWindowsアプリを見る {ARROW}</span></a>
</div></div></section>
<section id="profile"><div class="ct">
<div class="sh rv"><div class="sb" style="background:var(--gl);color:var(--green)">会社概要</div><h2 class="st">会社情報</h2><p class="ss">信頼とスピードを両立した意思決定を行っています。</p></div>
<div class="ig">
<div class="ic rv"><h3>📋 企業概要</h3><dl>
<div class="ir"><dt>会社名</dt><dd>合同会社シティーリバー</dd></div>
<div class="ir"><dt>代表</dt><dd>市川 武宏</dd></div>
<div class="ir"><dt>所在地</dt><dd>〒470-0132 愛知県日進市梅森町上松649番地1</dd></div>
<div class="ir"><dt>電話</dt><dd><a href="tel:090-8868-6505">090-8868-6505</a></dd></div>
<div class="ir"><dt>メール</dt><dd><a href="mailto:cityriver8039@gmail.com">cityriver8039@gmail.com</a></dd></div>
</dl></div>
<div class="ic rv rd1"><h3>💡 私たちの姿勢</h3>
<div style="border-left:3px solid var(--accent);padding-left:20px;margin-bottom:16px"><p style="font-size:16px;font-weight:500;color:var(--text);line-height:1.8">都市に流れる水のように、多様なニーズを受け止め、柔らかくかつ確実に価値へとつなぐ。</p></div>
<p style="font-size:14px;color:var(--text-s);line-height:1.8">投資では持続性と透明性を重視し、クリエイティブ領域では感性と機能性の融合を追求。店舗運営では地域との共創を軸に、循環するビジネスの流れをデザインします。</p>
</div></div></div></section>
<section id="contact"><div class="ct"><div class="cs rv">
<h2>お問い合わせ</h2><p>新規プロジェクトのご相談、コラボレーション、メディア取材など、お気軽にご連絡ください。</p>
<div class="ca"><a class="btn bp" href="mailto:cityriver8039@gmail.com">メールで問い合わせる</a><a class="btn bs" href="tel:090-8868-6505">電話する</a></div>
</div></div></section>'''
with open(BASE / "index.html", "w", encoding="utf-8", newline="\n") as f:
    f.write(shell("合同会社シティーリバー", "投資業、イラスト制作、Webデザイン、note記事作成、コンビニエンスストア運営を通じて街に新しい流れを生み出します。", idx))
print("  index.html OK")

# ─── SERVICE PAGES ─────────────────────────────────────────────────
SERVICES = [
    ("investment.html","投資業","📈","成長分野への戦略的投資",[("事業概要","成長分野への戦略投資と、長期的な視点に立った資産形成のパートナーとして、確かなリターンを目指します。"),("投資方針","テクノロジー、ヘルスケア、環境エネルギーなどの成長セクターに注目し、中長期的な視点で投資判断を行います。"),("強み","多角的な事業基盤を持つことで、単一市場のリスクに依存しない投資ポートフォリオを構築しています。")]),
    ("illustration.html","イラスト制作","🎨","心を動かすアートワーク",[("事業概要","ブランドの世界観やプロジェクトの想いを、細部まで丁寧に描き出すアートワークで印象を最大化します。"),("対応範囲","Webイラスト、キャラクターデザイン、ロゴ制作、広告ビジュアル、書籍カバーなど幅広いジャンルに対応。"),("制作フロー","ヒアリング → コンセプト設計 → ラフ → 本制作 → 納品の5ステップで進行します。")]),
    ("webdesign.html","Webデザイン","💻","成果につながるWeb制作",[("事業概要","洗練されたビジュアルと堅牢な情報設計で成果につながるサイトを構築します。"),("技術スタック","React、Next.js、Svelte、Hono、Cloudflare Workersなど最新技術を活用。"),("特徴","レスポンシブ対応、SEO最適化、アクセシビリティ対応を標準装備。")]),
    ("note-writing.html","note記事作成","✍️","心に響くコンテンツ制作",[("事業概要","読者の心に響く丁寧な文章で、ブランドストーリーや専門知識を魅力的に発信。SEO最適化で検索上位を目指します。"),("サービス内容","企業ブログ、技術記事、ブランドストーリー、インタビュー記事など目的に合わせた記事を作成。"),("特徴","SEOキーワード分析、競合調査、読者ペルソナの設計を行い、成果にコミットします。")]),
    ("convenience-store.html","コンビニエンスストア運営","🏪","地域に根ざした店舗づくり",[("事業概要","地域に密着した店舗づくりで、日々の暮らしに寄り添うサービスを提供します。"),("特徴","テクノロジーを活用した効率的な店舗運営と、きめ細やかなサービスを両立。"),("ビジョン","地域コミュニティのハブとして、新しい価値を創造し続けます。")]),
    ("cityriver.html","会社案内","🏢","合同会社シティーリバーについて",[("会社概要","投資業、イラスト制作、Webデザイン、note記事作成、コンビニエンスストア運営の5つの事業を展開する総合企業です。"),("ミッション","「街に、ビジネスと創造の新しい流れを描く」をミッションに、社会に価値を提供します。"),("代表メッセージ","都市に流れる水のように、多様なニーズを受け止め、柔らかくかつ確実に価値へとつなぐ。")]),
]

for fn, title, icon, sub, secs in SERVICES:
    b = f'<section class="hero" style="padding:80px 40px 60px"><div class="ct"><div class="bc"><a href="index.html">ホーム</a><span>/</span>{h(title)}</div><div class="hbg">{icon} {h(title)}</div><h1>{h(title)}</h1><p class="hs">{h(sub)}</p></div></section><section><div class="ct">'
    for i,(st,sb) in enumerate(secs):
        b += f'<div class="rv{" rd"+str(i%3+1) if i else ""}" style="margin-bottom:40px"><h2 style="font-size:24px;font-weight:700;margin-bottom:14px">{h(st)}</h2><p style="font-size:15px;color:var(--text-s);line-height:1.9">{h(sb)}</p></div>'
    b += f'<div style="margin-top:48px;padding-top:32px;border-top:1px solid var(--border)"><a href="index.html" class="btn bs">{BACK} ホームに戻る</a></div></div></section>'
    with open(BASE / fn, "w", encoding="utf-8", newline="\n") as f:
        f.write(shell(title, sub, b))
    print(f"  {fn} OK")

# ─── LIST PAGE GENERATOR ───────────────────────────────────────────
def gen_list_page(apps, page_title, page_icon, accent_color, accent_bg, slug_prefix, categories, out_file):
    cat_groups = {}
    for c in categories:
        cat_groups[c["name"]] = [a for a in apps if a.get("category") == c["name"]]
    cat_nav = '<button class="cb act" data-cat="">すべて</button>'
    for c in categories:
        if cat_groups.get(c["name"]):
            cat_nav += f'<button class="cb" data-cat="{h(c["name"])}">{c.get("emoji","")} {h(c["name"])}</button>'

    cards = ""
    for c in categories:
        items = cat_groups.get(c["name"], [])
        if not items: continue
        cards += f'<div class="cs2" data-cat="{h(c["name"])}" style="margin-bottom:48px">'
        cards += f'<h2 style="font-size:20px;font-weight:700;margin-bottom:8px;display:flex;align-items:center;gap:10px">{c.get("emoji","")} {h(c["name"])}</h2>'
        cards += f'<p style="font-size:13px;color:var(--text-s);margin-bottom:20px">{len(items)} 件</p>'
        cards += '<div class="cg">'
        for a in items:
            gh_link = f'<a href="{h(a["github"])}" class="gl" target="_blank" rel="noopener">{GH}</a>' if a.get("github") else ""
            cards += f'''<div class="cd rv" data-name="{h(a["name"])}" data-desc="{h(a["desc"])}" data-cat="{h(a.get("category",""))}">
<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-bottom:10px"><h3>{h(a["name"])}</h3><span class="ctg">v{h(a["ver"])}</span></div>
<p>{h(a["desc"])}</p>
<div class="cf"><a href="{slug_prefix}{h(a["slug"])}.html" class="cl2">詳細を見る {ARROW}</a><div style="display:flex;align-items:center;gap:8px">{gh_link}</div></div></div>'''
        cards += '</div></div>'

    total = len(apps)
    body = f'''<section style="padding-top:40px"><div class="ct">
<div class="bc"><a href="index.html">ホーム</a><span>/</span><a href="index.html#products">プロダクト</a><span>/</span>{h(page_title)}</div>
<div class="ph"><div class="pb" style="background:{accent_bg};color:{accent_color}">{page_icon} {h(page_title)}</div><h1>{h(page_title)}</h1><p>{total}+ のプロダクトをご覧いただけます</p></div>
<div class="si3"><input class="si4" type="text" placeholder="🔍 アプリ名で検索..."></div>
<div class="cn">{cat_nav}</div>
{cards}
</div></section>'''
    return shell(page_title, f"合同会社シティーリバーの{page_title}", body)

# ─── DETAIL PAGE GENERATOR ─────────────────────────────────────────
def gen_feature_bullets(desc, tech):
    bullets = []
    kw = {"AI":"AIによるインテリジェントな分析","リアルタイム":"リアルタイム処理","自動":"自動化ワークフロー","検索":"高速検索","管理":"直感的な管理","変換":"多フォーマット変換","プライバシー":"プライバシー保護","音声":"音声処理","画像":"画像処理","カンバン":"カンバン管理","ターミナル":"マルチターミナル"}
    dl = desc.lower() if desc else ""
    for k,v in kw.items():
        if k.lower() in dl or k in desc:
            bullets.append(v)
        if len(bullets)>=4: break
    if len(bullets)<2: bullets.append("Windowsネイティブの高速動作")
    if len(bullets)<3: bullets.append("シンプルで直感的なUI")
    if "Rust" in (tech or ""):
        bullets.append("Rust製の安全で高速な実装")
    elif len(bullets)<4:
        bullets.append("最適化された設計")
    return bullets[:5]

def gen_detail_page(app, back_url, back_label, prefix, accent_color, accent_bg):
    name = h(app["name"])
    desc = h(app["desc"])
    ver = h(app["ver"])
    tech = h(app.get("tech",""))
    cat = h(app.get("category",""))
    github = app.get("github")
    tech_items = [t.strip() for t in (app.get("tech") or "").split(",") if t.strip()]
    bullets = gen_feature_bullets(app["desc"], app.get("tech",""))
    bullets_html = "".join(f"<li>{h(b)}</li>" for b in bullets)
    tech_html = "".join(f"<li>{h(t)}</li>" for t in tech_items)
    gh_btn = f'<a href="{h(github)}" class="btn bp" target="_blank" rel="noopener">{GH} GitHub</a>' if github else ""
    gh_section = f'<h2>ソースコード</h2><p><a href="{h(github)}" target="_blank" rel="noopener">GitHub</a> で公開中。Issue・Pull Requestを歓迎します。</p>' if github else ""

    body = f'''<section style="padding-top:40px"><div class="ct" style="max-width:900px">
<div class="bc"><a href="{prefix}index.html">ホーム</a><span>/</span><a href="{prefix}index.html#products">プロダクト</a><span>/</span><a href="{prefix}{back_url}">{h(back_label)}</a><span>/</span>{name}</div>
<div class="dh"><div class="pb" style="background:{accent_bg};color:{accent_color}">{cat}</div><h1>{name}</h1><p class="ds">{desc}</p>
<div class="mb"><div class="mi"><strong>v{ver}</strong></div><div class="mi">{tech}</div><div class="mi">{cat}</div></div>
<div class="da">{gh_btn}<a href="{prefix}{back_url}" class="btn bs">{BACK} 一覧に戻る</a></div></div>
<div class="dc"><p>{desc}</p><h2>主な機能</h2><ul>{bullets_html}</ul><h2>技術スタック</h2><ul class="tl">{tech_html}</ul>{gh_section}</div>
<a href="{prefix}{back_url}" class="btn bs" style="margin-top:40px">{BACK} {h(back_label)}に戻る</a>
</div></section>'''
    return shell(app["name"], desc, body, prefix)


# ─── WINDOWS APPS ──────────────────────────────────────────────────
WIN_CATS = [
    {"name":"AIツール","emoji":"🤖"},{"name":"開発ツール","emoji":"🛠️"},
    {"name":"メディア","emoji":"🎬"},{"name":"システム","emoji":"⚙️"},
    {"name":"プロダクティビティ","emoji":"📋"},{"name":"プライバシー","emoji":"🔒"},
    {"name":"ユーティリティ","emoji":"🔧"},{"name":"ライフスタイル","emoji":"🏠"},
]

print("Generating Windows app pages...")
with open(BASE / "winapp" / "_index.json", "r", encoding="utf-8") as f:
    winapps = json.load(f)
with open(BASE / "windows-apps.html", "w", encoding="utf-8", newline="\n") as f:
    f.write(gen_list_page(winapps, "Windowsアプリ一覧", "🖥️", "var(--amber)", "var(--aml)", "winapp/", WIN_CATS, "windows-apps.html"))
print(f"  windows-apps.html ({len(winapps)} apps)")
for app in winapps:
    dp = gen_detail_page(app, "windows-apps.html", "Windowsアプリ", "../", "var(--amber)", "var(--aml)")
    with open(BASE / "winapp" / f'{app["slug"]}.html', "w", encoding="utf-8", newline="\n") as f:
        f.write(dp)
print(f"  winapp/*.html ({len(winapps)} detail pages)")

# ─── WEB APPS ──────────────────────────────────────────────────────
WEB_CATS = [
    {"name":"AIツール","emoji":"🤖"},{"name":"ビジネス","emoji":"💼"},
    {"name":"エンタメ","emoji":"🎮"},{"name":"ライフスタイル","emoji":"🏠"},
    {"name":"開発ツール","emoji":"🛠️"},{"name":"教育","emoji":"📚"},
    {"name":"ユーティリティ","emoji":"🔧"},{"name":"SNS","emoji":"📱"},
]

print("Generating Web app pages...")
with open(BASE / "webapp" / "_index.json", "r", encoding="utf-8") as f:
    webapps = json.load(f)
# Collect unique categories
web_cat_names = set(a.get("category","") for a in webapps)
web_cats_final = [c for c in WEB_CATS if c["name"] in web_cat_names]
for cn in web_cat_names:
    if cn and not any(c["name"]==cn for c in web_cats_final):
        web_cats_final.append({"name":cn,"emoji":"📦"})
with open(BASE / "webapps.html", "w", encoding="utf-8", newline="\n") as f:
    f.write(gen_list_page(webapps, "Webアプリ一覧", "🌐", "var(--cyan)", "var(--cl)", "webapp/", web_cats_final, "webapps.html"))
print(f"  webapps.html ({len(webapps)} apps)")
for app in webapps:
    dp = gen_detail_page(app, "webapps.html", "Webアプリ", "../", "var(--cyan)", "var(--cl)")
    with open(BASE / "webapp" / f'{app["slug"]}.html', "w", encoding="utf-8", newline="\n") as f:
        f.write(dp)
print(f"  webapp/*.html ({len(webapps)} detail pages)")

# ─── EXTENSIONS ────────────────────────────────────────────────────
EXT_CATS = [
    {"name":"生産性向上","emoji":"⚡"},{"name":"note.com","emoji":"📝"},
    {"name":"AI支援","emoji":"🤖"},{"name":"ユーティリティ","emoji":"🔧"},
    {"name":"SNS","emoji":"📱"},{"name":"ショッピング","emoji":"🛒"},
    {"name":"エンタメ","emoji":"🎮"},{"name":"開発ツール","emoji":"🛠️"},
]

print("Generating Extension pages...")
with open(BASE / "ext" / "_index.json", "r", encoding="utf-8") as f:
    exts = json.load(f)
ext_cat_names = set(a.get("category","") for a in exts)
ext_cats_final = [c for c in EXT_CATS if c["name"] in ext_cat_names]
for cn in ext_cat_names:
    if cn and not any(c["name"]==cn for c in ext_cats_final):
        ext_cats_final.append({"name":cn,"emoji":"📦"})
with open(BASE / "extensions.html", "w", encoding="utf-8", newline="\n") as f:
    f.write(gen_list_page(exts, "ブラウザ拡張機能一覧", "🧩", "var(--accent)", "var(--al)", "ext/", ext_cats_final, "extensions.html"))
print(f"  extensions.html ({len(exts)} extensions)")
for app in exts:
    dp = gen_detail_page(app, "extensions.html", "拡張機能", "../", "var(--accent)", "var(--al)")
    with open(BASE / "ext" / f'{app["slug"]}.html', "w", encoding="utf-8", newline="\n") as f:
        f.write(dp)
print(f"  ext/*.html ({len(exts)} detail pages)")

# ─── SUMMARY ───────────────────────────────────────────────────────
total = 1 + len(SERVICES) + 1 + len(winapps) + 1 + len(webapps) + 1 + len(exts)
print(f"\n=== DONE! Total: {total} pages generated ===")
