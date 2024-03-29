import asyncio
from typing import Protocol, NamedTuple

import httpx
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from fake_useragent import UserAgent

import concurrent.futures

from . import schemas  # , repos


class ParserServiceInterface(Protocol):

    # Логика для сохранения файла на сервер
    # def create_file(self, file_name: str, data: str) -> NoReturn:
    #     ...
    #
    # def get_file_data(self, file_name: str) -> str:
    #     ...

    async def get_matches(self, url: str, pattern: str):
        ...

    def _parse_page(self, url: str, pattern: str) -> schemas.MatchResponse:
        ...

    @staticmethod
    def _get_page_data(url: str) -> str:
        ...

    @staticmethod
    def _find_matches(soup: BeautifulSoup, pattern: str) -> ResultSet:
        ...

    def _reformat_page(self, soup: BeautifulSoup, pattern: str) -> list:
        ...


class ParserServiceV1(NamedTuple):
    # repo будет необходим в случае записи файла на сервер
    # repo: repos.ParserRepoInterface

    # def create_file(self, file_name: str, data: str) -> NoReturn:
    #     ...
    #
    # def get_file_data(self, file_name: str) -> str:
    #     ...

    async def get_matches(self, url: str, pattern: str):
        loop = asyncio.get_running_loop()
        executor = concurrent.futures.ThreadPoolExecutor()
        future = loop.run_in_executor(executor, self._parse_page, url, pattern)
        return await future

    def _parse_page(self, url: str, pattern: str) -> schemas.MatchResponse:
        page = self._get_page_data(url)
        soup = BeautifulSoup(page, 'lxml')
        data = self._reformat_page(soup, pattern)
        soup.
        response = schemas.MatchResponse(page=soup.decode_contents(), matches=data)
        return response

    @staticmethod
    def _get_page_data(url: str) -> str:
        try:
            useragent = UserAgent()
            headers = {
                'User-Agent': useragent.random}
            response = httpx.get(url=url, headers=headers)
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as exc:
            print(f"Error while requesting {exc.request.url!r}.")

    @staticmethod
    def _find_matches(soup: BeautifulSoup, pattern: str) -> ResultSet:
        return soup.find_all(string=lambda text: text and pattern.lower() in text.lower())

    def _reformat_page(self, soup: BeautifulSoup, pattern: str) -> list:
        results = self._find_matches(soup, pattern)
        data = []
        for result in results:
            parent = result.find_parent()
            text = str(parent)
            index_start = text.lower().find(pattern.lower())
            index_end = index_start+len(pattern)
            origin = text[index_start: index_end]
            new_pattern = f'<mark>{origin}</mark>'
            match = schemas.Match(search_block=text, text_to_replace=text.replace(origin, new_pattern))
            data.append(match)
        return data
