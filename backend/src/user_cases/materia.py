import json

from domain.models import Materia
from utils.validarCampos import ValidadorCampos
from infra.repositories import MateriaRepository, ConsultarProfessor
from infra.db.models_data import Materia as Materia_data
from config import log

from typing import List, Optional

class ControllerMateria:
    """Controlador responsável por coordenar operações relacionadas a matérias."""

    def __init__(self, nome: Optional[str] = None,
                 id_disciplina: Optional[int] = None,
                 id_professor: Optional[int] = None,
                 id_materia: Optional[int] = None,
        ) -> None:
        self.__nome = nome
        self.__id_disciplina = id_disciplina
        self.__id_professor = id_professor
        self.__id_materia = id_materia

    def criar_materia(self) -> str:
        """Cria uma nova matéria no banco de dados."""
        resultado = CriarMateriaNoBanco(nome = self.__nome,
                                        id_disciplina = self.__id_disciplina,
                                        id_professor = self.__id_professor).executar()
        return resultado

    def listar_materias(self) -> str:
        """Lista todas as matérias de um professor especificado."""
        materias_data = ListarMateriasNoBanco(id_professor = self.__id_professor).executar()
        materias_dominio = FormatarMateria().formatar_materia_data_para_dominio(materias_data = materias_data)
        return FormatarMateria().gerar_json(materias_dominio = materias_dominio)
        
    def atualizar_materia(self) -> str:
        """Atualiza os dados da matéria com base no ID."""
        resultado = AtualizarMateriaNoBanco(id_materia = self.__id_materia, 
                                            novo_nome = self.__nome,
                                            novo_id_disciplina = self.__id_disciplina,
                                            novo_id_professor = self.__id_professor).executar()
        return resultado

    def deletar_materia(self) -> str:
        """Remove uma matéria do banco pelo ID."""
        return DeletarMateriaDoBanco(id_materia = self.__id_materia).executar()


class CriarMateriaNoBanco:
    def __init__(self, nome: str, id_disciplina: int, id_professor: int):
        self.__materia = Materia(nome = nome, id_professor = id_professor, id_materia = 0)

    def executar(self) -> str:
        
        # Validação de campos obrigatórios
        resultado = ValidadorCampos.validar_campos_preenchidos([
            self.__materia.nome,
            self.__materia.id_disciplina,
            self.__materia.id_professor
        ])
        if resultado is not None:
            return resultado
        
        try:
            # Verifica existência do professor antes de criar a matéria
            if ConsultarProfessor(self.__materia.id_professor) is None:
                return f"Professor com ID {self.__materia.id_professor} não encontrado."
            
            else:
                MateriaRepository().criar(self.__materia)
                log.info(f"Matéria '{self.__materia.nome}' criada com sucesso.")
                return "Matéria criada com sucesso"
        except Exception as e:
            log.error(f"Erro ao criar matéria: {e}")
            return "Erro ao criar matéria"


class ListarMateriasNoBanco:
    def __init__(self, id_professor: int):
        self.__id_professor = id_professor
    
    def executar(self) -> list[Materia_data]:
        try:
            materias = MateriaRepository().listar_por_professor(self.__id_professor)
            log.debug(f"{len(materias)} matérias encontradas.")
            return materias
        except Exception as e:
            log.error(f"Erro ao listar matérias: {e}")
            return []


class AtualizarMateriaNoBanco:
    def __init__(self, id_materia: int, novo_nome: str, novo_id_disciplina: int, novo_id_professor: int):
        self.__id = id_materia
        self.__novo_nome = novo_nome
        self.__id_disciplina = novo_id_disciplina
        self.__id_professor = novo_id_professor

    def executar(self) -> str:
        
        # Validação de campos obrigatórios
        resultado = ValidadorCampos.validar_campos_preenchidos([
            self.__id,
            self.__novo_nome,
            self.__id_disciplina,
            self.__id_professor
        ])
        
        if resultado is not None:
            return resultado
            
        try:
            # Verifica existência do professor antes de atualizar a matéria
            if ConsultarProfessor(self.__id_professor) is None:
                return f"Professor com ID {self.__materia.id_professor} não encontrado."
            
            else:
                atualizado = MateriaRepository().atualizar(id_materia = self.__id, novo_nome = self.__novo_nome, novo_id_disciplina = self.__id_disciplina, novo_id_professor = self.__id_professor)
                if atualizado:
                    log.info(f"Matéria {self.__id} atualizada com sucesso.")
                    return "Matéria atualizada com sucesso"
                else:
                    return "Matéria não encontrada"
        except Exception as e:
            log.error(f"Erro ao atualizar matéria: {e}")
            return "Erro ao atualizar matéria"


class DeletarMateriaDoBanco:
    def __init__(self, id_materia: int):
        self.__id = id_materia

    def executar(self) -> str:
        try:
            deletado = MateriaRepository().deletar(self.__id)
            if deletado:
                log.info(f"Matéria {self.__id} deletada.")
                return "Matéria deletada com sucesso"
            else:
                return "Matéria não encontrada"
        except Exception as e:
            log.error(f"Erro ao deletar matéria: {e}")
            return "Erro ao deletar matéria"
        
class FormatarMateria:
    """Classe responsável por converter materia_data → materia (dominio) → string json"""

    def formatar_materia_data_para_dominio(self, materias_data: List[Materia_data]) -> List[Materia]:
        materias_dom = []
        for materia in materias_data:
            materia_dom = Materia(
                id_materia = materia.id,
                nome = materia.nome_materia,
                id_disciplina = materia.id_disciplina,
                id_professor = materia.id_professor
            )
            materias_dom.append(materia_dom)
        return materias_dom

    def gerar_json(self, materias_dominio: List[Materia]) -> str:
        
        lista = [
            {
                "id": materia.id,
                "nome": materia.nome,
                "id_disciplina": materia.id_disciplina,
                "id_professor": materia.id_professor
            }
            for materia in materias_dominio
        ]
        
        return json.dumps({"materias": lista}, ensure_ascii=False, indent=4)