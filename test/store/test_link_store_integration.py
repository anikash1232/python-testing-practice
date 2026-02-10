"""Integration tests for LinkStore with file persistence."""

import json
from pathlib import Path

import pytest

from models.link import Link
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


@pytest.mark.integration
def test_list_with_empty_and_non_empty_initial_files(tmp_path: Path) -> None:
    """Verify list() returns empty for an empty store and returns stored items for non-empty store."""
    file_path = tmp_path / "links.json"

    # Start with an empty store file (dict expected by LinkStore)
    storage = JSONFileIO(data_path=file_path)
    storage.persist({})

    store = LinkStore(storage)
    first_list = store.list()
    assert first_list == {}  # empty dict

    # Populate the underlying file with a single item and ensure list reflects it
    sample = {"example": {"slug": "example", "target": "http://example.local/test"}}
    storage.persist(sample)

    store = LinkStore(
        JSONFileIO(data_path=file_path)
    )  # re-open to simulate new process
    second_list = store.list()
    assert "example" in second_list
    assert second_list["example"].target == "http://example.local/test"


@pytest.mark.integration
def test_put_persists_addition(tmp_path: Path) -> None:
    """Verify put() adds an item and the addition is persisted to disk."""
    file_path = tmp_path / "links.json"
    storage = JSONFileIO(data_path=file_path)
    storage.persist({})

    store = LinkStore(storage)
    store.put("put-slug", Link(slug="put-slug", target="http://example.local/put-test"))

    content = json.loads(file_path.read_text(encoding="utf-8"))
    assert "put-slug" in content
    assert content["put-slug"]["target"] == "http://example.local/put-test"


@pytest.mark.integration
def test_delete_persists_deletion(tmp_path: Path) -> None:
    """Verify delete() removes an item and the deletion is persisted to disk."""
    file_path = tmp_path / "links.json"
    storage = JSONFileIO(data_path=file_path)
    storage.persist(
        {"del-slug": {"slug": "del-slug", "target": "http://example.local/delete-test"}}
    )

    store = LinkStore(storage)
    # ensure present
    assert "del-slug" in json.loads(file_path.read_text(encoding="utf-8"))

    store.delete("del-slug")

    content = json.loads(file_path.read_text(encoding="utf-8"))
    assert "del-slug" not in content
