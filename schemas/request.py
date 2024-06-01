from typing import Optional

from pydantic import BaseModel, HttpUrl


class CreateShortModelDto(BaseModel):
    url: HttpUrl
    expire_time: Optional[int] = 3600
