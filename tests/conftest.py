"""Fixture definitions."""

import os
import sys
import traceback
from collections.abc import Iterable
from pathlib import Path

import pytest
import responses
from click.testing import CliRunner

# We want to be able to test scriv without any extras installed.  But responses
# installs PyYaml.  If we are testing the no-extras scenario, then: after we've
# imported responses above, and before we import any scriv modules below,
# clobber the yaml module so that scriv's import will fail, simulating PyYaml
# not being available.
if os.getenv("SCRIV_TEST_NO_EXTRAS", ""):
    sys.modules["yaml"] = None  # type: ignore[assignment]

# pylint: disable=wrong-import-position

from scriv.cli import cli as scriv_cli

from .faker import FakeGit, FakeRunCommand

# Pytest will rewrite assertions in test modules, but not elsewhere.
# This tells pytest to also rewrite assertions in these files:
pytest.register_assert_rewrite("tests.helpers")


@pytest.fixture()
def fake_run_command(mocker):
    """Replace gitinfo.run_command with a fake."""
    return FakeRunCommand(mocker)


@pytest.fixture()
def fake_git(fake_run_command) -> FakeGit:
    """Get a FakeGit to use in tests."""
    return FakeGit(fake_run_command)


@pytest.fixture()
def temp_dir(tmpdir) -> Iterable[Path]:
    """Make and change into the tmpdir directory, as a Path."""
    old_dir = os.getcwd()
    tmpdir.chdir()
    try:
        yield Path(str(tmpdir))
    finally:
        os.chdir(old_dir)


@pytest.fixture()
def cli_invoke(temp_dir: Path):
    """
    Produce a function to invoke the Scriv cli with click.CliRunner.

    The test will run in a temp directory.
    """

    def invoke(command, expect_ok=True):
        runner = CliRunner(mix_stderr=False)
        result = runner.invoke(scriv_cli, command)
        print(result.stdout, end="")
        print(result.stderr, end="", file=sys.stderr)
        if result.exception:
            traceback.print_exception(
                None, result.exception, result.exception.__traceback__
            )
        if expect_ok:
            assert result.exception is None
            assert result.exit_code == 0
        return result

    return invoke


@pytest.fixture()
def changelog_d(temp_dir: Path) -> Path:
    """Make a changelog.d directory, and return a Path() to it."""
    the_changelog_d = temp_dir / "changelog.d"
    the_changelog_d.mkdir()
    return the_changelog_d


@pytest.fixture(autouse=True, name="responses")
def no_http_requests():
    """Activate `responses` for all tests, so no real HTTP happens."""
    with responses.RequestsMock() as rsps:
        yield rsps
