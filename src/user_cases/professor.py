import json
from datetime import date

from typing import Optional, List

from config import log
from utils.validarCampos import ValidadorCampos
from domain import Professor, Aluno

from infra.repositories import (
    ConsultarTurma,
    AdicionarNotaParaAluno,
    AtualizarQuantidadeDeFaltasParaAluno,
    ConsultarAlunosVinculadosAoProfessorNoBanco,
    ConsultarProfessor as ConsultarProfessorBanco,
    ConsultarDisciplinasEMateriasVinculadasAoProfessor,
    ProfessorRepository,
    ConsultaBancoEscola,
    ConsultaBancoAluno
)

from infra.db.models_data import Professor as ProfessorData, Aluno as AlunoData


class ControllerProfessorAlunosVinculados:
    """Controlador para fazer o fluxo de gerar json de retorno do professor e seus alunos vinculados."""

    def __init__(self, id_professor: str):
        """Inicializa o controlador com o ID do professor.

        :param str id_professor: O ID do professor a ser consultado.
        """
        self.__id_professor = id_professor
        self.__list_alunos: Optional[list[Aluno]] = None

    def fluxo_para_consultar_professor_e_seus_alunos(self) -> str:
        """Executa o fluxo completo para consultar um professor e formatar seus alunos vinculados em JSON.

        :return str: Uma string JSON contendo os dados do professor e seus alunos, ou uma mensagem de erro.
        """

        professor_data = ConsultarProfessor(
            id_professor=self.__id_professor
        ).get_professor_data()

        if not professor_data:
            log.warning("Não encontrado professor com esse ID no banco")
            return "Não existe professor. Validar ID do professor passado"

        self.__professor: Professor = self.__formatar_professordata_para_professor(
            professor_data=professor_data
        )

        self.__alunos_vinculados_ao_professor()
        return self.__formatar_alunos_json()

    def __formatar_professordata_para_professor(
        self, professor_data: ProfessorData
    ) -> Professor:
        """Executa o fluxo completo para consultar um professor e formatar seus alunos vinculados em JSON.

        :return str: Uma string JSON contendo os dados do professor e seus alunos, ou uma mensagem de erro.
        """
        professor = Professor(
            id=professor_data.id,
            nome=professor_data.nome,
            cpf=professor_data.cpf,
            cargo=professor_data.cargo,
            id_escola=professor_data.id_escola,
        )
        return professor

    def __alunos_vinculados_ao_professor(self) -> None:
        """Consulta e atribui a lista de alunos vinculados ao professor."""
        self.__list_alunos: Optional[list[Aluno]] = (
            ConsultarAlunosVinculadosAoProfessor(
                id_professor=self.__professor.id
            ).get_alunos_vinculados()
        )

    def __formatar_alunos_json(self) -> str:
        """Formata os dados do professor e seus alunos vinculados em uma string JSON.

        :return str: Uma string JSON com os detalhes do professor e a lista de alunos, ou um JSON de erro.
        """
        if not self.__list_alunos:
            return json.dumps(
                {
                    "Professor": self.__professor.nome,
                    "error": "Professor não tem turma para ter alunos vinculados",
                }
            )

        alunos_list_json = []
        for aluno in self.__list_alunos:
            alunos_list_json.append(
                {
                    "id": aluno.id,
                    "nome": aluno.nome,
                    "idade": aluno.idade,
                    "faltas": aluno.faltas,
                    "id_turma": aluno.id_turma,
                }
            )

        output_data = {
            "professor": {
                "id": self.__professor.id,
                "nome": self.__professor.nome,
                "cpf": self.__professor.cpf,
                "cargo": self.__professor.cargo,
                "id_escola": self.__professor.id_escola,
            },
            "total_alunos_vinculados": len(self.__list_alunos)
            if self.__list_alunos
            else 0,
            "alunos_vinculados": alunos_list_json,
        }

        return json.dumps(output_data, indent=4, ensure_ascii=False)


