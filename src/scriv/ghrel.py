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
@click_log.simple_verbosity_option(logger)
def github_release() -> None:
    """
    Update GitHub releases from the changelog.
    """
    scriv = Scriv()
    changelog = scriv.changelog()
    changelog.read()

    tags = set(run_simple_command("git tag").split())
    repo = get_github_repo()
    if repo is None:
        sys.exit("Couldn't determine GitHub repo.")

    releases = get_releases(repo)

    for title, sections in changelog.entries().items():
        if title is None:
            continue
        version = extract_version(title)
        if version is None:
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
