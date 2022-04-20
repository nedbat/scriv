"""
Tests of tests/faker.py

Mostly error paths, since the happy paths are covered by other tests.
"""

from scriv import shell


def test_no_such_command(fake_run_command):
    assert shell.run_command("wut") == (
        False,
        "no fake command handler: ['wut']",
    )


def test_no_such_git_command(fake_git):
    assert shell.run_command("git hello") == (
        False,
        "no fake git command: ['git', 'hello']",
    )
    assert shell.run_command("git config --wut") == (
        False,
        "no fake git command: ['git', 'config', '--wut']",
    )
