from sqlalchemy import Column, String, Integer, ForeignKey
from infra.db.settings.base import Base

class Cargo(Base):
    __tablename__ = "cargo"

    id = Column(Integer, primary_key= True, autoincrement= True)
    cargo = Column(String)
    
    def __repr__(self) -> str:
        return f"\Cargo [id={self.id}, cargo={self.cargo} ]"
