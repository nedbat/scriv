"""Get information from git."""

import os

from scriv.shell import run_command


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
    ok, out = run_command("git rev-parse --symbolic-full-name HEAD")
    if not ok:
        return ""

    branch = out.strip()
    if branch.startswith("refs/heads/"):
        branch = branch[len("refs/heads/") :]
    return branch
