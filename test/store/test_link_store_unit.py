"""Unit tests for LinkStore without disk operations."""

from unittest.mock import MagicMock

from store.json_file_io import JSONFileIO
from store.link_store import LinkStore


def test_get_returns_link_when_slug_exists() -> None:
    """Test that get returns the correct link for an existing slug."""

    # Arrange
    mock_storage = MagicMock(spec=JSONFileIO)
    mock_storage.load.return_value = {
        "example": {"slug": "example", "target": "https://example.com"},
        "github": {"slug": "github", "target": "https://github.com"},
    }

    # Act
    store = LinkStore(storage=mock_storage)
    result = store.get("example")

    # Assert
    assert result is not None
    assert result.slug == "example"
    assert result.target == "https://example.com"
    mock_storage.load.assert_called_once()


def test_get_returns_none_when_slug_not_found() -> None:
    """Test that get returns None for a non-existent slug."""

    # Arrange
    mock_storage = MagicMock(spec=JSONFileIO)
    mock_storage.load.return_value = None

    # Act
    store = LinkStore(storage=mock_storage)
    result = store.get("nonexistent")

    # Assert
    assert result is None
    mock_storage.load.assert_called_once()
