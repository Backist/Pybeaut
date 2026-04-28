"""
Tests for Colorate — static coloring, gradient modes, and Format.

Error() is tested with enter=False to avoid blocking on input().
"""
import re
import pytest
from unittest.mock import patch
from pybeaut import Colors, Colorate, _MakeColors

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def strip_ansi(text: str) -> str:
    return _ANSI_RE.sub("", text)

ANSI_START = "\033[38;2;"
WHITE_RESET = "\033[38;2;255;255;255m"

SINGLE_LINE = "Hello"
MULTI_LINE = "Hello\nWorld\nPybeaut"
GRADIENT = Colors.red_to_green  # 24 elements, safe for all gradient tests


# ---------------------------------------------------------------------------
# Color (static)
# ---------------------------------------------------------------------------
class TestColor:
    def test_returns_string(self):
        assert isinstance(Colorate.Color(Colors.red, "test"), str)

    def test_contains_original_text(self):
        result = Colorate.Color(Colors.red, "hello")
        assert "hello" in result

    def test_starts_with_color(self):
        result = Colorate.Color(Colors.red, "hi", end=True)
        assert result.startswith(Colors.red)

    def test_end_true_appends_white_reset(self):
        result = Colorate.Color(Colors.red, "hi", end=True)
        assert result.endswith(WHITE_RESET)

    def test_end_false_no_extra_reset(self):
        result = Colorate.Color(Colors.red, "hi", end=False)
        assert result == Colors.red + "hi"

    def test_different_static_colors(self):
        for color in [Colors.blue, Colors.green, Colors.yellow, Colors.purple]:
            result = Colorate.Color(color, "x")
            assert isinstance(result, str)
            assert "x" in result

    def test_multiline_text(self):
        result = Colorate.Color(Colors.cyan, MULTI_LINE)
        assert "Hello" in result
        assert "World" in result


# ---------------------------------------------------------------------------
# Vertical
# ---------------------------------------------------------------------------
class TestVertical:
    def test_returns_string(self):
        result = Colorate.Vertical(GRADIENT, SINGLE_LINE)
        assert isinstance(result, str)

    def test_contains_text(self):
        result = Colorate.Vertical(GRADIENT, SINGLE_LINE)
        assert "Hello" in result

    def test_output_longer_than_input(self):
        result = Colorate.Vertical(GRADIENT, SINGLE_LINE)
        assert len(result) > len(SINGLE_LINE)

    def test_multi_line_each_line_colored(self):
        result = Colorate.Vertical(GRADIENT, MULTI_LINE)
        assert result.count(ANSI_START) >= 3

    def test_fill_mode_colors_per_character(self):
        plain = Colorate.Vertical(GRADIENT, "AB")
        filled = Colorate.Vertical(GRADIENT, "AB", fill=True)
        assert filled.count(ANSI_START) >= plain.count(ANSI_START)

    def test_speed_parameter_accepted(self):
        result = Colorate.Vertical(GRADIENT, MULTI_LINE, speed=2)
        assert isinstance(result, str)

    def test_cut_skips_initial_colors(self):
        result_no_cut = Colorate.Vertical(GRADIENT, MULTI_LINE, cut=0)
        result_cut = Colorate.Vertical(GRADIENT, MULTI_LINE, cut=5)
        assert result_no_cut != result_cut

    def test_stop_limits_color_progression(self):
        result = Colorate.Vertical(GRADIENT, MULTI_LINE, stop=3)
        assert isinstance(result, str)

    def test_preserves_leading_whitespace(self):
        indented = "  Hello\n  World"
        result = Colorate.Vertical(GRADIENT, indented)
        lines = result.splitlines()
        assert any(line.startswith("  ") for line in lines)

    def test_no_trailing_newline(self):
        result = Colorate.Vertical(GRADIENT, MULTI_LINE)
        assert not result.endswith("\n")


# ---------------------------------------------------------------------------
# Horizontal
# ---------------------------------------------------------------------------
class TestHorizontal:
    def test_returns_string(self):
        assert isinstance(Colorate.Horizontal(GRADIENT, SINGLE_LINE), str)

    def test_contains_text(self):
        result = Colorate.Horizontal(GRADIENT, SINGLE_LINE)
        assert "Hello" in result

    def test_output_longer_than_input(self):
        result = Colorate.Horizontal(GRADIENT, SINGLE_LINE)
        assert len(result) > len(SINGLE_LINE)

    def test_each_character_gets_color(self):
        result = Colorate.Horizontal(GRADIENT, "ABC")
        assert result.count(ANSI_START) >= 3

    def test_multi_line(self):
        result = Colorate.Horizontal(GRADIENT, MULTI_LINE)
        assert "Hello" in result
        assert "World" in result

    def test_speed_parameter_accepted(self):
        result = Colorate.Horizontal(GRADIENT, SINGLE_LINE, speed=2)
        assert isinstance(result, str)

    def test_cut_changes_output(self):
        result0 = Colorate.Horizontal(GRADIENT, SINGLE_LINE, cut=0)
        result5 = Colorate.Horizontal(GRADIENT, SINGLE_LINE, cut=5)
        assert result0 != result5

    def test_no_trailing_newline(self):
        result = Colorate.Horizontal(GRADIENT, MULTI_LINE)
        assert not result.endswith("\n")


