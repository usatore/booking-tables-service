from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers.tables import router as router_tables
from app.routers.reservations import router as router_reservations


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app=FastAPI(lifespan=lifespan)

app.include_router(router_tables)
app.include_router(router_reservations)