from sqlalchemy import select, delete
from app.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def delete(cls, id: int):
        async with async_session_maker() as session:
            # Находим объект по ID
            query = select(cls.model).where(cls.model.id == id)
            result = await session.execute(query)
            obj = result.scalar_one_or_none()
            if obj is None:
                return None  # Или выбросить исключение, если нужно
            # Удаляем объект через ORM
            await session.delete(obj)
            await session.commit()
            return {"message": f"Deleted {cls.model.__name__} with id {id}"}

    """
    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()
    """
