"""
Tests for System (terminal control) and Cursor (cursor visibility).

os.system calls are mocked so the test runner itself is not affected.
The Cursor tests mock stdout on POSIX and ctypes on Windows.
"""
import sys
import os
import pytest
from unittest.mock import patch, MagicMock, call
from pybeaut import System, Cursor


# ---------------------------------------------------------------------------
# System class
# ---------------------------------------------------------------------------
class TestSystemAttributes:
    def test_windows_is_bool(self):
        assert isinstance(System.Windows, bool)

    def test_windows_matches_os_name(self):
        assert System.Windows == (os.name == "nt")


class TestSystemInit:
    def test_calls_system_with_empty_string(self, no_system):
        System.Init()
        no_system.assert_called_once_with("")

    def test_returns_none(self, no_system):
        assert System.Init() is None


class TestSystemClear:
    def test_calls_system(self, no_system):
        System.Clear()
        assert no_system.called

    def test_calls_cls_on_windows(self, no_system):
        with patch.object(System, "Windows", True):
            System.Clear()
        no_system.assert_called_with("cls")

    def test_calls_clear_on_posix(self, no_system):
        with patch.object(System, "Windows", False):
            System.Clear()
        no_system.assert_called_with("clear")

    def test_returns_system_exit_code(self, no_system):
        no_system.return_value = 0
        result = System.Clear()
        assert result == 0


class TestSystemTitle:
    def test_on_windows_calls_title_command(self, no_system):
        with patch.object(System, "Windows", True):
            System.Title("MyApp")
        no_system.assert_called_with("title MyApp")

    def test_on_posix_does_nothing(self, no_system):
        with patch.object(System, "Windows", False):
            result = System.Title("MyApp")
        no_system.assert_not_called()
        assert result is None

    def test_title_with_spaces(self, no_system):
        with patch.object(System, "Windows", True):
            System.Title("My App Title")
        no_system.assert_called_with("title My App Title")


class TestSystemSize:
    def test_on_windows_calls_mode_command(self, no_system):
        with patch.object(System, "Windows", True):
            System.Size(80, 24)
        no_system.assert_called_with("mode 80,24")

    def test_on_posix_does_nothing(self, no_system):
        with patch.object(System, "Windows", False):
            result = System.Size(80, 24)
        no_system.assert_not_called()
        assert result is None

    def test_different_dimensions(self, no_system):
        with patch.object(System, "Windows", True):
            System.Size(120, 40)
        no_system.assert_called_with("mode 120,40")


class TestSystemCommand:
    def test_passes_command_to_system(self, no_system):
        System.Command("echo hello")
        no_system.assert_called_once_with("echo hello")

    def test_returns_system_exit_code(self, no_system):
        no_system.return_value = 0
        assert System.Command("echo hi") == 0

    def test_empty_command(self, no_system):
        System.Command("")
        no_system.assert_called_once_with("")


# ---------------------------------------------------------------------------
# Cursor class
# ---------------------------------------------------------------------------
class TestCursorPosix:
    """Test ANSI escape output on POSIX systems."""

    def test_hide_cursor_writes_escape_sequence(self):
        mock_stdout = MagicMock()
        with patch("pybeaut._name", "posix"), \
             patch("pybeaut._stdout", mock_stdout):
            Cursor.HideCursor()
        mock_stdout.write.assert_called_with("\033[?25l")
        mock_stdout.flush.assert_called()

    def test_show_cursor_writes_escape_sequence(self):
        mock_stdout = MagicMock()
        with patch("pybeaut._name", "posix"), \
             patch("pybeaut._stdout", mock_stdout):
            Cursor.ShowCursor()
        mock_stdout.write.assert_called_with("\033[?25h")
        mock_stdout.flush.assert_called()

    def test_hide_then_show_different_sequences(self):
        written = []
        mock_stdout = MagicMock()
        mock_stdout.write.side_effect = written.append
        with patch("pybeaut._name", "posix"), \
             patch("pybeaut._stdout", mock_stdout):
            Cursor.HideCursor()
            Cursor.ShowCursor()
        assert "\033[?25l" in written
        assert "\033[?25h" in written


class TestCursorWindows:
    """Test that Windows cursor path calls the ctypes internals."""

    def _make_windll_mock(self):
        mock_windll = MagicMock()
        mock_windll.kernel32.GetStdHandle.return_value = MagicMock()
        mock_windll.kernel32.GetConsoleCursorInfo.return_value = 1
        mock_windll.kernel32.SetConsoleCursorInfo.return_value = 1
        return mock_windll

    def test_hide_cursor_calls_set_console_cursor_info(self):
        mock_windll = self._make_windll_mock()
        with patch("pybeaut._name", "nt"), \
             patch("pybeaut.windll", mock_windll, create=True):
            Cursor.HideCursor()
        mock_windll.kernel32.SetConsoleCursorInfo.assert_called_once()

    def test_show_cursor_calls_set_console_cursor_info(self):
        mock_windll = self._make_windll_mock()
        with patch("pybeaut._name", "nt"), \
             patch("pybeaut.windll", mock_windll, create=True):
            Cursor.ShowCursor()
        mock_windll.kernel32.SetConsoleCursorInfo.assert_called_once()

    def test_hide_and_show_both_call_get_and_set(self):
        mock_windll = self._make_windll_mock()
        with patch("pybeaut._name", "nt"), \
             patch("pybeaut.windll", mock_windll, create=True):
            Cursor.HideCursor()
            Cursor.ShowCursor()
        assert mock_windll.kernel32.SetConsoleCursorInfo.call_count == 2
