from fastapi import APIRouter
from app.dao.table import TableDAO
from app.schemas.table import STable
from fastapi import status

router = APIRouter(prefix="/tables", tags=["Столики"])


@router.get("", response_model=list[STable], status_code=status.HTTP_200_OK)
async def get_all_tables():
    return await TableDAO.find_all()


@router.post("", response_model=STable, status_code=status.HTTP_201_CREATED)
async def create_new_table():
    pass


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table(id: int):
    await TableDAO.delete(id=id)
