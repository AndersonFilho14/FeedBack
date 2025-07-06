from typing import List, Optional
from collections import defaultdict

from infra import DBConnectionHandler

from infra.db.models_data import (
    Aluno as AlunoData,
    Turma as TurmaData,
    ProfessorTurma as ProfessorTurmaData,
    Professor as ProfessorData,
    Disciplina as DisciplinaData,
    Materia as MateriaData,
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


class AtualizarQuantidadeDeFaltasParaAluno:
    """
    Classe de caso de uso para atualizar a quantidade de faltas de um aluno.

    Este fluxo garante que apenas professores vinculados ao aluno possam realizar
    a atualização das faltas no sistema.
    """

    def __init__(
        self, id_professor: int, id_aluno: int, nova_quantidade_de_faltas: int
    ) -> None:
        """
        Inicializa o fluxo de atualização de faltas para um aluno.

        :param id_professor: O ID do professor que está realizando a atualização.
        :param id_aluno: O ID do aluno cujas faltas serão atualizadas.
        :param nova_quantidade_de_faltas: A nova quantidade de faltas a ser registrada para o aluno.
        """
        self.__id_professor: int = id_professor
        self.__id_aluno: int = id_aluno
        self.__nova_quantidade_de_faltas: int = nova_quantidade_de_faltas
        self.__id_professor: int = id_professor

    def fluxo_atualizar_falta_aluno(self) -> Optional[bool]:
        """
        Executa o fluxo completo para atualizar as faltas de um aluno.

        Primeiro, verifica se o aluno está vinculado ao professor. Se a vinculação
        não for confirmada, a operação é abortada. Caso contrário, as faltas do aluno
        são atualizadas no banco de dados.

        :return: True se a atualização for bem-sucedida, None caso o aluno não
                 esteja vinculado ao professor.
        """
        retorno = self.__consultar_se_aluno_esta_vinculado_ao_professer()
        if not retorno:
            return None

        self.__atualizar_falta_de_alunos()
        return True

    def __consultar_se_aluno_esta_vinculado_ao_professer(self) -> Optional[int]:
        """
        Verifica se um aluno específico está vinculado a um determinado professor.

        Realiza uma consulta complexa no banco de dados, unindo tabelas de alunos,
        turmas e professores para confirmar a relação entre aluno e professor.

        :return: O ID do aluno se ele estiver vinculado ao professor, ou None caso contrário.
        """
        with DBConnectionHandler() as session:
            retorno = (
                session.query(AlunoData.id)
                .join(TurmaData, AlunoData.id_turma == TurmaData.id)
                .join(ProfessorTurmaData, ProfessorTurmaData.id_turma == TurmaData.id)
                .join(
                    ProfessorData, ProfessorData.id == ProfessorTurmaData.id_professor
                )
                .filter(
                    ProfessorData.id == self.__id_professor,
                    AlunoData.id == self.__id_aluno,
                )
                .first()
            )
        return retorno

    def __atualizar_falta_de_alunos(self) -> None:
        """
        Atualiza a quantidade de faltas de um aluno no banco de dados.

        Este método privado executa a operação de atualização diretamente na tabela
        de alunos, persistindo a nova quantidade de faltas.
        """
        with DBConnectionHandler() as session:
            session.query(AlunoData).filter(AlunoData.id == self.__id_aluno).update(
                {"faltas": self.__nova_quantidade_de_faltas}
            )

            session.commit()


class ConsultarDisciplinasEMateriasVinculadasAoProfessor:
    """
    Consulta as disciplinas e matérias que estão vinculadas a um professor específico.

    Esta classe de caso de uso recupera informações detalhadas sobre quais disciplinas
    e matérias um professor está atualmente lecionando, utilizando seu ID como critério.
    """

    def __init__(self, id_professor: int) -> None:
        """
        Inicializa o caso de uso com o ID do professor para a consulta.

        :param id_professor: O ID do professor cujas disciplinas e matérias serão consultadas.
        """
        self.__id_professor = id_professor

    def consultar(self) -> dict:
        """
        Executa a consulta no banco de dados para obter as disciplinas e matérias.

        Realiza um JOIN entre as tabelas de Materia, Disciplina e Professor para
        filtrar os resultados com base no ID do professor fornecido.

        :return: Um dicionário onde as chaves são os nomes das disciplinas
                 e os valores são listas com os nomes das matérias.
                 Ex: {"Matemática": ["Álgebra", "Geometria"]}.
                 Retorna um dicionário vazio se nenhuma vinculação for encontrada.
        """
        with DBConnectionHandler() as session:
            resultado = (
                session.query(DisciplinaData.nome_disciplina, MateriaData.nome_materia)
                .select_from(MateriaData)
                .join(DisciplinaData, MateriaData.id_disciplina == DisciplinaData.id)
                .join(ProfessorData, MateriaData.id_professor == ProfessorData.id)
                .filter(ProfessorData.id == self.__id_professor)
                .all()
            )

        disciplinas_agrupadas = defaultdict(list)

        for disciplina, materia in resultado:
            disciplinas_agrupadas[disciplina].append(materia)

        return dict(disciplinas_agrupadas)
