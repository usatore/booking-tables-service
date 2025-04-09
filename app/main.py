from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers.tables import router as router_tables
from app.routers.reservations import router as router_reservations
from app.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Приложение запускается...")
    yield
    logger.info("Приложение завершает работу...")


app = FastAPI(lifespan=lifespan)

logger.info("Подключаем роутеры")
app.include_router(router_tables)
app.include_router(router_reservations)
