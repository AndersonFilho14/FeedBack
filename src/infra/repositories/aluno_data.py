from typing import List, Dict
from infra import DBConnectionHandler
from infra.db.models_data import Aluno as AlunoData
from domain.models import Aluno


class AlunoRepository:
    """Repositório responsável por persistir e consultar alunos."""

    def criar(self, aluno: Aluno) -> None:
        """Insere um novo aluno no banco."""
        aluno_orm = AlunoData(
            nome = aluno.nome,
            cpf = aluno.cpf,
            idade = aluno.idade,
            faltas = aluno.faltas,
            nota_score_preditivo = aluno.nota_score_preditivo,
            id_escola = aluno.id_escola,
            id_turma = aluno.id_turma,
            id_responsavel = aluno.id_responsavel,
        )
        with DBConnectionHandler() as session:
            session.add(aluno_orm)
            session.commit()

    def listar_por_escola(self, id_escola: int) -> List[Dict]:
        """Retorna lista de alunos filtrados por escola."""
        with DBConnectionHandler() as session:
            alunos = (
                session.query(AlunoData)
                .filter(AlunoData.id_escola == id_escola)
                .all()
            )
            return [
                {
                    "id": a.id,
                    "nome": a.nome,
                    "cpf": a.cpf,
                    "idade": a.idade,
                    "faltas": a.faltas,
                    "nota_score_preditivo": a.nota_score_preditivo,
                    "id_escola": a.id_escola,
                    "id_turma": a.id_turma,
                    "id_responsavel": a.id_responsavel,
                }
                for a in alunos
            ]

    def atualizar(
        self,
        id_aluno: int,
        novo_nome: str,
        nova_idade: int,
        novas_faltas: int,
        novo_id_turma: int,
        novo_id_responsavel: int,
    ) -> bool:
        """Atualiza os dados do aluno com base no ID. Retorna True se atualizado, False se não encontrado."""
        with DBConnectionHandler() as session:
            aluno = (
                session.query(AlunoData)
                .filter(AlunoData.id == id_aluno)
                .first()
            )
            if not aluno:
                return False

            aluno.nome = novo_nome
            aluno.idade = nova_idade
            aluno.faltas = novas_faltas
            aluno.id_turma = novo_id_turma
            aluno.id_responsavel = novo_id_responsavel
            session.commit()
            return True

    def deletar(self, id_aluno: int) -> bool:
        """Deleta o aluno pelo id. Retorna True se deletado, False se não encontrado."""
        with DBConnectionHandler() as session:
            aluno = (
                session.query(AlunoData)
                .filter(AlunoData.id == id_aluno)
                .first()
            )
            if not aluno:
                return False
            session.delete(aluno)
            session.commit()
            return True
