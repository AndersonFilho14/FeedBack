from sqlalchemy import Column, String, Integer

from infra.db.settings.base import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key= True, autoincrement= True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)

    def __repr__(self) -> str:
        return f"\nUsers [id={self.id}, first_name={self.first_name} ]"
