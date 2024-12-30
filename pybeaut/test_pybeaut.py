import pytest
from . import Colors, Colorate, Center, Add, Banner



@pytest.mark.parametrize("text,color", [
    ("Hello", Colors.red),
    ("World", Colors.green),
], ids=["red_text", "green_text"])
def test_colorate_color(text, color):
    # Act
    result = Colorate.Color(color, text)
    # Assert
    assert isinstance(result, str)
    assert len(result) > len(text)

@pytest.mark.parametrize("text,color,mode", [
    ("Test", Colors.red_to_green, Colorate.Vertical),
    ("Pybeaut", Colors.blue_to_red, Colorate.Horizontal),
], ids=["vertical_gradient", "horizontal_gradient"])
def test_colorate_gradient(text, color, mode):
    # Act
    result = mode(color, text)
    # Assert
    assert isinstance(result, str)
    assert len(result) > len(text)

@pytest.mark.parametrize("text,align", [
    ("Centered", Center.center),
    ("Left Aligned", Center.left),
    ("Right Aligned", Center.right),
], ids=["center_align", "left_align", "right_align"])
def test_center_group_align(text, align):
    # Act
    result = Center.GroupAlign(text, align)
    # Assert
    assert isinstance(result, str)
    assert len(result.splitlines()) > 0

@pytest.mark.parametrize("banner1,banner2,spaces", [
    ("Header", "Content", 1),
    ("Title", "Subtitle", 0),
], ids=["with_spaces", "no_spaces"])
def test_add_banners(banner1, banner2, spaces):
    # Act
    result = Add.Add(banner1, banner2, spaces)
    # Assert
    assert isinstance(result, str)
    assert len(result.splitlines()) > 0

@pytest.mark.parametrize("content,box_type", [
    ("Test", Banner.SimpleCube),
    ("Pybeaut", Banner.DoubleCube),
], ids=["simple_cube", "double_cube"])
def test_banner_cube(content, box_type):
    # Act
    result = box_type(content)
    # Assert
    assert isinstance(result, str)
    assert len(result.splitlines()) > 0
