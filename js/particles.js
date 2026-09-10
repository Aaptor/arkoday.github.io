/**
 * Static Background Pattern Controller for Arkoday's Portfolio.
 * Replaces the animated particle canvas with static, high-aesthetic vector patterns
 * (Architectural Precision Grid with Crosshairs, Topographic Contours, Isometric Lattice, or Dot Matrix).
 * Zero CPU overhead, zero dependencies, auto-adapts to theme changes.
 */
(function () {
  "use strict";

  var PATTERNS = ["grid", "topography", "isometric", "dots"];
  var PATTERN_NAMES = {
    grid: "Architectural Grid",
    topography: "Topographic Contours",
    isometric: "Isometric Lattice",
    dots: "Dot Matrix"
  };

  function getStoredPattern() {
    try {
      var stored = localStorage.getItem("pattern");
      if (stored && PATTERNS.indexOf(stored) !== -1) {
        return stored;
      }
    } catch (e) {
      // localStorage may be restricted in private mode
    }
    return "grid";
  }

  function updateToggleButtons(pattern) {
    var name = PATTERN_NAMES[pattern] || pattern;
    var nextIndex = (PATTERNS.indexOf(pattern) + 1) % PATTERNS.length;
    var nextName = PATTERN_NAMES[PATTERNS[nextIndex]];
    var label = "Pattern: " + name + " (Click for " + nextName + ")";

    var buttons = document.querySelectorAll(".pattern-toggle");
    buttons.forEach(function (btn) {
      btn.setAttribute("aria-label", label);
      btn.setAttribute("title", label);
    });
  }

  function applyPattern(pattern, save) {
    if (PATTERNS.indexOf(pattern) === -1) pattern = "grid";
    document.documentElement.setAttribute("data-pattern", pattern);
    if (save) {
      try {
        localStorage.setItem("pattern", pattern);
      } catch (e) {}
    }
    updateToggleButtons(pattern);
  }

  function cyclePattern() {
    var current = document.documentElement.getAttribute("data-pattern") || getStoredPattern();
    var idx = PATTERNS.indexOf(current);
    var next = PATTERNS[(idx + 1) % PATTERNS.length];
    applyPattern(next, true);
    return next;
  }

  // Safely remove legacy canvas element if still present
  function removeLegacyCanvas() {
    var canvas = document.getElementById("particle-canvas");
    if (canvas && canvas.parentNode) {
      canvas.parentNode.removeChild(canvas);
    }
  }

  // Initialize
  var initialPattern = getStoredPattern();
  applyPattern(initialPattern, false);

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      removeLegacyCanvas();
      updateToggleButtons(initialPattern);
    });
  } else {
    removeLegacyCanvas();
    updateToggleButtons(initialPattern);
  }

  // Event delegation for pattern switcher buttons
  document.addEventListener("click", function (e) {
    var btn = e.target.closest(".pattern-toggle");
    if (!btn) return;
    cyclePattern();
  });

  // Expose global helpers for easy testing in console
  window.setPortfolioPattern = function (name) {
    applyPattern(name, true);
  };
  window.cyclePortfolioPattern = cyclePattern;
  window.getPortfolioPattern = function () {
    return document.documentElement.getAttribute("data-pattern") || getStoredPattern();
  };
})();
