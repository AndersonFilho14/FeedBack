from typing import Optional, List

from infra import DBConnectionHandler

from infra.db.models_data import (
    Aluno as AlunoData,
    Turma as TurmaData,
    Avaliacao as AvaliacaoData,
    Materia as MateriaData,
    Responsavel as ResponsavelData,
    Escola as EscolaData,
)
from domain.models import Aluno, Responsavel
from datetime import datetime


class ConsultarTurma:
    """Lida com a consulta da turma de um aluno no banco de dados."""

    def __init__(self, id_aluno: int) -> None:
        """Inicializa a classe ConsultarTurma com o ID do aluno."""
        self.__id_aluno = id_aluno

    def __consultar_no_banco(self) -> Optional[int]:
        """Consulta o banco de dados por um aluno com o ID fornecido, retornando o ID da sua turma ou None."""
        with DBConnectionHandler() as session:
            aluno = (
                session.query(AlunoData)
                .filter(AlunoData.id == self.__id_aluno)
                .first()
            )
        if aluno:
            return aluno.id_turma
        return None

    def get_id_turma(self) -> Optional[int]:
        """Recupera o ID da turma do aluno."""
        return self.__consultar_no_banco()
    

class AlunoRepository:
    """Repositório responsável por persistir e consultar dados relacionados alunos."""

    def criar(self, aluno: Aluno, responsavel: Responsavel) -> None:
        """Insere um novo aluno no banco."""
        aluno_orm = AlunoData(
            nome = aluno.nome,
            cpf = aluno.cpf,
            faltas = aluno.faltas,
            nota_score_preditivo = aluno.nota_score_preditivo,
            id_escola = aluno.id_escola,
            data_nascimento = aluno.data_nascimento,
            sexo = aluno.sexo,
            nacionalidade = aluno.nacionalidade,
            id_turma = aluno.id_turma, # Inicializado como 0, será atualizado na função de criação/edição de turmas
            id_responsavel = aluno.id_responsavel,  # Inicializado como 0, será atualizado após a inserção do responsável no banco
        )

        responsavel_orm = ResponsavelData(
            nome = responsavel.nome,
            telefone = responsavel.telefone
        )

        with DBConnectionHandler() as session:
            # Cadastra o responsável
            session.add(responsavel_orm)
            session.commit()
            session.refresh(responsavel_orm)  # garante que id está atualizado

            # Associa o id dele ao aluno e cadastra o aluno
            aluno_orm.id_responsavel = responsavel_orm.id
            session.add(aluno_orm)
            session.commit()
            session.refresh(aluno_orm)

            # Busca todas as disciplinas
            materias = session.query(MateriaData).all()

            # Para cada matéria, cria 4 avaliações para o novo aluno
            avaliacoes = []
            for materia in materias:
                for tipo in ["1Va", "2Va", "3Va", "4Va"]:
                    avaliacao = AvaliacaoData(
                        tipo_avaliacao=tipo,
                        data_avaliacao=datetime.now(),
                        nota=0.0,
                        id_aluno=aluno_orm.id,
                        id_materia = materia.id,
                        id_professor = materia.id_professor,
                    )
                    avaliacoes.append(avaliacao)

            session.add_all(avaliacoes)
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
        novo_cpf: str,
        nova_data_nascimento: str,
        novo_sexo: str,
        nova_nacionalidade: str,
        novo_nome_responsavel: str,
        novo_numero_responsavel: str,
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
            aluno.cpf = novo_cpf
            aluno.data_nascimento = nova_data_nascimento
            aluno.sexo = novo_sexo
            aluno.nacionalidade = nova_nacionalidade

            # Atualiza o responsável
            responsavel = (
                session.query(ResponsavelData)
                .filter(ResponsavelData.id == aluno.id_responsavel)
                .first()
            )
            if responsavel is not None:
                responsavel.nome = novo_nome_responsavel
                responsavel.telefone = novo_numero_responsavel
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

            # Exclui todas as avaliações associadas ao aluno
            session.query(AvaliacaoData).filter(AvaliacaoData.id_aluno == id_aluno).delete()

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
        
    def buscar_aluno_por_id(self) -> Optional[AlunoData]:
        """Busca um aluno pelo ID e Retorna o objeto AlunoData  se encontrado, senão None."""
        with DBConnectionHandler() as session:
            return session.query(AlunoData).filter_by(id = self.__id_aluno).first()
        
    def buscar_por_cpf_e_id(self) -> bool:
        """Verifica se o CPF já está cadastrado em outro professor com ID diferente, e retorna um booleano com base nisso.."""
        with DBConnectionHandler() as session:
            aluno = session.query(AlunoData).filter_by(cpf=self.__cpf).first()
            return aluno is not None and aluno.id != self.__id_aluno
        

class ConsultaDadosAluno:
    """Consulta dados relacionados ao aluno: responsável, turma e escola."""

    def __init__(self, id_aluno: int):
        self.id_aluno = id_aluno

    def nome_responsavel(self) -> Optional[str]:
        with DBConnectionHandler() as session:
            aluno = session.query(AlunoData).filter(AlunoData.id == self.id_aluno).first()
            if aluno and aluno.id_responsavel:
                responsavel = session.query(ResponsavelData).filter(ResponsavelData.id == aluno.id_responsavel).first()
                if responsavel:
                    return responsavel.nome
            return None

    def nome_turma(self) -> Optional[str]:
        with DBConnectionHandler() as session:
            aluno = session.query(AlunoData).filter(AlunoData.id == self.id_aluno).first()
            if aluno and aluno.id_turma:
                turma = session.query(TurmaData).filter(TurmaData.id == aluno.id_turma).first()
                if turma:
                    return turma.nome
            return None

    def nome_escola(self) -> Optional[str]:
        with DBConnectionHandler() as session:
            aluno = session.query(AlunoData).filter(AlunoData.id == self.id_aluno).first()
            if aluno and aluno.id_escola:
                escola = session.query(EscolaData).filter(EscolaData.id == aluno.id_escola).first()
                if escola:
                    return escola.nome
            return None