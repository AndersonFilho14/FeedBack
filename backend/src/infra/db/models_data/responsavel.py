from sqlalchemy import Column, Integer, String
from infra.db.settings.base import Base


class Responsavel(Base):
    """
    Tabela que armazena os dados dos responsáveis pelos alunos.

    Atributos:
        id (int): Identificador único do responsável.
        nome (str): Nome completo do responsável.
        cpf (str): CPF do responsável.
        parentesco (str): Grau de parentesco com o aluno (ex: "Mãe", "Pai").
    """

    __tablename__ = "responsavel"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20), nullable=True)

    def __repr__(self) -> str:
        return f"<Responsavel id={self.id}, nome='{self.nome}'>"