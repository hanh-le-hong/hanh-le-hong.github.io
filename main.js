// ==========================================================================
// APRIL HANH — DUAL MODE CONTROLLER (RENAISSANCE ↔ ROBOTIC)
// ==========================================================================

(function () {
  const root = document.documentElement;
  const toggleBtn = document.getElementById("theme-toggle");
  const modeIndicator = document.getElementById("mode-indicator");
  const STORAGE_KEY = "april-hanh-theme";

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    if (modeIndicator) {
      modeIndicator.textContent =
        theme === "robotic"
          ? "MODE // ROBOTIC SYSTEM"
          : "MODE // CLASSICAL GALLERY";
    }
    try {
      localStorage.setItem(STORAGE_KEY, theme);
    } catch (_) {
      // Ignore storage errors in private browsing
    }
  }

  // Restore saved preference if present
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved === "renaissance" || saved === "robotic") {
      applyTheme(saved);
    }
  } catch (_) {}

  if (toggleBtn) {
    toggleBtn.addEventListener("click", function () {
      const current = root.getAttribute("data-theme") || "renaissance";
      const next = current === "renaissance" ? "robotic" : "renaissance";
      applyTheme(next);
    });
  }
})();
