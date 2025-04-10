from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session_maker
from app.logger import logger


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, **filter_by):
        try:
            logger.info(
                f"Поиск всех записей в {cls.model.__name__} с фильтром: {filter_by}"
            )
            async with async_session_maker() as session:
                query = select(cls.model).filter_by(**filter_by)
                result = await session.execute(query)
                records = result.scalars().all()
                logger.info(f"Найдено {len(records)} записей в {cls.model.__name__}.")
                return records
        except SQLAlchemyError as e:
            logger.error(
                f"Ошибка при выполнении запроса в {cls.model.__name__}: {str(e)}"
            )
            raise

    @classmethod
    async def delete(cls, id: int):
        try:
            logger.info(f"Попытка удалить {cls.model.__name__} с ID {id}.")
            async with async_session_maker() as session:
                # Находим объект по ID
                query = select(cls.model).where(cls.model.id == id)
                result = await session.execute(query)
                obj = result.scalar_one_or_none()

                if obj is None:
                    logger.warning(f"{cls.model.__name__} с ID {id} не найден.")
                    return None  # Или выбросить исключение, если нужно

                # Удаляем объект через ORM
                await session.delete(obj)
                await session.commit()
                logger.info(f"{cls.model.__name__} с ID {id} был успешно удален.")
                return {"message": f"Deleted {cls.model.__name__} with id {id}"}
        except SQLAlchemyError as e:
            logger.error(
                f"Ошибка при удалении {cls.model.__name__} с ID {id}: {str(e)}"
            )
            raise

    """
    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()
    """
