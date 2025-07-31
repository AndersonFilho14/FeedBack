import json
from config import log
from datetime import datetime

from utils.validarCampos import ValidadorCampos
from infra.repositories import TurmaRepository, ConsultaEscolaBanco, ListarAssociadosDaTurma
from domain.models import Turma
from infra.db.models_data import Turma as Turma_data
from infra.db.models_data import Professor as Professor_data
from infra.db.models_data import Aluno as Aluno_data

from typing import Optional, List

class ControllerTurma:
    """Controlador responsável por coordenar operações relacionadas a turmas."""

    def __init__(self, nome: Optional[str] = None, ano_letivo: Optional[int] = None, id_escola: Optional[int] = None, 
                 id_turma: Optional[int] = None, id_professor: Optional[int] = None, ids_alunos: Optional[List[int]] = None, 
                 id_professor_anterior: Optional[int] = None, ids_alunos_anteriores: Optional[List[int]] = None) -> None:
        
        self.__nome = nome
        self.__id_escola = id_escola
        self.__id_turma = id_turma
        self.__id_professor = id_professor
        self.__ids_alunos = ids_alunos
        self.__id_professor_anterior = id_professor_anterior
        self.__ids_alunos_anteriores = ids_alunos_anteriores

    def criar_turma(self) -> str:
        """Cria uma nova turma no banco de dados."""
        resultado = CriarTurmaNoBanco(nome = self.__nome,
                                      id_escola = self.__id_escola,
                                      ids_alunos=self.__ids_alunos,
                                      id_professor=self.__id_professor).executar()
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
            ids_alunos_atuais=self.__ids_alunos,
            id_professor_atual=self.__id_professor,
            ids_alunos_anteriores=self.__ids_alunos_anteriores,
            id_professor_anterior=self.__id_professor_anterior
        ).executar()

    def deletar_turma(self) -> str:
        """Remove uma turma do banco pelo ID."""
        return DeletarTurmaDoBanco(id_turma=self.__id_turma).executar()


class CriarTurmaNoBanco:
    def __init__(self, nome: str, id_escola: int, id_professor: List[int], ids_alunos: List[int]):
        ano_letivo = datetime.now().year
        self.__turma = Turma(nome = nome, ano_letivo = ano_letivo, id_escola = id_escola, id = 0, id_professor= id_professor, ids_alunos=ids_alunos)

    def executar(self) -> str:
        
        # Verifica se os atributos necessários estão todos preenchidos
        resultado = ValidadorCampos.validar_campos_preenchidos([
            self.__turma.nome,
        ])
        
        if resultado is not None:
            return resultado
        
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

    def executar(self) -> list[Turma_data]:
        try:
            turmas = TurmaRepository().listar_por_escola(self.__id_escola)
            log.debug(f"{len(turmas)} turmas encontradas na escola {self.__id_escola}.")
            return turmas
        except Exception as e:
            log.error(f"Erro ao listar turmas da escola {self.__id_escola}: {e}")
            return []


class AtualizarTurmaNoBanco:
    def __init__(self, id_turma: int, novo_nome: str, id_professor_atual: int, id_professor_anterior: int,
                  ids_alunos_atuais: List[int], ids_alunos_anteriores: List[int] ):
        self.__id = id_turma
        self.__novo_nome = novo_nome
        self.__id_professor_atual = id_professor_atual
        self.__id_professor_anterior = id_professor_anterior
        self.__ids_alunos_atuais = ids_alunos_atuais
        self.__ids_alunos_anteriores = ids_alunos_anteriores


    def executar(self) -> str:
        
        # Verifica se os atributos necessários estão todos preenchidos
        resultado = ValidadorCampos.validar_campos_preenchidos([
            self.__novo_nome,
        ])
        
        if resultado is not None:
            return resultado
        
        try:
            atualizado = TurmaRepository().atualizar(id_turma = self.__id, novo_nome = self.__novo_nome,
                                                      ids_alunos_atuais=self.__ids_alunos_atuais,
                                                      ids_alunos_anteriores=self.__ids_alunos_anteriores,
                                                      id_professor_atual=self.__id_professor_atual, 
                                                      id_professor_anterior=self.__id_professor_anterior)
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
            consulta = ListarAssociadosDaTurma(id_turma= turma.id)
            professor = consulta.buscar_professor_associado()
            
            turma_dom = Turma(
                id = turma.id,
                nome = turma.nome,
                ano_letivo = turma.ano_letivo,
                id_escola = turma.id_escola,
                id_professor = professor.id if professor else None,
            )
            turmas_dom.append(turma_dom)
        return turmas_dom

    def gerar_json(self, turmas_dominio: List[Turma]) -> str:
            """
            Gera um JSON com informações de turmas, incluindo professores e alunos associados.

            :param turmas_dominio: Lista de objetos Turma.
            :return: String JSON formatada com indentação.
            """
            resultado = []

            for turma in turmas_dominio:
                consulta = ListarAssociadosDaTurma(id_turma= turma.id)
                alunos = consulta.listar_alunos_associados()

                json_turma = {
                    "turma_id": turma.id,
                    "nome": turma.nome,
                    "id_escola": turma.id_escola,
                    "professor": turma.id_professor,
                    "ano_letivo": turma.ano_letivo,
                    "alunos": [{"id": aluno.id, "nome": aluno.nome} for aluno in alunos ]
                }

                resultado.append(json_turma)

            return json.dumps(resultado, ensure_ascii=False, indent=4)
