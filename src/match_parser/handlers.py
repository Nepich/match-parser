from typing import Protocol, NamedTuple

from . import services, schemas


class ParserHandlerInterface(Protocol):

    async def get_matches(self, url: str, pattern: str):
        ...


class ParserHandlerV1(NamedTuple):
    service: services.ParserServiceInterface

    async def get_matches(self, request: schemas.SearchRequest) -> schemas.MatchResponse:
        return await self.service.get_matches(str(request.url), request.pattern)
