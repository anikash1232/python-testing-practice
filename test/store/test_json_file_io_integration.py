"""Integration tests for JSONFileIO with actual file operations."""

from pathlib import Path

import pytest

from store.json_file_io import JSONFileIO

# === TESTS ===


@pytest.mark.integration
def test_load_returns_none_for_nonexistent_file(tmp_path: Path) -> None:
    """Test that load returns None when the file doesn't exist."""
    # Arrange
    temp_storage_file_new = tmp_path / "storage.json"
    storage = JSONFileIO(temp_storage_file_new)

    # Act
    result = storage.load()

    # Assert
    assert result is None


@pytest.mark.integration
def test_load_returns_data_from_existing_file(tmp_path: Path) -> None:
    """Test that load correctly reads and parses data from an existing file."""
    # Arrange
    temp_storage_file_with_data = tmp_path / "storage_with_data.json"
    temp_storage_file_with_data.write_text('{"test": "data", "number": 42}')
    storage = JSONFileIO(temp_storage_file_with_data)

    # Act
    result = storage.load()

    # Assert
    assert result == {"test": "data", "number": 42}


@pytest.mark.integration
def test_load_returns_empty_dict_from_empty_file(tmp_path: Path) -> None:
    """Test that load correctly reads an empty JSON file."""
    # Arrange
    temp_storage_file_empty = tmp_path / "storage_empty.json"
    temp_storage_file_empty.write_text("{}")
    storage = JSONFileIO(temp_storage_file_empty)

    # Act
    result = storage.load()

    # Assert
    assert result == {}
