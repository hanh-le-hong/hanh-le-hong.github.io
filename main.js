// ==========================================================================
// AiPRIL — WINTER (DEFAULT) / SPRING SWITCHER
// ==========================================================================

(function () {
  const root = document.documentElement;
  const toggleBtn = document.getElementById("theme-toggle");
  const STORAGE_KEY = "aipril-default-winter-v1";

  function applySeason(season) {
    root.setAttribute("data-theme", season);
    try {
      localStorage.setItem(STORAGE_KEY, season);
    } catch (_) {}
  }

  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved === "winter" || saved === "spring") {
      applySeason(saved);
    } else {
      applySeason("winter");
    }
  } catch (_) {
    applySeason("winter");
  }

  if (toggleBtn) {
    toggleBtn.addEventListener("click", function () {
      const current = root.getAttribute("data-theme") || "winter";
      const next = current === "winter" ? "spring" : "winter";
      applySeason(next);
    });
  }
})();
