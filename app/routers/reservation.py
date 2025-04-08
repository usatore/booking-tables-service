from fastapi import APIRouter

router = APIRouter(
    prefix='/reservations',
    tags=['Брони']
)

@router.get('')
async def get_all_reservations():
    pass

@router.post('')
async def create_new_reservation():
    pass

@router.delete('/{id}')
async def delete_reservation(id: int):
    pass
