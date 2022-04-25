"""Test creation logic."""

import os.path
from pathlib import Path

import freezegun

from scriv.config import Config
from scriv.scriv import Scriv


class TestNewFragmentPath:
    """
    Tests of the paths of new fragments.
    """

    @freezegun.freeze_time("2012-10-01T07:08:09")
    def test_new_fragment_path(self, fake_git):
        fake_git.set_config("github.user", "joedev")
        fake_git.set_branch("master")
        scriv = Scriv(config=Config(fragment_directory="notes"))
        assert scriv.new_fragment().path == Path(
            "notes/20121001_070809_joedev.rst"
        )

    @freezegun.freeze_time("2012-10-01T07:08:09")
    def test_new_fragment_path_with_custom_main(self, fake_git):
        fake_git.set_config("github.user", "joedev")
        fake_git.set_branch("mainline")
        scriv = Scriv(
            config=Config(
                fragment_directory="notes", main_branches=["main", "mainline"]
            )
        )
        assert scriv.new_fragment().path == Path(
            "notes/20121001_070809_joedev.rst"
        )

    @freezegun.freeze_time("2013-02-25T15:16:17")
    def test_new_fragment_path_with_branch(self, fake_git):
        fake_git.set_config("github.user", "joedev")
        fake_git.set_branch("joedeveloper/feature-123.4")
        scriv = Scriv(config=Config(fragment_directory="notes"))
        assert scriv.new_fragment().path == Path(
            "notes/20130225_151617_joedev_feature_123_4.rst"
        )


class TestNewFragmentContent:
    """
    Tests of the content of new fragments.
    """

    def test_new_fragment_contents_rst(self):
        scriv = Scriv(config=Config(format="rst"))
        content = scriv.new_fragment().content
        assert content.startswith(".. ")
        assert ".. A new scriv changelog fragment" in content
        assert ".. Added\n.. -----\n" in content
        assert all(cat in content for cat in scriv.config.categories)

    def test_new_fragment_contents_rst_with_customized_header(self):
        scriv = Scriv(config=Config(format="rst", rst_header_chars="#~"))
        content = scriv.new_fragment().content
        assert content.startswith(".. ")
        assert ".. A new scriv changelog fragment" in content
        assert ".. Added\n.. ~~~~~\n" in content
        assert all(cat in content for cat in scriv.config.categories)

    def test_no_categories_rst(self, changelog_d):
        # If the project isn't using categories, then the new fragment is
        # simpler with no heading.
        scriv = Scriv(config=Config(categories=[]))
        content = scriv.new_fragment().content
        assert ".. A new scriv changelog fragment." in content
        assert "- A bullet item for this fragment. EDIT ME!" in content
        assert "Uncomment the header that is right" not in content
        assert ".. Added" not in content

    def test_new_fragment_contents_md(self):
        scriv = Scriv(config=Config(format="md"))
        content = scriv.new_fragment().content
        assert content.startswith("<!--")
        assert "A new scriv changelog fragment" in content
        assert "### Added\n" in content
        assert all(cat in content for cat in scriv.config.categories)


class TestCreate:
    """
    Tests of the create functionality.
    """

    def test_create_no_output_directory(self, cli_invoke):
        # With no changelog.d directory, create fails with a FileNotFoundError.
        result = cli_invoke(["create"], expect_ok=False)
        assert result.exit_code == 1
        assert (
            str(result.exception)
            == "Output directory 'changelog.d' doesn't exist, please create it."
        )

    def test_create_fragment(self, fake_git, cli_invoke, changelog_d):
        # Create will make one file with the current time in the name.
        fake_git.set_config("github.user", "joedev")
        with freezegun.freeze_time("2013-02-25T15:16:17"):
            cli_invoke(["create"])

        frags = sorted(changelog_d.iterdir())
        assert len(frags) == 1
        frag = frags[0]
        assert frag.name == "20130225_151617_joedev.rst"
        contents = frag.read_text()
        assert "A new scriv changelog fragment" in contents
        assert ".. Added\n.. -----\n" in contents

        # Using create later will make a second file with a new timestamp.
        with freezegun.freeze_time("2013-02-25T15:18:19"):
            cli_invoke(["create"])

        frags = sorted(changelog_d.iterdir())
        assert len(frags) == 2
        latest_frag = frags[-1]
        assert latest_frag.name == "20130225_151819_joedev.rst"

    def test_create_file_exists(self, fake_git, cli_invoke, changelog_d):
        # Create won't overwrite an existing fragment file.
        (changelog_d / "20130225_151617_joedev.rst").write_text("I'm precious!")
        fake_git.set_config("github.user", "joedev")
        with freezegun.freeze_time("2013-02-25T15:16:17"):
            result = cli_invoke(["create"], expect_ok=False)

        # "create" ended with an error and a message.
        assert result.exit_code == 1
        expected = (
            "File changelog.d"
            + getattr(os.path, "sep", "")
            + "20130225_151617_joedev.rst already exists, not overwriting\n"
        )
        assert result.stdout == expected

        # Our precious file is unharmed.
        frags = sorted(changelog_d.iterdir())
        assert len(frags) == 1
        frag = frags[0]
        assert frag.name == "20130225_151617_joedev.rst"
        assert frag.read_text() == "I'm precious!"


