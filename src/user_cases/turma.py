from config import log

from infra.repositories import TurmaRepository
from domain.models import Turma

from typing import Optional

class ControllerGestorTurma:
    """Controlador responsável por coordenar operações relacionadas a turmas."""

    def __init__(self, nome: Optional[str] = None, ano_letivo: Optional[int] = None, id_escola: Optional[int] = None, id_turma: Optional[int] = None) -> None:
        self.__nome = nome
        self.__ano_letivo = ano_letivo
        self.__id_escola = id_escola
        self.__id_turma = id_turma

    def __criar_turma(self) -> str:
        """Cria uma nova turma no banco de dados."""
        resultado = CriarTurmaNoBanco(nome = self.__nome, ano_letivo = self.__ano_letivo, id_escola = self.__id_escola).__executar()
        return resultado

    def __listar_turmas(self) -> list[dict]:
        """Lista todas as turmas da escola especificada."""
        return ListarTurmasDaEscola(id_escola=self.__id_escola).__executar()

    def __atualizar_turmas(self) -> str:
        """Atualiza os dados da turma com base no ID."""
        return AtualizarTurmaNoBanco(
            id_turma = self.__id_turma,
            novo_nome = self.__nome,
            ano_letivo = self.__ano_letivo,
            novo_id_escola = self.__id_escola
        ).__executar()

    def __deletar_turma(self) -> str:
        """Remove uma turma do banco pelo ID."""
        return DeletarTurmaDoBanco(id_turma=self.__id_turma).__executar()


class CriarTurmaNoBanco:
    def __init__(self, nome: str, ano_letivo: int ,id_escola: int):
        self.__turma = Turma(nome = nome, ano_letivo = ano_letivo, id_escola = id_escola)

    def __executar(self) -> str:
        try:
            TurmaRepository().criar(self.__turma)
            log.info(f"Turma '{self.__turma.nome}' criada com sucesso.")
            return "Turma criada com sucesso"
        except Exception as e:
            log.error(f"Erro ao criar turma: {e}")
            return "Erro ao criar turma"


class ListarTurmasDaEscola:
    def __init__(self, id_escola: int):
        self.__id_escola = id_escola

    def __executar(self) -> list[dict]:
        try:
            turmas = TurmaRepository().listar_por_escola(self.__id_escola)
            log.debug(f"{len(turmas)} turmas encontradas na escola {self.__id_escola}.")
            
            #todo: converter em turmas de domain e converter para json
            return turmas
        except Exception as e:
            log.error(f"Erro ao listar turmas da escola {self.__id_escola}: {e}")
            return []


class AtualizarTurmaNoBanco:
    def __init__(self, id_turma: int, novo_nome: str, ano_letivo: int, novo_id_escola: int):
        self.__id = id_turma
        self.__novo_nome = novo_nome
        self.__ano_letivo = ano_letivo
        self.__novo_id_escola = novo_id_escola

    def __executar(self) -> str:
        try:
            atualizado = TurmaRepository().atualizar(self.__id, self.__novo_nome, self.__ano_letivo, self.__novo_id_escola)
            if atualizado:
                log.info(f"Turma {self.__id} atualizada com sucesso.")
                return "Turma atualizada com sucesso"
            else:
                return "Turma não encontrada"
        except Exception as e:
            log.error(f"Erro ao atualizar turma: {e}")
            return "Erro ao atualizar turma"


class DeletarTurmaDoBanco:
    def __init__(self, id_turma: int):
        self.__id = id_turma

    def __executar(self) -> str:
        try:
            deletado = TurmaRepository().deletar(self.__id)
            if deletado:
                log.info(f"Turma {self.__id} deletada.")
                return "Turma deletada com sucesso"
            else:
                return "Turma não encontrada"
        except Exception as e:
            log.error(f"Erro ao deletar turma: {e}")
            return "Erro ao deletar turma"
