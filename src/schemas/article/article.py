from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from ..base import BaseSchema
from .author import AuthorSchema


@dataclass
class ArticleSchema(BaseSchema):
    title: str
    description: str

    id_: UUID | None = None
    pub_date: datetime | None = None
    summary: str | None = None
    authors: list[AuthorSchema] | None = None
