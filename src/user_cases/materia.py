from domain.models import Materia
from infra.repositories import MateriaRepository

from config import log

from typing import Optional

class ControllerGestorMateria:
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

    def __criar_materia(self) -> str:
        """Cria uma nova matéria no banco de dados."""
        resultado = CriarMateriaNoBanco(nome = self.__nome,
                                        id_disciplina = self.__id_disciplina,
                                        id_professor = self.__id_professor).__executar()
        return resultado

    def __listar_materias(self) -> list[dict]:
        """Lista todas as matérias de um professor especificado."""
        return ListarMateriasNoBanco(id_escola = self.__id_professor).__executar()

    def __atualizar_materia(self) -> str:
        """Atualiza os dados da matéria com base no ID."""
        resultado = AtualizarMateriaNoBanco(id_materia = self.__id_materia, 
                                            novo_nome = self.__nome,
                                            novo_id_disciplina = self.__id_disciplina,
                                            novo_id_professor = self.__id_professor).__executar()
        return resultado

    def __deletar_materia(self) -> str:
        """Remove uma matéria do banco pelo ID."""
        return DeletarMateriaDoBanco(id_materia = self.__id_materia).__executar()


class CriarMateriaNoBanco:
    def __init__(self, nome: str, id_disciplina: int, id_professor: int):
        self.__materia = Materia(nome = nome, id_disciplina = id_disciplina, id_professor = id_professor, id_materia = None)

    def __executar(self) -> str:
        try:
            MateriaRepository().criar(self.__materia)
            log.info(f"Matéria '{self.__materia.nome}' criada com sucesso.")
            return "Matéria criada com sucesso"
        except Exception as e:
            log.error(f"Erro ao criar matéria: {e}")
            return "Erro ao criar matéria"


class ListarMateriasNoBanco:
    def __init__(self, id_escola: int):
        self.__id_escola = id_escola
    
    def __executar(self) -> list[dict]:
        try:
            materias = MateriaRepository().listar(self.__id_escola)
            log.debug(f"{len(materias)} matérias encontradas.")
            
            # todo: converter as matérias para materias domain e converter pra json
            return materias
        except Exception as e:
            log.error(f"Erro ao listar matérias: {e}")
            return []


class AtualizarMateriaNoBanco:
    def __init__(self, id_materia: int, novo_nome: str, nova_carga_horaria: int):
        self.__id = id_materia
        self.__novo_nome = novo_nome
        self.__nova_carga_horaria = nova_carga_horaria

    def __executar(self) -> str:
        try:
            atualizado = MateriaRepository().atualizar(self.__id, self.__novo_nome, self.__nova_carga_horaria)
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

    def __executar(self) -> str:
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
        