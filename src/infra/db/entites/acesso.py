from sqlalchemy import Column, String, Integer, ForeignKey
from infra.db.settings.base import Base

class Acesso(Base):
    __tablename__ = "acesso"

    id = Column(Integer, primary_key= True, autoincrement= True)
    user = Column(String, nullable=True)
    senha = Column(String, nullable=True)
    
    cargo = Column(Integer, ForeignKey('cargo.id'))
    professor_id = Column(Integer, ForeignKey('professor.id'))

    def __repr__(self) -> str:
        return f"\nAcesso [id={self.id}, user={self.user} ]"
