from pydantic import BaseModel, HttpUrl


class Match(BaseModel):
    url: HttpUrl
    pattern: str


class MatchResponse(BaseModel):
    url: HttpUrl
    matches: list[dict]
