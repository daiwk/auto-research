"""Link Chinese paper pages to their English siblings without rewriting them."""

from pathlib import PurePosixPath


def on_page_markdown(markdown, page, config, files):
    source = PurePosixPath(page.file.src_uri)
    if source.name != "README.md":
        return markdown
    sibling = source.with_name("README-en.md")
    if files.get_file_from_path(sibling.as_posix()) is None:
        return markdown
    return f"[Read this paper write-up in English]({sibling.name})\n\n{markdown}"
