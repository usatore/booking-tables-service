from sqlalchemy import select, and_
from fastapi import HTTPException, status
from datetime import timedelta
from app.database import async_session_maker
from datetime import datetime
from app.models.reservation import Reservation
from app.models.table import Table
from app.dao.base import BaseDAO
from sqlalchemy.orm import joinedload


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
        async with async_session_maker() as session:
            # Проверка, что столик существует
            table_query = select(Table).where(Table.id == table_id)
            result = await session.execute(table_query)
            table = result.scalar_one_or_none()

            if not table:
                raise HTTPException(
                    status_code=404, detail=f"Table with id {table_id} not found"
                )

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
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"Table {table_id} already booked from {res.reservation_time} to {res_end})",
                    )

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
            return new_reservation
