from pydantic import BaseModel
from typing import Optional


class STable(BaseModel):
    id: int
    name: str
    seats: int
    location: Optional[str] = None

    class Config:
        from_attributes = True

