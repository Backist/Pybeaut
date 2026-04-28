"""
Tests for Center — XCenter, YCenter, Center, GroupAlign, TextAlign.

Terminal-size-dependent functions are exercised with both the mock fixture
and explicit space arguments so the tests run reliably in any environment.
"""
import pytest
from pybeaut import Center


SINGLE = "Hello"
MULTI = "Hello\nWorld\nFoo"


# ---------------------------------------------------------------------------
# XCenter
# ---------------------------------------------------------------------------
class TestXCenter:
    def test_returns_string(self):
        assert isinstance(Center.XCenter(SINGLE, spaces=5), str)

    def test_explicit_spaces_prepended(self):
        result = Center.XCenter(SINGLE, spaces=4)
        assert result.startswith("    ")

    def test_zero_spaces_no_prepend(self):
        result = Center.XCenter(SINGLE, spaces=0)
        assert result == SINGLE

    def test_multiline_all_lines_indented(self):
        result = Center.XCenter(MULTI, spaces=3)
        for line in result.splitlines():
            assert line.startswith("   ")

    def test_multiline_line_count_preserved(self):
        result = Center.XCenter(MULTI, spaces=2)
        assert len(result.splitlines()) == len(MULTI.splitlines())

    def test_custom_icon_used_as_fill(self):
        result = Center.XCenter(SINGLE, spaces=2, icon="-")
        assert result.startswith("--")

    def test_auto_spaces_from_terminal(self, terminal_80x24):
        result = Center.XCenter(SINGLE)
        assert isinstance(result, str)
        assert SINGLE in result

    def test_ose_error_returns_zero_spaces(self):
        from unittest.mock import patch
        with patch("pybeaut._terminal_size", side_effect=OSError):
            result = Center.XCenter(SINGLE)
        assert result == SINGLE


# ---------------------------------------------------------------------------
# YCenter
# ---------------------------------------------------------------------------
class TestYCenter:
    def test_returns_string(self):
        assert isinstance(Center.YCenter(SINGLE, spaces=2), str)

    def test_explicit_spaces_prepends_newlines(self):
        result = Center.YCenter(SINGLE, spaces=3)
        assert result.startswith("\n\n\n")

    def test_zero_spaces_no_newline_prepend(self):
        result = Center.YCenter(SINGLE, spaces=0)
        assert not result.startswith("\n")

    def test_content_preserved(self):
        result = Center.YCenter(MULTI, spaces=2)
        assert "Hello" in result
        assert "World" in result

    def test_custom_icon(self):
        result = Center.YCenter(SINGLE, spaces=2, icon="X")
        assert result.startswith("XX")

    def test_auto_spaces_from_terminal(self, terminal_80x24):
        result = Center.YCenter(SINGLE)
        assert isinstance(result, str)

    def test_ose_error_returns_zero_spaces(self):
        from unittest.mock import patch
        with patch("pybeaut._terminal_size", side_effect=OSError):
            result = Center.YCenter(SINGLE)
        assert SINGLE in result


