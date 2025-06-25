from typing import List, Optional

from infra import DBConnectionHandler

from infra.db.models_data import (
    Aluno as AlunoData,
    Turma as TurmaData,
    ProfessorTurma as ProfessorTurmaData,
    Professor as ProfessorData,
)


class ConsultarProfessor:
    """Lida com a consulta de um único registro de professor no banco de dados."""

    def __init__(self, id_professor: int) -> None:
        """Inicializa a classe ConsultarProfessor com o ID do professor."""
        self.__id_professor = id_professor

    def __consultar_no_banco(self) -> Optional[ProfessorData]:
        """Consulta o banco de dados por um professor com o ID fornecido, retornando o objeto ProfessorData ou None."""
        with DBConnectionHandler() as session:
            retorno = (
                session.query(ProfessorData)
                .filter(ProfessorData.id == self.__id_professor)
                .first()
            )
        return retorno

    def get_professor_retorno(self) -> Optional[ProfessorData]:
        """Recupera os dados do professor, retornando o objeto ProfessorData ou None."""
        return self.__consultar_no_banco()


class ConsultarAlunosVinculadosAoProfessorNoBanco:
    """Lida com a consulta de alunos vinculados a um professor específico."""

    def __init__(self, professor_id: int) -> None:
        """Inicializa a classe consultando e armazenando os alunos vinculados ao ID do professor fornecido."""
        self.__alunos = self.__consultar_alunos(professor_id=professor_id)

    def __consultar_alunos(self, professor_id: int) -> List[AlunoData]:
        """Consulta o banco de dados por todos os alunos vinculados a um determinado professor através de suas turmas, retornando uma lista de objetos AlunoData."""
        with DBConnectionHandler() as session:
            alunos = (
                session.query(AlunoData)
                .join(TurmaData, AlunoData.id_turma == TurmaData.id)
                .join(ProfessorTurmaData, ProfessorTurmaData.id_turma == TurmaData.id)
                .join(
                    ProfessorData, ProfessorData.id == ProfessorTurmaData.id_professor
                )
                .filter(ProfessorData.id == professor_id)
                .all()
            )
            return alunos

    def get_alunos(self) -> List[AlunoData]:
        """Recupera a lista de objetos AlunoData que representam os alunos vinculados ao professor."""
        return self.__alunos
