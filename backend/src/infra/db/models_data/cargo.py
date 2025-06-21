from sqlalchemy import Column, Integer, String
from infra.db.settings.base import Base

class Cargo(Base):
    """
    Tabela que define os diferentes cargos ou perfis de acesso na aplicação.

    Exemplos: "Administrador", "Coordenador", "Professor", "Aluno", "Responsável".

    Atributos:
        id (int): Identificador único do cargo.
        nome_cargo (str): Nome do cargo, deve ser único.
    """
    __tablename__ = "cargo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_cargo = Column(String(50), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Cargo id={self.id}, nome_cargo='{self.nome_cargo}'>"