class ControllerProfessorAtualizarFalta:
    """
    Controlador para a regra de negócio de atualização da quantidade de faltas de um aluno.

    Gerencia o fluxo de validação do professor e a subsequente atualização das faltas
    de um aluno específico no sistema.
    """

    def __init__(
        self, id_professor: str, id_aluno: str, nova_quantidade_de_faltas: int
    ):
        """
        Inicializa o controlador com os dados necessários para a atualização de faltas.

        Valida a existência do professor e prepara os IDs do aluno e a nova quantidade de faltas.

        :param id_professor: O ID do professor, em formato string, que está solicitando a atualização.
        :param id_aluno: O ID do aluno, em formato string, cujas faltas serão atualizadas.
        :param nova_quantidade_de_falta: A nova quantidade de faltas a ser atribuída ao aluno.
        """

        self.__professor: Optional[ProfessorData] = ConsultarProfessor(
            id_professor=id_professor
        ).get_professor_data()
        self.__id_aluno: int = int(id_aluno)
        self.__faltas: int = int(nova_quantidade_de_faltas)

    def fluxo_crud_de_nota_do_aluno(self) -> str:
        """
        Executa o fluxo principal de atualização da quantidade de faltas do aluno.

        Verifica se o professor existe e, em seguida, tenta atualizar as faltas do aluno.
        Retorna uma mensagem de status indicando o resultado da operação.

        :return: Uma string contendo a mensagem de status da operação (sucesso ou falha).
        """
        if not self.__professor:
            return "Professor não encontrado no banco. Validar credencial"

        status_da_atualizacao = self.__atualizar_falta_de_alunos()

        return status_da_atualizacao

    def __atualizar_falta_de_alunos(self) -> str:
        """
        Chama o caso de uso para atualizar a quantidade de faltas de um aluno.

        Este método privado interage com a camada de caso de uso para persistir
        a nova quantidade de faltas no banco de dados.

        :return: Uma string indicando se a atualização foi bem-sucedida ou se houve falha na consulta.
        """
        retorno = AtualizarQuantidadeDeFaltasParaAluno(
            id_aluno=self.__id_aluno,
            id_professor=self.__professor.id,
            nova_quantidade_de_faltas=self.__faltas,
        ).fluxo_atualizar_falta_aluno()
        if not retorno:
            return f"Não conseguio atualizar quantidade de faltas para aluno de id {self.__id_aluno}, validar requisitos"
        return f"Conseguio atualizar quantidade de faltas para o aluno de id {self.__id_aluno} "


class ConsultarProfessor:
    """Classe para consultar dados de um professor no banco de dados."""

    def __init__(self, id_professor: str) -> None:
        """Inicializa a consulta do professor pelo ID.

        :param str id_professor: O ID do professor a ser consultado.
        """
        self.__professor_data: Optional[ProfessorData] = self.__consultar_professor(
            id_professor=int(id_professor)
        )

    def __consultar_professor(self, id_professor: int) -> Professor:
        """Realiza a consulta do professor no repositório do banco de dados.

        :param int id_professor: O ID inteiro do professor para a consulta.
        :return ProfessorData: Um objeto ProfessorData contendo os dados do professor, se encontrado.
        """
        professor: Optional[ProfessorData] = ConsultarProfessorBanco(
            id_professor=id_professor
        ).get_professor_retorno()
        return professor

    def get_professor_data(self) -> Optional[ProfessorData]:
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
        self.__professor_id: int = id_professor
        log.debug(id_professor)
        self.__alunos_vinculado = self.__alunos_vinculado_ao_professor()
        self.__formatar_alunodata_para_alunos()

    def __alunos_vinculado_ao_professor(self) -> List[AlunoData]:
        """Busca a lista de AlunoData vinculados ao professor no banco de dados.

        :return List[AlunoData]: Uma lista de objetos AlunoData vinculados ao professor.
        """
        alunos = ConsultarAlunosVinculadosAoProfessorNoBanco(
            professor_id=self.__professor_id
        )
        return alunos.get_alunos()

    def __formatar_alunodata_para_alunos(self) -> None:
        """Formata a lista de AlunoData para o modelo de domínio Aluno."""
        lista_alunos = []
        for aluno in self.__alunos_vinculado:
            lista_alunos.append(self.__fazer_aluno(aluno=aluno))
        self.__alunos_vinculado = lista_alunos

    def __fazer_aluno(self, aluno: AlunoData) -> Aluno:
        """Cria uma instância do modelo de domínio Aluno a partir de AlunoData.

        :param AlunoData aluno: Objeto AlunoData com os dados brutos do aluno.
        :return Aluno: Uma instância do modelo de domínio Aluno.
        """
        aluno_model: Aluno = Aluno(
            id=aluno.id,
            nome=aluno.nome,
            cpf=aluno.cpf,
            idade=aluno.idade,
            faltas=aluno.faltas,
            nota_score_preditivo=aluno.nota_score_preditivo,
            id_escola=aluno.id_escola,
            id_turma=aluno.id_turma,
            id_responsavel=aluno.id_responsavel,
        )
        return aluno_model

    def get_alunos_vinculados(self) -> Optional[list[Aluno]]:
        """Retorna a lista de alunos vinculados ao professor.

        :return Optional[list[Aluno]]: Uma lista de objetos Aluno, se existirem, caso contrário None.
        """
        return self.__alunos_vinculado


