from bs4 import BeautifulSoup
from pydantic import BaseModel, HttpUrl


class SearchRequest(BaseModel):
    url: HttpUrl
    pattern: str


class Match(BaseModel):
    search_block: str
    text_to_replace: str


class MatchResponse(BaseModel):
    page: str
    matches: list[Match]
