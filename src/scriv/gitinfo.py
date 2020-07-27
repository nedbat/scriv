"""Get information from git."""

import os

from .shell import run_command, run_simple_command


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
