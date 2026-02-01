"""Integration tests for LinkStore with file persistence."""

from pathlib import Path

import pytest

from store.json_file_io import JSONFileIO
from store.link_store import LinkStore

# === TESTS ===


@pytest.mark.integration
def test_link_get(tmp_path: Path) -> None:
    """Test storing and retrieving a link with file persistence."""
    # Arrange
    data_file = tmp_path / "links_with_data.json"
    data_file.write_text('{"unc": {"slug": "unc", "target": "https://www.unc.edu"}}')
    temp_store_file_with_data = JSONFileIO(data_file)
    store = LinkStore(temp_store_file_with_data)

    # Act
    retrieved = store.get("unc")

    # Assert
    assert retrieved is not None
    assert retrieved.slug == "unc"
    assert retrieved.target == "https://www.unc.edu"


@pytest.mark.integration
def test_link_get_new_file(tmp_path: Path) -> None:
    """Test storing and retrieving a link with file persistence."""
    # Arrange
    temp_store_file_new = JSONFileIO(tmp_path / "links.json")
    store = LinkStore(temp_store_file_new)

    # Act
    retrieved = store.get("unc")

    # Assert
    assert retrieved is None
