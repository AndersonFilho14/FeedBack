import json
from datetime import date

from typing import Optional, List, Dict

from config import log
from utils.validarCampos import ValidadorCampos
from domain import Professor, Aluno

from infra.repositories import (
    ConsultarTurma,
    AtualizarNotaParaAluno,
    AtualizarQuantidadeDeFaltasParaAluno,
    ConsultarAlunosVinculadosAoProfessorNoBanco,
    ConsultarProfessor as ConsultarProfessorBanco,
    ConsultarDisciplinasEMateriasVinculadasAoProfessor,
    ProfessorRepository,
    ConsultaEscolaBanco,
    ConsultaAlunoBanco
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
            nacionalidade=professor_data.nacionalidade,
            estado_civil=professor_data.estado_civil,
            telefone=professor_data.telefone,
            email=professor_data.email,
            data_nascimento=professor_data.data_nascimento,
            senha=professor_data.senha,
            sexo=professor_data.sexo
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
                    "cpf": aluno.cpf,
                    "faltas": aluno.faltas,
                    "nota_score_preditivo": aluno.nota_score_preditivo,
                    "data_nascimento": aluno.data_nascimento.strftime("%Y-%m-%d") if aluno.data_nascimento else None,
                    "sexo": aluno.sexo,
                    "nacionalidade": aluno.nacionalidade,
                    "id_escola": aluno.id_escola,
                    "id_turma": aluno.id_turma,
                    "id_responsavel": aluno.id_responsavel
                }
            )

        output_data = {
            "professor": {
                "id": self.__professor.id,
                "nome": self.__professor.nome,
                "cpf": self.__professor.cpf,
                "cargo": self.__professor.cargo,
                "id_escola": self.__professor.id_escola,
                "nacionalidade": self.__professor.nacionalidade,
                "estado_civil": self.__professor.estado_civil,
                "telefone": self.__professor.telefone,
                "email": self.__professor.email,
                "data_nascimento": self.__professor.data_nascimento.strftime("%Y-%m-%d") if self.__professor.data_nascimento else None,
                "senha": self.__professor.senha
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

    def __init__(self, id_professor: str, faltas_alunos: List[Dict[str, int]]) -> None:
        """
        Inicializa o controlador com o ID do professor e uma lista de dados de faltas dos alunos.

        :param id_professor: ID do professor.
        :param faltas_alunos: Lista de dicionários com os dados dos alunos e faltas.
                              Exemplo: [{"id_aluno": 1, "faltas": 2}, ...]
        """
        professor = ConsultarProfessor(id_professor=id_professor).get_professor_data()
        self.__professor = professor
        self.__faltas_alunos = faltas_alunos

    def processar_faltas_para_alunos(self) -> str:
        """
        Executa o fluxo principal de atualização da quantidade de faltas do aluno.

        Verifica se o professor existe e, em seguida, tenta atualizar as faltas do aluno.
        Retorna uma mensagem de status indicando o resultado da operação.

        :return: Uma string contendo a mensagem de status da operação (sucesso ou falha).
        """
        if not self.__professor:
            return "Professor não encontrado no banco. Validar credencial"
        
        resultados = []

        for item in self.__faltas_alunos:
            id_aluno = item.get("id_aluno")
            faltas = item.get("faltas")

            resultado = self.__atualizar_falta_de_aluno(id_aluno, faltas)
            resultados.append(resultado)

        return resultados
    
    def __atualizar_falta_de_aluno(self, id_aluno: int, faltas: int) -> str:
        """
        Chama o caso de uso para atualizar a quantidade de faltas de um aluno.

        Este método privado interage com a camada de caso de uso para persistir
        a nova quantidade de faltas no banco de dados.

        :return: Uma string indicando se a atualização foi bem-sucedida ou se houve falha na consulta.
        """
        retorno = AtualizarQuantidadeDeFaltasParaAluno(
            id_aluno=id_aluno,
            id_professor=self.__professor.id,
            nova_quantidade_de_faltas=faltas,
        ).fluxo_atualizar_falta_aluno()

        if not retorno:
            return f"Falha ao atualizar faltas para o aluno ID {id_aluno}."
        return f"Faltas atualizadas para aluno ID {id_aluno}."


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
            faltas=aluno.faltas,
            nota_score_preditivo=aluno.nota_score_preditivo,
            data_nascimento=aluno.data_nascimento,
            sexo=aluno.sexo,
            nacionalidade=aluno.nacionalidade,
            id_escola=aluno.id_escola,
            id_turma=aluno.id_turma,
            id_responsavel=aluno.id_responsavel
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


class ControllerProfessorAtualizarNotaAoAluno:
    """
    Controla o fluxo de negócio para um professor adicionar uma nota a um aluno.

    Esta classe recebe um payload (dicionário), orquestra uma série de validações,
    consultas e, finalmente, a inserção dos dados da avaliação no sistema.
    """
    def __init__(self, notas_alunos: list[dict]) -> None:
        """
        Inicializa o controller com o payload da requisição.

        :param post: Um dicionário contendo os dados brutos da avaliação,
                     geralmente vindo de uma requisição HTTP JSON.
        """
        self.__notas_alunos = notas_alunos

    def atualizar_notas(self):
        """
        Prepara e executa o caso de uso para adicionar a nota no banco de dados.

        Utiliza os atributos da instância (preenchidos durante a validação)
        para instanciar `AdicionarNotaParaAluno` e persistir a avaliação.

        :return: O dicionário de resultado retornado pelo caso de uso de inserção.
        """
        resultados = []
        data_de_hoje = date.today()

        for item in self.__notas_alunos:
            nota = item.get("nota")
            id_avaliacao = item.get("id_avaliacao")
            resultado = AtualizarNotaParaAluno(nota=nota, data_avaliacao=data_de_hoje, id_avaliacao=id_avaliacao).atualizar_nota_aluno()
            resultados.append({"id_avaliacao": id_avaliacao, "resultado": resultado})
        return resultados


class ControllerProfessor:
    """Controlador responsável por coordenar operações relacionadas a professores."""

    # Tem que ser optional pq o controllerGestorEscola instancia em diferentes metodos o controller
    def __init__(self, nome: Optional[str] = None,
                 cpf: Optional[str] = None,
                 cargo: Optional[str] = None,
                 id_escola: Optional[int] = None,
                 id_professor: Optional[int] = None,
                 nacionalidade: Optional[str] = None,
                 estado_civil: Optional[str] = None,
                 telefone: Optional[str] = None,
                 email: Optional[str] = None,
                 senha: Optional[str] = None,
                 data_nascimento: Optional[str] = None,
                 sexo: Optional[str] = None
        ) -> None:
        self.__nome = nome
        self.__cpf = cpf
        self.__cargo = cargo
        self.__id_escola = id_escola
        self.__id_professor = id_professor
        self.__nacionalidade = nacionalidade
        self.__estado_civil = estado_civil
        self.__telefone = telefone
        self.__email = email
        self.__senha = senha
        self.__data_nascimento = data_nascimento
        self.__sexo = sexo

    def criar_professor(self) -> str:
        """Cria um novo professor no banco de dados."""
        resultado = CriarProfessorNoBanco(nome = self.__nome,
                                          cpf = self.__cpf,
                                          cargo = self.__cargo,
                                          id_escola=self.__id_escola,
                                          nacionalidade=self.__nacionalidade,
                                          estado_civil=self.__estado_civil,
                                          telefone=self.__telefone,
                                          email=self.__email,
                                          senha=self.__senha,
                                          data_nascimento=self.__data_nascimento,
                                          sexo=self.__sexo)._executar()
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
                                         novo_cpf = self.__cpf,
                                         novo_sexo = self.__sexo,
                                         novo_data_nascimento = self.__data_nascimento,
                                         novo_nacionalidade = self.__nacionalidade,
                                         novo_estado_civil = self.__estado_civil,
                                         novo_telefone = self.__telefone,
                                         novo_email = self.__email,
                                         novo_senha = self.__senha   
                                         )._executar()

    def deletar_professor(self) -> str:
        """Remove um professor do banco pelo ID."""
        return DeletarProfessorDoBanco(id_professor=self.__id_professor)._executar()


class CriarProfessorNoBanco:
    def __init__(self,
                  nome: str,
                  cpf: str,
                  cargo: str,
                  id_escola: int,
                  nacionalidade: str,
                  estado_civil: str,
                  telefone: str,
                  email: str,
                  senha: str,
                  data_nascimento: str,
                  sexo: str
                  ) -> None:
        data_nascimento = date.fromisoformat(data_nascimento) if data_nascimento else None
        self.__professor = Professor(nome = nome,
                                     cpf = cpf, 
                                     cargo = cargo,
                                     id_escola = id_escola,
                                     id = 0,
                                     nacionalidade=nacionalidade, 
                                     estado_civil=estado_civil,
                                     telefone=telefone,
                                     email=email,
                                     senha=senha,
                                     data_nascimento=data_nascimento,
                                     sexo=sexo)
    """Classe responsável por criar um professor no banco de dados."""

    def _executar(self) -> str:
        
        # Verifica se os campos obrigatórios foram preenchidos
        resultado = ValidadorCampos.validar_campos_preenchidos([
            self.__professor.nome,
            self.__professor.cpf,
            self.__professor.cargo,
            self.__professor.nacionalidade,
            self.__professor.estado_civil,
            self.__professor.telefone,
            self.__professor.email,
            self.__professor.senha
        ])
        
        if resultado is not None:
            return resultado
        
        try:
            # Verifica existência da escola
            if ConsultaEscolaBanco().buscar_por_id(self.__professor.id_escola) is None:
                return f"Escola com ID {self.__professor.id_escola} não encontrada."
            
            # Verifica existencia de algum aluno com cpf existente
            if ConsultaAlunoBanco(cpf=self.__professor.cpf).buscar_por_cpf() is not None:
                log.warning(f"Tentativa de cadastro com CPF já existente: {self.__professor.cpf}")
                return "CPF já vinculado, aluno."
            
            # Verifica existência de algum professor com cpf existente
            if ConsultarProfessorBanco(id_professor=self.__professor.id, cpf=self.__professor.cpf).get_professor_retorno_cpf() is not None:
                log.warning(f"Tentativa de cadastro com CPF já existente: {self.__professor.cpf}")
                return "CPF já vinculado, professor, professor."

            resultado_email = ValidadorCampos.validar_email(self.__professor.email)
            if resultado_email is not None:
                return resultado_email

            resultado_telefone = ValidadorCampos.validar_telefone(self.__professor.telefone)
            if resultado_telefone is not None:
                return resultado_telefone
            resultado_cpf = ValidadorCampos.validar_cpf(self.__professor.cpf)
            if resultado_cpf is not None:
                return resultado_cpf    
            
            
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
    def __init__(self, id_professor: int, novo_nome: str, novo_cargo: str, novo_cpf: int, novo_data_nascimento: str, 
                 novo_nacionalidade: str = None, novo_estado_civil: str = None, novo_telefone: str = None, 
                 novo_email: str = None, novo_senha: str = None, novo_sexo: str = None) -> None:
        self.__id = id_professor
        self.__novo_nome = novo_nome
        self.__novo_cargo = novo_cargo
        self.__novo_cpf = novo_cpf
        novo_data_nascimento = date.fromisoformat(novo_data_nascimento) if novo_data_nascimento else None
        self.__novo_data_nascimento = novo_data_nascimento
        self.__novo_nacionalidade = novo_nacionalidade
        self.__novo_estado_civil = novo_estado_civil
        self.__novo_telefone = novo_telefone
        self.__novo_email = novo_email
        self.__novo_senha = novo_senha
        self.__novo_sexo = novo_sexo
    """Classe responsável por atualizar os dados de um professor no banco de dados."""

    def _executar(self) -> str:
        
        # Verifica se os campos obrigatórios foram preenchidos
        resultado = ValidadorCampos.validar_campos_preenchidos([
            self.__id,
            self.__novo_nome,
            self.__novo_cargo,
            self.__novo_cpf,
            self.__novo_data_nascimento,
            self.__novo_nacionalidade,
            self.__novo_estado_civil,
            self.__novo_telefone,
            self.__novo_email,
            self.__novo_senha,
        ])
        
        if resultado is not None:
            return resultado
        
        try:               
            # Verifica existencia de algum aluno com cpf fornecido
            if ConsultaAlunoBanco(id_aluno =  self.__id, cpf = self.__novo_cpf).buscar_por_cpf_e_id():
                log.warning(f"Tentativa de atualização com CPF já existente: {self.__novo_cpf}")
                return "CPF já vinculado."
            
            # Verifica existência de algum professor com cpf existente
            if ConsultarProfessorBanco(id_professor=self.__id, cpf= self.__novo_cpf).get_professor_retorno_cpf_e_id():
                log.warning(f"Tentativa de atualização com CPF já existente: {self.__novo_cpf}")
                return "CPF já vinculado."  
            
            resultado_email = ValidadorCampos.validar_email(self.__novo_email)
            if resultado_email is not None:
                return resultado_email  
            
            resultado_telefone = ValidadorCampos.validar_telefone(self.__novo_telefone)
            if resultado_telefone is not None:  
                return resultado_telefone

            atualizado = ProfessorRepository().atualizar(self.__id, self.__novo_nome,
                                                         self.__novo_cargo,
                                                         self.__novo_cpf, self.__novo_data_nascimento,
                                                         self.__novo_nacionalidade, self.__novo_estado_civil,
                                                         self.__novo_telefone, self.__novo_email,
                                                         self.__novo_senha, self.__novo_sexo)
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
            prof_dom = Professor(  id = professor.id,
                                   nome = professor.nome,
                                   cpf = professor.cpf,
                                   cargo = professor.cargo,
                                   id_escola = professor.id_escola,
                                   nacionalidade = professor.nacionalidade,
                                   estado_civil = professor.estado_civil,
                                   telefone = professor.telefone,
                                   email = professor.email,
                                   data_nascimento = professor.data_nascimento,
                                   senha = professor.senha,
                                   sexo= professor.sexo
                                   )
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
                "id_escola": prof.id_escola,
                "nacionalidade": prof.nacionalidade,
                "estado_civil": prof.estado_civil,
                "telefone": prof.telefone,
                "email": prof.email,
                "data_nascimento": prof.data_nascimento.strftime("%Y-%m-%d") if prof.data_nascimento else None,
                "senha": prof.senha,
                "sexo": prof.sexo
            }
            for prof in professores_dominio
        ]
        return json.dumps({"professores": lista}, ensure_ascii = False, indent = 4)