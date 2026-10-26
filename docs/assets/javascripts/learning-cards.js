/* Progressive enhancement: every card remains readable without JavaScript. */
(() => {
  "use strict";

  if (window.__arLearningCardsBound) return;
  window.__arLearningCardsBound = true;
  const anchorReveals = new WeakMap();

  function initialize() {
    document.querySelectorAll("[data-learning-browser]").forEach((root) => {
      if (root.dataset.learningBound) return;
      const grid = root.querySelector(".ar-learning-grid");
      if (!grid) return;
      root.dataset.learningBound = "true";

      const search = root.querySelector("[data-learning-search]");
      const domain = root.querySelector("[data-learning-domain]");
      const theme = root.querySelector("[data-learning-theme]");
      const topic = root.querySelector("[data-learning-topic]");
      const status = root.querySelector("[data-learning-status]");
      const more = root.querySelector("[data-learning-more]");
      const cards = Array.from(grid.querySelectorAll("[data-learning-card]"), (card) => ({
        element: card,
        domain: card.dataset.domain || "",
        theme: card.dataset.theme || "",
        topic: card.dataset.topic || "",
        search: (card.dataset.search || card.textContent).toLowerCase(),
      }));
      const pageSize = Number(root.dataset.learningPageSize) || 24;
      let visible = pageSize;
      const params = new URLSearchParams(window.location.search);
      if (search) search.value = params.get("q") || "";
      if (theme && Array.from(theme.options).some((o) => o.value === params.get("theme"))) {
        theme.value = params.get("theme");
      }
      if (topic && Array.from(topic.options).some((o) => o.value === params.get("topic"))) {
        topic.value = params.get("topic");
        if (topic.value && theme) theme.value = topic.value.split("/")[0];
      }
      let empty = root.querySelector("[data-learning-empty]");
      if (!empty) {
        empty = document.createElement("p");
        empty.className = "ar-learning-empty";
        empty.dataset.learningEmpty = "";
        empty.textContent = "没有匹配的卡片。试试其他关键词，或选择全部主题。";
        grid.before(empty);
      }

      function syncTopics() {
        if (!topic) return;
        Array.from(topic.options).forEach((option) => {
          const excluded = Boolean(theme?.value && option.value && option.dataset.theme !== theme.value);
          option.hidden = excluded;
          option.disabled = excluded;
        });
        if (topic.selectedOptions[0]?.disabled) topic.value = "";
      }
      if (status) {
        status.setAttribute("role", "status");
        status.setAttribute("aria-live", "polite");
        status.setAttribute("aria-atomic", "true");
      }

      function render() {
        const words = (search?.value || "").trim().toLowerCase().split(/\s+/).filter(Boolean);
        const selectedDomain = domain?.value || "";
        const selectedTheme = theme?.value || "";
        const selectedTopic = topic?.value || "";
        let matched = 0;
        let shown = 0;
        cards.forEach((card) => {
          const matches = (!selectedDomain || selectedDomain === "all" || card.domain === selectedDomain)
            && (!selectedTheme || card.theme === selectedTheme)
            && (!selectedTopic || card.topic === selectedTopic)
            && words.every((word) => card.search.includes(word));
          if (matches) matched += 1;
          card.element.hidden = !matches || shown >= visible;
          if (!card.element.hidden) shown += 1;
        });
        empty.hidden = matched > 0;
        if (status) status.textContent = `匹配 ${matched} 张，已显示 ${shown} 张。`;
        if (more) {
          more.hidden = shown >= matched;
          more.textContent = `再显示 ${Math.min(pageSize, matched - shown)} 张`;
        }
      }

      function reset() {
        visible = pageSize;
        syncTopics();
        if (theme || topic) {
          const url = new URL(window.location.href);
          [["q", search?.value.trim()], ["theme", theme?.value], ["topic", topic?.value]].forEach(([key, value]) => {
            if (value) url.searchParams.set(key, value);
            else url.searchParams.delete(key);
          });
          url.hash = "";
          window.history.replaceState(null, "", url);
        }
        render();
      }

      search?.addEventListener("input", reset);
      domain?.addEventListener("change", reset);
      theme?.addEventListener("change", reset);
      topic?.addEventListener("change", () => {
        if (topic.value && theme) theme.value = topic.value.split("/")[0];
        reset();
      });
      more?.addEventListener("click", () => {
        const previouslyHidden = cards.filter((card) => card.element.hidden);
        visible += pageSize;
        render();
        // The last batch hides the button; keep keyboard focus in the new cards.
        if (more.hidden && document.activeElement === more) {
          previouslyHidden.find((card) => !card.element.hidden)?.element.querySelector("a")?.focus();
        }
      });
      root.classList.add("is-enhanced");
      syncTopics();
      // Stable paper anchors from old bookmarks also reveal cards beyond page one.
      function revealAnchor() {
        const anchor = window.location.hash.slice(1);
        const targetIndex = cards.findIndex((card) => card.element.querySelector("h2")?.id === anchor);
        if (targetIndex < 0) return;
        if (search) search.value = "";
        if (theme) theme.value = "";
        if (topic) topic.value = "";
        if (domain) domain.value = "";
        syncTopics();
        visible = Math.max(pageSize, targetIndex + 1);
        render();
        cards[targetIndex].element.scrollIntoView({ block: "start" });
      }
      anchorReveals.set(root, revealAnchor);
      render();
      revealAnchor();
    });
  }

  window.addEventListener("hashchange", () => {
    document.querySelectorAll("[data-learning-browser]").forEach((root) => anchorReveals.get(root)?.());
  });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize, { once: true });
  } else {
    initialize();
  }
  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(initialize);
  }
})();
