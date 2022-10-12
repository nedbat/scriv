"""Updating GitHub releases."""

import logging
import sys

import click
import click_log

from .github import create_release, get_releases, update_release
from .gitinfo import get_github_repo
from .scriv import Scriv
from .shell import run_simple_command
from .util import extract_version, is_prerelease_version

logger = logging.getLogger()


@click.command()
@click.option(
    "--all",
    "all_entries",
    is_flag=True,
    help="Use all of the changelog entries.",
)
@click_log.simple_verbosity_option(logger)
def github_release(all_entries: bool) -> None:
    """
    Create GitHub releases from the changelog.

    Only the most recent changelog entry is used, unless --all is provided.

    """
    scriv = Scriv()
    changelog = scriv.changelog()
    changelog.read()

    repo = get_github_repo()
    if repo is None:
        sys.exit("Couldn't determine GitHub repo.")

    tags = set(run_simple_command("git tag").split())
    releases = get_releases(repo)

    for title, sections in changelog.entries().items():
        if title is None:
            continue
        version = extract_version(title)
        if version is None:
            logger.warning(f"Entry {title!r} has no version, skipping.")
            continue

        if version in tags:
            section_text = "\n\n".join(sections)
            md = changelog.format_tools().convert_to_markdown(section_text)
            release_data = {
                "body": md,
                "name": version,
                "tag_name": version,
                "draft": False,
                "prerelease": is_prerelease_version(version),
            }
            if version in releases:
                release = releases[version]
                if release["body"] != md:
                    update_release(release, release_data)
            else:
                create_release(repo, release_data)
        else:
            logger.warning(
                f"Version {version} has no tag. No release will be made."
            )

        if not all_entries:
            break
