from sqlalchemy import Column, Integer, String
from infra.db.settings.base import Base


class Municipio(Base):
    """
    Tabela que armazena os dados dos municípios.

    Atributos:
        id (int): Identificador único do município.
        nome (str): Nome do município.
        regiao (str): Região onde o município está localizado (ex: "Nordeste").
        estado (str): Estado ao qual o município pertence (ex: "Pernambuco").
    """

    __tablename__ = "municipio"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    regiao = Column(String(50), nullable=True)
    estado = Column(String(50), nullable=False)

    def __repr__(self) -> str:
        return f"<Municipio id={self.id}, nome='{self.nome}'>"
