from typing import Optional, List

from infra import DBConnectionHandler

from infra.db.models_data import (
    Aluno as AlunoData,
    Turma as TurmaData,
)
from domain.models import Aluno


class ConsultarTurma:
    """Lida com a consulta de um único registro de professor no banco de dados."""

    def __init__(self, id_aluno: int) -> None:
        """Inicializa a classe ConsultarProfessor com o ID do professor."""
        self.__id_aluno = id_aluno

    def __consultar_no_banco(self) -> Optional[TurmaData.id]:
        """Consulta o banco de dados por um professor com o ID fornecido, retornando o objeto ProfessorData ou None."""
        with DBConnectionHandler() as session:
            retorno = (
                session.query(AlunoData)
                .filter(AlunoData.id == self.__id_aluno)
                .first()
            )
        if retorno:
            return retorno.id
        return None

    def get_id_turma(self):
        """Recupera os dados do professor, retornando o objeto ProfessorData ou None."""
        return self.__consultar_no_banco()
    

class AlunoRepository:
    """Repositório responsável por persistir e consultar dados relacionados alunos."""

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

    def listar_por_escola(self, id_escola: int) -> List[AlunoData]:
        """Retorna lista de alunos filtrados por escola."""
        with DBConnectionHandler() as session:
            alunos = session.query(AlunoData).filter(AlunoData.id_escola == id_escola).all()
            return alunos
        
    def listar_por_turma(self, id_turma: int) -> List[AlunoData]:
        """Retorna lista de alunos filtrados por turma."""
        with DBConnectionHandler() as session:
            alunos = session.query(AlunoData).filter(AlunoData.id_turma == id_turma).all()
            return alunos

    def atualizar(
        self,
        id_aluno: int,
        novo_nome: str,
        nova_idade: int,
        novas_faltas: int,
        novo_id_turma: int,
        novo_id_responsavel: int,
        novo_cpf: int
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
            aluno.cpf = novo_cpf
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
        
class ConsultaAlunoBanco:
    """Classe resonsável por fazer consultas para validar alguns atributos no banco"""

    def __init__(self, id_aluno: Optional[int] = None, cpf: Optional[int] = None) -> None:
        self.__id_aluno = id_aluno
        self.__cpf = cpf
    
    def buscar_por_cpf(self) -> Optional[AlunoData]:
        """Busca um aluno pelo CPF. Retorna o objeto AlunoData se encontrado, senão None."""
        with DBConnectionHandler() as session:
            return session.query(AlunoData).filter_by(cpf=self.__cpf).first()
        
    def buscar_por_cpf_e_id(self) -> bool:
        """Verifica se o CPF já está cadastrado em outro professor com ID diferente, e retorna um booleano com base nisso.."""
        with DBConnectionHandler() as session:
            aluno = session.query(AlunoData).filter_by(cpf=self.__cpf).first()
            return aluno is not None and aluno.id != self.__id_aluno