class ControllerConsultarMateriaEDisciplinasVinculadasAoProfessor:
    def __init__(self, id_professor: str):
        self.__id_professor: int = int(id_professor)

    def fluxo_para_consultar(self)-> dict| str:
        consultar_disciplinas = ConsultarDisciplinasEMateriasVinculadasAoProfessor(id_professor= self.__id_professor)
        disciplinas = consultar_disciplinas.consultar()

        if not disciplinas:
            return f'Professor de id {self.__id_professor} não tem disciplinas vinculadas'

        return disciplinas


class ControllerProfessorAdicionarNotaAoAluo:
    """
    Controla o fluxo de negócio para um professor adicionar uma nota a um aluno.

    Esta classe recebe um payload (dicionário), orquestra uma série de validações,
    consultas e, finalmente, a inserção dos dados da avaliação no sistema.
    """
    def __init__(self, post: dict) -> None:
        """
        Inicializa o controller com o payload da requisição.

        :param post: Um dicionário contendo os dados brutos da avaliação,
                     geralmente vindo de uma requisição HTTP JSON.
        """
        self.__post = post
        # Inicializa os atributos para evitar AttributeError se a validação falhar
        self.__tipo_avaliacao = None
        self.__nota = None
        self.__id_disciplina = None
        self.__id_materia = None
        self.__id_professor = None
        self.__id_aluno = None
        self.__id_turma = None


    def fluxo_para_adicionar(self) -> dict:
        """
        Orquestra o processo completo para adicionar a nota de um aluno.

        Executa uma sequência de etapas:
        1. Valida a presença das chaves obrigatórias no payload.
        2. Valida se os valores dessas chaves não são nulos.
        3. Consulta a turma do aluno.
        4. Insere a nota no banco de dados.

        :return: Um dicionário indicando o resultado da operação.
                 - Em caso de sucesso: {"sucesso": "mensagem"}
                 - Em caso de erro: {"erro": "mensagem de erro"}
        """
        if not self.__validar_post():
            log.error("Post não contem campos necessarios para adicionar nota")
            return {"error": "Post não contem campos nescessarios para fazer a avaliação do aluno"}

        if not self.__validar_campos():
            log.error("Um ou mais valores obrigatórios no post são nulos (None).")
            return {"erro": "Valores inválidos. Um ou mais campos obrigatórios estão nulos."}

        self.__consultar_turma()

        if not self.__id_turma:
            return {"error":"Não existe turma vinculada a esse aluno"}

        retorno_do_banco = self.__inserir_nota()

        return retorno_do_banco

    def __validar_post(self) -> bool:
        """
        Valida se o dicionário '__post' contém todas as chaves obrigatórias.

        :return: True se as chaves do post forem válidas, False caso contrário.
        """
        if not isinstance(self.__post, dict):
            return False

        chaves_obrigatorias = {'id_professor', 'tipo_avaliacao', 'nota', 'id_aluno', 'id_materia', 'id_disciplina'}

        return chaves_obrigatorias.issubset(self.__post.keys())

    def __validar_campos(self) -> bool:
        """
        Extrai valores do payload para atributos de instância e valida se não são nulos.

        Este método tem um efeito colateral importante: ele popula os atributos
        privados da classe (ex: self.__nota) com os valores do post.

        :return: True se todos os valores obrigatórios não forem None, False caso contrário.
        """
        self.__tipo_avaliacao = self.__post.get("tipo_avaliacao")
        self.__nota = self.__post.get("nota")
        self.__id_disciplina = self.__post.get("id_disciplina")
        self.__id_materia = self.__post.get("id_materia")
        self.__id_professor = self.__post.get("id_professor")
        self.__id_aluno = self.__post.get("id_aluno")


        valores_a_validar = [
            self.__tipo_avaliacao,
            self.__nota,
            self.__id_materia,
            self.__id_professor,
            self.__id_aluno,
            ]

        # Itera pela lista. Se qualquer um dos valores for None, retorna False imediatamente.
        for valor in valores_a_validar:
            if valor is None:
                return False

        # Se o loop terminar sem encontrar nenhum None, todos os campos são válidos.
        return True

    def __consultar_turma(self) -> None:
        """
        Consulta a turma do aluno e armazena o ID no atributo `self.__id_turma`.

        Este método instancia e utiliza o caso de uso `ConsultarTurma`.
        O resultado é armazenado como um efeito colateral na instância atual.
        """
        self.__id_turma = ConsultarTurma(id_aluno=self.__id_aluno).get_id_turma()

    def __inserir_nota(self):
        """
        Prepara e executa o caso de uso para adicionar a nota no banco de dados.

        Utiliza os atributos da instância (preenchidos durante a validação)
        para instanciar `AdicionarNotaParaAluno` e persistir a avaliação.

        :return: O dicionário de resultado retornado pelo caso de uso de inserção.
        """
        data_de_hoje = date.today()
        adicionar = AdicionarNotaParaAluno(id_aluno=self.__id_aluno, id_professor=self.__id_professor, nota=self.__nota, tipo_avaliacao=self.__tipo_avaliacao, data_avaliacao=data_de_hoje, id_disciplina=self.__id_disciplina, id_materia=self.__id_materia, id_turma=self.__id_turma)
        return adicionar.adicionar_nota()


