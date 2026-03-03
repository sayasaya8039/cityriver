import { Hono } from 'hono'
import { layout } from '../lib/layout'
import { extensions } from '../data/extensions'
import type { Product } from '../data/extensions'
import { webapps } from '../data/webapps'
import { winapps } from '../data/winapps'

export const products = new Hono()

function githubIcon(): string {
  return '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>'
}

function getUniqueCategories(items: Product[]): string[] {
  const cats = new Set<string>()
  for (const item of items) {
    cats.add(item.category)
  }
  return Array.from(cats).sort()
}

function groupByCategory(items: Product[]): Map<string, Product[]> {
  const map = new Map<string, Product[]>()
  for (const item of items) {
    const arr = map.get(item.category) || []
    arr.push(item)
    map.set(item.category, arr)
  }
  return map
}

function renderListingPage(
  items: Product[],
  title: string,
  badge: string,
  badgeBg: string,
  badgeColor: string,
  detailPrefix: string
): string {
  const categories = getUniqueCategories(items)
  const grouped = groupByCategory(items)

  const categoryButtons = categories
    .map((cat) => `<button class="cb" data-cat="${cat}">${cat}</button>`)
    .join('')

  let cardsHtml = ''
  for (const [cat, prods] of grouped) {
    const cards = prods
      .map(
        (p) => `
        <a href="${detailPrefix}/${p.slug}" class="cd" data-name="${p.name}" data-desc="${p.desc}">
          <div class="cf" style="margin-bottom:12px">
            <span class="ctg">${p.category}</span>
            ${p.github ? `<span class="gl">${githubIcon()}</span>` : ''}
          </div>
          <h3>${p.name}</h3>
          <p>${p.desc}</p>
          <div class="cf">
            <span class="mi" style="margin:0">v${p.ver}</span>
            <span class="cl2">詳細 →</span>
          </div>
        </a>`
      )
      .join('')

    cardsHtml += `
      <div class="cs2" id="cat-${cat}" data-category="${cat}">
        <h3 style="font-size:18px;font-weight:700;margin:32px 0 16px;padding-bottom:8px;border-bottom:1px solid var(--border)">${cat}</h3>
        <div class="cg">${cards}</div>
      </div>`
  }

  return `
<section style="padding-top:40px">
  <div class="ct">
    <div class="bc rv">
      <a href="/">ホーム</a>
      <span>/</span>
      <span>${title}</span>
    </div>
    <div class="ph rv">
      <span class="pb" style="background:${badgeBg};color:${badgeColor}">${badge}</span>
      <h1>${title}</h1>
      <p>${items.length}個のプロダクト</p>
    </div>
    <div class="si3 rv">
      <input type="text" id="searchInput" class="si4" placeholder="プロダクトを検索...">
    </div>
    <div class="cn rv">
      <button class="cb act" data-cat="all">すべて</button>
      ${categoryButtons}
    </div>
    ${cardsHtml}
    <div style="margin-top:40px" class="rv">
      <a href="/" class="btn bs">← ホームに戻る</a>
    </div>
  </div>
</section>
`
}

function renderDetailPage(
  item: Product,
  backPath: string,
  backLabel: string,
  breadcrumb: string
): string {
  const metaBadges: string[] = [
    `<span class="mi">v${item.ver}</span>`,
    `<span class="mi">${item.category}</span>`,
  ]
  if (item.tech) {
    metaBadges.push(`<span class="mi">${item.tech}</span>`)
  }

  const actionButtons: string[] = [
    `<a href="${backPath}" class="btn bs">← ${backLabel}</a>`,
  ]
  if (item.github) {
    actionButtons.push(
      `<a href="${item.github}" target="_blank" rel="noopener" class="btn bp">${githubIcon()} GitHub</a>`
    )
  }
  if (item.url) {
    actionButtons.push(
      `<a href="${item.url}" target="_blank" rel="noopener" class="btn bp">🔗 サイトを開く</a>`
    )
  }

  return `
<section style="padding-top:40px">
  <div class="ct">
    <div class="bc rv">
      <a href="/">ホーム</a>
      <span>/</span>
      <a href="${backPath}">${breadcrumb}</a>
      <span>/</span>
      <span>${item.name}</span>
    </div>
    <div class="dh rv">
      <span class="pb" style="background:var(--al);color:var(--accent)">${item.category}</span>
      <h1>${item.name}</h1>
      <p class="ds">${item.desc}</p>
      <div class="mb">${metaBadges.join('')}</div>
      <div class="da">${actionButtons.join('')}</div>
    </div>
    <div class="dc rv">
      <h2>概要</h2>
      <p>${item.desc}</p>
      <h2>特徴</h2>
      <ul>
        <li>バージョン ${item.ver}</li>
        <li>カテゴリ: ${item.category}</li>
        ${item.tech ? `<li>技術スタック: ${item.tech}</li>` : ''}
        ${item.github ? `<li>オープンソース (<a href="${item.github}" target="_blank" rel="noopener">GitHub</a>)</li>` : '<li>プロプライエタリ</li>'}
        ${item.url ? `<li>デモ: <a href="${item.url}" target="_blank" rel="noopener">${item.url}</a></li>` : ''}
      </ul>
      ${item.tech ? `<h2>技術スタック</h2><ul class="tl">${item.tech.split(', ').map((t) => `<li>${t}</li>`).join('')}</ul>` : ''}
    </div>
  </div>
</section>
`
}

