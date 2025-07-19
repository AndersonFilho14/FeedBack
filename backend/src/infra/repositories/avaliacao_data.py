from typing import List
from infra import DBConnectionHandler
from infra.db.models_data import Avaliacao, Aluno

class AvaliacaoRepository:

    def buscar_todas(self) -> List[Avaliacao]:
        """Retorna todas as avaliações do banco."""
        with DBConnectionHandler() as session:
            return session.query(Avaliacao).all()

    def buscar_por_aluno(self, id_aluno: int) -> List[Avaliacao]:
        """Retorna todas as avaliações de um aluno específico."""
        with DBConnectionHandler() as session:
            return (session.query(Avaliacao).filter(Avaliacao.id_aluno == id_aluno).all())

    def buscar_por_turma(self, id_turma: int) -> List[Avaliacao]:
        """Retorna todas as avaliações de uma turma específica."""
        with DBConnectionHandler() as session:
            return (session.query(Avaliacao).filter(Avaliacao.id_turma == id_turma).all() )

    def buscar_por_escola(self, id_escola: int) -> List[Avaliacao]:
        """Retorna todas as avaliações de uma escola específica via join com aluno."""
        with DBConnectionHandler() as session:
            return (session.query(Avaliacao).join(Aluno, Avaliacao.id_aluno == Aluno.id).filter(Aluno.id_escola == id_escola).all())

    def buscar_por_materia(self, id_materia: int) -> List[Avaliacao]:
        """Retorna todas as avaliações de uma disciplina específica."""
        with DBConnectionHandler() as session:
            return (session.query(Avaliacao).filter(Avaliacao.id_materia == id_materia).all())