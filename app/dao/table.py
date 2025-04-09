from app.dao.base import BaseDAO
from sqlalchemy import select
from app.models.table import Table
from app.database import async_session_maker
from app.exceptions import TableAlreadyExist
from app.logger import logger


class TableDAO(BaseDAO):
    model = Table

    @classmethod
    async def add(cls, name: str, seats: int, location: str = None):
        logger.info(
            f"Попытка добавить новый столик с именем '{name}', местами {seats}, локация: {location or 'не указана'}.")

        async with async_session_maker() as session:
            existing_query = select(cls.model).where(cls.model.name == name)
            existing_result = await session.execute(existing_query)
            existing_table = existing_result.scalar_one_or_none()

            if existing_table:
                logger.error(f"Столик с именем '{name}' уже существует.")
                raise TableAlreadyExist
            logger.info(f"Столик с именем '{name}' не найден, продолжение создания.")

            new_table = cls.model(name=name, seats=seats, location=location)
            session.add(new_table)
            await session.commit()
            await session.refresh(new_table)

            logger.info(f"Столик с именем '{name}' успешно добавлен.")
            return new_table
