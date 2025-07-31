from sqlalchemy import Column, Integer, String, ForeignKey
from infra.db.settings.base import Base


class Turma(Base):
    """
    Tabela que armazena os dados das turmas.

    Atributos:
        id (int): Identificador único da turma.
        nome (str): Nome ou identificação da turma (ex: "3º Ano A").
        ano_letivo (int): Ano letivo da turma.
        id_escola (int): Chave estrangeira para a tabela Escola.
    """

    __tablename__ = "turma"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    ano_letivo = Column(Integer, nullable=False)
    id_escola = Column(Integer, ForeignKey("escola.id"), nullable=False)

    def __repr__(self) -> str:
        return f"<Turma id={self.id}, nome='{self.nome}', ano={self.ano_letivo}>"
