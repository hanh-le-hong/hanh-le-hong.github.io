// ==========================================================================
// AiPRIL -- WINTER (DEFAULT) / SPRING SWITCHER, TERMINAL COPY & CMS LOADER
// ==========================================================================

(function () {
  const root = document.documentElement;
  const toggleBtn = document.getElementById("theme-toggle");
  const STORAGE_KEY = "aipril-default-winter-v1";
  const isLocal =
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1";

  // Reveal local-only CMS Studio controls only when running locally
  if (isLocal) {
    document.querySelectorAll(".local-only").forEach(function (el) {
      el.removeAttribute("hidden");
    });
  }

  function applySeason(season) {
    root.setAttribute("data-theme", season);
    let metaTheme = document.querySelector('meta[name="theme-color"]');
    if (!metaTheme) {
      metaTheme = document.createElement("meta");
      metaTheme.setAttribute("name", "theme-color");
      document.head.appendChild(metaTheme);
    }
    metaTheme.setAttribute("content", season === "spring" ? "#F8F8EF" : "#213953");
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

  // Quick-copy email button in Noodle-style terminal strip
  const copyBtn = document.getElementById("copy-email-btn");
  if (copyBtn) {
    copyBtn.addEventListener("click", function () {
      const text = copyBtn.getAttribute("data-copy") || "drink@iced-latte.com";
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () {
          copyBtn.textContent = "Copied!";
          copyBtn.classList.add("is-copied");
          setTimeout(function () {
            copyBtn.textContent = "Copy";
            copyBtn.classList.remove("is-copied");
          }, 2000);
        });
      }
    });
  }

  function escapeHtml(str) {
    return String(str || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
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
        : allPosts.filter(function (p) {
            return p.category === filterCategory;
          });

    if (list.length === 0) {
      feedEl.innerHTML = isLocal
        ? '<p class="empty-feed">No notes filed under this pillar yet. <a href="studio.html">Write the first one in Studio -&gt;</a></p>'
        : '<p class="empty-feed">No notes filed under this pillar yet. New essays coming soon.</p>';
      return;
    }

    feedEl.innerHTML = list
      .map(function (post) {
        return (
          '<a href="post.html?slug=' +
          encodeURIComponent(post.slug) +
          '" class="post-row">' +
          '<div class="post-row-meta">' +
          '<span class="tag">' +
          escapeHtml(post.category) +
          "</span>" +
          '<span class="post-row-date">' +
          escapeHtml(post.date) +
          "</span>" +
          "</div>" +
          '<div class="post-row-main">' +
          "<h3>" +
          escapeHtml(post.title) +
          "</h3>" +
          "<p>" +
          escapeHtml(post.summary || "") +
          "</p>" +
          "</div>" +
          '<div class="post-row-right">' +
          "<span>" +
          escapeHtml(post.readTime || "3 min read") +
          " -&gt;</span>" +
          "</div>" +
          "</a>"
        );
      })
      .join("");
  }

  if (feedEl) {
    fetch("posts/index.json?t=" + Date.now())
      .then(function (r) {
        return r.json();
      })
      .then(function (posts) {
        allPosts = Array.isArray(posts) ? posts : [];
        renderFeed("all");
      })
      .catch(function () {
        feedEl.innerHTML =
          '<p class="empty-feed">Could not load notes right now.</p>';
      });

    filterBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        filterBtns.forEach(function (b) {
          b.classList.remove("active");
        });
        btn.classList.add("active");
        renderFeed(btn.getAttribute("data-filter"));
      });
    });
  }
})();
