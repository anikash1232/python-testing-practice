"""Pydantic model for shortened links."""

from typing import Annotated

from pydantic import BaseModel, Field


class Link(BaseModel):
    """Represents a shortened link.

    Attributes:
        slug: Short identifier for the link.
        target: Destination URL for the link.
    """

    slug: Annotated[str, Field(frozen=True, min_length=3)]
    target: Annotated[str, Field(frozen=True, min_length=8)]
