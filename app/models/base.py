from typing import Optional
from datetime import datetime

from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.core.db import Base


class BaseModel(Base):
    __abstract__ = True
    # TODO добавить проверку > 0
    full_amount = Column(Integer, nullable=False)
    # TODO может не работать default
    # TODO добавить проверку > 0
    invested_amount = Column(Integer, nullable=False, default=0)
    fully_invested = Column(Boolean, nullable=False, default=False)
    # TODO исключить для пользователя
    create_date = Column(DateTime, index=True, default=datetime.utcnow)
    close_date = Column(DateTime, index=True, default=datetime.utcnow)