class ControllerProfessor:
    """Controlador responsável por coordenar operações relacionadas a professores."""

    # Tem que ser optional pq o controllerGestorEscola instancia em diferentes metodos o controller
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

    def criar_professor(self) -> str:
        """Cria um novo professor no banco de dados."""
        resultado = CriarProfessorNoBanco(nome = self.__nome,
                                          cpf = self.__cpf,
                                          cargo = self.__cargo,
                                          id_escola=self.__id_escola)._executar()
        return resultado

    def listar_professores(self) -> list[dict]:
        """Lista todos os professores da escola especificada."""
        professores_data =  ListarProfessoresDaEscola(id_escola = self.__id_escola)._executar()  
        formater = FormatarProfessor()
        professores_dominio = formater.formatar_professor_data_para_dominio(professores_data = professores_data)
        return formater.gerar_json(professores_dominio = professores_dominio)
    
    def atualizar_professor(self) -> str:
        """Atualiza os dados do professor com base no ID."""
        return AtualizarProfessorNoBanco(id_professor = self.__id_professor,
                                         novo_nome = self.__nome,
                                         novo_cargo = self.__cargo,
                                         novo_cpf = self.__cpf,)._executar()

    def deletar_professor(self) -> str:
        """Remove um professor do banco pelo ID."""
        return DeletarProfessorDoBanco(id_professor=self.__id_professor)._executar()


