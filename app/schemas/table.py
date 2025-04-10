from typing import Optional

from pydantic import BaseModel, ConfigDict


class STable(BaseModel):
    name: str
    seats: int
    location: Optional[str] = "Не указано"

    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)


class STableCreate(STable):
    pass


class STableRead(STable):
    id: int
