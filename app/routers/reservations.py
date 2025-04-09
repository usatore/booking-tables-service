from fastapi import APIRouter, status
from app.dao.reservation import ReservationDAO
from app.schemas.reservation import SReservationCreate, SReservationRead
from app.exceptions import ReservationNotFound

router = APIRouter(prefix="/reservations", tags=["Брони"])


@router.get("/", response_model=list[SReservationRead], status_code=status.HTTP_200_OK)
async def get_all_reservations():
    reservations = await ReservationDAO.find_all()
    return reservations


@router.post("/", response_model=SReservationRead, status_code=status.HTTP_201_CREATED)
async def create_new_reservation(reservation_data: SReservationCreate):
    return await ReservationDAO.add(
        customer_name=reservation_data.customer_name,
        table_id=reservation_data.table_id,
        reservation_time=reservation_data.reservation_time,
        duration_minutes=reservation_data.duration_minutes,
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(id: int):
    result = await ReservationDAO.delete(id=id)
    if not result:
        raise ReservationNotFound
    return {"message": "Бронь успешно удалена"}
