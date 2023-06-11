from typing import Protocol, NoReturn, NamedTuple


class ParserRepoInterface(Protocol):

    def create_file(self, file_name: str, data: str) -> NoReturn:
        ...

    def get_file_data(self, file_name: str) -> str:
        ...


class ParserRepoV1(NamedTuple):

    def create_file(self, file_name: str, data: str) -> NoReturn:
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(data)

    def get_file_data(self, file_name: str) -> str:
        with open(file_name, 'r', encoding='utf-8') as file:
            data = file.read()
            return data
