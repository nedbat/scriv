"""Extracting and checking links."""

import concurrent.futures
import logging
from collections.abc import Iterable

import markdown_it
import requests

logger = logging.getLogger(__name__)


def find_links(markdown_text: str) -> Iterable[str]:
    """Find all the URLs in some Markdown text."""

    def walk_tokens(tokens):
        for token in tokens:
            if token.type == "link_open":
                yield token.attrs["href"]
            if token.children:
                yield from walk_tokens(token.children)

    yield from walk_tokens(markdown_it.MarkdownIt().parse(markdown_text))


def check_markdown_links(markdown_text: str) -> None:
    """
    Check if the URLs in `markdown_text` are reachable.

    Returns None. Logs warnings for unreachable links.
    """
    links = set(find_links(markdown_text))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(check_one_link, links)


def check_one_link(url: str) -> None:
    """Check if a URL is reachable. Logs a warning if not."""
    try:
        resp = requests.head(url, timeout=60, allow_redirects=True)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.warning(f"Failed check for {url!r}: {exc}")
        return

    if resp.status_code == 200:
        logger.debug(f"OK link: {url!r}")
    else:
        logger.warning(
            f"Failed check for {url!r}: status code {resp.status_code}"
        )
