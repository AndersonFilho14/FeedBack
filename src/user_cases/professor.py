import json

from typing import Optional, List

from config import log

from domain import Professor, Aluno

from infra.repositories import ConsultarProfessor as ConsultarProfessorBanco, ConsultarAlunosVinculadosAoProfessorNoBanco, ProfessorRepository
from infra.db.models_data import (
    Professor as ProfessorData,
    Aluno as AlunoData
)

class ControllerProfessorAlunosVinculados:
    """Controlador para fazer o fluxo de gerar json de retorno do professor e seus alunos vinculados."""
    def __init__(self, id_professor : str):
        """Inicializa o controlador com o ID do professor.

        :param str id_professor: O ID do professor a ser consultado.
        """
        self.__id_professor = id_professor
        self.__list_alunos : Optional[list[Aluno]] = None

    def fluxo_para_consultar_professor_e_seus_alunos(self)->str:
        """Executa o fluxo completo para consultar um professor e formatar seus alunos vinculados em JSON.

        :return str: Uma string JSON contendo os dados do professor e seus alunos, ou uma mensagem de erro.
        """

        professor_data = ConsultarProfessor(id_professor=self.__id_professor).get_professor_data()

        if not professor_data:
            log.warning("Não encontrado professor com esse ID no banco")
            return "Não existe professor. Validar ID do professor passado"

        self.__professor : Professor = self.__formatar_professordata_para_professor(professor_data= professor_data)

        self.__alunos_vinculados_ao_professor()
        return self.__formatar_alunos_json()

    def __formatar_professordata_para_professor(self, professor_data : ProfessorData) -> Professor:
        """Executa o fluxo completo para consultar um professor e formatar seus alunos vinculados em JSON.

        :return str: Uma string JSON contendo os dados do professor e seus alunos, ou uma mensagem de erro.
        """
        professor = Professor(
            id= professor_data.id,
            nome= professor_data.nome,
            cpf= professor_data.cpf,
            cargo= professor_data.cargo,
            id_escola= professor_data.id_escola
        )
        return professor

    def __alunos_vinculados_ao_professor(self) -> None:
        """Consulta e atribui a lista de alunos vinculados ao professor."""
        self.__list_alunos : Optional[list[Aluno]] = ConsultarAlunosVinculadosAoProfessor(id_professor= self.__professor.id).get_alunos_vinculados()


    def __formatar_alunos_json(self) -> str:
        """Formata os dados do professor e seus alunos vinculados em uma string JSON.

        :return str: Uma string JSON com os detalhes do professor e a lista de alunos, ou um JSON de erro.
        """
        if not self.__list_alunos:
            return json.dumps({"Professor" : self.__professor.nome,
                            "error": "Professor não tem turma para ter alunos vinculados"})

        alunos_list_json = []
        for aluno in self.__list_alunos:
            alunos_list_json.append({
                "id": aluno.id,
                "nome": aluno.nome,
                "idade": aluno.idade,
                "faltas": aluno.faltas,
                "id_turma": aluno.id_turma
            })

        output_data = {
            "professor": {
                "id": self.__professor.id,
                "nome": self.__professor.nome,
                "cpf": self.__professor.cpf,
                "cargo": self.__professor.cargo,
                "id_escola": self.__professor.id_escola
            },
            "total_alunos_vinculados": len(self.__list_alunos) if self.__list_alunos else 0,
            "alunos_vinculados": alunos_list_json
        }

        return json.dumps(output_data, indent=4, ensure_ascii=False)


class ConsultarProfessor:
    """Classe para consultar dados de um professor no banco de dados."""
    def __init__(self, id_professor: str) -> None:
        """Inicializa a consulta do professor pelo ID.

        :param str id_professor: O ID do professor a ser consultado.
        """
        self.__professor_data : Optional[ProfessorData] = self.__consultar_professor(id_professor= int(id_professor))

    def __consultar_professor(self, id_professor: int)-> Professor:
        """Realiza a consulta do professor no repositório do banco de dados.

        :param int id_professor: O ID inteiro do professor para a consulta.
        :return ProfessorData: Um objeto ProfessorData contendo os dados do professor, se encontrado.
        """
        professor : Optional[ProfessorData] = ConsultarProfessorBanco(id_professor = id_professor).get_professor_retorno()
        return professor

    def get_professor_data(self)-> Optional[ProfessorData]:
        """Retorna os dados do professor consultado.

        :return Optional[ProfessorData]: Os dados do professor, se disponíveis, caso contrário None.
        """
        return self.__professor_data

