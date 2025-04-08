from fastapi import APIRouter
from app.dao.reservation import ReservationDAO

router = APIRouter(
    prefix='/reservations',
    tags=['Брони']
)

@router.get('')
async def get_all_reservations():
    return await ReservationDAO.find_all()

@router.post('')
async def create_new_reservation():
    pass

@router.delete('/{id}')
async def delete_reservation(id: int):
    pass
