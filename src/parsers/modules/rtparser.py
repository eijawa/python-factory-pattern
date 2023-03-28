from datetime import datetime

from bs4 import BeautifulSoup
from devtools import debug

from src.schemas import ArticleSchema, AuthorSchema

from .base import BaseParser


class RTParser(BaseParser):
    domain = "russian.rt"

    def _extract_data(self, page: str):
        self.bs = BeautifulSoup(page, "html.parser")

        return ArticleSchema(
            title=self.__get_title(),
            description=self.__get_description(),
            pub_date=self.__get_pub_date(),
            summary=self.__get_summary(),
            authors=self.__get_authors(),
        )

    def __get_title(self) -> str:
        t = self.bs.select_one("h1.article__heading")

        if t is None:
            return ""

        return t.text

    def __get_description(self) -> str:
        t = self.bs.select_one("div.article__text")

        if t is None:
            return ""

        return t.text

    def __get_pub_date(self):
        t = self.bs.select_one("time.date")

        return datetime.fromisoformat(t["datetime"])  # type: ignore

    def __get_summary(self):
        t = self.bs.select_one("div.article__summary")

        if t is None:
            return None

        return t.text

    def __get_authors(self):
        t = self.bs.select_one("div.article__author")

        if t is None:
            return None

        authors = []
        data = [d.strip() for d in t.text.split(",")]
        for d in data:
            s = d.split(" ")

            author = AuthorSchema(first_name=s[0], last_name=s[1])
            authors.append(author)

        return authors