class CriarProfessorNoBanco:
    def __init__(self, nome: str, cpf: str, cargo: str, id_escola: int):
        self.__professor = Professor(nome = nome, cpf = cpf, cargo = cargo, id_escola = id_escola, id = 0)
    
    def _executar(self) -> str:
        
        # Verifica se os campos obrigatórios foram preenchidos
        resultado = ValidadorCampos.validar_campos_preenchidos([
            self.__professor.nome,
            self.__professor.cpf,
            self.__professor.cargo,
            self.__professor.id_escola
        ])
        
        if resultado is not None:
            return resultado
        
        try:
            # Verifica existência da escola
            if ConsultaBancoEscola().buscar_por_id(self.__professor.id_escola) is None:
                return f"Escola com ID {self.__professor.id_escola} não encontrada."
            
            # Verifica existencia de algum aluno com cpf existente
            if ConsultaBancoAluno().buscar_por_cpf(cpf=self.__professor.cpf) is None:
                log.warning(f"Tentativa de cadastro com CPF já existente: {self.__professor.cpf}")
                return "CPF já vinculado."
            
            # Verifica existência de algum professor com cpf existente
            if ConsultarProfessorBanco(id_professor=self.__professor.id).get_professor_retorno_cpf(cpf=self.__professor.cpf) is None:
                log.warning(f"Tentativa de cadastro com CPF já existente: {self.__professor.cpf}")
                return "CPF já vinculado."
            
            ProfessorRepository().criar(self.__professor)
            log.info(f"Professor '{self.__professor.nome}' criado com sucesso.")
            return "Professor criado com sucesso"
        except Exception as e:
            log.error(f"Erro ao criar professor: {e}")
            return "Erro ao criar professor"


class ListarProfessoresDaEscola:
    def __init__(self, id_escola: int):
        self.__id_escola = id_escola

    def _executar(self) -> list[ProfessorData]:
        try:
            professores = ProfessorRepository().listar_por_escola(self.__id_escola)
            log.debug(f"{len(professores)} professores encontrados na escola {self.__id_escola}.")
            return professores
        except Exception as e:
            log.error(f"Erro ao listar professores da escola {self.__id_escola}: {e}")
            return []


class AtualizarProfessorNoBanco:
    def __init__(self, id_professor: int, novo_nome: str, novo_cargo: str, novo_cpf: int):
        self.__id = id_professor
        self.__novo_nome = novo_nome
        self.__novo_cargo = novo_cargo
        self.__novo_cpf = novo_cpf

    def _executar(self) -> str:
        
        # Verifica se os campos obrigatórios foram preenchidos
        resultado = ValidadorCampos.validar_campos_preenchidos([
            self.__id,
            self.__novo_nome,
            self.__novo_cargo,
            self.__novo_cpf
        ])
        
        if resultado is not None:
            return resultado
        
        try:               
            # Verifica existencia de algum aluno com cpf fornecido
            if ConsultaBancoAluno().buscar_por_cpf_e_id(cpf=self.__novo_cpf, id = self.__id):
                log.warning(f"Tentativa de atualização com CPF já existente: {self.__novo_cpf}")
                return "CPF já vinculado."
            
            # Verifica existência de algum professor com cpf existente
            if ConsultarProfessorBanco(id_professor=self.__id).get_professor_retorno_cpf_e_id(cpf=self.__novo_cpf, id=self.__id):
                log.warning(f"Tentativa de atualização com CPF já existente: {self.__novo_cpf}")
                return "CPF já vinculado."  
                   
            atualizado = ProfessorRepository().atualizar(self.__id, self.__novo_nome,
                                                         self.__novo_cargo,
                                                         self.__novo_cpf)
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

    def _executar(self) -> str:
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
        
class FormatarProfessor:
    """Classe responsável por formatar professorData → professor (dominio) → e por fim converter isso para uma string json"""

    def formatar_professor_data_para_dominio(self, professores_data: List[ProfessorData]) -> List[Professor]:
        """Converte uma lista de ProfessorData (ORM) para Professor (domínio)."""
        professores_dom = []
        for professor in professores_data:
            prof_dom = Professor( id = professor.id, nome = professor.nome, cpf = professor.cpf, cargo = professor.cargo, id_escola = professor.id_escola)
            professores_dom.append(prof_dom)
        return professores_dom

    def gerar_json(self, professores_dominio: List[Professor]) -> str:
        """Retorna string JSON com a lista de professores."""
        lista = [
            {
                "id": prof.id,
                "nome": prof.nome,
                "cpf": prof.cpf,
                "cargo": prof.cargo,
                "id_escola": prof.id_escola
            }
            for prof in professores_dominio
        ]
        return json.dumps({"professores": lista}, ensure_ascii = False, indent = 4)