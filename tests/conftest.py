"""Shared fixtures for the pybeaut test suite."""
import re
import pytest
from unittest.mock import MagicMock, patch

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def strip_ansi(text: str) -> str:
    """Remove all ANSI escape color codes from *text*."""
    return _ANSI_RE.sub("", text)


@pytest.fixture
def terminal_80x24():
    """Mock terminal size of 80 columns x 24 lines."""
    mock_size = MagicMock()
    mock_size.columns = 80
    mock_size.lines = 24
    with patch("pybeaut._terminal_size", return_value=mock_size):
        yield mock_size


@pytest.fixture
def terminal_120x40():
    """Mock a wider terminal for edge-case centering tests."""
    mock_size = MagicMock()
    mock_size.columns = 120
    mock_size.lines = 40
    with patch("pybeaut._terminal_size", return_value=mock_size):
        yield mock_size


@pytest.fixture
def no_system():
    """Suppress all os.system calls and capture the invocations."""
    with patch("pybeaut._system", return_value=0) as mock:
        yield mock


@pytest.fixture
def no_sleep():
    """Suppress time.sleep calls so animation tests finish instantly."""
    with patch("pybeaut._sleep") as mock:
        yield mock


@pytest.fixture
def capture_stdout(capsys):
    """Thin wrapper that yields capsys for stdout/stderr capture."""
    yield capsys
