from sqlalchemy import Column, Integer, String, ForeignKey
from infra.db.settings.base import Base


class Escola(Base):
    """
    Tabela que armazena os dados das escolas.

    Atributos:
        id (int): Identificador único da escola.
        nome (str): Nome da escola.
        id_municipio (int): Chave estrangeira para a tabela Municipio.
    """

    __tablename__ = "escola"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(150), nullable=False)
    id_municipio = Column(Integer, ForeignKey("municipio.id"), nullable=False)

    def __repr__(self) -> str:
        return f"<Escola id={self.id}, nome='{self.nome}'>"
