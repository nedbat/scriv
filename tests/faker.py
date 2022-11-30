"""Fake implementations of some of our external information sources."""

import shlex
from typing import Callable, Dict, Iterable, List, Optional, Set, Tuple

from scriv.shell import CmdResult

# A function that simulates run_command.
CmdHandler = Callable[[List[str]], CmdResult]


class FakeRunCommand:
    """
    A fake implementation of run_command.

    Add handlers for commands with `add_handler`.
    """

    def __init__(self, mocker):
        """Make the faker."""
        self.handlers: Dict[str, CmdHandler] = {}
        mocker.patch("scriv.gitinfo.run_command", self)
        mocker.patch("scriv.shell.run_command", self)

    def add_handler(self, argv0: str, handler: CmdHandler) -> None:
        """
        Add a handler for a command.

        The first word of the command is `argv0`.  The handler will be called
        with the complete argv list.  It must return the same results that
        `run_command` would have returned.
        """
        self.handlers[argv0] = handler

    def __call__(self, cmd: str) -> CmdResult:
        """Do the faking!."""
        if isinstance(cmd, str):
            argv = shlex.split(cmd)
        else:
            argv = cmd
        if argv[0] in self.handlers:
            return self.handlers[argv[0]](argv)
        return (False, f"no fake command handler: {argv}")


class FakeGit:
    """Simulate aspects of our local Git."""

    def __init__(self, frc: FakeRunCommand) -> None:
        """Make a FakeGit from a FakeRunCommand."""
        # Initialize with basic defaults.
        self.config: Dict[str, str] = {
            "core.bare": "false",
            "core.repositoryformatversion": "0",
        }
        self.branch = "main"
        self.editor = "vi"
        self.tags: Set[str] = set()
        self.remotes: Dict[str, Tuple[str, str]] = {}

        # Hook up our run_command handler.
        frc.add_handler("git", self.run_command)

    def run_command(self, argv: List[str]) -> CmdResult:
        """Simulate git commands."""
        # todo: match/case someday
        if argv[1] == "config":
            if argv[2] == "--get":
                if argv[3] in self.config:
                    return (True, self.config[argv[3]] + "\n")
                else:
                    return (False, f"error: no such key: {argv[3]}")
        elif argv[1:] == ["rev-parse", "--abbrev-ref", "HEAD"]:
            return (True, self.branch + "\n")
        elif argv[1:] == ["tag"]:
            return (True, "".join(tag + "\n" for tag in self.tags))
        elif argv[1:] == ["var", "GIT_EDITOR"]:
            return (True, self.editor + "\n")
        elif argv[1:] == ["remote", "-v"]:
            out = []
            for name, (url, push_url) in self.remotes.items():
                out.append(f"{name}\t{url} (fetch)\n")
                out.append(f"{name}\t{push_url} (push)\n")
            return (True, "".join(out))
        # raise Exception(f"no fake git command: {argv}")
        return (False, f"no fake git command: {argv}")

    def set_config(self, name: str, value: str) -> None:
        """Set a fake Git configuration value."""
        self.config[name] = value

    def set_branch(self, branch_name: str) -> None:
        """Set the current fake branch."""
        self.branch = branch_name

    def set_editor(self, editor_name: str) -> None:
        """Set the name of the fake editor Git will launch."""
        self.editor = editor_name

    def add_tags(self, tags: Iterable[str]) -> None:
        """Add tags to the repo."""
        self.tags.update(tags)

    def add_remote(
        self, name: str, url: str, push_url: Optional[str] = None
    ) -> None:
        """Add a remote with a name and a url."""
        self.remotes[name] = (url, push_url or url)