class ConsultarAlunosVinculadosAoProfessor:
    """Classe para consultar alunos vinculados a um professor no banco de dados."""
    def __init__(self, id_professor: int) -> None:
        """Inicializa a consulta de alunos vinculados a um professor pelo ID.

        :param int id_professor: O ID do professor para o qual se deseja consultar os alunos.
        """
        self.__professor_id : int = id_professor
        log.debug(id_professor)
        self.__alunos_vinculado = self.__alunos_vinculado_ao_professor()
        self.__formatar_alunodata_para_alunos()

    def __alunos_vinculado_ao_professor(self)-> List[AlunoData]:
        """Busca a lista de AlunoData vinculados ao professor no banco de dados.

        :return List[AlunoData]: Uma lista de objetos AlunoData vinculados ao professor.
        """
        alunos = ConsultarAlunosVinculadosAoProfessorNoBanco(professor_id= self.__professor_id)
        return alunos.get_alunos()

    def __formatar_alunodata_para_alunos(self)->None:
        """Formata a lista de AlunoData para o modelo de domínio Aluno."""
        lista_alunos = []
        for aluno in self.__alunos_vinculado:
            lista_alunos.append(self.__fazer_aluno(aluno= aluno))
        self.__alunos_vinculado = lista_alunos

    def __fazer_aluno(self, aluno: AlunoData)-> Aluno:
        """Cria uma instância do modelo de domínio Aluno a partir de AlunoData.

        :param AlunoData aluno: Objeto AlunoData com os dados brutos do aluno.
        :return Aluno: Uma instância do modelo de domínio Aluno.
        """
        aluno_model: Aluno = Aluno(id=aluno.id, nome= aluno.nome, cpf= aluno.cpf, idade=aluno.idade, faltas=aluno.faltas, nota_score_preditivo= aluno.nota_score_preditivo, id_escola= aluno.id_escola, id_turma=aluno.id_turma, id_responsavel= aluno.id_responsavel)
        return aluno_model

    def get_alunos_vinculados(self)-> Optional[list[Aluno]]:
        """Retorna a lista de alunos vinculados ao professor.

        :return Optional[list[Aluno]]: Uma lista de objetos Aluno, se existirem, caso contrário None.
        """
        return self.__alunos_vinculado


class ControllerGestorProfessor:
    """Controlador responsável por coordenar operações relacionadas a professores."""

    # Tem que ser optional pq o controllerGestorEscola instancia diferentes em diferentes metodos o controller
    def __init__(self, nome: Optional[str] = None,
                 cpf: Optional[str] = None,
                 cargo: Optional[str] = None,
                 id_escola: Optional[int] = None,
                 id_professor: Optional[int] = None
        ) -> None:
        self.__nome = nome
        self.__cpf = cpf
        self.__cargo = cargo
        self.__id_escola = id_escola
        self.__id_professor = id_professor

    def __criar_professor(self) -> str:
        """Cria um novo professor no banco de dados."""
        resultado = CriarProfessorNoBanco(nome = self.__nome,
                                          cpf = self.__cpf,
                                          cargo = self.__cargo,
                                          id_escola=self.__id_escola).executar()
        return resultado

    def __listar_professores(self) -> list[dict]:
        """Lista todos os professores da escola especificada."""
        return ListarProfessoresDaEscola(id_escola = self.__id_escola).executar()

    def __atualizar_professor(self) -> str:
        """Atualiza os dados do professor com base no ID."""
        return AtualizarProfessorNoBanco(id_professor = self.__id_professor,
                                         novo_nome = self.__nome,
                                         novo_cargo = self.__cargo,
                                         novo_cpf = self.__cpf,
                                         novo_id_escola = self.__id_escola).executar()

    def __deletar_professor(self) -> str:
        """Remove um professor do banco pelo ID."""
        return DeletarProfessorDoBanco(id_professor=self.__id_professor).executar()


class CriarProfessorNoBanco:
    def __init__(self, nome: str, cpf: str, cargo: str, id_escola: int):
        self.__professor = Professor(nome = nome, cpf = cpf, cargo = cargo, id_escola = id_escola, id_professor = None)
    
    def executar(self) -> str:
        try:
            ProfessorRepository().criar(self.__professor)
            log.info(f"Professor '{self.__professor.nome}' criado com sucesso.")
            return "Professor criado com sucesso"
        except Exception as e:
            log.error(f"Erro ao criar professor: {e}")
            return "Erro ao criar professor"


class ListarProfessoresDaEscola:
    def __init__(self, id_escola: int):
        self.__id_escola = id_escola

    def executar(self) -> list[dict]:
        try:
            professores = ProfessorRepository().listar_por_escola(self.__id_escola)
            log.debug(f"{len(professores)} professores encontrados na escola {self.__id_escola}.")
            return professores
        except Exception as e:
            log.error(f"Erro ao listar professores da escola {self.__id_escola}: {e}")
            return []


class AtualizarProfessorNoBanco:
    def __init__(self, id_professor: int, novo_nome: str, novo_cargo: str, novo_cpf: int ,novo_id_escola: int):
        self.__id = id_professor
        self.__novo_nome = novo_nome
        self.__novo_cargo = novo_cargo
        self.__novo_cpf = novo_cpf
        self.__novo_id_escola = novo_id_escola

    def executar(self) -> str:
        try:
            atualizado = ProfessorRepository().atualizar(self.__id, self.__novo_nome,
                                                         self.__novo_cargo,
                                                         self.__novo_cpf,
                                                         self.__novo_id_escola)
            if atualizado:
                log.info(f"Professor {self.__id} atualizado com sucesso.")
                return "Professor atualizado com sucesso"
            else:
                return "Professor não encontrado"
        except Exception as e:
            log.error(f"Erro ao atualizar professor: {e}")
            return "Erro ao atualizar professor"


class DeletarProfessorDoBanco:
    def __init__(self, id_professor: int):
        self.__id = id_professor

    def executar(self) -> str:
        try:
            deletado = ProfessorRepository().deletar(self.__id)
            if deletado:
                log.info(f"Professor {self.__id} deletado.")
                return "Professor deletado com sucesso"
            else:
                return "Professor não encontrado"
        except Exception as e:
            log.error(f"Erro ao deletar professor: {e}")
            return "Erro ao deletar professor"
