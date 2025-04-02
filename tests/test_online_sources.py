from unittest.mock import Mock, patch

import pytest
import requests

from cmdhelper.online_sources import OnlineSourceHandler


@pytest.fixture
def online_handler():
    return OnlineSourceHandler()


@pytest.fixture
def mock_response():
    response = Mock()
    response.text = """
# ls
> List directory contents.

- List files and directories in the current directory:
  ls

- List files and directories including hidden ones:
  ls -a

- List with sizes in human-readable format:
  ls -lh
"""
    response.raise_for_status = Mock()
    return response


def test_init_handler():
    """Test handler initialization"""
    handler = OnlineSourceHandler()
    assert handler.timeout == 5
    assert "tldr-pages" in handler.tldr_url


@patch("requests.get")
def test_successful_tldr_fetch(mock_get, online_handler, mock_response):
    """Test successful TLDR page fetch"""
    mock_get.return_value = mock_response

    with patch("rich.console.Console.print") as mock_print:
        online_handler._show_tldr("ls")
        mock_get.assert_called_once()
        mock_print.assert_called_once()


@patch("requests.get")
def test_failed_tldr_fetch(mock_get, online_handler):
    """Test TLDR fetch failure"""
    mock_get.side_effect = requests.RequestException("Network error")

    with patch("rich.console.Console.print") as mock_print:
        online_handler._show_tldr("nonexistent")
        mock_print.assert_called_with("[red]Failed to fetch from TLDR: Network error[/red]")


@patch("rich.prompt.Confirm.ask")
def test_show_online_help_confirmed(mock_ask, online_handler):
    """Test user confirms showing online help"""
    mock_ask.return_value = True

    with patch.object(online_handler, "_show_tldr") as mock_show:
        online_handler.show_online_help("ls")
        mock_show.assert_called_once_with("ls")


@patch("rich.prompt.Confirm.ask")
def test_show_online_help_declined(mock_ask, online_handler):
    """Test user declines showing online help"""
    mock_ask.return_value = False

    with patch.object(online_handler, "_show_tldr") as mock_show:
        online_handler.show_online_help("ls")
        mock_show.assert_not_called()
