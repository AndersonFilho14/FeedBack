from sqlalchemy import Column, Integer, String
from infra.db.settings.base import Base


class Disciplina(Base):
    """
    Tabela que define as disciplinas oferecidas no sistema educacional.

    Atributos:
        id (int): Identificador único da disciplina.
        nome_disciplina (str): Nome da disciplina (ex: "Matemática", "Português").
    """

    __tablename__ = "disciplina"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_disciplina = Column(String(100), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Disciplina id={self.id}, nome='{self.nome_disciplina}'>"
