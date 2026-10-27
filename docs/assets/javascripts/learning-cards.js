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
      const levels = Array.from(root.querySelectorAll("[data-learning-level]"));
      const cards = Array.from(grid.querySelectorAll("[data-learning-card]"), (card) => ({
        element: card,
        domain: card.dataset.domain || "",
        theme: card.dataset.theme || "",
        topic: card.dataset.topic || "",
        identity: card.dataset.identity || "",
        paperTitle: card.dataset.paperTitle || "",
        level: card.dataset.level || "",
        pending: card.dataset.learningPending === "true",
        search: (card.dataset.search || card.textContent).toLowerCase(),
      }));
      const pageSize = Number(root.dataset.learningPageSize) || 24;
      let visible = pageSize;
      const params = new URLSearchParams(window.location.search);
      let selectedPaper = params.get("paper") || "";
      let selectedLevel = levels.some(button => button.dataset.learningLevel === params.get("level"))
        ? params.get("level") : "";
      const paperFilter = document.createElement("p");
      paperFilter.className = "ar-learning-paper-filter";
      const paperName = document.createElement("span");
      const clearPaper = document.createElement("button");
      clearPaper.type = "button";
      clearPaper.textContent = "清除论文筛选";
      paperFilter.append(paperName, clearPaper);
      root.querySelector('.ar-learning-controls').before(paperFilter);
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
        empty.textContent = "没有匹配的问题。试试其他关键词，或选择全部主题。";
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
        let matchedQuestions = 0;
        let shownQuestions = 0;
        let pending = 0;
        const papers = new Set();
        cards.forEach((card) => {
          const matches = (!selectedDomain || selectedDomain === "all" || card.domain === selectedDomain)
            && (!selectedTheme || card.theme === selectedTheme)
            && (!selectedTopic || card.topic === selectedTopic)
            && (!selectedPaper || card.identity === selectedPaper)
            && (!selectedLevel || card.level === selectedLevel)
            && words.every((word) => card.search.includes(word));
          if (matches) {
            matched += 1;
            papers.add(card.identity);
            if (card.pending) pending += 1;
            else matchedQuestions += 1;
          }
          card.element.hidden = !matches || shown >= visible;
          if (!card.element.hidden) {
            shown += 1;
            if (!card.pending) shownQuestions += 1;
          }
        });
        empty.hidden = matched > 0;
        levels.forEach(button => button.setAttribute("aria-pressed", String(button.dataset.learningLevel === selectedLevel)));
        root.dataset.paperFiltered = selectedPaper ? "true" : "false";
        if (search) search.placeholder = selectedPaper ? "搜索本篇论文的问题" : "搜索问题、论文或机制";
        paperFilter.hidden = !selectedPaper;
        if (selectedPaper) paperName.textContent = '当前论文：' + (cards.find(card => card.identity === selectedPaper)?.paperTitle || selectedPaper);
        if (status) status.textContent = `匹配 ${matchedQuestions} 问，涉及 ${papers.size} 篇，已显示 ${shownQuestions} 问。`
          + (pending ? ` ${pending} 篇待补问答。` : "");
        if (more) {
          more.hidden = shown >= matched;
          more.textContent = `再显示 ${Math.min(pageSize, matched - shown)} ${pending ? "条记录" : "个问题"}`;
        }
      }

      function reset() {
        visible = pageSize;
        syncTopics();
        const url = new URL(window.location.href);
        [["q", search?.value.trim()], ["theme", theme?.value], ["topic", topic?.value], ["paper", selectedPaper], ["level", selectedLevel]].forEach(([key, value]) => {
          if (value) url.searchParams.set(key, value);
          else url.searchParams.delete(key);
        });
        url.hash = "";
        window.history.replaceState(null, "", url);
        render();
      }

      search?.addEventListener("input", reset);
      levels.forEach(button => button.addEventListener("click", () => {
        selectedLevel = button.dataset.learningLevel;
        reset();
      }));
      clearPaper.addEventListener("click", () => { selectedPaper = ""; reset(); });
      domain?.addEventListener("change", reset);
      theme?.addEventListener("change", () => { selectedPaper = ""; reset(); });
      topic?.addEventListener("change", () => {
        selectedPaper = "";
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
        const target = document.getElementById(anchor);
        const targetIndex = cards.findIndex((card) => target && card.element.contains(target));
        if (targetIndex < 0) return;
        if (search) search.value = "";
        if (theme) theme.value = "";
        if (topic) topic.value = "";
        if (domain) domain.value = "";
        selectedLevel = "";
        if (selectedPaper !== cards[targetIndex].identity) selectedPaper = "";
        syncTopics();
        visible = Math.max(pageSize, targetIndex + 1);
        render();
        if (anchor.startsWith("qa-")) {
          const answer = cards[targetIndex].element.querySelector('.ar-learning-answer');
          if (answer) answer.open = true;
        }
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
