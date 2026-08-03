/*
  外部リンクに識別属性を付ける補助スクリプトです。
  Cloudflare Web Analyticsの標準計測はページビュー中心です。
  将来、別のイベント分析基盤を追加する場合も、この属性を利用できます。
*/
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll('a[href^="http"]').forEach((link) => {
    try {
      const url = new URL(link.href);
      if (url.hostname !== window.location.hostname) {
        link.dataset.outbound = url.hostname;
        link.rel = "noopener noreferrer";
      }
    } catch (_) {
      // Invalid URLs are ignored.
    }
  });
});
