"""
Tests for the Colors class and the Col alias.

Covers: static colors, dynamic colors, mappings, StaticRGB, StaticMIX,
DynamicMIX, Symbol, and list completeness.
"""
import pytest
from pybeaut import Colors, Col, _MakeColors

ANSI_START = "\033[38;2;"


# ---------------------------------------------------------------------------
# Static color attributes
# ---------------------------------------------------------------------------
STATIC_COLOR_PARAMS = [
    ("red",         Colors.red,         "255;0;0"),
    ("green",       Colors.green,       "0;255;0"),
    ("blue",        Colors.blue,        "0;0;255"),
    ("white",       Colors.white,       "255;255;255"),
    ("black",       Colors.black,       "0;0;0"),
    ("gray",        Colors.gray,        "150;150;150"),
    ("yellow",      Colors.yellow,      "255;255;0"),
    ("purple",      Colors.purple,      "255;0;255"),
    ("cyan",        Colors.cyan,        "0;255;255"),
    ("orange",      Colors.orange,      "255;150;0"),
    ("pink",        Colors.pink,        "255;0;150"),
    ("turquoise",   Colors.turquoise,   "0;150;255"),
    ("light_gray",  Colors.light_gray,  "200;200;200"),
    ("dark_gray",   Colors.dark_gray,   "100;100;100"),
    ("light_red",   Colors.light_red,   "255;100;100"),
    ("light_green", Colors.light_green, "100;255;100"),
    ("light_blue",  Colors.light_blue,  "100;100;255"),
    ("dark_red",    Colors.dark_red,    "100;0;0"),
    ("dark_green",  Colors.dark_green,  "0;100;0"),
    ("dark_blue",   Colors.dark_blue,   "0;0;100"),
]


@pytest.mark.parametrize("name,color,rgb", STATIC_COLOR_PARAMS, ids=[p[0] for p in STATIC_COLOR_PARAMS])
class TestStaticColorAttributes:
    def test_is_string(self, name, color, rgb):
        assert isinstance(color, str)

    def test_starts_with_ansi(self, name, color, rgb):
        assert color.startswith(ANSI_START)

    def test_ends_with_m(self, name, color, rgb):
        assert color.endswith("m")

    def test_rgb_values_embedded(self, name, color, rgb):
        assert rgb in color


# ---------------------------------------------------------------------------
# Special attributes
# ---------------------------------------------------------------------------
class TestSpecialAttributes:
    def test_reset_equals_white(self):
        assert Colors.reset == Colors.white

    def test_col_is_colors_alias(self):
        assert Col is Colors


# ---------------------------------------------------------------------------
# static_colors list
# ---------------------------------------------------------------------------
class TestStaticColorsList:
    def test_has_correct_length(self):
        assert len(Colors.static_colors) == 21

    def test_all_elements_are_strings(self):
        assert all(isinstance(c, str) for c in Colors.static_colors)

    def test_contains_red(self):
        assert Colors.red in Colors.static_colors

    def test_contains_reset(self):
        assert Colors.reset in Colors.static_colors


# ---------------------------------------------------------------------------
# static_colors_mapping dict
# ---------------------------------------------------------------------------
EXPECTED_STATIC_KEYS = [
    "red", "green", "blue", "white", "black", "gray", "yellow", "purple",
    "cyan", "orange", "pink", "turquoise", "light_gray", "dark_gray",
    "light_red", "light_green", "light_blue", "dark_red", "dark_green",
    "dark_blue", "reset",
]


class TestStaticColorsMapping:
    def test_has_correct_keys(self):
        assert set(Colors.static_colors_mapping.keys()) == set(EXPECTED_STATIC_KEYS)

    def test_values_match_attributes(self):
        for name in EXPECTED_STATIC_KEYS:
            assert Colors.static_colors_mapping[name] == getattr(Colors, name)

    def test_red_value_correct(self):
        assert Colors.static_colors_mapping["red"] == Colors.red

    def test_blue_value_correct(self):
        assert Colors.static_colors_mapping["blue"] == Colors.blue


# ---------------------------------------------------------------------------
# dynamic_colors_mapping dict
# ---------------------------------------------------------------------------
EXPECTED_DYNAMIC_KEYS = [
    "bw", "br", "bg", "bb", "wb", "wr", "wg", "wbl",
    "rb", "rw", "ry", "rp", "gb", "gw", "gy", "gc",
    "blb", "blw", "bc", "bp", "yr", "yg", "pr", "pb", "cg", "cb",
]


class TestDynamicColorsMapping:
    def test_has_correct_keys(self):
        assert set(Colors.dynamic_colors_mapping.keys()) == set(EXPECTED_DYNAMIC_KEYS)

    def test_values_are_lists(self):
        for key, value in Colors.dynamic_colors_mapping.items():
            assert isinstance(value, list), f"Key {key!r} should be a list"

    def test_bw_maps_to_black_to_white(self):
        assert Colors.dynamic_colors_mapping["bw"] is Colors.black_to_white


