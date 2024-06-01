from datetime import datetime

from pydantic import BaseModel, HttpUrl


class ShortKeyDto(BaseModel):
    shorten_key: str
    expire_at: datetime


class ShortCountDto(BaseModel):
    shorten_key: str
    count: int
    expire_at: datetime


class OriginalUrlDto(BaseModel):
    original_url: HttpUrl
