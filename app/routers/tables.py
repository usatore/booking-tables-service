from fastapi import APIRouter
from app.dao.table import TableDAO

router = APIRouter(
    prefix='/tables',
    tags=['Столики']
)

@router.get('')
async def get_all_tables():
    return await TableDAO.find_all()

@router.post('')
async def create_new_table():
    pass

@router.delete('/{id}')
async def delete_table(id: int):
    pass
