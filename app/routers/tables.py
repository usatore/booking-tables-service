from fastapi import APIRouter
from app.dao.table import TableDAO
from app.schemas.table import STableCreate, STableRead
from fastapi import status
from app.exceptions import TableNotFound
from app.logger import logger

router = APIRouter(prefix="/tables", tags=["Столики"])

@router.get("", response_model=list[STableRead], status_code=status.HTTP_200_OK)
async def get_all_tables():
    logger.info("Запрос на получение всех столиков.")
    tables = await TableDAO.find_all()
    logger.info(f"Найдено {len(tables)} столиков.")
    return tables

@router.post("", response_model=STableRead, status_code=status.HTTP_201_CREATED)
async def create_new_table(table_data: STableCreate):
    logger.info(f"Запрос на создание столика с именем {table_data.name}, количество мест: {table_data.seats}, локация: {table_data.location}.")
    try:
        new_table = await TableDAO.add(
            name=table_data.name,
            seats=table_data.seats,
            location=table_data.location,
        )
        logger.info(f"Столик с именем {table_data.name} успешно создан.")
        return new_table
    except Exception as e:
        logger.error(f"Ошибка при создании столика {table_data.name}: {str(e)}")
        raise e

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table(id: int):
    logger.info(f"Запрос на удаление столика с ID {id}.")
    result = await TableDAO.delete(id=id)
    if not result:
        logger.error(f"Столик с ID {id} не найден для удаления.")
        raise TableNotFound
    logger.info(f"Столик с ID {id} успешно удален.")
    return {"message": "Столик успешно удален"}
