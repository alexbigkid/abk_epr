"""Command line options for the Bing Wallpaper application."""

import sys
from unittest.mock import patch, MagicMock

import pytest

from abk_epr import clo


# Mock CONST for tests
class CONST:
    """Mocking CONST class from the constants.py."""

    NAME = "TestApp"
    VERSION = "1.2.3"
    LICENSE = "MIT"
    KEYWORDS = ["test", "cli"]
    AUTHORS = [{"name": "Alice", "email": "alice@example.com"}]
    MAINTAINERS = [{"name": "Bob", "email": "bob@example.com"}]


# Patch the CONST inside clo module
clo.CONST = CONST


@pytest.fixture
def cmd_options():
    """Command Options."""
    return clo.CommandLineOptions()


@patch("abk_epr.clo.LoggerManager.get_logger", return_value=MagicMock())
@patch("abk_epr.clo.LoggerManager.configure")
def test_handle_options_version_exit(mock_configure, mock_get_logger, cmd_options):
    """Test that passing '--version' prints version info and exits cleanly."""
    testargs = ["prog", "--version"]
    cmd_options._args = testargs
    with (
        patch.object(sys, "argv", testargs),
        patch("builtins.print") as mock_print,
        pytest.raises(SystemExit) as exc_info,
    ):
        cmd_options.handle_options()

    mock_print.assert_called_once_with(f"{CONST.NAME} version: {CONST.VERSION}")
    assert exc_info.value.code == 0  # noqa: S101
    mock_configure.assert_not_called()
    mock_get_logger.assert_not_called()


@patch("abk_epr.clo.LoggerManager.get_logger", return_value=MagicMock())
@patch("abk_epr.clo.LoggerManager.configure")
def test_handle_options_about_exit(mock_configure, mock_get_logger, cmd_options):
    """Test that passing '--about' prints app metadata and exits cleanly."""
    testargs = ["prog", "--about"]
    cmd_options._args = testargs
    with (
        patch.object(sys, "argv", testargs),
        patch("builtins.print") as mock_print,
        pytest.raises(SystemExit) as exc_info,
    ):
        cmd_options.handle_options()

    mock_print.assert_any_call(f"Name       : {CONST.NAME}")
    mock_print.assert_any_call(f"Version    : {CONST.VERSION}")
    assert exc_info.value.code == 0  # noqa: S101
    mock_configure.assert_not_called()
    mock_get_logger.assert_not_called()


@patch("abk_epr.clo.LoggerManager.get_logger", return_value=MagicMock())
@patch("abk_epr.clo.LoggerManager.configure")
def test_handle_options_parse_args(mock_configure, mock_get_logger, cmd_options):
    """Test that command-line arguments are correctly parsed into options."""
    testargs = ["prog", "-d", "test_dir", "-l"]
    with patch.object(sys, "argv", testargs):
        cmd_options.handle_options()

    assert cmd_options.options.dir == "test_dir"  # noqa: S101
    assert cmd_options.options.log_into_file is True  # noqa: S101
    assert cmd_options.options.quiet is False  # noqa: S101
    mock_configure.assert_called_once_with(log_into_file=True, quiet=False)
    mock_get_logger.assert_called_once_with("abk_epr.clo")
