from sqlalchemy import Column, Integer, ForeignKey
from infra.db.settings.base import Base

class ProfessorTurma(Base):
    """
    Tabela de ligação para o relacionamento N:N entre Professor e Turma.
    Permite que um professor lecione em várias turmas e uma turma tenha vários professores.

    Atributos:
        id_professor (int): Chave estrangeira para a tabela Professor.
        id_turma (int): Chave estrangeira para a tabela Turma.
    """
    __tablename__ = "professor_turma"

    id_professor = Column(Integer, ForeignKey('professor.id'), primary_key=True)
    id_turma = Column(Integer, ForeignKey('turma.id'), primary_key=True)

    def __repr__(self) -> str:
        return f"<ProfessorTurma id_professor={self.id_professor}, id_turma={self.id_turma}>"
