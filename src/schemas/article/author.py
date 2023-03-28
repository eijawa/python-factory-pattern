from dataclasses import dataclass
from uuid import UUID

from ..base import BaseSchema


@dataclass
class AuthorSchema(BaseSchema):
    first_name: str
    last_name: str

    id_: UUID | None = None
