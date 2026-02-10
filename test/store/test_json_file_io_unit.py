"""Unit tests for JSONFileIO without disk operations."""

import json
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

from store.json_file_io import JSONFileIO


def test_load_returns_none_when_file_does_not_exist() -> None:
    """Test that load returns None when the file does not exist."""
    # Arrange
    mock_path = MagicMock(spec=Path)
    mock_path.exists.return_value = False
    storage = JSONFileIO(data_path=mock_path)

    # Act
    result = storage.load()

    # Assert
    assert result is None
    mock_path.exists.assert_called_once()


def test_load_returns_data_from_file() -> None:
    """Test that load returns parsed JSON data from the file."""
    # Arrange
    mock_path = MagicMock(spec=Path)
    mock_path.exists.return_value = True
    test_data = {"key": "value", "number": 42}
    mock_file = mock_open(read_data='{"key": "value", "number": 42}')

    storage = JSONFileIO(data_path=mock_path)

    # Act
    with patch.object(mock_path, "open", mock_file):
        result = storage.load()

    # Assert
    assert result == test_data
    mock_path.exists.assert_called_once()
    mock_file.assert_called_once_with("r")


def test_persist_creates_parent_dir_and_writes_json():
    # Arrange
    mock_path = MagicMock(spec=Path)

    mock_parent = MagicMock(spec=Path)
    mock_path.parent = mock_parent

    test_data = {"key": "value", "number": 42}
    m_open = mock_open()

    storage = JSONFileIO(data_path=mock_path)

    # Act
    with patch.object(mock_path, "open", m_open):
        with patch.object(json, "dump") as mock_json_dump:
            storage.persist(test_data)

    # Asssert
    mock_parent.mkdir.assert_called_once_with(parents=True, exist_ok=True)
    m_open.assert_called_once_with("w")
    handle = m_open()
    mock_json_dump.assert_called_once_with(test_data, handle)
