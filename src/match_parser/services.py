import asyncio
from queue import Queue
from typing import Protocol, NamedTuple

import httpx
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from fake_useragent import UserAgent

import concurrent.futures


# from . import repos


class ParserServiceInterface(Protocol):

    # Логика для сохранения файла на сервер
    # def create_file(self, file_name: str, data: str) -> NoReturn:
    #     ...
    #
    # def get_file_data(self, file_name: str) -> str:
    #     ...

    async def get_matches(self, url: str, pattern: str):
        ...

    def _parse_page(self, url: str, pattern: str):
        ...

    @staticmethod
    def _get_page_data(url: str) -> str:
        ...

    @staticmethod
    def _find_matches(soup: BeautifulSoup, pattern: str) -> ResultSet:
        ...

    def _reformat_page(self, soup: BeautifulSoup, pattern: str) -> dict:
        ...


class ParserServiceV1(NamedTuple):
    # repo будет необходим в случае записи файла на сервер
    # repo: repos.ParserRepoInterface

    # def create_file(self, file_name: str, data: str) -> NoReturn:
    #     ...
    #
    # def get_file_data(self, file_name: str) -> str:
    #     ...
    queue: Queue = Queue()

    async def get_matches(self, url: str, pattern: str):
        loop = asyncio.get_running_loop()
        executor = concurrent.futures.ThreadPoolExecutor()
        future = loop.run_in_executor(executor, self._parse_page, url, pattern)
        return await future

    def _parse_page(self, url: str, pattern: str):
        page = self._get_page_data(url)
        soup = BeautifulSoup(page, 'lxml')
        data = self._reformat_page(soup, pattern)
        response = {'url': url} | data
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
        return soup.find_all(string=lambda text: text and pattern in text)

    def _reformat_page(self, soup: BeautifulSoup, pattern: str) -> dict:
        results = self._find_matches(soup, pattern)
        new_pattern = f'<mark>{pattern}</mark>'
        data = {}
        match_count = 0
        for result in results:
            parent = result.find_parent()
            text = str(parent)
            while not any(parent.get_attribute_list('id')):
                parent = parent.find_parent()
            class_ids = parent.get_attribute_list('id')
            data[match_count] = {
                'search_block': text,
                'text_to_replace': text.replace(pattern, new_pattern)
            }
        return data
