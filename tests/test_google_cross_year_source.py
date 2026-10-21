from pathlib import Path

from auto_research.discovery_sources import discover_external, load_sources


def test_google_recent_cross_year_scan_is_unfiltered_bounded_and_honest():
    config = Path(__file__).resolve().parents[1] / "configs/paper-discovery-sources.json"
    sources = load_sources(config, "agent")
    source = next(s for s in sources if s.name == "Google Research recent cross-year publications")
    assert "category=" not in source.url and source.max_pages == 2
    assert any("category=2026" in s.url for s in sources)
    requested = []

    def fetcher(url):
        requested.append(url)
        return '<form data-max-pages="950"></form><a href="/pubs/next-year-paper/">2027 venue paper</a>'

    class Client:
        def lookup(self, ids):
            assert not ids
            return []

    _, _, failures, stats = discover_external([source], client=Client(), fetcher=fetcher)
    directories = [url for url in requested if "?sort=" in url]
    assert not failures and len(directories) == 2
    assert "page=2" in directories[1] and "category=" not in directories[1]
    assert requested[-1] == "https://research.google/pubs/next-year-paper/"
    assert stats[0]["pagination_capped"] is True
    assert stats[0]["pages_available"] == 950
    assert stats[0]["unresolved_publications"]
