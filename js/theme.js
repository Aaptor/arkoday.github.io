/* Theme toggle with localStorage persistence and OS preference synchronization. */
(function () {
  "use strict";

  function getSystemTheme() {
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches
      ? "light"
      : "dark";
  }

  function getActiveTheme() {
    var stored = localStorage.getItem("theme");
    if (stored === "light" || stored === "dark") {
      return stored;
    }
    return getSystemTheme();
  }

  function updateToggleButtons(theme) {
    var nextTheme = theme === "dark" ? "light" : "dark";
    var label = "Switch to " + nextTheme + " theme";
    var buttons = document.querySelectorAll(".theme-toggle");
    buttons.forEach(function (btn) {
      btn.setAttribute("aria-label", label);
      btn.setAttribute("title", label);
    });
  }

  function applyTheme(theme, save) {
    document.documentElement.setAttribute("data-theme", theme);
    if (save) {
      try {
        localStorage.setItem("theme", theme);
      } catch (e) {
        // localStorage might be unavailable or restricted
      }
    }
    updateToggleButtons(theme);
  }

  // Initialize button state and bind events when DOM is loaded
  document.addEventListener("DOMContentLoaded", function () {
    var current = getActiveTheme();
    updateToggleButtons(current);

    document.addEventListener("click", function (e) {
      var btn = e.target.closest(".theme-toggle");
      if (!btn) return;
      var active = getActiveTheme();
      var targetTheme = active === "dark" ? "light" : "dark";
      applyTheme(targetTheme, true);
    });
  });

  // Listen for system theme changes if user hasn't chosen manually
  if (window.matchMedia) {
    window.matchMedia("(prefers-color-scheme: light)").addEventListener("change", function (e) {
      if (!localStorage.getItem("theme")) {
        applyTheme(e.matches ? "light" : "dark", false);
      }
    });
  }
})();
