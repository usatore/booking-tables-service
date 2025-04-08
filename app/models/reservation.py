from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Reservation(Base):
    __tablename__ = "reservation"

    id = Column(Integer, primary_key=True, nullable=False)
    customer_name = Column(String, nullable=False)
    table_id = Column(ForeignKey("table.id"))
    reservation_time = Column(DateTime(timezone=True))
    duration_minutes = Column(Integer)

    table = relationship("Table", back_populates="reservation")
