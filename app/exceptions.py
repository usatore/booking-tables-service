from fastapi import HTTPException, status


class AppException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class TableAlreadyExist(AppException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Столик с этим именем уже существует"


class TableNotFound(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Столик не найден"


class TableAlreadyReserved(AppException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Столик уже занят в это время"


class ReservationNotFound(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Бронь не найдена"


class DurationNotPositive(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Продолжительность брони должна быть больше, чем 0 минут"
