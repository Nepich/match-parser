from pydantic import BaseModel, HttpUrl


class Match(BaseModel):
    url: HttpUrl
    pattern: str
