import { Hono } from 'hono'
import { layout } from '../lib/layout'

export const home = new Hono()

home.get('/', (c) => {
  const content = `
<div class="hero">
  <div class="rv" style="margin-bottom:24px">
    <img src="/images/cityriver-logo.png" alt="CityRiver LLC" style="max-width:480px;width:90%;height:auto;border-radius:16px;filter:drop-shadow(0 8px 32px rgba(59,130,246,.35))" loading="eager">
  </div>
  <div class="hbg rv">Flowing With The City</div>
  <h1 class="rv rd1">テクノロジーで<br><span class="gt">暮らしを豊かに</span></h1>
  <p class="hs rv rd2">Chrome拡張機能・Webアプリ・Windowsアプリの開発から、投資事業、イラスト制作まで。<br>多角的なアプローチで新しい価値を創造します。</p>
  <div class="ha rv rd3">
    <a href="#products" class="btn bp">プロダクト一覧 →</a>
    <a href="#contact" class="btn bs">お問い合わせ</a>
  </div>
</div>

<section id="services">
  <div class="ct">
    <div class="sh rv">
      <span class="sb" style="background:var(--al);color:var(--accent)">Services</span>
      <h2 class="st">事業内容</h2>
      <p class="ss">テクノロジーとクリエイティビティで、多角的に価値を創造</p>
    </div>
    <div class="svg">
      <a href="/investment" class="sc rv">
        <span class="si2">📈</span>
        <h3>投資業</h3>
        <p>成長分野への戦略的投資と長期的な視点に立った資産形成をサポートします</p>
      </a>
      <a href="/illustration" class="sc rv rd1">
        <span class="si2">🎨</span>
        <h3>イラスト制作</h3>
        <p>ブランドの世界観を表現する高品質なアートワークを制作します</p>
      </a>
      <a href="/webdesign" class="sc rv rd2">
        <span class="si2">💻</span>
        <h3>Webデザイン</h3>
        <p>洗練されたデザインと堅牢な技術で成果につながるサイトを構築します</p>
      </a>
      <a href="/note-writing" class="sc rv">
        <span class="si2">✍️</span>
        <h3>note記事作成</h3>
        <p>読者の心に響くコンテンツでブランドストーリーを魅力的に発信します</p>
      </a>
      <a href="/convenience-store" class="sc rv rd1">
        <span class="si2">🏪</span>
        <h3>コンビニエンスストア運営</h3>
        <p>地域に密着した店舗づくりで日々の暮らしに寄り添うサービスを提供します</p>
      </a>
    </div>
  </div>
</section>

<section id="products" style="background:var(--bg-section)">
  <div class="ct">
    <div class="sh rv">
      <span class="sb" style="background:var(--cl);color:var(--cyan)">Products</span>
      <h2 class="st">プロダクト</h2>
      <p class="ss">日々の課題を解決する多彩なツールを開発・提供</p>
    </div>
    <div class="sr rv">
      <div class="si">
        <span class="sn" data-count="30" data-suffix="+">0</span>
        <span class="sl">拡張機能</span>
      </div>
      <div class="si">
        <span class="sn" data-count="33" data-suffix="+">0</span>
        <span class="sl">Webアプリ</span>
      </div>
      <div class="si">
        <span class="sn" data-count="36" data-suffix="+">0</span>
        <span class="sl">Windowsアプリ</span>
      </div>
      <div class="si">
        <span class="sn" data-count="99" data-suffix="+">0</span>
        <span class="sl">プロダクト合計</span>
      </div>
    </div>
    <div class="pg">
      <a href="/extensions" class="pc rv">
        <div class="ci pu">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>
        </div>
        <h3>Chrome拡張機能</h3>
        <p>ブラウザの機能を拡張する30以上のChrome拡張機能。生産性向上からAI活用まで。</p>
        <span class="cl2">一覧を見る <span>→</span></span>
      </a>
      <a href="/webapps" class="pc rv rd1">
        <div class="ci cy">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
        </div>
        <h3>Webアプリケーション</h3>
        <p>React・Next.js・SvelteKitなど最新技術で構築した33以上のWebアプリケーション。</p>
        <span class="cl2">一覧を見る <span>→</span></span>
      </a>
      <a href="/windows-apps" class="pc rv rd2">
        <div class="ci am">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/></svg>
        </div>
        <h3>Windowsアプリケーション</h3>
        <p>Tauri・Electron・Rust・Pythonで開発した36以上のデスクトップアプリケーション。</p>
        <span class="cl2">一覧を見る <span>→</span></span>
      </a>
    </div>
  </div>
</section>

<section id="profile">
  <div class="ct">
    <div class="sh rv">
      <span class="sb" style="background:var(--aml);color:var(--amber)">Company</span>
      <h2 class="st">会社情報</h2>
    </div>
    <div class="ig rv">
      <div class="ic">
        <h3>会社概要</h3>
        <dl>
          <div class="ir"><dt>会社名</dt><dd>合同会社シティーリバー</dd></div>
          <div class="ir"><dt>英文名</dt><dd>CityRiver LLC</dd></div>
          <div class="ir"><dt>設立</dt><dd>2025年</dd></div>
          <div class="ir"><dt>代表</dt><dd>代表社員</dd></div>
          <div class="ir"><dt>事業内容</dt><dd>ソフトウェア開発・投資業・イラスト制作・Webデザイン・小売業</dd></div>
          <div class="ir"><dt>所在地</dt><dd>愛知県</dd></div>
        </dl>
      </div>
      <div class="ic">
        <h3>企業理念</h3>
        <dl>
          <div class="ir"><dt>ミッション</dt><dd>テクノロジーで暮らしを豊かにする</dd></div>
          <div class="ir"><dt>ビジョン</dt><dd>多角的なアプローチで新しい価値を創造し、社会に貢献する企業を目指す</dd></div>
          <div class="ir"><dt>バリュー</dt><dd>革新性・信頼性・多様性を大切にし、常に挑戦し続ける</dd></div>
        </dl>
      </div>
    </div>
  </div>
</section>

<section id="contact">
  <div class="ct">
    <div class="cs rv">
      <h2>お問い合わせ</h2>
      <p>プロダクトに関するご質問、事業に関するお問い合わせなど<br>お気軽にご連絡ください。</p>
      <div class="ca">
        <a href="mailto:contact@cityriver.jp" class="btn bp">メールで問い合わせ</a>
        <a href="https://github.com/sayasaya8039" target="_blank" rel="noopener" class="btn bs">GitHub</a>
      </div>
    </div>
  </div>
</section>
`

  return c.html(layout(content))
})
