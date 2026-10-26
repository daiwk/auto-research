/* Progressive enhancement: every card remains readable without JavaScript. */
(() => {
  "use strict";

  if (window.__arLearningCardsBound) return;
  window.__arLearningCardsBound = true;
  const PAGE_SIZE = 24;

  function initialize() {
    document.querySelectorAll("[data-learning-browser]").forEach((root) => {
      if (root.dataset.learningBound) return;
      const grid = root.querySelector(".ar-learning-grid");
      if (!grid) return;
      root.dataset.learningBound = "true";

      const search = root.querySelector("[data-learning-search]");
      const domain = root.querySelector("[data-learning-domain]");
      const status = root.querySelector("[data-learning-status]");
      const more = root.querySelector("[data-learning-more]");
      const cards = Array.from(grid.querySelectorAll("[data-learning-card]"), (card) => ({
        element: card,
        domain: card.dataset.domain || "",
        search: (card.dataset.search || card.textContent).toLowerCase(),
      }));
      let visible = PAGE_SIZE;
      let empty = root.querySelector("[data-learning-empty]");
      if (!empty) {
        empty = document.createElement("p");
        empty.className = "ar-learning-empty";
        empty.dataset.learningEmpty = "";
        empty.textContent = "没有匹配的卡片。试试其他关键词，或选择全部领域。";
        grid.before(empty);
      }
      if (status) {
        status.setAttribute("role", "status");
        status.setAttribute("aria-live", "polite");
        status.setAttribute("aria-atomic", "true");
      }

      function render() {
        const words = (search?.value || "").trim().toLowerCase().split(/\s+/).filter(Boolean);
        const selectedDomain = domain?.value || "";
        let matched = 0;
        let shown = 0;
        cards.forEach((card) => {
          const matches = (!selectedDomain || selectedDomain === "all" || card.domain === selectedDomain)
            && words.every((word) => card.search.includes(word));
          if (matches) matched += 1;
          card.element.hidden = !matches || shown >= visible;
          if (!card.element.hidden) shown += 1;
        });
        empty.hidden = matched > 0;
        if (status) status.textContent = `匹配 ${matched} 张，已显示 ${shown} 张。`;
        if (more) {
          more.hidden = shown >= matched;
          more.textContent = `再显示 ${Math.min(PAGE_SIZE, matched - shown)} 张`;
        }
      }

      function reset() {
        visible = PAGE_SIZE;
        render();
      }

      search?.addEventListener("input", reset);
      domain?.addEventListener("change", reset);
      more?.addEventListener("click", () => {
        const previouslyHidden = cards.filter((card) => card.element.hidden);
        visible += PAGE_SIZE;
        render();
        // The last batch hides the button; keep keyboard focus in the new cards.
        if (more.hidden && document.activeElement === more) {
          previouslyHidden.find((card) => !card.element.hidden)?.element.querySelector("a")?.focus();
        }
      });
      root.classList.add("is-enhanced");
      render();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize, { once: true });
  } else {
    initialize();
  }
  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(initialize);
  }
})();
