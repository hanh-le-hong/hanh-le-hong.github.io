// ==========================================================================
// AiPRIL — WINTER (DEFAULT) / SPRING SWITCHER + CMS POSTS LOADER
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

  // Dynamic Writing Feed on Homepage
  const feedEl = document.getElementById("posts-feed");
  const filterBtns = document.querySelectorAll(".filter-chip");
  let allPosts = [];

  function renderFeed(filterCategory) {
    if (!feedEl) return;
    const list =
      !filterCategory || filterCategory === "all"
        ? allPosts
        : allPosts.filter((p) => p.category === filterCategory);

    if (list.length === 0) {
      feedEl.innerHTML =
        '<p class="empty-feed">No posts in this pillar yet. <a href="studio.html">Write the first one in Studio →</a></p>';
      return;
    }

    feedEl.innerHTML = list
      .map(
        (post) => `
      <a href="post.html?slug=${encodeURIComponent(post.slug)}" class="post-row">
        <div class="post-row-meta">
          <span class="mono-tag">${post.category}</span>
          <span class="post-row-date">${post.date}</span>
        </div>
        <div class="post-row-main">
          <h3>${post.title}</h3>
          <p>${post.summary || ""}</p>
        </div>
        <div class="post-row-right">
          <span>${post.readTime || "3 min read"} →</span>
        </div>
      </a>
    `
      )
      .join("");
  }

  if (feedEl) {
    fetch("posts/index.json?t=" + Date.now())
      .then((r) => r.json())
      .then((posts) => {
        allPosts = posts;
        renderFeed("all");
      })
      .catch(() => {});

    filterBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        filterBtns.forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        renderFeed(btn.getAttribute("data-filter"));
      });
    });
  }
})();
