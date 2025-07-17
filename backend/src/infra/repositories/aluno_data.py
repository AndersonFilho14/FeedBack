from typing import Optional

import logging
from infra import DBConnectionHandler

from infra.db.models_data import (
    Aluno as AlunoData,
    Turma as TurmaData,
)

logging.basicConfig(level=logging.ERROR)  # Configure logging (adjust level as needed)
logger = logging.getLogger(__name__)  # Get a logger for this module

class ConsultarTurma:
    """Lida com a consulta de um único registro de professor no banco de dados."""

    def __init__(self, id_aluno: int) -> None:
        """Inicializa a classe ConsultarProfessor com o ID do professor."""
        self.__id_aluno = id_aluno

    def __consultar_no_banco(self) -> Optional[int]:
        try:
            with DBConnectionHandler() as session:
                aluno = (
                    session.query(AlunoData).filter(AlunoData.id == self.__id_aluno).first()
                )
                if aluno:
                    return aluno.id_turma
                return None
        except Exception as e:
            logger.exception("Erro durante a consulta ao banco:")  # Use exception for traceback
            return None

    def get_id_turma(self):
        """Recupera os dados do professor, retornando o objeto ProfessorData ou None."""
        return self.__consultar_no_banco()
