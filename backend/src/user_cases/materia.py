import json

from domain.models import Materia
from infra.repositories.materia_data import ConsultaMateriaBanco

from utils.validarCampos import ValidadorCampos
from infra.repositories import MateriaRepository, ConsultarProfessor
from infra.db.models_data import Materia as Materia_data
from config import log

from typing import List, Optional

class ControllerMateria:
    """Controlador responsável por coordenar operações relacionadas a matérias."""

    def __init__(self, nome: Optional[str] = None,
                 id_professor: Optional[int] = None,
                 id_materia: Optional[int] = None,
        ) -> None:
        self.__nome = nome
        self.__id_professor = id_professor
        self.__id_materia = id_materia

    def criar_materia(self) -> str:
        """Cria uma nova matéria no banco de dados."""
        resultado = CriarMateriaNoBanco(nome = self.__nome,id_professor = self.__id_professor).executar()
        return resultado

    def listar_materias(self) -> str:
        """Lista todas as matérias de um professor especificado."""
        materias_data = ListarMateriasNoBanco().executar()
        materias_dominio = FormatarMateria().formatar_materia_data_para_dominio(materias_data = materias_data)
        return FormatarMateria().gerar_json(materias_dominio = materias_dominio)
        
    def atualizar_materia(self) -> str:
        """Atualiza os dados da matéria com base no ID."""
        resultado = AtualizarMateriaNoBanco(id_materia = self.__id_materia, 
                                            novo_nome = self.__nome,
                                            novo_id_professor = self.__id_professor).executar()
        return resultado

    def deletar_materia(self) -> str:
        """Remove uma matéria do banco pelo ID."""
        return DeletarMateriaDoBanco(id_materia = self.__id_materia).executar()

    def buscar_materia(self) -> Materia:
        """Busca uma matéria por meio do ID."""
        materia_data = ConsultaMateriaBanco().buscar_materia_por_id(id_materia=self.__id_materia)
        
        if not materia_data:
            raise ValueError(f"Matéria com ID {self.__id_materia} não encontrada.")

        lista_materia = [materia_data]

        return FormatarMateria().formatar_materia_data_para_dominio(lista_materia)[0]

class CriarMateriaNoBanco:
    def __init__(self, nome: str, id_professor: int):
        self.__materia = Materia(nome = nome, id_professor = id_professor, id_materia = 0, id_disciplina=0)
    def executar(self) -> str:
        
        # Validação de campos obrigatórios
        resultado = ValidadorCampos.validar_campos_preenchidos([
            self.__materia.nome,
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
 
 
    def executar(self) -> list[Materia_data]:
        try:
            materias = MateriaRepository().listar()
            log.debug(f"{len(materias)} matérias encontradas.")
            return materias
        except Exception as e:
            log.error(f"Erro ao listar matérias: {e}")
            return []


class AtualizarMateriaNoBanco:
    def __init__(self, id_materia: int, novo_nome: str, novo_id_professor: int):
        self.__id = id_materia
        self.__novo_nome = novo_nome
        self.__id_professor = novo_id_professor

    def executar(self) -> str:
        
        # Validação de campos obrigatórios
        resultado = ValidadorCampos.validar_campos_preenchidos([
            self.__id,
            self.__novo_nome,
            self.__id_professor
        ])
        
        if resultado is not None:
            return resultado
            
        try:
            # Verifica existência do professor antes de atualizar a matéria
            if ConsultarProfessor(self.__id_professor) is None:
                return f"Professor com ID {self.__id_professor} não encontrado."
            
            else:
                atualizado = MateriaRepository().atualizar(id_materia = self.__id, novo_nome = self.__novo_nome, novo_id_professor = self.__id_professor)
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
