from typing import Optional
from domain.models import Aluno
from infra.repositories import AlunoRepository
from config import log


class ControllerGestorAluno:
    """Controlador responsável por coordenar operações de CRUD relacionadas a alunos."""

    def __init__(
        self,
        nome: Optional[str] = None,
        cpf: Optional[str] = None,
        idade: Optional[int] = None,
        faltas: Optional[int] = 0,
        nota_score_preditivo: Optional[float] = None,
        id_escola: Optional[int] = None,
        id_turma: Optional[int] = None,
        id_responsavel: Optional[int] = None,
        id_aluno: Optional[int] = None,
    ) -> None:
        self.__nome = nome
        self.__cpf = cpf
        self.__idade = idade
        self.__faltas = faltas
        self.__nota_score = nota_score_preditivo
        self.__id_escola = id_escola
        self.__id_turma = id_turma
        self.__id_responsavel = id_responsavel
        self.__id_aluno = id_aluno

    def __criar_aluno(self) -> str:
        resultado = CriarAlunoNoBanco(
            nome = self.__nome,
            cpf = self.__cpf,
            idade = self.__idade,
            faltas = self.__faltas,
            nota_score_preditivo = self.__nota_score,
            id_escola = self.__id_escola,
            id_turma = self.__id_turma,
            id_responsavel = self.__id_responsavel
        ).__executar()
        return resultado

    def __listar_alunos(self) -> list[dict]:
        return ListarAlunosDoBanco(id_escola=self.__id_escola).__executar()

    def __atualizar_aluno(self) -> str:
        return AtualizarAlunoNoBanco(
            id_aluno = self.__id_aluno,
            novo_nome = self.__nome,
            nova_idade = self.__idade,
            novas_faltas = self.__faltas,
            novo_id_turma = self.__id_turma,
            novo_id_responsavel = self.__id_responsavel
        ).__executar()

    def __deletar_aluno(self) -> str:
        return DeletarAlunoDoBanco(id_aluno = self.__id_aluno).__executar()


class CriarAlunoNoBanco:
    def __init__(
        self,
        nome: str,
        cpf: str,
        idade: int,
        faltas: int,
        nota_score_preditivo: Optional[float],
        id_escola: int,
        id_turma: int,
        id_responsavel: int
    ):
        self.__aluno = Aluno(
            nome = nome,
            cpf = cpf,
            idade = idade,
            faltas = faltas,
            nota_score_preditivo = nota_score_preditivo,
            id_escola = id_escola,
            id_turma = id_turma,
            id_responsavel = id_responsavel
        )

    def __executar(self) -> str:
        try:
            AlunoRepository().criar(self.__aluno)
            log.info(f"Aluno '{self.__aluno.nome}' criado com sucesso.")
            return "Aluno criado com sucesso"
        except Exception as e:
            log.error(f"Erro ao criar aluno: {e}")
            return "Erro ao criar aluno"


class ListarAlunosDoBanco:
    def __init__(self, id_escola: int):
        self.__id_escola = id_escola

    def __executar(self) -> list[dict]:
        try:
            alunos = AlunoRepository().listar_por_escola(self.__id_escola)
            log.debug(f"{len(alunos)} alunos encontrados na escola {self.__id_escola}.")
            return alunos
        except Exception as e:
            log.error(f"Erro ao listar alunos: {e}")
            return []


class AtualizarAlunoNoBanco:
    def __init__(self, id_aluno: int, novo_nome: str, nova_idade: int, novas_faltas: int, novo_id_turma: int, novo_id_responsavel: int):
        self.__id = id_aluno
        self.__novo_nome = novo_nome
        self.__nova_idade = nova_idade
        self.__novas_faltas = novas_faltas
        self.__novo_id_turma = novo_id_turma
        self.__novo_id_responsavel = novo_id_responsavel

    def __executar(self) -> str:
        try:
            atualizado = AlunoRepository().atualizar(
                self.__id,
                self.__novo_nome,
                self.__nova_idade,
                self.__novas_faltas,
                self.__novo_id_turma,
                self.__novo_id_responsavel
            )
            if atualizado:
                log.info(f"Aluno {self.__id} atualizado com sucesso.")
                return "Aluno atualizado com sucesso"
            else:
                return "Aluno não encontrado"
        except Exception as e:
            log.error(f"Erro ao atualizar aluno: {e}")
            return "Erro ao atualizar aluno"


class DeletarAlunoDoBanco:
    def __init__(self, id_aluno: int):
        self.__id = id_aluno

    def __executar(self) -> str:
        try:
            deletado = AlunoRepository().deletar(self.__id)
            if deletado:
                log.info(f"Aluno {self.__id} deletado.")
                return "Aluno deletado com sucesso"
            else:
                return "Aluno não encontrado"
        except Exception as e:
            log.error(f"Erro ao deletar aluno: {e}")
            return "Erro ao deletar aluno"
