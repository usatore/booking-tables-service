from datetime import datetime, timedelta

from sqlalchemy import select

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.exceptions import DurationNotPositive, TableAlreadyReserved, TableNotFound
from app.logger import logger
from app.models.reservation import Reservation
from app.models.table import Table


class ReservationDAO(BaseDAO):
    model = Reservation

    @classmethod
    async def add(
        cls,
        customer_name: str,
        table_id: int,
        reservation_time: datetime,
        duration_minutes: int,
    ):
        logger.info(
            f"Попытка добавить новую бронь для клиента '{customer_name}', столик {table_id}, время {reservation_time}."
        )

        if duration_minutes <= 0:
            logger.error(f"Некорректная длительность брони: {duration_minutes} минут.")
            raise DurationNotPositive

        async with async_session_maker() as session:
            # Проверка, что столик существует
            table_query = select(Table).where(Table.id == table_id)
            result = await session.execute(table_query)
            table = result.scalar_one_or_none()

            if not table:
                logger.error(f"Столик с ID {table_id} не найден.")
                raise TableNotFound
            logger.info(f"Столик с ID {table_id} найден, продолжение обработки брони.")

            reservation_end = reservation_time + timedelta(minutes=duration_minutes)

            # Получаем все брони на тот же столик
            existing_query = select(cls.model).where(cls.model.table_id == table_id)
            existing_result = await session.execute(existing_query)
            existing_reservations = existing_result.scalars().all()

            # Проверяем пересечения по времени
            for res in existing_reservations:
                res_end = res.reservation_time + timedelta(minutes=res.duration_minutes)
                if (
                    reservation_time < res_end
                    and reservation_end > res.reservation_time
                ):
                    logger.error(
                        f"Столик {table_id} уже забронирован на время с {res.reservation_time} по {res_end}."
                    )
                    raise TableAlreadyReserved

            # Если всё ок — добавляем
            new_reservation = cls.model(
                customer_name=customer_name,
                table_id=table_id,
                reservation_time=reservation_time,
                duration_minutes=duration_minutes,
            )

            session.add(new_reservation)
            await session.commit()
            await session.refresh(new_reservation)
            logger.info(
                f"Бронь для клиента '{customer_name}' на столик {table_id} успешно создана."
            )
            return new_reservation