def fake_edit(mocker, expected_filename, contents, expected_editor=None):
    """
    Create a fake editing session.
    """

    def do_the_edit(filename, editor):
        pfilename = Path(filename)
        assert pfilename == expected_filename
        assert pfilename.exists()
        if expected_editor is not None:
            assert editor == expected_editor
        pfilename.write_text(contents, encoding="utf-8")

    return mocker.patch("click.edit", do_the_edit)


class TestCreateEdit:
    """
    Tests of editing created fragments.
    """

    def test_create_edit(self, mocker, fake_git, cli_invoke, changelog_d):
        # "scriv create --edit" will invoke a text editor.
        fake_git.set_config("github.user", "joedev")
        fake_git.set_editor("my_fav_editor")
        expected = Path("changelog.d/20130225_151617_joedev.rst")
        fake_edit(
            mocker,
            expected,
            expected_editor="my_fav_editor",
            contents="- My change is great!",
        )
        with freezegun.freeze_time("2013-02-25T15:16:17"):
            cli_invoke(["create", "--edit"])
        assert expected.exists()

    def test_create_edit_preference(
        self, mocker, fake_git, cli_invoke, changelog_d
    ):
        # The user can set a git configuration to default to --edit.
        fake_git.set_config("scriv.create.edit", "true")
        fake_git.set_config("github.user", "joedev")
        fake_git.set_editor("my_fav_editor")
        mock_edit = mocker.patch("click.edit")
        expected = Path("changelog.d/20130225_151617_joedev.rst")
        with freezegun.freeze_time("2013-02-25T15:16:17"):
            cli_invoke(["create"])
        mock_edit.assert_called_once_with(
            filename=str(expected), editor="my_fav_editor"
        )

    def test_create_edit_preference_no_edit(
        self, mocker, fake_git, cli_invoke, changelog_d
    ):
        # The user can set a git configuration to default to --edit, but
        # --no-edit will turn it off.
        fake_git.set_config("scriv.create.edit", "true")
        fake_git.set_config("github.user", "joedev")
        mock_edit = mocker.patch("click.edit")
        with freezegun.freeze_time("2013-02-25T15:16:17"):
            cli_invoke(["create", "--no-edit"])
        mock_edit.assert_not_called()

    def test_create_edit_abort(self, mocker, fake_git, cli_invoke, changelog_d):
        # User can edit the file to have no content, that will abort the create.
        fake_git.set_config("scriv.create.edit", "true")
        fake_git.set_config("github.user", "joedev")
        expected = Path("changelog.d/20130225_151617_joedev.rst")
        fake_edit(mocker, expected, contents=".. Nothing\n.. more nothing.\n")
        with freezegun.freeze_time("2013-02-25T15:16:17"):
            cli_invoke(["create"])
        assert not expected.exists()


class TestCreateAdd:
    """
    Tests of auto-adding created fragments.
    """

    def test_create_add(
        self, caplog, mocker, fake_git, cli_invoke, changelog_d
    ):
        # "scriv create --add" will invoke "git add" on the file.
        fake_git.set_config("github.user", "joedev")
        mock_call = mocker.patch("subprocess.call")
        mock_call.return_value = 0
        with freezegun.freeze_time("2013-02-25T15:16:17"):
            cli_invoke(["create", "--add"])
        file_path = (
            "changelog.d"
            + getattr(os.path, "sep", "")
            + "20130225_151617_joedev.rst"
        )
        mock_call.assert_called_once_with(["git", "add", file_path])
        assert "Added " + file_path in caplog.text

    def test_create_add_preference(
        self, mocker, fake_git, cli_invoke, changelog_d
    ):
        # The user can set a git configuration to default to --add.
        fake_git.set_config("github.user", "joedev")
        fake_git.set_config("scriv.create.add", "true")
        mock_call = mocker.patch("subprocess.call")
        mock_call.return_value = 0
        with freezegun.freeze_time("2013-02-25T15:16:17"):
            cli_invoke(["create"])
        file_path = (
            "changelog.d"
            + getattr(os.path, "sep", "")
            + "20130225_151617_joedev.rst"
        )
        mock_call.assert_called_once_with(["git", "add", file_path])

    def test_create_add_preference_no_add(
        self, caplog, mocker, fake_git, cli_invoke, changelog_d
    ):
        # The user can set a git configuration to default to --add, but --no-add
        # will turn it off.
        fake_git.set_config("github.user", "joedev")
        fake_git.set_config("scriv.create.add", "true")
        mock_call = mocker.patch("subprocess.call")
        with freezegun.freeze_time("2013-02-25T15:16:17"):
            cli_invoke(["create", "--no-add"])
        mock_call.assert_not_called()
        assert "Added" not in caplog.text

    def test_create_add_fail(
        self, caplog, mocker, fake_git, cli_invoke, changelog_d
    ):
        # We properly handle failure to add.
        fake_git.set_config("github.user", "joedev")
        mock_call = mocker.patch("subprocess.call")
        mock_call.return_value = 99
        with freezegun.freeze_time("2013-02-25T15:16:17"):
            result = cli_invoke(["create", "--add"], expect_ok=False)
        file_path = (
            "changelog.d"
            + getattr(os.path, "sep", "")  # getattr() prevents MyPy errors
            + "20130225_151617_joedev.rst"
        )
        mock_call.assert_called_once_with(["git", "add", file_path])
        assert result.exit_code == 99
        assert "Added" not in caplog.text
        assert "Couldn't add " + file_path in caplog.text
