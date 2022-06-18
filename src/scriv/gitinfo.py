"""Get information from git."""

import logging
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

import click

from .shell import run_command, run_simple_command

logger = logging.getLogger()


def user_nick() -> str:
    """
    Get a short name for the current user.
    """
    ok, out = run_command("git config --get github.user")
    if ok:
        return out.strip()

    ok, out = run_command("git config --get user.email")
    if ok:
        nick = out.partition("@")[0]
        return nick

    return os.getenv("USER", "somebody")


def current_branch_name() -> str:
    """
    Get the current branch name.
    """
    return run_simple_command("git rev-parse --abbrev-ref HEAD")


def git_config(option: str) -> str:
    """
    Return a git config value.
    """
    return run_simple_command(f"git config --get {option}")


def git_config_bool(option: str) -> bool:
    """
    Return a boolean git config value, defaulting to False.
    """
    return git_config(option) == "true"


def git_edit(filename: Path) -> None:
    """Edit a file using the same editor Git chooses."""
    git_editor = run_simple_command("git var GIT_EDITOR")
    click.edit(filename=str(filename), editor=git_editor)


def git_add(filename: Path) -> None:
    """Git add a file. If it fails, sys.exit."""
    ret = subprocess.call(["git", "add", str(filename)])
    if ret == 0:
        logger.info(f"Added {filename}")
    else:
        logger.error(f"Couldn't add {filename}")
        sys.exit(ret)


def git_rm(filename: Path) -> None:
    """Git rm a file. If it fails, sys.exit."""
    ret = subprocess.call(["git", "rm", str(filename)])
    if ret == 0:
        logger.info(f"Removed {filename}")
    else:
        logger.error(f"Couldn't remove {filename}")
        sys.exit(ret)


def get_github_repo() -> Optional[str]:
    """
    Find the GitHub name/repo for this project.

    If there is no remote on GitHub, or more than one, return None.
    """
    urls = run_simple_command(
        # Backslashes and quoting are hard cross-platform, so avoid them.
        ["git", "config", "--get-regex", "remote[.].*[.]url"]
    ).splitlines()
    github_repos = []
    for url in urls:
        m = re.search(r"github.com[:/]([^/]+/[^/]+)", url)
        if m:
            repo = m[1]
            # I think it always has .git appended..
            if repo.endswith(".git"):  # pragma: no branch
                repo = repo[:-4]
            github_repos.append(repo)
    if len(github_repos) == 1:
        return github_repos[0]
    return None
