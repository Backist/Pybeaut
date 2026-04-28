"""
Tests for _MakeColors — the internal ANSI helper class.

All functions are pure/deterministic, so no mocking is needed.
"""
import pytest
from pybeaut import _MakeColors, Colors

ANSI_START = "\033[38;2;"
WHITE_RESET = "\033[38;2;255;255;255m"


# ---------------------------------------------------------------------------
# _makeansi
# ---------------------------------------------------------------------------
class TestMakeansi:
    def test_returns_string(self):
        assert isinstance(_MakeColors._makeansi("255;0;0", "hello"), str)

    def test_contains_ansi_start_sequence(self):
        result = _MakeColors._makeansi("255;0;0", "hello")
        assert ANSI_START in result

    def test_contains_original_text(self):
        result = _MakeColors._makeansi("0;255;0", "world")
        assert "world" in result

    def test_ends_with_white_reset(self):
        result = _MakeColors._makeansi("0;0;255", "test")
        assert result.endswith(WHITE_RESET)

    def test_empty_text_still_valid(self):
        result = _MakeColors._makeansi("255;0;0", "")
        assert isinstance(result, str)
        assert ANSI_START in result

    def test_colour_embedded_between_codes(self):
        result = _MakeColors._makeansi("100;150;200", "X")
        assert "100;150;200" in result


# ---------------------------------------------------------------------------
# _rmansi
# ---------------------------------------------------------------------------
class TestRmansi:
    def test_strips_ansi_start_prefix(self):
        col = f"{ANSI_START}255;0;0m"
        assert ANSI_START not in _MakeColors._rmansi(col)

    def test_strips_trailing_m(self):
        col = f"{ANSI_START}255;0;0m"
        assert _MakeColors._rmansi(col) == "255;0;0"

    def test_plain_rgb_string_unchanged(self):
        assert _MakeColors._rmansi("100;200;50") == "100;200;50"

    def test_real_red_color(self):
        assert _MakeColors._rmansi(Colors.red) == "255;0;0"

    def test_real_blue_color(self):
        assert _MakeColors._rmansi(Colors.blue) == "0;0;255"

    def test_real_green_color(self):
        assert _MakeColors._rmansi(Colors.green) == "0;255;0"

    def test_white_color(self):
        assert _MakeColors._rmansi(Colors.white) == "255;255;255"


# ---------------------------------------------------------------------------
# _start
# ---------------------------------------------------------------------------
class TestStart:
    def test_returns_string(self):
        assert isinstance(_MakeColors._start("255;0;0"), str)

    def test_exact_format(self):
        assert _MakeColors._start("255;0;0") == "\033[38;2;255;0;0m"

    def test_starts_with_escape(self):
        assert _MakeColors._start("10;20;30").startswith(ANSI_START)

    def test_ends_with_m(self):
        assert _MakeColors._start("10;20;30").endswith("m")

    def test_roundtrip_with_rmansi(self):
        rgb = "123;45;67"
        assert _MakeColors._rmansi(_MakeColors._start(rgb)) == rgb


# ---------------------------------------------------------------------------
# _end
# ---------------------------------------------------------------------------
class TestEnd:
    def test_returns_white_reset(self):
        assert _MakeColors._end() == WHITE_RESET

    def test_is_string(self):
        assert isinstance(_MakeColors._end(), str)

    def test_idempotent(self):
        assert _MakeColors._end() == _MakeColors._end()


# ---------------------------------------------------------------------------
# _maketext
# ---------------------------------------------------------------------------
class TestMaketext:
    def test_contains_text_without_end(self):
        color = _MakeColors._start("255;0;0")
        result = _MakeColors._maketext(color, "hi", end=False)
        assert "hi" in result

    def test_no_reset_when_end_false(self):
        color = _MakeColors._start("255;0;0")
        result = _MakeColors._maketext(color, "hi", end=False)
        assert result == color + "hi"

    def test_reset_appended_when_end_true(self):
        color = _MakeColors._start("0;200;0")
        result = _MakeColors._maketext(color, "bye", end=True)
        assert result.endswith(WHITE_RESET)

    def test_color_prefix_present(self):
        color = _MakeColors._start("0;0;255")
        result = _MakeColors._maketext(color, "z", end=False)
        assert result.startswith(color)


