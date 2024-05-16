from typing import Optional
from datetime import datetime

from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.core.db import Base


class BaseModel(Base):
    __abstract__ = True
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False, default=0)
    fully_invested = Column(Boolean, nullable=False, default=False)
    # TODO Убедитесь, что в поле create_date у вновь создаваемых объектов
    #  записываются разные значения даты и времени.
    #  в параметр default нужно передавать не результат вызова функции,
    #  а саму функцию.
    create_date = Column(DateTime, index=True, default=datetime.utcnow)
    close_date = Column(DateTime, index=True)
