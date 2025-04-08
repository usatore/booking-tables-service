from sqlalchemy import BigInteger, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Table(Base):
    __tablename__ = "table"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    seats = Column(Integer, nullable=False)
    location = Column(String, nullable=False)

    reservations = relationship("Reservation", back_populates="table")
