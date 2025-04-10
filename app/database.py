from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings
from app.logger import logger

try:
    engine = create_async_engine(settings.DATABASE_URL)
    logger.info("Подключение к базе данных")
except Exception as e:
    logger.error(f"Ошибка при подключении к базе данных: {str(e)}")

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
