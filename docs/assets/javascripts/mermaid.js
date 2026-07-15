document$.subscribe(async function () {
  if (!window.mermaid) return;

  const darkMode = window.matchMedia("(prefers-color-scheme: dark)").matches;
  mermaid.initialize({
    startOnLoad: false,
    securityLevel: "strict",
    theme: darkMode ? "dark" : "neutral",
    flowchart: { useMaxWidth: false, htmlLabels: true }
  });
  await mermaid.run({ querySelector: ".mermaid" });
});
