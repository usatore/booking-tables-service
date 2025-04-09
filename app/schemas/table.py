from pydantic import BaseModel
from typing import Optional


class STable(BaseModel):
    name: str
    seats: int
    location: Optional[str] = "Не указано"

    class Config:
        from_attributes = True


class STableCreate(STable):
    pass

class STableRead(STable):
    id: int