# ---------------------------------------------------------------------------
# _getspaces
# ---------------------------------------------------------------------------
class TestGetspaces:
    def test_no_leading_spaces(self):
        assert _MakeColors._getspaces("hello") == 0

    def test_single_leading_space(self):
        assert _MakeColors._getspaces(" hello") == 1

    def test_multiple_leading_spaces(self):
        assert _MakeColors._getspaces("   hello") == 3

    def test_empty_string(self):
        assert _MakeColors._getspaces("") == 0

    def test_only_spaces(self):
        assert _MakeColors._getspaces("   ") == 3

    def test_tabs_count_as_one_char_each(self):
        assert _MakeColors._getspaces("\t\thello") == 2


# ---------------------------------------------------------------------------
# _makergbcol
# ---------------------------------------------------------------------------
class TestMakergbcol:
    def test_returns_list(self):
        result = _MakeColors._makergbcol(Colors.red_to_yellow, Colors.yellow_to_green)
        assert isinstance(result, list)

    def test_length_is_48(self):
        # Takes first 12 of each list (24 total), then extends with reversed(24) → 48
        result = _MakeColors._makergbcol(Colors.red_to_yellow, Colors.yellow_to_green)
        assert len(result) == 48

    def test_elements_are_strings(self):
        result = _MakeColors._makergbcol(Colors.red_to_yellow, Colors.yellow_to_green)
        assert all(isinstance(x, str) for x in result)

    def test_different_input_pairs(self):
        result = _MakeColors._makergbcol(Colors.blue_to_cyan, Colors.cyan_to_green)
        assert len(result) == 48


# ---------------------------------------------------------------------------
# _makerainbow
# ---------------------------------------------------------------------------
class TestMakerainbow:
    def test_returns_list(self):
        result = _MakeColors._makerainbow(Colors.red_to_green)
        assert isinstance(result, list)

    def test_single_color_list(self):
        result = _MakeColors._makerainbow(Colors.red_to_green)
        assert len(result) == len(Colors.red_to_green[:24])

    def test_combines_two_colors(self):
        result = _MakeColors._makerainbow(Colors.red_to_green, Colors.green_to_blue)
        assert len(result) > len(Colors.red_to_green[:24])

    def test_elements_are_strings(self):
        result = _MakeColors._makerainbow(Colors.red_to_green)
        assert all(isinstance(x, str) for x in result)


# ---------------------------------------------------------------------------
# _reverse
# ---------------------------------------------------------------------------
class TestReverse:
    def test_doubles_the_list(self):
        lst = ["a", "b", "c"]
        result = _MakeColors._reverse(list(lst))
        assert len(result) == 6

    def test_second_half_is_reversed_first_half(self):
        lst = ["a", "b", "c"]
        result = _MakeColors._reverse(list(lst))
        assert result[3:] == ["c", "b", "a"]

    def test_returns_same_list_object(self):
        lst = ["x", "y"]
        result = _MakeColors._reverse(lst)
        assert result is lst

    def test_single_element(self):
        lst = ["only"]
        result = _MakeColors._reverse(lst)
        assert result == ["only", "only"]


# ---------------------------------------------------------------------------
# _mixcolors
# ---------------------------------------------------------------------------
class TestMixcolors:
    def test_returns_list(self):
        result = _MakeColors._mixcolors(Colors.red, Colors.blue)
        assert isinstance(result, list)

    def test_without_reverse_has_9_elements(self):
        result = _MakeColors._mixcolors(Colors.red, Colors.blue, _reverse=False)
        assert len(result) == 9

    def test_with_reverse_doubles_to_18(self):
        result = _MakeColors._mixcolors(Colors.red, Colors.blue, _reverse=True)
        assert len(result) == 18

    def test_elements_are_rgb_strings(self):
        result = _MakeColors._mixcolors(Colors.red, Colors.blue, _reverse=False)
        for item in result:
            assert isinstance(item, str)
            parts = item.split(";")
            assert len(parts) == 3

    def test_first_element_is_source_color(self):
        result = _MakeColors._mixcolors(Colors.red, Colors.blue, _reverse=False)
        assert result[0] == _MakeColors._rmansi(Colors.red)

    def test_last_element_is_target_color(self):
        result = _MakeColors._mixcolors(Colors.red, Colors.blue, _reverse=False)
        assert result[-1] == _MakeColors._rmansi(Colors.blue)
