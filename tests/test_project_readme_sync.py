from scripts.sync_project_readme import TARGET, rendered


def test_documentation_site_readme_matches_repository_readme():
    assert TARGET.read_text(encoding="utf-8") == rendered()
