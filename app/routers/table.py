from fastapi import APIRouter

router = APIRouter(
    prefix='/tables',
    tags=['Столики']
)

@router.get('')
async def get_all_tables():
    pass

@router.post('')
async def create_new_table():
    pass

@router.delete('/{id}')
async def delete_table(id: int):
    pass
