from fastapi import APIRouter, status
from app.dao.reservation import ReservationDAO
from app.schemas.reservation import SReservationCreate, SReservationRead
from app.exceptions import ReservationNotFound
from app.logger import logger

router = APIRouter(prefix="/reservations", tags=["Брони"])

@router.get("/", response_model=list[SReservationRead], status_code=status.HTTP_200_OK)
async def get_all_reservations():
    logger.info("Запрос на получение всех бронирований.")
    reservations = await ReservationDAO.find_all()
    logger.info(f"Найдено {len(reservations)} бронирований.")
    return reservations

@router.post("/", response_model=SReservationRead, status_code=status.HTTP_201_CREATED)
async def create_new_reservation(reservation_data: SReservationCreate):
    logger.info(f"Запрос на создание брони для клиента {reservation_data.customer_name}, столик ID: {reservation_data.table_id}.")
    try:
        new_reservation = await ReservationDAO.add(
            customer_name=reservation_data.customer_name,
            table_id=reservation_data.table_id,
            reservation_time=reservation_data.reservation_time,
            duration_minutes=reservation_data.duration_minutes,
        )
        logger.info(f"Бронь успешно создана для клиента {reservation_data.customer_name}, столик ID: {reservation_data.table_id}.")
        return new_reservation
    except Exception as e:
        logger.error(f"Ошибка при создании брони для клиента {reservation_data.customer_name}: {str(e)}")
        raise e

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(id: int):
    logger.info(f"Запрос на удаление брони с ID {id}.")
    result = await ReservationDAO.delete(id=id)
    if not result:
        logger.error(f"Бронь с ID {id} не найдена для удаления.")
        raise ReservationNotFound
    logger.info(f"Бронь с ID {id} успешно удалена.")
    return {"message": "Бронь успешно удалена"}
