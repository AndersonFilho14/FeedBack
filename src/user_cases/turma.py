import json
from config import log

from utils.validarCampos import ValidadorCampos
from infra.repositories import TurmaRepository, ConsultaBancoEscola
from domain.models import Turma
from infra.db.models_data import Turma as Turma_data

from typing import Optional, List

class ControllerTurma:
    """Controlador responsável por coordenar operações relacionadas a turmas."""

    def __init__(self, nome: Optional[str] = None, ano_letivo: Optional[int] = None, id_escola: Optional[int] = None, id_turma: Optional[int] = None) -> None:
        self.__nome = nome
        self.__ano_letivo = ano_letivo
        self.__id_escola = id_escola
        self.__id_turma = id_turma

    def criar_turma(self) -> str:
        """Cria uma nova turma no banco de dados."""
        resultado = CriarTurmaNoBanco(nome = self.__nome, ano_letivo = self.__ano_letivo, id_escola = self.__id_escola).executar()
        return resultado

    def listar_turmas(self) -> str:
        """Lista todas as turmas da escola especificada."""
        turmas_data = ListarTurmasDaEscola(id_escola=self.__id_escola).executar()
        turmas_dominio = FormatarTurma().formatar_turma_data_para_dominio(turmas_data = turmas_data)
        return FormatarTurma().gerar_json(turmas_dominio = turmas_dominio)
    
    def atualizar_turmas(self) -> str:
        """Atualiza os dados da turma com base no ID."""
        return AtualizarTurmaNoBanco(
            id_turma = self.__id_turma,
            novo_nome = self.__nome,
            ano_letivo = self.__ano_letivo,
            novo_id_escola = self.__id_escola
        ).executar()

    def deletar_turma(self) -> str:
        """Remove uma turma do banco pelo ID."""
        return DeletarTurmaDoBanco(id_turma=self.__id_turma).executar()


class CriarTurmaNoBanco:
    def __init__(self, nome: str, ano_letivo: int ,id_escola: int):
        self.__turma = Turma(nome = nome, ano_letivo = ano_letivo, id_escola = id_escola, id = 0)

    def executar(self) -> str:
        
        # Verifica se os atributos necessários estão todos preenchidos
        resultado = ValidadorCampos.validar_campos_preenchidos([
            self.__turma.nome,
            self.__turma.ano_letivo,
            self.__turma.id_escola
        ])
        
        if resultado is not None:
            return resultado
        
        try:
            # Verifica existência da escola
            if ConsultaBancoEscola().buscar_por_id(self.__turma.id_escola) is None:
                return f"Escola com ID {self.__aluno.id_escola} não encontrada."
            
            TurmaRepository().criar(self.__turma)
            log.info(f"Turma '{self.__turma.nome}' criada com sucesso.")
            return "Turma criada com sucesso"
        except Exception as e:
            log.error(f"Erro ao criar turma: {e}")
            return "Erro ao criar turma"


class ListarTurmasDaEscola:
    def __init__(self, id_escola: int):
        self.__id_escola = id_escola

    def executar(self) -> list[Turma_data]:
        try:
            turmas = TurmaRepository().listar_por_escola(self.__id_escola)
            log.debug(f"{len(turmas)} turmas encontradas na escola {self.__id_escola}.")
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

    def executar(self) -> str:
        
        # Verifica se os atributos necessários estão todos preenchidos
        resultado = ValidadorCampos.validar_campos_preenchidos([
            self.__id,
            self.__novo_nome,
            self.__ano_letivo,
            self.__novo_id_escola
        ])
        
        if resultado is not None:
            return resultado
        
        try:
            atualizado = TurmaRepository().atualizar(id_turma = self.__id, novo_nome = self.__novo_nome, novo_ano_letivo = self.__ano_letivo, novo_id_escola = self.__novo_id_escola)
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

    def executar(self) -> str:
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

class FormatarTurma:
    """Classe responsável por converter TurmaData (ORM) em Turma (domínio) e gerar JSON formatado."""

    def formatar_turma_data_para_dominio(self, turmas_data: List[Turma_data]) -> List[Turma]:
        turmas_dom = []
        for turma in turmas_data:
            turma_dom = Turma(
                id = turma.id,
                nome = turma.nome,
                ano_letivo = turma.ano_letivo,
                id_escola = turma.id_escola
            )
            turmas_dom.append(turma_dom)
        return turmas_dom

    def gerar_json(self, turmas_dominio: List[Turma]) -> str:

        lista = [
            {
                "id": turma.id,
                "nome": turma.nome,
                "ano_letivo": turma.ano_letivo,
                "id_escola": turma.id_escola
            }
            for turma in turmas_dominio
        ]
        return json.dumps({"turmas": lista}, ensure_ascii=False, indent=4)
