"""Get information from git."""

import logging
import os
import subprocess
import sys

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
    return run_simple_command("git config --get {}".format(option))


def git_config_bool(option: str) -> bool:
    """
    Return a boolean git config value.
    """
    return git_config(option) == "true"


def git_editor() -> str:
    """
    Get the command name of the editor Git will launch.
    """
    return run_simple_command("git var GIT_EDITOR")


def git_edit(filename: str) -> None:
    """Edit a file using the same editor Git chooses."""
    click.edit(filename=filename, editor=git_editor())


def git_add(filename: str) -> None:
    """Git add a file. If it fails, sys.exit."""
    ret = subprocess.call(["git", "add", filename])
    if ret == 0:
        logger.info("Added {}".format(filename))
    else:
        logger.error("Couldn't add {}".format(filename))
        sys.exit(ret)


def git_rm(filename: str) -> None:
    """Git rm a file. If it fails, sys.exit."""
    ret = subprocess.call(["git", "rm", filename])
    if ret == 0:
        logger.info("Removed {}".format(filename))
    else:
        logger.error("Couldn't remove {}".format(filename))
        sys.exit(ret)
