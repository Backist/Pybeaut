"""
Tests for Add — banner combination and layout helpers.
"""
import pytest
from pybeaut import Add

B1 = "Hello\nWorld\nFoo"      # 3 lines, longest = 5
B2 = "Pybeaut\nLib"           # 2 lines, longest = 7
SINGLE1 = "Left"
SINGLE2 = "Right"


# ---------------------------------------------------------------------------
# Add.Add
# ---------------------------------------------------------------------------
class TestAddAdd:
    def test_returns_string(self):
        assert isinstance(Add.Add(SINGLE1, SINGLE2), str)

    def test_result_has_lines(self):
        result = Add.Add(B1, B2)
        assert len(result.splitlines()) > 0

    def test_content_from_both_banners_present(self):
        result = Add.Add(B1, B2)
        assert "Hello" in result or "World" in result or "Foo" in result
        assert "Pybeaut" in result or "Lib" in result

    def test_zero_spaces(self):
        result = Add.Add(B1, B2, spaces=0)
        assert isinstance(result, str)

    def test_equal_height_banners(self):
        b1 = "A\nB\nC"
        b2 = "X\nY\nZ"
        result = Add.Add(b1, b2, spaces=0)
        lines = result.splitlines()
        assert len(lines) == 3

    def test_banner1_taller_than_banner2(self):
        tall = "Line1\nLine2\nLine3\nLine4"
        short = "Only"
        result = Add.Add(tall, short, spaces=0)
        assert isinstance(result, str)
        assert len(result.splitlines()) >= 4

    def test_banner2_taller_than_banner1(self):
        short = "Only"
        tall = "Line1\nLine2\nLine3\nLine4"
        result = Add.Add(short, tall, spaces=0)
        assert isinstance(result, str)
        assert len(result.splitlines()) >= 4

    def test_center_true_auto_calculates_spaces(self):
        result = Add.Add(B1, B2, center=True)
        assert isinstance(result, str)

    def test_excessive_spaces_clamped(self):
        result = Add.Add(SINGLE1, SINGLE2, spaces=9999)
        assert isinstance(result, str)

    def test_single_line_banners(self):
        result = Add.Add("A", "B", spaces=0)
        assert "A" in result
        assert "B" in result

    def test_output_ends_with_newline(self):
        result = Add.Add(B1, B2, spaces=0)
        assert result.endswith("\n")

    def test_banner1_lines_padded_uniformly(self):
        b1 = "Hi\nHello"
        result = Add.Add(b1, "X\nX", spaces=0)
        lines = result.splitlines()
        # Every line should have the same total prefix width
        prefixes = []
        for line in lines:
            before_second = line.split("X")[0] if "X" in line else line
            prefixes.append(len(before_second))
        assert len(set(prefixes)) == 1


# ---------------------------------------------------------------------------
# Add._length
# ---------------------------------------------------------------------------
class TestAddLength:
    def test_empty_list(self):
        assert Add._length([]) == 0

    def test_single_element(self):
        assert Add._length(["hello"]) == 5

    def test_multiple_elements(self):
        assert Add._length(["hi", "hello", "hey"]) == 5

    def test_all_same_length(self):
        assert Add._length(["abc", "def", "ghi"]) == 3

    def test_empty_strings(self):
        assert Add._length(["", ""]) == 0


# ---------------------------------------------------------------------------
# Add._edit
# ---------------------------------------------------------------------------
class TestAddEdit:
    def test_all_lines_padded_to_size(self):
        lines = ["hi", "hello", "hey"]
        result = Add._edit(lines, 10)
        assert all(len(line) == 10 for line in result)

    def test_size_equals_max_length_no_change_in_longest(self):
        lines = ["hello", "hi"]
        result = Add._edit(lines, 5)
        assert result[0] == "hello"

    def test_shorter_lines_get_spaces_appended(self):
        lines = ["hi", "hello"]
        result = Add._edit(lines, 5)
        assert result[0] == "hi   "

    def test_returns_list(self):
        assert isinstance(Add._edit(["a", "bb"], 3), list)

    def test_original_list_not_mutated(self):
        original = ["abc", "de"]
        Add._edit(original, 5)
        assert original == ["abc", "de"]


# ---------------------------------------------------------------------------
# Add.MaximumSpaces exception
# ---------------------------------------------------------------------------
class TestMaximumSpacesException:
    def test_is_exception(self):
        assert issubclass(Add.MaximumSpaces, Exception)

    def test_message_contains_spaces_value(self):
        exc = Add.MaximumSpaces(42)
        assert "42" in str(exc)

    def test_can_be_raised_and_caught(self):
        with pytest.raises(Add.MaximumSpaces):
            raise Add.MaximumSpaces(10)
