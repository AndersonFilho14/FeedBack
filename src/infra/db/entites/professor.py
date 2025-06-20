from sqlalchemy import Column, String, Integer

from infra.db.settings.base import Base

class Professor(Base):
    __tablename__ = "professor"

    id = Column(Integer, primary_key= True, autoincrement= True)
    nome = Column(String(100), )
