from sqlalchemy import Column, String, Text

from base import BaseModel


class CharityProject(BaseModel):
    name = Column(String(100), unique=True, nullable=False)
    # TODO добавить проверку на длину не менее 1
    description = Column(Text, nullable=False)
