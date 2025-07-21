from datetime import date
from typing import List, Optional

from config import log

from infra import DBConnectionHandler

from infra.db.models_data import (
    Aluno as AlunoData,
    Turma as TurmaData,
    ProfessorTurma as ProfessorTurmaData,
    Professor as ProfessorData,
    Disciplina as DisciplinaData,
    Materia as MateriaData,
    Avaliacao as AvaliacaoData,
)
from domain.models import Professor


class ConsultarProfessor:
    """Lida com a consulta de um único registro de professor no banco de dados."""

    def __init__(self, id_professor: Optional[int] = None, cpf: Optional[int] = None) -> None:
        """Inicializa a classe ConsultarProfessor com o ID do professor."""
        self.__id_professor = id_professor
        self.__cpf_professor = cpf

    def __consultar_no_banco(self) -> Optional[ProfessorData]:
        """Consulta o banco de dados por um professor com o ID fornecido, retornando o objeto ProfessorData ou None."""
        with DBConnectionHandler() as session:
            retorno = (
                session.query(ProfessorData)
                .filter(ProfessorData.id == self.__id_professor)
                .first()
            )
        return retorno
    
    def __Consultar_cpf_no_banco(self) -> Optional[ProfessorData]:
        """Busca um aluno pelo CPF. Retorna o objeto ProfessorData se encontrado, senão None."""
        with DBConnectionHandler() as session:
            return session.query(ProfessorData).filter_by(cpf = self.__cpf_professor).first()
    
    def __Consultar_cpf_e_id_no_banco(self) -> bool:
        """Verifica se o CPF já está cadastrado em outro professor com ID diferente, e retorna um booleano com base nisso."""
        with DBConnectionHandler() as session:
            professor = session.query(ProfessorData).filter_by(cpf=self.__cpf_professor).first()
            return professor is not None and professor.id != self.__id_professor

    def get_professor_retorno(self) -> Optional[ProfessorData]:
        """Recupera os dados do professor, retornando o objeto ProfessorData ou None."""
        return self.__consultar_no_banco()
    
    def get_professor_retorno_cpf(self) -> Optional[ProfessorData]:
        """Recupera os dados do professor, retornando o objeto ProfessorData ou None."""
        return self.__Consultar_cpf_no_banco()
    
    def get_professor_retorno_cpf_e_id(self) -> bool:
        """Recupera os dados do professor, retornando um booleano."""
        return self.__Consultar_cpf_e_id_no_banco()


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
            resultado_query = (
                session.query(
                    DisciplinaData.id,
                    DisciplinaData.nome_disciplina,
                    MateriaData.id,
                    MateriaData.nome_materia,
                )
                .select_from(MateriaData)
                .join(DisciplinaData, MateriaData.id_disciplina == DisciplinaData.id)
                .join(ProfessorData, MateriaData.id_professor == ProfessorData.id)
                .filter(ProfessorData.id == self.__id_professor)
                .all()
            )

        disciplinas_formatadas = {}

        for id_disciplina, nome_disciplina, id_materia, nome_materia in resultado_query:

            # 3. Se a disciplina ainda não está no nosso dicionário, a inicializamos
            if nome_disciplina not in disciplinas_formatadas:
                disciplinas_formatadas[nome_disciplina] = {
                    "id_disciplina": id_disciplina,
                    "materias": []
                }

            # 4. Adicione a matéria (com seu ID e nome) à lista de matérias da disciplina correspondente
            disciplinas_formatadas[nome_disciplina]["materias"].append({
                "id_materia": id_materia,
                "nome_materia": nome_materia
            })

        return disciplinas_formatadas

class AtualizarNotaParaAluno:
    """
    Caso de uso para adicionar uma nova avaliação (nota) para um aluno no banco de dados.
    """
    def __init__(self, nota: float, data_avaliacao: date, id_avaliacao: int) -> None:

        self.__nota = nota
        self.__data_avaliacao = data_avaliacao
        self.__id_avaliacao = id_avaliacao

    def atualizar_nota_aluno(self) -> dict:
            """
            Atualiza a nota e a data de uma avaliação existente no banco de dados.

            :return: Um dicionário indicando sucesso ou erro.
            """
            try:
                with DBConnectionHandler() as session:
                    avaliacao = session.query(AvaliacaoData).filter(AvaliacaoData.id == self.__id_avaliacao).first()
                    if not avaliacao:
                        return {"erro": f"Avaliação com id {self.__id_avaliacao} não encontrada."}

                    avaliacao.nota = self.__nota
                    avaliacao.data_avaliacao = self.__data_avaliacao
                    session.commit()
                    return {"sucesso": f"Nota da avaliação {self.__id_avaliacao} atualizada com sucesso."}
            except Exception as e:
                return {"erro": f"Erro ao atualizar nota: {str(e)}"}
            

class ProfessorRepository:
    def criar(self, professor_dom: Professor) -> None:
        """Insere um novo professor no banco."""
        
        # Convertendo professor de domain para professor de infra
        professor_orm = ProfessorData(nome = professor_dom.nome,
                                      cpf = professor_dom.cpf,
                                      cargo = professor_dom.cargo,
                                      id_escola = professor_dom.id_escola,
                                      email = professor_dom.email,
                                      telefone = professor_dom.telefone,
                                      estado_civil = professor_dom.estado_civil,
                                      data_nascimento = professor_dom.data_nascimento,
                                      senha = professor_dom.senha,
                                      nacionalidade = professor_dom.nacionalidade,
                                      sexo = professor_dom.sexo
                                    )
        
        with DBConnectionHandler() as session:
            session.add(professor_orm)
            session.commit()

    def listar_por_escola(self, id_escola: int) -> List[ProfessorData]:
        """Retorna lista de professores filtrados por escola."""
        with DBConnectionHandler() as session:
            professores = session.query(ProfessorData).filter(ProfessorData.id_escola == id_escola).all()
            return professores

    def atualizar(self, id_professor: int,
                   novo_nome: str, novo_cargo: str, 
                   novo_cpf: int, novo_data_nascimento: date,
                   novo_nacionalidade: str, novo_estado_civil: str,
                   novo_telefone: str, novo_email: str, nova_senha: str, novo_sexo: str) -> bool:
        """Atualiza os dados do professor com base no ID. Retorna True se atualizado, False se não encontrado."""
        with DBConnectionHandler() as session:
            professor = session.query(ProfessorData).filter(ProfessorData.id == id_professor).first()
            if not professor:
                return False
            professor.nome = novo_nome
            professor.cargo = novo_cargo
            professor.cpf = novo_cpf
            professor.data_nascimento = novo_data_nascimento
            professor.nacionalidade = novo_nacionalidade
            professor.estado_civil = novo_estado_civil
            professor.telefone = novo_telefone
            professor.email = novo_email
            professor.senha = nova_senha
            professor.sexo = novo_sexo
            session.commit()
            return True

    def deletar(self, id_professor: int) -> bool:
        """Deleta o professor pelo id. Retorna True se deletado, False se não encontrado."""
        with DBConnectionHandler() as session:
            professor = session.query(ProfessorData).filter(ProfessorData.id == id_professor).first()
            if not professor:
                return False
            session.delete(professor)
            session.commit()
            return True