// Listing pages
products.get('/extensions', (c) => {
  const content = renderListingPage(
    extensions,
    'Chrome拡張機能',
    '🧩 Extensions',
    'var(--al)',
    'var(--accent)',
    '/ext'
  )
  return c.html(layout(content, 'Chrome拡張機能', 'Chrome拡張機能の一覧'))
})

products.get('/webapps', (c) => {
  const content = renderListingPage(
    webapps,
    'Webアプリケーション',
    '🌐 Web Apps',
    'var(--cl)',
    'var(--cyan)',
    '/webapp'
  )
  return c.html(layout(content, 'Webアプリケーション', 'Webアプリケーションの一覧'))
})

products.get('/windows-apps', (c) => {
  const content = renderListingPage(
    winapps,
    'Windowsアプリケーション',
    '🖥️ Windows Apps',
    'var(--aml)',
    'var(--amber)',
    '/winapp'
  )
  return c.html(layout(content, 'Windowsアプリケーション', 'Windowsアプリケーションの一覧'))
})

// Detail pages
products.get('/ext/:slug', (c) => {
  const slug = c.req.param('slug')
  const item = extensions.find((e) => e.slug === slug)
  if (!item) return c.notFound()
  const content = renderDetailPage(item, '/extensions', '拡張機能一覧', 'Chrome拡張機能')
  return c.html(layout(content, item.name, item.desc))
})

products.get('/webapp/:slug', (c) => {
  const slug = c.req.param('slug')
  const item = webapps.find((e) => e.slug === slug)
  if (!item) return c.notFound()
  const content = renderDetailPage(item, '/webapps', 'Webアプリ一覧', 'Webアプリケーション')
  return c.html(layout(content, item.name, item.desc))
})

products.get('/winapp/:slug', (c) => {
  const slug = c.req.param('slug')
  const item = winapps.find((e) => e.slug === slug)
  if (!item) return c.notFound()
  let content = renderDetailPage(item, '/windows-apps', 'Winアプリ一覧', 'Windowsアプリケーション')
  if (slug === 'smux') {
    const smuxScreenshots = `
      <div style="margin-top:24px"><a href="/winapp/smux-reference.html" class="btn bp" style="display:inline-flex;align-items:center;gap:6px">&#x1F4CB; 設定 &amp; コマンド一覧</a></div>
      <h2>スクリーンショット</h2>
      <div style="margin-bottom:32px">
        <img src="/winapp/images/smux-claude-code.png" alt="smux で Claude Code を実行中" style="width:100%;border-radius:12px;border:1px solid var(--border);box-shadow:0 4px 20px rgba(0,0,0,.08)" loading="lazy">
        <p style="margin-top:14px;font-size:15px;color:var(--ts);line-height:1.7"><strong style="color:var(--tp)">Claude Code teammate-mode との連携。</strong>左側サイドバーにワークスペース名・Gitブランチ・作業ディレクトリを表示。tmux互換CLIにより <code>claude --teammate-mode tmux</code> でAIエージェントとのシームレスな協調作業が可能。</p>
      </div>
      <div style="margin-bottom:32px">
        <img src="/winapp/images/smux-split-panes.png" alt="4分割ペインで並列 AI コーディング" style="width:100%;border-radius:12px;border:1px solid var(--border);box-shadow:0 4px 20px rgba(0,0,0,.08)" loading="lazy">
        <p style="margin-top:14px;font-size:15px;color:var(--ts);line-height:1.7"><strong style="color:var(--tp)">4分割ペインによる並列AIコーディング。</strong>Ctrl+D / Ctrl+Shift+D でペインを自由に分割し、各ペインで独立したClaude Codeセッションを同時実行。GPU加速描画により4ペイン同時でも滑らかな操作感を維持。</p>
      </div>`
    content = content.replace(
      '</ul>',
      `</ul>${smuxScreenshots}`
    )
  }
  return c.html(layout(content, item.name, item.desc))
})
