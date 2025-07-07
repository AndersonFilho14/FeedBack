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
    
    def __Consultar_cpf_no_banco(self, cpf: int, id: int) -> Optional[ProfessorData]:
        """Busca um aluno pelo CPF. Retorna o objeto ProfessorData se encontrado, senão None."""
        with DBConnectionHandler() as session:
            return session.query(ProfessorData).filter_by(cpf=cpf).first()
    
    def __Consultar_cpf_e_id_no_banco(self, cpf: int, id: int) -> bool:
        """Verifica se o CPF já está cadastrado em outro professor com ID diferente, e retorna um booleano com base nisso."""
        with DBConnectionHandler() as session:
            professor = session.query(ProfessorData).filter_by(cpf=cpf).first()
            return professor is not None and professor.id != id

    def get_professor_retorno(self) -> Optional[ProfessorData]:
        """Recupera os dados do professor, retornando o objeto ProfessorData ou None."""
        return self.__consultar_no_banco()
    
    def get_professor_retorno_cpf(self, cpf: int) -> Optional[ProfessorData]:
        """Recupera os dados do professor, retornando o objeto ProfessorData ou None."""
        return self.__Consultar_cpf_no_banco(cpf=cpf, id=id)
    
    def get_professor_retorno_cpf_e_id(self, cpf: int, id: int) -> bool:
        """Recupera os dados do professor, retornando um booleano."""
        return self.__Consultar_cpf_e_id_no_banco(cpf=cpf, id=id)


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

class AdicionarNotaParaAluno:
    """
    Caso de uso para adicionar uma nova avaliação (nota) para um aluno no banco de dados.
    """
    def __init__(self, id_aluno: int, id_professor: int, nota: float, tipo_avaliacao: str,
                 data_avaliacao: date, id_disciplina: int, id_materia: int, id_turma: int):


        self.__id_aluno = id_aluno
        self.__id_professor = id_professor
        self.__nota = nota
        self.__tipo_avaliacao = tipo_avaliacao
        self.__data_avaliacao = data_avaliacao
        self.__id_disciplina = id_disciplina
        self.__id_materia = id_materia
        self.__id_turma = id_turma

    def adicionar_nota(self) -> dict:
        """
        Método público que orquestra a inserção da nota no banco de dados.
        Inclui tratamento de erros.

        :return: Um dicionário com o resultado da operação.
        """
        try:
            nova_avaliacao = self.__inserir_no_banco()
            return {
                "sucesso": True,
                "nova_avaliacao_id": nova_avaliacao.id,
                "mensagem": f"Avaliação para o aluno {self.__id_aluno} inserida com sucesso."
            }
        except Exception as e:
            # Em caso de erro, o rollback já é tratado no __inserir_no_banco
            log.error(f"Erro ao adicionar nota para o aluno {self.__id_aluno}: {e}")
            return {
                "sucesso": False,
                "erro": str(e)
            }

    def __inserir_no_banco(self) -> AvaliacaoData:
        """
        Método privado que lida diretamente com a sessão do banco de dados
        para inserir a nova avaliação.
        """
        with DBConnectionHandler() as session:
            try:
                # 1. Cria uma instância do modelo 'Avaliacao' com os dados da classe
                nova_avaliacao = AvaliacaoData(
                    id_aluno=self.__id_aluno,
                    id_professor=self.__id_professor,
                    nota=self.__nota,
                    tipo_avaliacao=self.__tipo_avaliacao,
                    data_avaliacao=self.__data_avaliacao,
                    id_disciplina=self.__id_disciplina,
                    id_materia=self.__id_materia,
                    id_turma=self.__id_turma
                )

                # 2. Adiciona o novo objeto à sessão do SQLAlchemy
                session.add(nova_avaliacao)

                # 3. Confirma (commit) a transação, salvando os dados no banco
                session.commit()

                # 4. (Opcional, mas recomendado) Atualiza a instância 'nova_avaliacao'
                #    para obter dados gerados pelo banco, como o 'id' autoincrementado.
                session.refresh(nova_avaliacao)

                return nova_avaliacao

            except Exception as e:
                # 5. Em caso de qualquer erro (ex: um id_aluno que não existe),
                #    desfaz a transação (rollback) para não deixar o banco em estado inconsistente.
                session.rollback()
                log.error(f"Ocorreu um rollback ao tentar inserir a avaliação: {e}")
                raise e # Lança a exceção novamente para ser capturada pelo método público
            

class ProfessorRepository:
    def criar(self, professor_dom: Professor) -> None:
        """Insere um novo professor no banco."""
        
        # Convertendo professor de domain para professor de infra
        professor_orm = ProfessorData(nome = professor_dom.nome,
                                      cpf = professor_dom.cpf,
                                      cargo = professor_dom.cargo,
                                      id_escola = professor_dom.id_escola)
        
        with DBConnectionHandler() as session:
            session.add(professor_orm)
            session.commit()

    def listar_por_escola(self, id_escola: int) -> List[ProfessorData]:
        """Retorna lista de professores filtrados por escola."""
        with DBConnectionHandler() as session:
            professores = session.query(ProfessorData).filter(ProfessorData.id_escola == id_escola).all()
            return professores

    def atualizar(self, id_professor: int, novo_nome: str, novo_cargo: str, novo_cpf: int) -> bool:
        """Atualiza os dados do professor com base no ID. Retorna True se atualizado, False se não encontrado."""
        with DBConnectionHandler() as session:
            professor = session.query(ProfessorData).filter(ProfessorData.id == id_professor).first()
            if not professor:
                return False
            professor.nome = novo_nome
            professor.cargo = novo_cargo
            professor.cpf = novo_cpf
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
