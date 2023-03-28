from abc import ABC, abstractmethod
from io import BytesIO
from time import time

import requests
from requests import Response
from requests.exceptions import HTTPError
from urllib3.util import Url, parse_url

from src.parsers.typings import ParsedData


class AbstractParser(ABC):
    @abstractmethod
    def parse(self, url: str) -> ParsedData:
        pass


class BaseParser(AbstractParser):
    MAX_SECONDARY_IMAGES_COUNT: int = 5

    _path_prefix: str = ""
    _headers: dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0",
    }

    domain: str = ""

    def parse(self, url: str) -> ParsedData:
        _url: Url = parse_url(url)

        try:
            start_time = time()

            page: str = self.__get_page(_url)
            data = self._extract_data(page)

            duration = time() - start_time
        except HTTPError:
            # Произошла ошибка получения страницы
            data = None
            duration = 0.0

        return ParsedData(
            url=_url, parser=self.__class__.__name__, data=data, duration=duration
        )

    def _get_request(self, url: Url) -> Response:
        response = requests.get(url.url, headers=self._headers)

        if response.status_code != 200:
            raise HTTPError

        return response

    def _get_image_raw(self, url: Url) -> BytesIO:
        response = self._get_request(url)

        return BytesIO(initial_bytes=response.content)

    def __get_page(self, url: Url) -> str:
        """Возвращает HTML-код страницы"""

        response = self._get_request(url)

        return response.text

    def _extract_data(self, page: str):
        """
        Метод, обрабатывающий контент со страницы
        """
        
        raise NotImplementedError
