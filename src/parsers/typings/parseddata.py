from dataclasses import dataclass, field
from datetime import datetime
from typing import Generic

from urllib3.util import Url

from .vars import Schema


@dataclass
class ParsedData(Generic[Schema]):
    url: Url
    parser: str

    data: Schema

    duration: float # Длительность парсинга
    date: datetime = field(default_factory=datetime.now)