# ---------------------------------------------------------------------------
# dynamic_colors list
# ---------------------------------------------------------------------------
class TestDynamicColorsList:
    def test_is_not_empty(self):
        assert len(Colors.dynamic_colors) > 0

    def test_all_elements_are_lists(self):
        assert all(isinstance(c, list) for c in Colors.dynamic_colors)

    def test_each_gradient_has_at_least_24_elements(self):
        # Basic gradients → 24, composite (makergbcol) → 48, rainbow → 72
        for gradient in Colors.dynamic_colors:
            assert len(gradient) >= 24, (
                f"Expected ≥24 elements, got {len(gradient)}: {gradient[:3]}..."
            )

    def test_elements_are_rgb_strings(self):
        for gradient in Colors.dynamic_colors:
            for item in gradient:
                parts = item.split(";")
                assert len(parts) == 3, f"Bad RGB string: {item!r}"

    def test_contains_composite_gradients(self):
        assert Colors.red_to_blue in Colors.dynamic_colors
        assert Colors.rainbow in Colors.dynamic_colors


# ---------------------------------------------------------------------------
# all_colors list
# ---------------------------------------------------------------------------
class TestAllColors:
    def test_is_not_empty(self):
        assert len(Colors.all_colors) > 0

    def test_contains_all_static_colors(self):
        for color in Colors.static_colors:
            assert color in Colors.all_colors

    def test_contains_all_dynamic_colors(self):
        for color in Colors.dynamic_colors:
            assert color in Colors.all_colors


# ---------------------------------------------------------------------------
# StaticRGB
# ---------------------------------------------------------------------------
class TestStaticRGB:
    def test_returns_string(self):
        assert isinstance(Colors.StaticRGB(255, 0, 0), str)

    def test_starts_with_ansi(self):
        assert Colors.StaticRGB(100, 150, 200).startswith(ANSI_START)

    def test_red_matches_attribute(self):
        assert Colors.StaticRGB(255, 0, 0) == Colors.red

    def test_green_matches_attribute(self):
        assert Colors.StaticRGB(0, 255, 0) == Colors.green

    def test_blue_matches_attribute(self):
        assert Colors.StaticRGB(0, 0, 255) == Colors.blue

    def test_rgb_values_in_output(self):
        result = Colors.StaticRGB(10, 20, 30)
        assert "10;20;30" in result


# ---------------------------------------------------------------------------
# StaticMIX
# ---------------------------------------------------------------------------
class TestStaticMIX:
    def test_returns_string_with_start(self):
        result = Colors.StaticMIX([Colors.red, Colors.blue])
        assert isinstance(result, str)
        assert result.startswith(ANSI_START)

    def test_returns_plain_string_without_start(self):
        result = Colors.StaticMIX([Colors.red, Colors.blue], _start=False)
        assert isinstance(result, str)
        assert not result.startswith(ANSI_START)

    def test_red_blue_mix_is_purple(self):
        result = Colors.StaticMIX([Colors.red, Colors.blue], _start=False)
        r, g, b = (int(x) for x in result.split(";"))
        assert r > 0 and b > 0 and g == 0

    def test_mix_of_three_colors(self):
        result = Colors.StaticMIX([Colors.red, Colors.green, Colors.blue], _start=False)
        parts = result.split(";")
        assert len(parts) == 3

    def test_mixing_same_color_returns_same_color(self):
        result = Colors.StaticMIX([Colors.red, Colors.red], _start=False)
        assert result == "255;0;0"

    def test_white_black_mix_is_gray(self):
        result = Colors.StaticMIX([Colors.white, Colors.black], _start=False)
        r, g, b = (int(x) for x in result.split(";"))
        assert r == g == b == 128


# ---------------------------------------------------------------------------
# DynamicMIX
# ---------------------------------------------------------------------------
class TestDynamicMIX:
    def test_returns_list(self):
        result = Colors.DynamicMIX([Colors.red, Colors.blue])
        assert isinstance(result, list)

    def test_two_colors_produces_18_elements(self):
        result = Colors.DynamicMIX([Colors.red, Colors.blue])
        assert len(result) == 18

    def test_three_colors_produces_more_elements(self):
        result_2 = Colors.DynamicMIX([Colors.red, Colors.blue])
        result_3 = Colors.DynamicMIX([Colors.red, Colors.green, Colors.blue])
        assert len(result_3) > len(result_2)

    def test_elements_are_strings(self):
        result = Colors.DynamicMIX([Colors.red, Colors.blue])
        assert all(isinstance(x, str) for x in result)


# ---------------------------------------------------------------------------
# Symbol
# ---------------------------------------------------------------------------
class TestSymbol:
    def test_returns_string(self):
        result = Colors.Symbol("!", Colors.red, Colors.white)
        assert isinstance(result, str)

    def test_contains_symbol(self):
        result = Colors.Symbol("!", Colors.red, Colors.white)
        assert "!" in result

    def test_default_brackets(self):
        result = Colors.Symbol("!", Colors.red, Colors.white)
        assert "[" in result and "]" in result

    def test_custom_brackets(self):
        result = Colors.Symbol("*", Colors.green, Colors.white, left="(", right=")")
        assert "(" in result and ")" in result

    def test_ends_with_reset(self):
        result = Colors.Symbol("?", Colors.blue, Colors.white)
        assert result.endswith(Colors.reset)
