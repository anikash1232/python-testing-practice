"""Integration tests for LinkStore with file persistence."""

import json
from pathlib import Path

import pytest

from models.link import Link
from store.json_file_io import JSONFileIO
from store.link_store import LinkStore


@pytest.fixture
def empty_store(tmp_path: Path) -> tuple[LinkStore, JSONFileIO, Path]:
    """Provide a LinkStore backed by an empty JSON file on disk."""
    file_path = tmp_path / "links.json"
    storage = JSONFileIO(data_path=file_path)
    storage.persist({})
    store = LinkStore(storage)
    return store, storage, file_path


@pytest.mark.integration
def test_link_get(tmp_path: Path) -> None:
    """Test storing and retrieving a link with file persistence."""
    data_file = tmp_path / "links_with_data.json"
    data_file.write_text('{"unc": {"slug": "unc", "target": "https://www.unc.edu"}}')
    temp_store_file_with_data = JSONFileIO(data_file)
    store = LinkStore(temp_store_file_with_data)

    retrieved = store.get("unc")

    assert retrieved is not None
    assert retrieved.slug == "unc"
    assert retrieved.target == "https://www.unc.edu"


@pytest.mark.integration
def test_link_get_new_file(tmp_path: Path) -> None:
    """Test storing and retrieving a link with file persistence."""
    temp_store_file_new = JSONFileIO(tmp_path / "links.json")
    store = LinkStore(temp_store_file_new)

    retrieved = store.get("unc")

    assert retrieved is None


@pytest.mark.integration
def test_list_with_empty_and_non_empty_initial_files(
    empty_store: tuple[LinkStore, JSONFileIO, Path],
) -> None:
    """Verify list() returns empty for an empty store and returns stored items."""
    store, storage, file_path = empty_store

    first_list = store.list()
    assert first_list == {}

    sample = {"example": {"slug": "example", "target": "http://example.local/test"}}
    storage.persist(sample)

    store = LinkStore(JSONFileIO(data_path=file_path))
    second_list = store.list()
    assert "example" in second_list
    assert second_list["example"].target == "http://example.local/test"


@pytest.mark.integration
def test_put_persists_addition(
    empty_store: tuple[LinkStore, JSONFileIO, Path],
) -> None:
    """Verify put() adds an item and the addition is persisted to disk."""
    store, _storage, file_path = empty_store

    store.put("put-slug", Link(slug="put-slug", target="http://example.local/put-test"))

    content = json.loads(file_path.read_text(encoding="utf-8"))
    assert "put-slug" in content
    assert content["put-slug"]["target"] == "http://example.local/put-test"


@pytest.mark.integration
def test_delete_persists_deletion(
    empty_store: tuple[LinkStore, JSONFileIO, Path],
) -> None:
    """Verify delete() removes an item and the deletion is persisted to disk."""
    store, storage, file_path = empty_store
    storage.persist(
        {"del-slug": {"slug": "del-slug", "target": "http://example.local/delete-test"}}
    )
    store = LinkStore(storage)

    assert "del-slug" in json.loads(file_path.read_text(encoding="utf-8"))

    store.delete("del-slug")

    content = json.loads(file_path.read_text(encoding="utf-8"))
    assert "del-slug" not in content
