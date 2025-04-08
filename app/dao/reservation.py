from app.dao.base import BaseDAO
from app.models.reservation import Reservation


class ReservationDAO(BaseDAO):
    model = Reservation