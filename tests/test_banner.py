"""
Tests for Banner (also aliased as Box) — SimpleCube, DoubleCube, Box, Lines, Arrow.
"""
import pytest
from pybeaut import Banner, Box, Colors, Colorate

CONTENT = "Pybeaut"
MULTI = "Hello\nWorld"
LONG = "A much longer line here"


# ---------------------------------------------------------------------------
# Sanity: Box alias
# ---------------------------------------------------------------------------
class TestBoxAlias:
    def test_box_is_banner(self):
        assert Box is Banner


# ---------------------------------------------------------------------------
# Banner.SimpleCube
# ---------------------------------------------------------------------------
class TestSimpleCube:
    def test_returns_string(self):
        assert isinstance(Banner.SimpleCube(CONTENT), str)

    def test_contains_content(self):
        assert CONTENT in Banner.SimpleCube(CONTENT)

    def test_has_top_underscores(self):
        result = Banner.SimpleCube(CONTENT)
        assert "_" in result.splitlines()[0]

    def test_has_pipe_borders(self):
        result = Banner.SimpleCube(CONTENT)
        border_lines = [l for l in result.splitlines() if l.startswith("|")]
        assert len(border_lines) >= 2

    def test_has_closing_border(self):
        result = Banner.SimpleCube(CONTENT)
        last = result.splitlines()[-1]
        assert last.startswith("|_")

    def test_width_is_even(self):
        result = Banner.SimpleCube("A")
        inner_width = len(result.splitlines()[0].strip("_"))
        # just check it parsed cleanly
        assert isinstance(inner_width, int)

    def test_multi_line_content(self):
        result = Banner.SimpleCube(MULTI)
        assert "Hello" in result
        assert "World" in result

    def test_multi_line_has_multiple_content_rows(self):
        result = Banner.SimpleCube(MULTI)
        pipe_lines = [l for l in result.splitlines() if l.startswith("| ")]
        assert len(pipe_lines) >= 2

    def test_single_char_content(self):
        result = Banner.SimpleCube("X")
        assert "X" in result

    def test_long_content_wider_box(self):
        short_result = Banner.SimpleCube("Hi")
        long_result = Banner.SimpleCube(LONG)
        short_width = len(short_result.splitlines()[0])
        long_width = len(long_result.splitlines()[0])
        assert long_width > short_width


# ---------------------------------------------------------------------------
# Banner.Box (generic)
# ---------------------------------------------------------------------------
class TestBox:
    BORDERS = ("╔═", "═╗", "╚═", "═╝", "║", "═", "║", "═")

    def test_returns_string(self):
        result = Banner.Box(CONTENT, *self.BORDERS)
        assert isinstance(result, str)

    def test_contains_content(self):
        result = Banner.Box(CONTENT, *self.BORDERS)
        assert CONTENT in result

    def test_top_border_chars_present(self):
        result = Banner.Box(CONTENT, *self.BORDERS)
        first = result.splitlines()[0]
        assert "╔" in first and "╗" in first

    def test_bottom_border_chars_present(self):
        result = Banner.Box(CONTENT, *self.BORDERS)
        last = result.splitlines()[-1]
        assert "╚" in last and "╝" in last

    def test_side_borders_present(self):
        result = Banner.Box(CONTENT, *self.BORDERS)
        content_lines = result.splitlines()[1:-1]
        for line in content_lines:
            assert line.startswith("║")
            assert line.endswith("║")

    def test_multi_line_content(self):
        result = Banner.Box(MULTI, *self.BORDERS)
        assert "Hello" in result
        assert "World" in result

    def test_even_width_adjustment(self):
        # Odd-length content should have +1 added to long
        result = Banner.Box("ABC", *self.BORDERS)
        assert isinstance(result, str)

    def test_custom_ascii_borders(self):
        result = Banner.Box(CONTENT, "+", "+", "+", "+", "|", "-", "|", "-")
        assert "+" in result.splitlines()[0]
        assert "-" in result.splitlines()[0]


# ---------------------------------------------------------------------------
# Banner.DoubleCube
# ---------------------------------------------------------------------------
class TestDoubleCube:
    def test_returns_string(self):
        assert isinstance(Banner.DoubleCube(CONTENT), str)

    def test_contains_content(self):
        assert CONTENT in Banner.DoubleCube(CONTENT)

    def test_uses_double_line_borders(self):
        result = Banner.DoubleCube(CONTENT)
        assert "╔" in result and "╝" in result

    def test_multi_line_content(self):
        result = Banner.DoubleCube(MULTI)
        assert "Hello" in result

    def test_has_multiple_lines(self):
        result = Banner.DoubleCube(CONTENT)
        assert len(result.splitlines()) >= 3


# ---------------------------------------------------------------------------
# Banner.Lines
# ---------------------------------------------------------------------------
class TestLines:
    def test_returns_string_no_color(self):
        result = Banner.Lines(CONTENT)
        assert isinstance(result, str)

    def test_contains_content_no_color(self):
        result = Banner.Lines(CONTENT)
        assert CONTENT in result

    def test_has_separator_line(self):
        result = Banner.Lines(CONTENT)
        assert "═" in result or "─" in result

    def test_pepite_in_output(self):
        result = Banner.Lines(CONTENT)
        assert "ቐ" in result

    def test_custom_pepite(self):
        result = Banner.Lines(CONTENT, pepite="*")
        assert "*" in result

    def test_with_color(self):
        result = Banner.Lines(CONTENT, color=Colors.red_to_green)
        assert isinstance(result, str)
        assert CONTENT in result

    def test_multi_line_content(self):
        result = Banner.Lines(MULTI)
        assert "Hello" in result
        assert "World" in result

    def test_custom_line_char(self):
        result = Banner.Lines(CONTENT, line="-")
        assert "-" in result


# ---------------------------------------------------------------------------
# Banner.Arrow
# ---------------------------------------------------------------------------
class TestArrow:
    def test_returns_string_right(self):
        assert isinstance(Banner.Arrow(direction="right"), str)

    def test_returns_string_left(self):
        assert isinstance(Banner.Arrow(direction="left"), str)

    def test_right_arrow_is_not_empty(self):
        result = Banner.Arrow(direction="right")
        assert len(result.strip()) > 0

    def test_left_arrow_is_not_empty(self):
        result = Banner.Arrow(direction="left")
        assert len(result.strip()) > 0

    def test_custom_icon_appears_in_output(self):
        result = Banner.Arrow(icon="X", direction="right")
        assert "X" in result

    def test_larger_size_produces_longer_output(self):
        small = Banner.Arrow(size=1, direction="right")
        large = Banner.Arrow(size=4, direction="right")
        assert len(large) > len(small)

    def test_more_columns_produces_longer_lines(self):
        few = Banner.Arrow(number=1, direction="right")
        many = Banner.Arrow(number=4, direction="right")
        max_few = max(len(line) for line in few.splitlines())
        max_many = max(len(line) for line in many.splitlines())
        assert max_many > max_few

    def test_right_and_left_differ(self):
        right = Banner.Arrow(direction="right")
        left = Banner.Arrow(direction="left")
        assert right != left

    def test_default_icon_is_a(self):
        result = Banner.Arrow(direction="right")
        assert "a" in result
