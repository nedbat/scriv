"""Test creation logic."""

import freezegun
import pytest

from scriv.config import Config
from scriv.create import new_fragment_contents, new_fragment_path


@freezegun.freeze_time("2012-10-01T07:08:09")
def test_new_fragment_path(fake_git):
    fake_git.set_config("github.user", "joedev")
    fake_git.set_branch("master")
    config = Config(fragment_directory="notes")
    assert new_fragment_path(config) == "notes/20121001_070809_joedev.rst"


@freezegun.freeze_time("2012-10-01T07:08:09")
def test_new_fragment_path_with_custom_main(fake_git):
    fake_git.set_config("github.user", "joedev")
    fake_git.set_branch("mainline")
    config = Config(fragment_directory="notes", main_branches=["main", "mainline"])
    assert new_fragment_path(config) == "notes/20121001_070809_joedev.rst"


@freezegun.freeze_time("2013-02-25T15:16:17")
def test_new_fragment_path_with_branch(fake_git):
    fake_git.set_config("github.user", "joedev")
    fake_git.set_branch("joedeveloper/feature-123.4")
    config = Config(fragment_directory="notes")
    assert new_fragment_path(config) == "notes/20130225_151617_joedev_feature_123_4.rst"


def test_new_fragment_contents_rst():
    config = Config(format="rst")
    contents = new_fragment_contents(config)
    assert contents.startswith(".. ")
    assert ".. A new scriv changelog fragment" in contents
    assert ".. Added\n.. -----\n" in contents
    assert all(cat in contents for cat in config.categories)


def test_new_fragment_contents_rst_with_customized_header():
    config = Config(format="rst", rst_header_chars="#~")
    contents = new_fragment_contents(config)
    assert contents.startswith(".. ")
    assert ".. A new scriv changelog fragment" in contents
    assert ".. Added\n.. ~~~~~\n" in contents
    assert all(cat in contents for cat in config.categories)


def test_no_categories_rst(changelog_d):
    # If the project isn't using categories, then the new fragment is simpler.
    config = Config(categories="")
    contents = new_fragment_contents(config)
    assert ".. A new scriv changelog fragment." in contents
    assert "- A bullet item for this fragment. EDIT ME!" in contents
    assert "Uncomment the header that is right" not in contents
    assert ".. Added" not in contents


def test_new_fragment_contents_md():
    config = Config(format="md")
    contents = new_fragment_contents(config)
    assert contents.startswith("<!--")
    assert "A new scriv changelog fragment" in contents
    assert "### Added\n" in contents
    assert all(cat in contents for cat in config.categories)


def test_new_fragment_contents_unknown():
    with pytest.raises(ValueError, match=r"'format' must be in \['rst', 'md'\] \(got 'xyzzy'\)"):
        Config(format="xyzzy")


def test_create_no_output_directory(cli_invoke):
    # With no changelog.d directory, create fails with a FileNotFoundError.
    result = cli_invoke(["create"], expect_ok=False)
    assert result.exit_code == 1
    assert isinstance(result.exception, FileNotFoundError)
    assert "changelog.d" in str(result.exception)


def test_create_fragment(fake_git, cli_invoke, changelog_d):
    # Create will make one file with the current time in the name.
    fake_git.set_config("github.user", "joedev")
    with freezegun.freeze_time("2013-02-25T15:16:17"):
        cli_invoke(["create"])

    frags = sorted(changelog_d.iterdir())
    assert len(frags) == 1
    frag = frags[0]
    assert "20130225_151617_joedev.rst" == frag.name
    contents = frag.read_text()
    assert "A new scriv changelog fragment" in contents
    assert ".. Added\n.. -----\n" in contents

    # Using create later will make a second file with a new timestamp.
    with freezegun.freeze_time("2013-02-25T15:18:19"):
        cli_invoke(["create"])

    frags = sorted(changelog_d.iterdir())
    assert len(frags) == 2
    latest_frag = frags[-1]
    assert "20130225_151819_joedev.rst" == latest_frag.name


def test_create_edit(mocker, fake_git, cli_invoke, changelog_d):
    # "scriv create --edit" will invoke a text editor.
    fake_git.set_config("github.user", "joedev")
    fake_git.set_editor("my_fav_editor")
    mock_edit = mocker.patch("click.edit")
    with freezegun.freeze_time("2013-02-25T15:16:17"):
        cli_invoke(["create", "--edit"])
    mock_edit.assert_called_once_with(filename="changelog.d/20130225_151617_joedev.rst", editor="my_fav_editor")


