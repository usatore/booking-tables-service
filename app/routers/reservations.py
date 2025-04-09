from fastapi import APIRouter, HTTPException, status
from app.dao.reservation import ReservationDAO
from app.schemas.reservation import SReservationCreate, SReservationRead

router = APIRouter(
    prefix='/reservations',
    tags=['Брони']
)

@router.get('/', status_code=status.HTTP_200_OK)
async def get_all_reservations():
    reservations = await ReservationDAO.find_all()
    if not reservations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Брони не найдены")
    return reservations

@router.post('/', response_model=SReservationRead, status_code=status.HTTP_201_CREATED)
async def create_new_reservation(reservation_data: SReservationCreate):
    return await ReservationDAO.add(
        customer_name=reservation_data.customer_name,
        table_id=reservation_data.table_id,
        reservation_time=reservation_data.reservation_time,
        duration_minutes=reservation_data.duration_minutes,
    )

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(id: int):
    result = await ReservationDAO.delete(id=id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Бронь с id {id} не найдена")
    return {"message": "Бронь успешно удалена"}