# ---------------------------------------------------------------------------
# Diagonal
# ---------------------------------------------------------------------------
class TestDiagonal:
    def test_returns_string(self):
        assert isinstance(Colorate.Diagonal(GRADIENT, SINGLE_LINE), str)

    def test_contains_text(self):
        result = Colorate.Diagonal(GRADIENT, SINGLE_LINE)
        assert "Hello" in result

    def test_output_has_ansi_codes(self):
        result = Colorate.Diagonal(GRADIENT, SINGLE_LINE)
        assert ANSI_START in result

    def test_multi_line_has_ansi_codes(self):
        result = Colorate.Diagonal(GRADIENT, MULTI_LINE)
        assert result.count(ANSI_START) >= 3

    def test_speed_parameter_accepted(self):
        result = Colorate.Diagonal(GRADIENT, MULTI_LINE, speed=3)
        assert isinstance(result, str)

    def test_cut_changes_output(self):
        r0 = Colorate.Diagonal(GRADIENT, MULTI_LINE, cut=0)
        r6 = Colorate.Diagonal(GRADIENT, MULTI_LINE, cut=6)
        assert r0 != r6

    def test_no_trailing_newline(self):
        result = Colorate.Diagonal(GRADIENT, MULTI_LINE)
        assert not result.endswith("\n")


# ---------------------------------------------------------------------------
# DiagonalBackwards
# ---------------------------------------------------------------------------
class TestDiagonalBackwards:
    def test_returns_string(self):
        assert isinstance(Colorate.DiagonalBackwards(GRADIENT, SINGLE_LINE), str)

    def test_contains_text(self):
        result = Colorate.DiagonalBackwards(GRADIENT, SINGLE_LINE)
        assert "Hello" in result

    def test_has_ansi_codes(self):
        result = Colorate.DiagonalBackwards(GRADIENT, SINGLE_LINE)
        assert ANSI_START in result

    def test_different_from_forward_diagonal(self):
        fwd = Colorate.Diagonal(GRADIENT, MULTI_LINE)
        bwd = Colorate.DiagonalBackwards(GRADIENT, MULTI_LINE)
        assert fwd != bwd

    def test_multi_line_has_multiple_codes(self):
        result = Colorate.DiagonalBackwards(GRADIENT, MULTI_LINE)
        assert result.count(ANSI_START) >= 3

    def test_speed_parameter_accepted(self):
        result = Colorate.DiagonalBackwards(GRADIENT, MULTI_LINE, speed=2)
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# Format
# ---------------------------------------------------------------------------
class TestFormat:
    def test_returns_string_horizontal(self):
        result = Colorate.Format("Hello World!", ["!"], Colorate.Horizontal, GRADIENT, Colors.red)
        assert isinstance(result, str)

    def test_returns_string_vertical(self):
        result = Colorate.Format(MULTI_LINE, ["H"], Colorate.Vertical, GRADIENT, Colors.green)
        assert isinstance(result, str)

    def test_second_chars_get_own_color(self):
        marker = "!"
        result = Colorate.Format(f"Hello{marker}", [marker], Colorate.Horizontal, GRADIENT, Colors.red)
        assert marker in result

    def test_empty_second_chars(self):
        result = Colorate.Format("Hello", [], Colorate.Horizontal, GRADIENT, Colors.yellow)
        assert "Hello" in result

    def test_multiple_second_chars(self):
        result = Colorate.Format("A!B@C", ["!", "@"], Colorate.Horizontal, GRADIENT, Colors.purple)
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# Error (enter=False to avoid blocking)
# ---------------------------------------------------------------------------
class TestError:
    def test_returns_none_without_input(self, capsys):
        result = Colorate.Error("oops", enter=False)
        assert result is None

    def test_prints_to_stdout(self, capsys):
        Colorate.Error("oops", enter=False)
        captured = capsys.readouterr()
        assert "oops" in captured.out

    def test_custom_color_accepted(self, capsys):
        Colorate.Error("fail", color=Colors.yellow, enter=False)
        captured = capsys.readouterr()
        assert "fail" in captured.out

    def test_spaces_parameter_adds_newlines(self, capsys):
        Colorate.Error("msg", enter=False, spaces=2)
        captured = capsys.readouterr()
        assert captured.out.count("\n") >= 2

    def test_wait_as_number_calls_sleep(self):
        with patch("pybeaut._sleep") as mock_sleep:
            Colorate.Error("slow", enter=False, wait=1)
            mock_sleep.assert_called_once_with(1)

    def test_wait_false_does_not_sleep(self):
        with patch("pybeaut._sleep") as mock_sleep:
            Colorate.Error("fast", enter=False, wait=False)
            mock_sleep.assert_not_called()