# ---------------------------------------------------------------------------
# Center (both axes)
# ---------------------------------------------------------------------------
class TestCenterBothAxes:
    def test_returns_string(self):
        assert isinstance(Center.Center(SINGLE, xspaces=3, yspaces=2), str)

    def test_content_preserved(self):
        result = Center.Center(MULTI, xspaces=2, yspaces=1)
        assert "Hello" in result
        assert "World" in result

    def test_y_newlines_present(self):
        result = Center.Center(SINGLE, xspaces=0, yspaces=3)
        assert result.count("\n") >= 3

    def test_x_spaces_present(self):
        result = Center.Center(SINGLE, xspaces=4, yspaces=0)
        for line in result.splitlines():
            if line.strip():
                assert line.startswith("    ")

    def test_auto_both_from_terminal(self, terminal_80x24):
        result = Center.Center(SINGLE)
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# GroupAlign
# ---------------------------------------------------------------------------
class TestGroupAlign:
    def test_center_returns_string(self, terminal_80x24):
        result = Center.GroupAlign(SINGLE, Center.center)
        assert isinstance(result, str)

    def test_left_returns_original_text(self, terminal_80x24):
        result = Center.GroupAlign(MULTI, Center.left)
        assert result == MULTI

    def test_right_returns_string(self, terminal_80x24):
        result = Center.GroupAlign(MULTI, Center.right)
        assert isinstance(result, str)

    def test_right_lines_have_leading_spaces(self, terminal_80x24):
        result = Center.GroupAlign("Hi\nBye", Center.right)
        for line in result.splitlines():
            assert line.startswith(" ")

    def test_invalid_align_raises_bad_alignment(self, terminal_80x24):
        with pytest.raises(Center.BadAlignment):
            Center.GroupAlign(SINGLE, "INVALID")

    def test_case_insensitive_alignment(self, terminal_80x24):
        result = Center.GroupAlign(SINGLE, "left")
        assert result == SINGLE

    def test_center_uppercase(self, terminal_80x24):
        result = Center.GroupAlign(SINGLE, "CENTER")
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# TextAlign
# ---------------------------------------------------------------------------
class TestTextAlign:
    def test_left_returns_original(self):
        assert Center.TextAlign(MULTI, Center.left) == MULTI

    def test_center_returns_string(self):
        result = Center.TextAlign(MULTI, Center.center)
        assert isinstance(result, str)

    def test_center_shorter_lines_have_more_indent(self):
        text = "Hello World\nHi"
        result = Center.TextAlign(text, Center.center)
        lines = result.splitlines()
        short_indent = len(lines[1]) - len(lines[1].lstrip())
        long_indent = len(lines[0]) - len(lines[0].lstrip())
        assert short_indent > long_indent

    def test_right_returns_string(self):
        result = Center.TextAlign(MULTI, Center.right)
        assert isinstance(result, str)

    def test_right_longest_line_no_padding(self):
        text = "LongLine\nSh"
        result = Center.TextAlign(text, Center.right)
        lines = result.splitlines()
        longest = max(lines, key=len)
        assert longest.rstrip() == longest

    def test_invalid_align_raises_bad_alignment(self):
        with pytest.raises(Center.BadAlignment):
            Center.TextAlign(SINGLE, "BLAH")

    def test_case_insensitive(self):
        result = Center.TextAlign(MULTI, "right")
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# BadAlignment exception
# ---------------------------------------------------------------------------
class TestBadAlignment:
    def test_is_exception(self):
        assert issubclass(Center.BadAlignment, Exception)

    def test_message_mentions_options(self):
        exc = Center.BadAlignment()
        msg = str(exc)
        assert "Center.center" in msg or "CENTER" in msg.upper()

    def test_raised_by_group_align(self, terminal_80x24):
        with pytest.raises(Center.BadAlignment):
            Center.GroupAlign(SINGLE, "nope")

    def test_raised_by_text_align(self):
        with pytest.raises(Center.BadAlignment):
            Center.TextAlign(SINGLE, "nope")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------
class TestInternalHelpers:
    def test_xspaces_returns_int(self, terminal_80x24):
        result = Center._xspaces(SINGLE)
        assert isinstance(result, int)

    def test_xspaces_shorter_text_more_space(self, terminal_80x24):
        short = Center._xspaces("Hi")
        long_ = Center._xspaces("Hello World and more text")
        assert short >= long_

    def test_xspaces_ose_returns_zero(self):
        from unittest.mock import patch
        with patch("pybeaut._terminal_size", side_effect=OSError):
            assert Center._xspaces(SINGLE) == 0

    def test_yspaces_returns_int(self, terminal_80x24):
        result = Center._yspaces(SINGLE)
        assert isinstance(result, int)

    def test_yspaces_fewer_lines_more_space(self, terminal_80x24):
        one_line = Center._yspaces("Single")
        three_lines = Center._yspaces(MULTI)
        assert one_line >= three_lines

    def test_yspaces_ose_returns_zero(self):
        from unittest.mock import patch
        with patch("pybeaut._terminal_size", side_effect=OSError):
            assert Center._yspaces(SINGLE) == 0
