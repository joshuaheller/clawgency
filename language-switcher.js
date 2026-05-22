'use strict';

(function initLanguageSwitcher() {
  if (document.querySelector('.lang-switch')) return;

  const path = window.location.pathname;
  const isEnglish = path === '/en' || path.startsWith('/en/');

  function toEnglishPathname(pathname) {
    if (pathname === '/' || pathname === '') return '/en/index.html';
    if (pathname === '/index.html') return '/en/index.html';
    if (pathname.startsWith('/en/')) return pathname;
    return `/en${pathname.startsWith('/') ? pathname : `/${pathname}`}`;
  }

  function toGermanPathname(pathname) {
    if (!pathname.startsWith('/en/')) return pathname || '/';
    const stripped = pathname.replace(/^\/en\//, '/');
    if (stripped === '/index.html') return '/';
    return stripped;
  }

  const targetPath = isEnglish ? toGermanPathname(path) : toEnglishPathname(path);
  const targetUrl = `${targetPath}${window.location.search || ''}${window.location.hash || ''}`;

  const labels = isEnglish
    ? { current: 'EN', target: 'DE', aria: 'Switch language to German' }
    : { current: 'DE', target: 'EN', aria: 'Sprache auf Englisch umstellen' };

  const wrap = document.createElement('div');
  wrap.className = 'lang-switch';

  const current = document.createElement('span');
  current.className = 'lang-switch__current';
  current.textContent = labels.current;

  const link = document.createElement('a');
  link.className = 'lang-switch__target';
  link.href = targetUrl;
  link.setAttribute('hreflang', isEnglish ? 'de' : 'en');
  link.setAttribute('aria-label', labels.aria);
  link.textContent = labels.target;

  wrap.appendChild(current);
  wrap.appendChild(link);
  document.body.appendChild(wrap);

  const style = document.createElement('style');
  style.textContent = '.lang-switch{position:fixed;right:1rem;bottom:1rem;z-index:10001;display:inline-flex;align-items:center;overflow:hidden;border-radius:9999px;border:1px solid rgba(255,255,255,.16);background:rgba(11,12,16,.86);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);font-family:"Space Grotesk",sans-serif;box-shadow:0 8px 26px rgba(0,0,0,.32)}.lang-switch__current,.lang-switch__target{padding:.45rem .72rem;font-size:.78rem;font-weight:700;letter-spacing:.03em}.lang-switch__current{color:#e8eaf0;background:rgba(255,255,255,.06)}.lang-switch__target{color:#fff;background:#e63946;text-decoration:none;transition:background .2s ease}.lang-switch__target:hover{background:#f24b58}@media(max-width:640px){.lang-switch{bottom:.85rem;right:.85rem}}';
  document.head.appendChild(style);
})();
