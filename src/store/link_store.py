"""File-backed store abstraction for shortened links."""

from typing import Optional

from models import Link
from store.json_file_io import JSONFileIO


class LinkStore:
    """Stores and retrieves shortened links using a file-based data source.

    Attributes:
        _storage: JSON file I/O backend for persistence.
        _urls: Mapping of slug to stored link.
    """

    _storage: JSONFileIO
    _urls: dict[str, Link]

    def __init__(self, storage: JSONFileIO):
        """Initialize the store.

        Args:
            storage: JSONFileIO instance for persistence.
        """
        self._storage = storage
        self._urls = self._load_data()

    def get(self, slug: str) -> Optional[Link]:
        """Return the stored link for a slug.

        Args:
            slug: Short identifier for the link.

        Returns:
            The stored link, or None if not found.
        """
        return self._urls.get(slug, None)

    def put(self, slug: str, url: Link) -> None:
        """Store or replace a link for a slug.

        Args:
            slug: Short identifier for the link.
            url: Link object to store and persist.
        """
        self._urls[slug] = url
        serialized = {key: link.model_dump() for key, link in self._urls.items()}
        self._storage.persist(serialized)

    def delete(self, slug: str) -> None:
        """Remove a stored link.

        Args:
            slug: Short identifier for the link.
        """
        self._urls.pop(slug, None)

        data = {}
        for s, link in self._urls.items():
            data[s] = link.model_dump()

        self._storage.persist(data)

    def list(self) -> dict[str, Link]:
        return self._urls.copy()

    def _load_data(self) -> dict[str, Link]:
        """Load persisted links from disk if data path exists.

        Returns:
            Dictionary mapping slug to Link, empty if no data file exists.
        """
        data = self._storage.load()
        if data is None:
            return {}

        return {slug: Link(**link_data) for slug, link_data in data.items()}
