from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Table(Base):
    __tablename__ = "table"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    seats = Column(Integer, nullable=False)
    location = Column(String, nullable=True)

    reservations = relationship(
        "Reservation", back_populates="table", cascade="all, delete-orphan"
    )
