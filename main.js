// ==========================================================================
// AiPRIL — SPRING (RENAISSANCE) / WINTER (ROBOTIC) SWITCHER
// ==========================================================================

(function () {
  const root = document.documentElement;
  const toggleBtn = document.getElementById("theme-toggle");
  const seasonReadout = document.getElementById("season-readout");
  const STORAGE_KEY = "aipril-season-theme";

  function applySeason(season) {
    root.setAttribute("data-theme", season);
    if (seasonReadout) {
      seasonReadout.textContent =
        season === "winter"
          ? "WINTER // ROBOTIC LOGIC"
          : "SPRING // RENAISSANCE LIGHT";
    }
    try {
      localStorage.setItem(STORAGE_KEY, season);
    } catch (_) {}
  }

  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved === "spring" || saved === "winter") {
      applySeason(saved);
    }
  } catch (_) {}

  if (toggleBtn) {
    toggleBtn.addEventListener("click", function () {
      const current = root.getAttribute("data-theme") || "spring";
      const next = current === "spring" ? "winter" : "spring";
      applySeason(next);
    });
  }
})();
