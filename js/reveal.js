/* Scroll-reveal, progressive enhancement.
 *
 * Elements are visible by default in CSS. This script adds .js-reveal to
 * <html>, which is the hook that hides .reveal elements until they scroll
 * into view — so with JavaScript disabled or broken, everything stays
 * visible rather than the page appearing blank.
 *
 * Honours prefers-reduced-motion: if the visitor asked for less motion, the
 * hiding class is never added at all.
 */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduced || !("IntersectionObserver" in window)) return;

  var root = document.documentElement;
  root.classList.add("js-reveal");

  function show(el) {
    el.classList.add("is-visible");
  }

  document.addEventListener("DOMContentLoaded", function () {
    var items = document.querySelectorAll(".reveal");
    if (!items.length) {
      root.classList.remove("js-reveal");
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          show(entry.target);
          observer.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.05 }
    );

    items.forEach(function (el, i) {
      // small stagger so a row of cards arrives in sequence
      el.style.transitionDelay = Math.min(i, 6) * 60 + "ms";
      observer.observe(el);
    });

    // Safety net: if anything is still hidden after 3s (an observer that
    // never fired, a browser quirk), reveal it rather than leave a blank page.
    window.setTimeout(function () {
      document.querySelectorAll(".reveal:not(.is-visible)").forEach(show);
    }, 3000);
  });
})();
