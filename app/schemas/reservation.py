from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.table import STableRead


class SReservation(BaseModel):
    customer_name: str
    reservation_time: datetime
    duration_minutes: int

    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)


class SReservationCreate(SReservation):
    table_id: int


class SReservationRead(SReservation):
    id: int
    table: STableRead