def test_create_edit_preference(mocker, fake_git, cli_invoke, changelog_d):
    # The user can set a git configuration to default to --edit.
    fake_git.set_config("scriv.create.edit", "true")
    fake_git.set_config("github.user", "joedev")
    fake_git.set_editor("my_fav_editor")
    mock_edit = mocker.patch("click.edit")
    with freezegun.freeze_time("2013-02-25T15:16:17"):
        cli_invoke(["create"])
    mock_edit.assert_called_once_with(filename="changelog.d/20130225_151617_joedev.rst", editor="my_fav_editor")


def test_create_edit_preference_no_edit(mocker, fake_git, cli_invoke, changelog_d):
    # The user can set a git configuration to default to --edit, but --no-edit
    # will turn it off.
    fake_git.set_config("scriv.create.edit", "true")
    fake_git.set_config("github.user", "joedev")
    mock_edit = mocker.patch("click.edit")
    with freezegun.freeze_time("2013-02-25T15:16:17"):
        cli_invoke(["create", "--no-edit"])
    mock_edit.assert_not_called()


def test_create_add(caplog, mocker, fake_git, cli_invoke, changelog_d):
    # "scriv create --add" will invoke "git add" on the file.
    fake_git.set_config("github.user", "joedev")
    mock_call = mocker.patch("subprocess.call")
    mock_call.return_value = 0
    with freezegun.freeze_time("2013-02-25T15:16:17"):
        cli_invoke(["create", "--add"])
    mock_call.assert_called_once_with(["git", "add", "changelog.d/20130225_151617_joedev.rst"])
    assert "Added changelog.d/20130225_151617_joedev.rst" in caplog.text


def test_create_add_preference(mocker, fake_git, cli_invoke, changelog_d):
    # The user can set a git configuration to default to --add.
    fake_git.set_config("github.user", "joedev")
    fake_git.set_config("scriv.create.add", "true")
    mock_call = mocker.patch("subprocess.call")
    mock_call.return_value = 0
    with freezegun.freeze_time("2013-02-25T15:16:17"):
        cli_invoke(["create"])
    mock_call.assert_called_once_with(["git", "add", "changelog.d/20130225_151617_joedev.rst"])


def test_create_add_preference_no_add(caplog, mocker, fake_git, cli_invoke, changelog_d):
    # The user can set a git configuration to default to --add, but --no-add
    # will turn it off.
    fake_git.set_config("github.user", "joedev")
    fake_git.set_config("scriv.create.add", "true")
    mock_call = mocker.patch("subprocess.call")
    with freezegun.freeze_time("2013-02-25T15:16:17"):
        cli_invoke(["create", "--no-add"])
    mock_call.assert_not_called()
    assert "Added" not in caplog.text


def test_create_add_fail(caplog, mocker, fake_git, cli_invoke, changelog_d):
    # We properly handle failure to add.
    fake_git.set_config("github.user", "joedev")
    mock_call = mocker.patch("subprocess.call")
    mock_call.return_value = 99
    with freezegun.freeze_time("2013-02-25T15:16:17"):
        result = cli_invoke(["create", "--add"], expect_ok=False)
    mock_call.assert_called_once_with(["git", "add", "changelog.d/20130225_151617_joedev.rst"])
    assert result.exit_code == 99
    assert "Added" not in caplog.text
    assert "Couldn't add changelog.d/20130225_151617_joedev.rst" in caplog.text


def test_create_file_exists(fake_git, cli_invoke, changelog_d):
    # Create won't overwrite an existing fragment file.
    (changelog_d / "20130225_151617_joedev.rst").write_text("I'm precious!")
    fake_git.set_config("github.user", "joedev")
    with freezegun.freeze_time("2013-02-25T15:16:17"):
        result = cli_invoke(["create"], expect_ok=False)

    # "create" ended with an error and a message.
    assert 1 == result.exit_code
    assert "File changelog.d/20130225_151617_joedev.rst already exists, not overwriting\n" == result.stdout

    # Our precious file is unharmed.
    frags = sorted(changelog_d.iterdir())
    assert len(frags) == 1
    frag = frags[0]
    assert "20130225_151617_joedev.rst" == frag.name
    assert "I'm precious!" == frag.read_text()
