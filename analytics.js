// ==========================================================================
// AiPRIL -- POSTHOG ANALYTICS (bto-posthog standard for static sites)
// - Strict no-op when posthogKey is empty or on localhost / preview hosts.
// - Tracks snake_case object_action events tied to real conversion outcomes.
// ==========================================================================

(function () {
  const cfg = window.__AIPRIL_ANALYTICS__ || {};
  const key = String(cfg.posthogKey || "").trim();
  const host = window.location.hostname;
  const isProdDomain = host === "iced-latte.com" || host === "www.iced-latte.com";

  window.aiprilTrack = function (eventName, props) {
    if (!isProdDomain || !key) return;
    if (window.posthog && typeof window.posthog.capture === "function") {
      window.posthog.capture(eventName, props || {});
    }
  };

  // Never load SDK or send events when key is absent or outside production domain
  if (!key || !isProdDomain) {
    return;
  }

  const apiHost = cfg.posthogHost || "https://us.i.posthog.com";
  const uiHost = cfg.uiHost || "https://us.posthog.com";

  /* eslint-disable */
  !(function (t, e) {
    var o, n, p, r;
    e.__SV ||
      ((window.posthog = e),
      (e._i = []),
      (e.init = function (i, s, a) {
        function g(t, e) {
          var o = e.split(".");
          2 == o.length && ((t = t[o[0]]), (e = o[1])),
            (t[e] = function () {
              t.push([e].concat(Array.prototype.slice.call(arguments, 0)));
            });
        }
        ((p = t.createElement("script")).type = "text/javascript"),
          (p.crossOrigin = "anonymous"),
          (p.async = !0),
          (p.src =
            s.api_host.replace(".i.posthog.com", "-assets.i.posthog.com") +
            "/static/array.js"),
          (r = t.getElementsByTagName("script")[0]).parentNode.insertBefore(p, r);
        var u = e;
        for (
          void 0 !== a ? (u = e[a] = []) : (a = "posthog"),
            u.people = u.people || [],
            u.toString = function (t) {
              var e = "posthog";
              return "posthog" !== a && (e += "." + a), t || (e += " (stub)"), e;
            },
            u.people.toString = function () {
              return u.toString(1) + ".people (stub)";
            },
            o =
              "init capture register register_once register_for_session unregister unregister_for_session getFeatureFlag getFeatureFlagPayload isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey getNextSurveyStep identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty createPersonProfile opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing debug".split(
                " "
              ),
            n = 0;
          n < o.length;
          n++
        )
          g(u, o[n]);
        e._i.push([i, s, a]);
      }),
      (e.__SV = 1));
  })(document, window.posthog || []);
  /* eslint-enable */

  window.posthog.init(key, {
    api_host: apiHost,
    ui_host: uiHost,
    person_profiles: "identified_only",
    capture_pageview: true,
    capture_pageleave: true,
    autocapture: true,
    capture_exceptions: true,
    session_recording: {
      maskAllInputs: true
    }
  });

  function detectLocation(el) {
    if (el.closest(".hero")) return "hero";
    if (el.closest("#connect")) return "connect";
    if (el.closest(".article-author-box")) return "article_footer";
    if (el.closest(".header")) return "header";
    if (el.closest("#lab")) return "lab";
    if (el.closest("#about")) return "readme";
    return "page";
  }

  document.addEventListener("click", function (e) {
    const link = e.target.closest("a");
    if (!link) return;
    const href = link.getAttribute("href") || "";
    const loc = detectLocation(link);

    if (href.indexOf("mailto:") === 0) {
      window.aiprilTrack("email_clicked", { location: loc });
    } else if (href.indexOf("upwork.com/freelancers/lehonghanh") !== -1) {
      window.aiprilTrack("cta_clicked", { cta: "upwork_profile", location: loc });
    } else if (href.indexOf("linkedin.com/in/hanhlehong") !== -1) {
      window.aiprilTrack("cta_clicked", { cta: "linkedin", location: loc });
    } else if (href.indexOf("github.com/hanh-le-hong/marketing-systems-lab") !== -1) {
      window.aiprilTrack("lab_project_clicked", {
        project: "marketing_systems_lab",
        location: loc
      });
    } else if (href.indexOf("snapcard-dc0ca.web.app") !== -1) {
      window.aiprilTrack("lab_project_clicked", {
        project: "snapcard",
        location: loc
      });
    } else if (href.indexOf("github.com/hanh-le-hong") !== -1) {
      window.aiprilTrack("cta_clicked", { cta: "github", location: loc });
    } else if (href === "#writing") {
      window.aiprilTrack("cta_clicked", { cta: "read_notes", location: loc });
    }
  });

  // 80% scroll depth completion on static article pages (/writing/<slug>/)
  const articleEl = document.querySelector(".article-prose");
  const articleMeta = document.body.getAttribute("data-article-slug");
  if (articleEl && articleMeta) {
    let completed = false;
    const category = document.body.getAttribute("data-article-category") || "";
    window.addEventListener(
      "scroll",
      function () {
        if (completed) return;
        const rect = articleEl.getBoundingClientRect();
        const total = articleEl.offsetHeight || 1;
        const viewed = window.innerHeight - rect.top;
        if (viewed / total >= 0.8) {
          completed = true;
          window.aiprilTrack("article_read_completed", {
            slug: articleMeta,
            category: category
          });
        }
      },
      { passive: true }
    );
  }
})();
