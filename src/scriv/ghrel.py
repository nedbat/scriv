"""Updating GitHub releases."""

import logging
import re
import sys
from typing import Optional

import click
import click_log
import jinja2

from .github import create_release, get_releases, update_release
from .gitinfo import get_github_repos
from .scriv import Scriv
from .shell import run_simple_command
from .util import Version

logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--all",
    "all_entries",
    is_flag=True,
    help="Use all of the changelog entries.",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Don't post to GitHub, just show what would be done.",
)
@click.option(
    "--repo",
    help="The GitHub repo (owner/reponame) to create the release in.",
)
@click_log.simple_verbosity_option()
def github_release(
    all_entries: bool,
    dry_run: bool,
    repo: Optional[str] = None,
) -> None:
    """
    Create GitHub releases from the changelog.

    Only the most recent changelog entry is used, unless --all is provided.

    """
    scriv = Scriv()
    changelog = scriv.changelog()
    changelog.read()

    if repo is None:
        repos = get_github_repos()
        if len(repos) == 0:
            sys.exit("Couldn't find a GitHub repo")
        elif len(repos) > 1:
            repo_list = ", ".join(sorted(repos))
            sys.exit(f"More than one GitHub repo found: {repo_list}")

        repo = repos.pop()

    if not re.fullmatch(r"[^ /]+/[^ /]+", repo):
        sys.exit(f"Repo must be owner/reponame: {repo!r}")

    tags = set(map(Version, run_simple_command("git tag").split()))
    releases = {Version(k): v for k, v in get_releases(repo).items()}

    for title, sections in changelog.entries().items():
        if title is None:
            continue
        version = Version.from_text(title)
        if version is None:
            logger.warning(f"Entry {title!r} has no version, skipping.")
            continue

        if version not in tags:
            logger.warning(
                f"Version {version} has no tag. No release will be made."
            )
            continue

        section_text = "\n\n".join(sections)
        md = changelog.format_tools().convert_to_markdown(section_text)

        release_data = {
            "body": md,
            "name": str(version),
            "tag_name": str(version),
            "draft": False,
            "prerelease": version.is_prerelease(),
        }

        ghrel_template = jinja2.Template(scriv.config.ghrel_template)
        md = ghrel_template.render(
            body=md,
            version=version,
            release=release_data,
            config=scriv.config,
        )
        release_data["body"] = md

        if version in releases:
            release = releases[version]
            if release["body"] != md:
                logger.debug(
                    f"Updating release {version}, data = {release_data}"
                )
                if dry_run:
                    logger.info(f"Would update release {version}")
                    logger.info(f"Body:\n{md}")
                else:
                    update_release(release, release_data)
        else:
            logger.debug(f"Creating release, data = {release_data}")
            if dry_run:
                logger.info(f"Would create release {version}")
                logger.info(f"Body:\n{md}")
            else:
                create_release(repo, release_data)

        if not all_entries:
            break
