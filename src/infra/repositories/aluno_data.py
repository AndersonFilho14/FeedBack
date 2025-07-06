from typing import Optional

from infra import DBConnectionHandler

from infra.db.models_data import (
    Aluno as AlunoData,
    Turma as TurmaData,
)


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
