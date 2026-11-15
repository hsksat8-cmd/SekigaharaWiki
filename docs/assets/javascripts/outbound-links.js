/*
 * Open external HTTP(S) links in a new tab throughout SekigaharaWiki.
 * Preserve data-outbound used by optional analytics and existing rel values.
 * Internal JP/EN Wiki links, fragment links, and non-web schemes stay unchanged.
 */
(function () {
  "use strict";

  const wikiPath = "/SekigaharaWiki/";

  function isOutsideWiki(url) {
    if (url.protocol !== "http:" && url.protocol !== "https:") return false;
    if (url.origin !== window.location.origin) return true;

    // Pages on the same GitHub Pages host but outside this project are external.
    // When previewing at localhost /, preserve all same-origin preview links.
    if (window.location.pathname.startsWith(wikiPath) ||
        window.location.pathname === wikiPath.slice(0, -1)) {
      return url.pathname !== wikiPath.slice(0, -1) &&
             !url.pathname.startsWith(wikiPath);
    }
    return false;
  }

  function updateAnchor(link) {
    if (!link || !link.getAttribute("href")) return;
    let url;
    try {
      url = new URL(link.href, window.location.href);
    } catch (_) {
      return;
    }
    if (!isOutsideWiki(url)) return;

    link.target = "_blank";
    link.relList.add("noopener", "noreferrer");
    link.dataset.outbound = url.hostname;
  }

  function updateLinks(root) {
    if (!root || root.nodeType !== Node.ELEMENT_NODE &&
                 root.nodeType !== Node.DOCUMENT_NODE) return;
    if (root.matches && root.matches("a[href]")) updateAnchor(root);
    if (root.querySelectorAll) {
      root.querySelectorAll("a[href]").forEach(updateAnchor);
    }
  }

  function initialize() {
    updateLinks(document);

    // Material instant navigation can swap page content without another load.
    if (typeof document$ !== "undefined" && document$ &&
        typeof document$.subscribe === "function") {
      document$.subscribe(function () { updateLinks(document); });
    }

    // Also cover links inserted later (e.g. search results and plugins).
    const observer = new MutationObserver(function (mutations) {
      mutations.forEach(function (mutation) {
        if (mutation.type === "attributes") {
          updateAnchor(mutation.target);
        } else {
          mutation.addedNodes.forEach(updateLinks);
        }
      });
    });
    observer.observe(document.documentElement, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ["href"]
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize, { once: true });
  } else {
    initialize();
  }
})();
