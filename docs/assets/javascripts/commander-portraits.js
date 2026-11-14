/*
 * Commander portrait enhancement for SekigaharaWiki (JP and EN).
 * Leaves existing commander Markdown and its in-game statistics untouched.
 * The image files come from the user's 39-portrait upload.
 */
(function () {
  'use strict';

  // Only known commander profile slugs; directory index pages remain unchanged.
  const portraitSlugs = new Set([
    "akaza-naoyasu",
    "ankokuji-ekei",
    "asano-yoshinaga",
    "chosokabe-morichika",
    "date-masamune",
    "fukushima-masanori",
    "hiratsuka-tamehiro",
    "honda-tadakatsu",
    "hosokawa-tadaoki",
    "tokugawa-ieyasu",
    "ii-naomasa",
    "ikeda-terumasa",
    "ishida-mitsunari",
    "kato-kiyomasa",
    "kikkawa-hiroie",
    "kobayakawa-hideaki",
    "konishi-yukinaga",
    "kuroda-nagamasa",
    "kutsuki-mototsuna",
    "kyogoku-takatomo",
    "maeda-toshinaga",
    "mori-hidemoto",
    "nabeshima-naoshige",
    "niwa-nagashige",
    "ogawa-suketada",
    "otani-yoshitsugu",
    "shima-sakon",
    "satake-yoshinobu",
    "shimazu-yoshihiro",
    "tachibana-muneshige",
    "toda-shigemasa",
    "todo-takatora",
    "uesugi-kagekatsu",
    "ukita-hideie",
    "user-commander-1",
    "user-commander-2",
    "user-commander-3",
    "wakizaka-yasuharu",
    "yamauchi-kazutoyo"
]);

  function renderPortrait() {
    const raw = window.location.pathname.replace(/\/index\.html$/, '/');
    const path = raw.endsWith('/') ? raw : raw + '/';
    const match = path.match(/^(.*?)(?:en\/)?commanders\/(?:eastern|western|user)\/([^/]+)\/$/);
    if (!match) return;
    const slug = match[2];
    if (!portraitSlugs.has(slug)) return;

    const layout = document.querySelector('article .commander-data-layout');
    if (!layout) return;
    const flag = layout.querySelector(':scope > .commander-flag');
    const stats = layout.querySelector(':scope > .commander-stats');
    if (!flag || !stats) return;
    if (layout.querySelector(':scope > .commander-portrait')) return;

    // mkdocs-material serves this Wiki under /SekigaharaWiki/ on GitHub Pages.
    // The optional /en/ segment is already excluded by match[1].
    const imageUrl = match[1] + 'assets/images/commanders/' + encodeURIComponent(slug) + '.png';
    const english = /\/en\/commanders\//.test(path);
    const heading = document.querySelector('article h1');
    const name = heading ? heading.textContent.replace(/¶/g, '').trim() : slug;

    const portrait = document.createElement('figure');
    portrait.className = 'commander-portrait';
    const image = document.createElement('img');
    image.src = imageUrl;
    image.alt = english ? 'Portrait of ' + name : name + 'の武将画像';
    image.width = 288; // 1.5x the original 192px portrait width; CSS is responsive
    image.loading = 'lazy';
    image.decoding = 'async';
    const caption = document.createElement('figcaption');
    caption.textContent = english ? 'Commander portrait' : '武将画像';
    portrait.appendChild(image);
    portrait.appendChild(caption);
    layout.insertBefore(portrait, flag);
    layout.classList.add('has-portrait');
  }

  // Initial load, plus Material's instant-navigation document changes.
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderPortrait, { once: true });
  } else {
    renderPortrait();
  }
  if (typeof document$ !== 'undefined' && document$ && typeof document$.subscribe === 'function') {
    document$.subscribe(renderPortrait);
  }
})();
