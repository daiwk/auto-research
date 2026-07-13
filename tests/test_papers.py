from auto_research.papers import ArxivClient, parse_arxiv_feed


def test_parse_arxiv_feed():
    payload = b'''<?xml version="1.0" encoding="UTF-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
      <entry><id>http://arxiv.org/abs/2607.00001v1</id><published>2026-07-01T00:00:00Z</published>
      <title> A useful\n paper </title><summary> Abstract text. </summary>
      <author><name>A. Researcher</name></author></entry>
    </feed>'''
    papers = parse_arxiv_feed(payload)
    assert papers[0].title == "A useful paper"
    assert papers[0].arxiv_id == "2607.00001v1"
    assert papers[0].authors == ["A. Researcher"]


def test_search_builds_quoted_category_query(monkeypatch):
    captured = {}

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return None

        def read(self):
            return b'<feed xmlns="http://www.w3.org/2005/Atom" />'

    def fake_open(request, timeout):
        captured["url"] = request.full_url
        return Response()

    monkeypatch.setattr("urllib.request.urlopen", fake_open)
    ArxivClient().search("post-training LLM", 2, ("cs.CL", "cs.LG"))
    assert "all%3A%22post-training%22" in captured["url"]
    assert "cat%3Acs.CL" in captured["url"]
