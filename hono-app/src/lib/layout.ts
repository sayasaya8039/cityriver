import { logoBase64 } from './logo'
import { styles } from './styles'

export function layout(content: string, title?: string, description?: string): string {
  const pageTitle = title ? `${title} | 合同会社シティーリバー` : '合同会社シティーリバー - CityRiver LLC'
  const pageDesc = description || 'テクノロジーで暮らしを豊かに。Chrome拡張機能・Webアプリ・Windowsアプリの開発から、投資事業、イラスト制作まで幅広く展開する合同会社シティーリバーの公式サイトです。'

  return `<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${pageTitle}</title>
<meta name="description" content="${pageDesc}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<style>${styles}</style>
</head>
<body>
<div class="bg-blobs"><span></span><span></span><span></span></div>

<nav class="nw">
  <div class="nv">
    <a href="/" class="nl">
      <img src="${logoBase64}" alt="CityRiver" width="32" height="32">
      CityRiver
    </a>
    <div class="nk">
      <a href="/#services">事業内容</a>
      <a href="/#products">プロダクト</a>
      <a href="/extensions">拡張機能</a>
      <a href="/webapps">Webアプリ</a>
      <a href="/windows-apps">Winアプリ</a>
      <a href="/#profile">会社情報</a>
      <a href="/#contact" class="nc">お問い合わせ</a>
    </div>
    <div style="display:flex;align-items:center;gap:8px">
      <button class="tt" id="themeToggle" aria-label="テーマ切替">
        <svg id="sunIcon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
        <svg id="moonIcon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display:none"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
      </button>
      <button class="hb" id="hamburger" aria-label="メニュー">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</nav>

<div class="mm" id="mobileMenu">
  <a href="/#services">事業内容</a>
  <a href="/#products">プロダクト</a>
  <a href="/extensions">拡張機能</a>
  <a href="/webapps">Webアプリ</a>
  <a href="/windows-apps">Winアプリ</a>
  <a href="/#profile">会社情報</a>
  <a href="/#contact">お問い合わせ</a>
</div>

<div class="cw">
${content}
</div>

<footer>
  <div class="fi">
    <p class="fc">&copy; 2025 合同会社シティーリバー (CityRiver LLC). All rights reserved.</p>
    <div class="fl">
      <a href="/#services">事業内容</a>
      <a href="/#products">プロダクト</a>
      <a href="/#profile">会社情報</a>
      <a href="/#contact">お問い合わせ</a>
      <a href="/terms">利用規約</a>
    </div>
  </div>
</footer>

<button class="bt" id="backTop" aria-label="トップへ戻る">
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 15l-6-6-6 6"/></svg>
</button>

<script>
(function(){
  // Theme toggle
  var themeBtn=document.getElementById('themeToggle');
  var sunIcon=document.getElementById('sunIcon');
  var moonIcon=document.getElementById('moonIcon');
  var html=document.documentElement;
  var saved=localStorage.getItem('theme');
  if(saved==='dark'||(saved==null&&window.matchMedia('(prefers-color-scheme:dark)').matches)){
    html.setAttribute('data-theme','dark');
    sunIcon.style.display='none';moonIcon.style.display='block';
  }
  themeBtn.addEventListener('click',function(){
    var isDark=html.getAttribute('data-theme')==='dark';
    if(isDark){
      html.removeAttribute('data-theme');
      localStorage.setItem('theme','light');
      sunIcon.style.display='block';moonIcon.style.display='none';
    }else{
      html.setAttribute('data-theme','dark');
      localStorage.setItem('theme','dark');
      sunIcon.style.display='none';moonIcon.style.display='block';
    }
  });

  // Hamburger menu
  var hb=document.getElementById('hamburger');
  var mm=document.getElementById('mobileMenu');
  hb.addEventListener('click',function(){
    hb.classList.toggle('active');
    mm.classList.toggle('active');
  });
  mm.querySelectorAll('a').forEach(function(a){
    a.addEventListener('click',function(){
      hb.classList.remove('active');
      mm.classList.remove('active');
    });
  });

  // Back to top
  var bt=document.getElementById('backTop');
  window.addEventListener('scroll',function(){
    if(window.scrollY>300) bt.classList.add('vis');
    else bt.classList.remove('vis');
  });
  bt.addEventListener('click',function(){
    window.scrollTo({top:0,behavior:'smooth'});
  });

  // Intersection observer for reveal animations
  var obs=new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(e.isIntersecting){
        e.target.classList.add('vis');
        obs.unobserve(e.target);
      }
    });
  },{threshold:0.1});
  document.querySelectorAll('.rv').forEach(function(el){obs.observe(el)});

  // Counter animation
  function animateCounters(){
    document.querySelectorAll('.sn[data-count]').forEach(function(el){
      var target=parseInt(el.getAttribute('data-count'),10);
      var suffix=el.getAttribute('data-suffix')||'';
      var duration=1500;
      var start=0;
      var startTime=null;
      function step(ts){
        if(!startTime) startTime=ts;
        var progress=Math.min((ts-startTime)/duration,1);
        var eased=1-Math.pow(1-progress,3);
        el.textContent=Math.floor(eased*target)+suffix;
        if(progress<1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  }
  var counterSection=document.querySelector('.sr');
  if(counterSection){
    var cobs=new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(e.isIntersecting){
          animateCounters();
          cobs.unobserve(e.target);
        }
      });
    },{threshold:0.3});
    cobs.observe(counterSection);
  }

  // Search filter
  var searchInput=document.getElementById('searchInput');
  if(searchInput){
    searchInput.addEventListener('input',function(){
      var q=this.value.toLowerCase();
      document.querySelectorAll('.cd[data-name]').forEach(function(card){
        var name=(card.getAttribute('data-name')||'').toLowerCase();
        var desc=(card.getAttribute('data-desc')||'').toLowerCase();
        card.style.display=(name.indexOf(q)!==-1||desc.indexOf(q)!==-1)?'':'none';
      });
      // Also update category section visibility
      document.querySelectorAll('.cs2').forEach(function(sec){
        var cards=sec.querySelectorAll('.cd[data-name]');
        var anyVisible=false;
        cards.forEach(function(c){if(c.style.display!=='none') anyVisible=true;});
        sec.style.display=anyVisible?'':'none';
      });
    });
  }

  // Category filter
  document.querySelectorAll('.cb[data-cat]').forEach(function(btn){
    btn.addEventListener('click',function(){
      document.querySelectorAll('.cb[data-cat]').forEach(function(b){b.classList.remove('act')});
      this.classList.add('act');
      var cat=this.getAttribute('data-cat');
      document.querySelectorAll('.cs2').forEach(function(sec){
        if(cat==='all'){
          sec.style.display='';
        }else{
          sec.style.display=(sec.getAttribute('data-category')===cat)?'':'none';
        }
      });
      // Reset search
      if(searchInput) searchInput.value='';
      document.querySelectorAll('.cd[data-name]').forEach(function(c){c.style.display=''});
    });
  });
})();
</script>
</body>
</html>`
}
