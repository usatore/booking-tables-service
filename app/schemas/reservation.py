
from datetime import datetime
from pydantic import BaseModel
from app.schemas.table import STable

class SReservation(BaseModel):
    customer_name: str
    reservation_time: datetime
    duration_minutes: int

    class Config:
        from_attributes = True

class SReservationCreate(SReservation):
    table_id: int

class SReservationRead(SReservation):
    id: int
    table: STable
