from scripts.sync_project_readme import SOURCE, TARGET, rendered, site_html_link, site_link, sources, target_for


def test_documentation_site_readme_matches_repository_readme():
    for source in sources():
        assert target_for(source).read_text(encoding="utf-8") == rendered(source)


def test_mirror_rewrites_media_and_repo_links_without_losing_fragments():
    assert site_link("docs/assets/media/site-tour.webp") == "assets/media/site-tour.webp"
    assert site_link("readme_setup.md#mac") == "readme_setup.md#mac"
    assert site_link("README.md#参与和维护") == "project-readme.md#参与和维护"
    assert site_link("AGENTS.md").endswith("/blob/main/AGENTS.md")
    assert site_link("src/auto_research/").endswith("/tree/main/src/auto_research/")
    assert site_link("https://example.org/?x=1#y") == "https://example.org/?x=1#y"
    assert site_link("#local") == "#local"


def test_raw_html_links_target_deployed_routes_and_preserve_url_parts():
    assert site_html_link("docs/assets/media/site-tour.webp?v=2#poster") == "../assets/media/site-tour.webp?v=2#poster"
    assert site_html_link("readme_setup.md#mac") == "../readme_setup/#mac"
    assert site_html_link("docs/assets/media/README.md") == "../assets/media/"
    assert site_html_link("docs/index.md#intro") == "../#intro"
    assert site_html_link("#local") == "#local"
    assert site_html_link("https://example.org/?x=1#y") == "https://example.org/?x=1#y"


def test_main_mirror_preserves_reduced_motion_poster_and_video():
    text = rendered()
    assert 'srcset="../assets/media/site-tour-poster.webp"' in text
    assert 'src="../assets/media/site-tour.webp"' in text
    assert "](assets/media/site-tour.mp4)" in text
    assert TARGET.name == "project-readme.md"
    assert SOURCE.name == "README.md"


def test_rendered_picture_media_resolves_from_directory_page(tmp_path):
    from html.parser import HTMLParser
    from urllib.parse import urljoin

    import pytest

    pytest.importorskip("mkdocs")  # Required and executed by the documentation CI job.
    from mkdocs.config.defaults import MkDocsConfig
    from mkdocs.structure.files import File, get_files
    from mkdocs.structure.pages import Page

    config = MkDocsConfig()
    config.load_dict({
        "site_name": "README media regression",
        "docs_dir": str(TARGET.parent),
        "site_dir": str(tmp_path / "site"),
        "use_directory_urls": True,
        "markdown_extensions": ["md_in_html", "tables", "toc"],
    })
    errors, _ = config.validate()
    assert not errors
    files = get_files(config)
    # Media may be regenerated after the README; URL rewriting only needs its entry.
    if files.get_file_from_path("assets/media/site-tour.mp4") is None:
        files.append(File("assets/media/site-tour.mp4", str(TARGET.parent), config.site_dir, True))
    page = Page("Project README", files.get_file_from_path(TARGET.name), config)
    page.markdown, page.meta = rendered(), {}
    page.render(config, files)

    class MediaURLs(HTMLParser):
        def __init__(self):
            super().__init__()
            self.urls = []

        def handle_starttag(self, tag, attrs):
            if tag in {"img", "source"}:
                self.urls.extend(value for key, value in attrs if key in {"src", "srcset"})

    parser = MediaURLs()
    parser.feed(page.content)
    page_url = "https://example.test/auto-research/" + page.file.url
    resolved = {urljoin(page_url, url) for url in parser.urls if "site-tour" in url}
    assert resolved == {
        "https://example.test/auto-research/assets/media/site-tour.webp",
        "https://example.test/auto-research/assets/media/site-tour-poster.webp",
    }
    # Markdown source links still pass through MkDocs' own relative-link handling.
    assert 'href="../assets/media/site-tour.mp4"' in page.content
