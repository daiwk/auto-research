"""Link Chinese pages to available English counterparts without rewriting them."""

from pathlib import PurePosixPath
from posixpath import relpath


def on_page_markdown(markdown, page, config, files):
    source = PurePosixPath(page.file.src_uri)
    if source.parts[0] == "en" or source.name == "README-en.md" or source == PurePosixPath("index.md"):
        return markdown
    if source.name == "README.md":
        sibling = source.with_name("README-en.md")
        if files.get_file_from_path(sibling.as_posix()) is not None:
            return f"[Read this paper write-up in English]({sibling.name})\n\n{markdown}"
    target = "en/setup.md" if source == PurePosixPath("readme_setup.md") else f"en/{source.as_posix()}"
    if files.get_file_from_path(target) is not None:
        link = relpath(target, source.parent.as_posix())
        return f"[Read this page in English]({link})\n\n{markdown}"
    return markdown
