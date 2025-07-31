from flask import Blueprint, make_response, jsonify, request

from user_cases import (
    ControllerAcesso,
    ControllerProfessorAtualizarFalta,
    ControllerProfessorAlunosVinculados,
    ControllerProfessorAtualizarNotaAoAluno,  # noqa F401
    ControllerConsultarMateriaEDisciplinasVinculadasAoProfessor,
    ControllerEscola,
    ControllerMateria, 
    ControllerAluno, 
    ControllerMunicipio, 
    ControllerProfessor,
    ControllerTurma,
    ControllerRankingAvaliacao, 
    ControllerHistoricoAvaliacoes,
    ControllerDashboard
)

user_rout_bp = Blueprint("user_routes", __name__)


@user_rout_bp.route("/acesso/<string:user_name>/<string:passworld>", methods=["GET"])
def login(user_name: str, passworld: str) -> str:
    """Realiza a autenticação do usuário e gera um token de acesso.

    Este endpoint valida as credenciais (usuário e senha) fornecidas na URL.
    Se as credenciais forem válidas, retorna as informações do usuário e um
    token para autorização em outras rotas.

    :param user_name: Nome de usuário para o login (ex: 'prof_alfa').
    :param passworld: Senha do usuário (ex: 'senha123').
    :return: Uma resposta JSON com dados do usuário e token em caso de
             sucesso (200 OK), ou uma string de erro em caso de falha.
    """
    informacao: str = ControllerAcesso(
        user_name=user_name, passworld=passworld
    ).return_user_ou_texto()
    return informacao


@user_rout_bp.route(
    "/professor/visualizar_alunos/<string:id_professor>", methods=["GET"]
)
def professor_visualizar_alunos_vinculados_a_ele(id_professor: str) -> str:
    """Retorna a lista de alunos vinculados a um professor específico.

    A partir do ID de um professor, esta rota consulta o sistema e retorna
    todos os alunos que estão atualmente associados a ele, por exemplo,
    em suas turmas.

    :param id_professor: O ID numérico do professor a ser consultado.
    :return: Uma resposta JSON contendo uma lista de objetos, onde cada
             objeto representa um aluno. Retorna uma lista vazia se o
             professor não tiver alunos vinculados.
    """
    retorno = ControllerProfessorAlunosVinculados(
        id_professor=id_professor
    ).fluxo_para_consultar_professor_e_seus_alunos()
    return retorno


@user_rout_bp.route("/professor/atualizar_faltas_turma", methods=["PUT"])
def professor_atualizar_faltas_para_turma():
    """
    Atualiza a quantidade de faltas de múltiplos alunos em uma turma.

    Esta rota permite que um professor atualize, em lote, a quantidade de
    faltas de diversos alunos associados a uma turma. Os dados são enviados
    via JSON no corpo da requisição.

    :request JSON: Um objeto contendo:
        - id_professor (str): ID do professor que está realizando a operação.
        - faltas (List[Dict]): Lista de objetos com id do aluno e nova quantidade de faltas.
          Exemplo: [{"id_aluno": 1, "faltas": 2}, ...]

    :return: Mensagem em string de sucesso ou erro.
    """

    dados = request.get_json()

    id_professor = dados["id_professor"]
    lista_faltas = dados["faltas"]  # Ex: [{ "id_aluno": 1, "faltas": 2 }, ...]

    controller = ControllerProfessorAtualizarFalta(
        id_professor=id_professor,
        faltas_alunos=lista_faltas
    )
    retorno = controller.processar_faltas_para_alunos()
    return retorno

@user_rout_bp.route('/materia_e_disciplina_que_o_professor_ensina/<string:id_professor>', methods=['GET'])
def consultar_materia_e_disciplina_do_professor(id_professor: str):
    """Consulta e retorna as disciplinas e matérias que um professor leciona.

    Retorna uma estrutura aninhada que agrupa as matérias sob suas
    respectivas disciplinas para o professor especificado, incluindo
    os IDs de cada entidade.

    :param id_professor: O ID do professor a ser consultado.
    :return: Uma resposta JSON com os dados agrupados.
             Exemplo de retorno:
             ```json
             {
                 "Português": {
                     "id_disciplina": 1,
                     "materias": [
                         {
                             "id_materia": 1,
                             "nome_materia": "Gramática"
                         }
                     ]
                 }
             }
             ```
    """
    consultar = ControllerConsultarMateriaEDisciplinasVinculadasAoProfessor(id_professor=id_professor)
    retorno = consultar.fluxo_para_consultar()
    print(retorno)
    print(type(retorno))
    return make_response(jsonify(retorno))

@user_rout_bp.route("/professor/atualizar_nota", methods=["PUT"])
def prof_atualizar_nota_a_aluno():
    """
    Atualiza a nota de múltiplos alunos.

    **JSON Body esperado:**
    {
        "notas": [
            { "id_avaliacao": 1, "nota": 8.5 },
            { "id_avaliacao": 2, "nota": 7.0 }
        ]
    }

    :return: Uma resposta JSON contendo o resultado da operação.
    """
    dados = request.get_json()
    lista_notas = dados["notas"]  # Ex: [{ "id_aluno": 1, "nota": 8.5 }, ...]

    controller = ControllerProfessorAtualizarNotaAoAluno(
        notas_alunos=lista_notas
    )
    retorno = controller.atualizar_notas()
    return make_response(jsonify(retorno))


class ValidarToken:
    def __init__(self, token_a_validar: str):
        self.__token: str = ReservarToken.get_token()
        self.__token_a_validar: str = token_a_validar

    def validar_token(self) -> bool:
        if self.__token_a_validar == self.__token:
            return True
        return False


class ReservarToken:
    __token: str = ""

    @classmethod
    def set_token(cls, token: str) -> None:
        if not isinstance(token, str):
            raise ValueError("Token não é uma string")

        cls.__token = token

    def get_token(cls) -> str:
        return cls.__token
    

# --------------- CRIAR ALUNO ---------------
@user_rout_bp.route("/aluno", methods=["POST"])
def criar_aluno():
    """
    Cria um novo aluno.

    **JSON Body esperado**:
    ```json
    {
        "nome": "Maria Teste",
        "cpf": "12345678901",
        "data_nascimento": "2010-05-10",
        "sexo": "feminino",
        "nacionalidade": "Brasileira",
        "id_escola": 1,
        "id_turma": 2,
        "nome_responsavel": "João Responsável",
        "numero_responsavel": "11999999999",
        "etnia": 1,
        "educacao_pais": 3,
        "tempo_estudo_semanal": 6.0,
        "apoio_pais": 1,
        "aulas_particulares": 0,
        "extra_curriculares": 1,
        "esportes": 0,
        "aula_musica": 0,
        "voluntariado": 1
    }
    ```

    :return: JSON com mensagem de sucesso ou erro.
    """
    dados = request.json

    controller = ControllerAluno(
        nome=dados.get("nome"),
        cpf=dados.get("cpf"),
        data_nascimento=dados.get("data_nascimento"),
        sexo=dados.get("sexo"),
        nacionalidade=dados.get("nacionalidade"),
        id_escola=dados.get("id_escola"),
        id_turma=dados.get("id_turma"),
        nome_responsavel=dados.get("nome_responsavel"),
        numero_responsavel=dados.get("numero_responsavel"),
        etnia=dados.get("etnia"),
        educacao_pais=dados.get("educacao_pais"),
        tempo_estudo_semanal=dados.get("tempo_estudo_semanal"),
        apoio_pais=dados.get("apoio_pais"),
        aulas_particulares=dados.get("aulas_particulares"),
        extra_curriculares=dados.get("extra_curriculares"),
        esportes=dados.get("esportes"),
        aula_musica=dados.get("aula_musica"),
        voluntariado=dados.get("voluntariado")
    )

    resultado = controller.criar_aluno()
    return make_response(jsonify({"mensagem": resultado}))



# --------------- LISTAR ALUNOS POR ESCOLA ---------------
@user_rout_bp.route("/alunos/escola/<int:id_escola>", methods=["GET"])
def listar_alunos_escola(id_escola):
    """
    Lista todos os alunos vinculados a uma escola.

    :param id_escola: ID da escola.
    :return: JSON estruturado com a lista de alunos.
    """
    controller = ControllerAluno(id_escola=id_escola)
    resultado = controller.listar_alunos_Escola()   # já retorna string JSON
    return make_response(resultado)


# --------------- LISTAR ALUNOS POR TURMA ---------------
@user_rout_bp.route("/alunos/turma/<int:id_turma>", methods=["GET"])
def listar_alunos_turma(id_turma):
    """
    Lista todos os alunos de uma turma.

    :param id_turma: ID da turma.
    :return: JSON estruturado com a lista de alunos.
    """
    controller = ControllerAluno(id_turma=id_turma)
    resultado_json = controller.listar_alunos_turma()    # já retorna string JSON
    return make_response(resultado_json)


# --------------- ATUALIZAR ALUNO ---------------
@user_rout_bp.route("/aluno/<int:id_aluno>", methods=["PUT"])
def atualizar_aluno(id_aluno):
    """
    Atualiza os dados de um aluno.

    **JSON Body esperado**:
    ```json
    {
        "id_aluno": 1,
        "nome": "Maria Atualizada",
        "cpf": "12345678901",
        "data_nascimento": "2010-05-10",
        "sexo": "feminino",
        "nacionalidade": "Brasileira",
        "nome_responsavel": "João Responsável",
        "numero_responsavel": "11999999999",
        "etnia": 2,
        "educacao_pais": 3,
        "tempo_estudo_semanal": 5.5,
        "apoio_pais": 1,
        "aulas_particulares": 0,
        "extra_curriculares": 1,
        "esportes": 1,
        "aula_musica": 0,
        "voluntariado": 1
    }
    ```

    :param id_aluno: ID do aluno a ser atualizado.
    :return: Mensagem em string de sucesso ou erro.
    """
    dados = request.json
    controller = ControllerAluno(
        id_aluno=id_aluno,
        nome=dados.get("nome"),
        cpf=dados.get("cpf"),
        data_nascimento=dados.get("data_nascimento"),
        sexo=dados.get("sexo"),
        nacionalidade=dados.get("nacionalidade"),
        nome_responsavel=dados.get("nome_responsavel"),
        numero_responsavel=dados.get("numero_responsavel"),
        etnia=dados.get("etnia"),
        educacao_pais=dados.get("educacao_pais"),
        tempo_estudo_semanal=dados.get("tempo_estudo_semanal"),
        apoio_pais=dados.get("apoio_pais"),
        aulas_particulares=dados.get("aulas_particulares"),
        extra_curriculares=dados.get("extra_curriculares"),
        esportes=dados.get("esportes"),
        aula_musica=dados.get("aula_musica"),
        voluntariado=dados.get("voluntariado"),
    )
    resultado = controller.atualizar_aluno()
    return make_response(jsonify({"mensagem": resultado}))


# --------------- DELETAR ALUNO ---------------
@user_rout_bp.route("/aluno/<int:id_aluno>", methods=["DELETE"])
def deletar_aluno(id_aluno):
    """
    Remove um aluno do sistema.

    :param id_aluno: ID do aluno a ser removido.
    :return: Mensagem em string de sucesso ou erro.
    """
    controller = ControllerAluno(id_aluno=id_aluno)
    resultado = controller.deletar_aluno()
    return make_response(jsonify({"mensagem": resultado})) 

 
 # --------------------- CRIAR ESCOLAS ---------------------   
@user_rout_bp.route("/escola", methods=["POST"])
def criar_escola():
    """
    Cria uma nova escola no sistema.

    Espera um JSON com os campos:
    {
        "nome": "Escola Exemplo",
        "id_municipio": 1,
        "nome_usuario": "escola_exemplo",
        "senha": "senha123"
    }

    :return: Mensagem em string de sucesso ou erro.
    """
    dados = request.json
    controller = ControllerEscola(
        nome=dados.get("nome"),
        id_municipio=dados.get("id_municipio"),
        nome_usuario=dados.get("nome_usuario"),
        senha=dados.get("senha")
    )
    resultado = controller.criar_escola()
    return make_response(jsonify({"mensagem": resultado}))


# --------------------- LISTAR ESCOLAS ---------------------
@user_rout_bp.route("/escola", methods=["GET"])
def listar_escolas():
    """
    Lista todas as escolas de um município específico.

    :param id_municipio: ID do município passado na URL.
    :return: JSON contendo a lista de escolas formatadas.
    """
    controller = ControllerEscola(id_municipio=1)
    resultado_json = controller.listar_escolas()
    return make_response(resultado_json)

# --------------------- ATUALIZAR ESCOLA ---------------------
@user_rout_bp.route("/escola/<int:id_escola>", methods=["PUT"])
def atualizar_escola(id_escola):
    """
    Atualiza os dados de uma escola existente.

    Espera um JSON com os campos:
    {
        "nome": "Novo Nome da Escola",
        "nome_usuario": "novo_usuario",
        "senha": "nova_senha"
    }

    :param id_escola: ID da escola a ser atualizada.
    :return: Mensagem em string de sucesso ou erro.
    """
    dados = request.json
    controller = ControllerEscola(
        id_escola=id_escola,
        nome=dados.get("nome"),
        nome_usuario=dados.get("nome_usuario"),
        senha=dados.get("senha")
    )
    resultado = controller.atualizar_escola()
    return make_response(jsonify({"mensagem": resultado}))


# --------------------- DELETAR ESCOLA ---------------------
@user_rout_bp.route("/escola/<int:id_escola>", methods=["DELETE"])
def deletar_escola(id_escola):
    """
    Remove uma escola do sistema com base no ID informado.

    :param id_escola: ID da escola a ser removida.
    :return: Mensagem em string de sucesso ou erro.
    """
    controller = ControllerEscola(id_escola=id_escola)
    resultado = controller.deletar_escola()
    return make_response(jsonify({"mensagem": resultado}))

# --------------------- BUSCAR ESCOLA ---------------------
@user_rout_bp.route("/escola/<int:id_escola>", methods=["GET"])
def obter_escola(id_escola: int):
    """
    Rota para buscar uma escola pelo ID.

    Retorno:
        200 OK com JSON da escola encontrada
        404 Not Found se a escola não existir
    """
    try:
        controller = ControllerEscola(id_escola=id_escola)
        escola = controller.buscar_escola()
        return jsonify(escola.__dict__), 200  # ou use um método to_dict() se houver
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404

# --------------------- CRIAR MATÉRIA ---------------------
@user_rout_bp.route("/materia", methods=["POST"])
def criar_materia():
    """
    Cria uma nova matéria.

    **JSON Body esperado**:
    ```json
    {
        "nome": "Gramática",
    }
    ```

    :return: Mensagem em string de sucesso ou erro.
    """
    dados = request.json
    controller = ControllerMateria(
        nome=dados.get("nome"),
    )
    resultado = controller.criar_materia()
    return make_response(jsonify({"mensagem": resultado}))


# --------------------- LISTAR MATÉRIAS  ---------------------###
@user_rout_bp.route("/materia", methods=["GET"])
def listar_materias():
    """
    Lista todas as matérias.    
    :return: JSON estruturado com a lista de matérias.
    """
    controller = ControllerMateria()
    resultado_json = controller.listar_materias()  
    return make_response(resultado_json)

# --------------------- BUSCA MATÉRIAS POR ID ---------------------###
@user_rout_bp.route("/materia/<int:id_materia>", methods=["GET"])
def buscar_materias_por_id(id_materia: int):
    """
    buscar as matérias vinculadas por id.

    :param id_materia: ID da matéria a ser buscada.
    :return: JSON estruturado com a lista de matérias.
    """

    controller = ControllerMateria(id_materia=id_materia)
    materia = controller.buscar_materia()
    return jsonify(materia.__dict__), 200 
  

# --------------------- ATUALIZAR MATÉRIA ---------------------
@user_rout_bp.route("/materia/<int:id_materia>", methods=["PUT"])
def atualizar_materia(id_materia):
    """
    Atualiza os dados de uma matéria existente.

    **JSON Body esperado**:
    ```json
    {
        "nome": "Gramática Avançada",
    }
    ```

    :param id_materia: ID da matéria a ser atualizada.
    :return: Mensagem em string de sucesso ou erro.
    """
    dados = request.json
    controller = ControllerMateria(
        id_materia=id_materia,
        nome=dados.get("nome"),
    )
    resultado = controller.atualizar_materia()
    return make_response(jsonify({"mensagem": resultado}))


# --------------------- DELETAR MATÉRIA ---------------------
@user_rout_bp.route("/materia/<int:id_materia>", methods=["DELETE"])
def deletar_materia(id_materia):
    """
    Remove uma matéria do sistema.

    :param id_materia: ID da matéria a ser excluída.
    :return: Mensagem em string de sucesso ou erro.
    """
    controller = ControllerMateria(id_materia=id_materia)
    resultado = controller.deletar_materia()
    return make_response(jsonify({"mensagem": resultado}))


# ------------------ CRIAR MUNICÍPIO ------------------
@user_rout_bp.route("/municipio", methods=["POST"])
def criar_municipio():
    """
    Cria um novo município no sistema.

    **JSON Body esperado**:
    ```json
    {
        "nome": "Porto Alegre",
        "estado": "RS",
        "regiao": "Sul"
    }
    ```

    :return: Mensagem em string de sucesso ou erro.
    """
    dados = request.json
    controller = ControllerMunicipio(
        nome=dados.get("nome"),
        estado=dados.get("estado"),
        regiao=dados.get("regiao")
    )
    resultado = controller.criar_municipio()
    return make_response(jsonify({"mensagem": resultado}))


# ------------------ LISTAR MUNICÍPIOS ------------------
@user_rout_bp.route("/municipios", methods=["GET"])
def listar_municipios():
    """
    Retorna a lista de todos os municípios cadastrados.

    :return: JSON contendo a lista de municípios.
    """
    controller = ControllerMunicipio()
    resultado = controller.listar_municipios()  # já retorna string JSON
    return make_response(resultado)


# ------------------ ATUALIZAR MUNICÍPIO ------------------
@user_rout_bp.route("/municipio/<int:id_municipio>", methods=["PUT"])
def atualizar_municipio(id_municipio):
    """
    Atualiza os dados de um município existente.

    **JSON Body esperado**:
    ```json
    {
        "nome": "Novo Nome",
        "estado": "SC",
        "regiao": "Sul"
    }
    ```

    :param id_municipio: ID do município a ser atualizado.
    :return: Mensagem em string de sucesso ou erro.
    """
    dados = request.json
    controller = ControllerMunicipio(
        id_municipio=id_municipio,
        nome=dados.get("nome"),
        estado=dados.get("estado"),
        regiao=dados.get("regiao")
    )
    resultado = controller.atualizar_municipio()
    return make_response(jsonify({"mensagem": resultado}))


# ------------------ DELETAR MUNICÍPIO ------------------
@user_rout_bp.route("/municipio/<int:id_municipio>", methods=["DELETE"])
def deletar_municipio(id_municipio):
    """
    Remove um município do sistema.

    :param id_municipio: ID do município a ser deletado.
    :return: Mensagem em string de sucesso ou erro.
    """
    controller = ControllerMunicipio(id_municipio=id_municipio)
    resultado = controller.deletar_municipio()
    return make_response(jsonify({"mensagem": resultado}))

# ------------------ CRIAR PROFESSOR ------------------
@user_rout_bp.route("/professor", methods=["POST"])
def criar_professor():
    """
    Cria um novo professor.

    **JSON Body esperado**:
    {
        "nome": "João Silva",
        "cpf": "12345678901",
        "cargo": "Matemática",
        "id_escola": 1,
        "nacionalidade": "Brasileiro",
        "estado_civil": "Solteiro",
        "telefone": "11999999999",
        "email": "joao_user.com",
        "senha": "mortadela123",
        "data_nascimento": "2000-01-01",
        "sexo": "Masculino"
    }

    :return: Mensagem em string de sucesso ou erro.
    """
    dados = request.json
    controller = ControllerProfessor(
        nome=dados.get("nome"),
        cpf=dados.get("cpf"),
        cargo=dados.get("cargo"),
        id_escola=dados.get("id_escola"),
        nacionalidade=dados.get("nacionalidade"),
        estado_civil=dados.get("estado_civil"),
        telefone=dados.get("telefone"),
        nome_usuario=dados.get("email"),
        senha=dados.get("senha"),
        data_nascimento=dados.get("data_nascimento"),
        sexo=dados.get("sexo")
    )
    resultado = controller.criar_professor()
    return make_response(jsonify({"mensagem": resultado}))


# ------------------ LISTAR PROFESSORES POR ESCOLA ------------------
@user_rout_bp.route("/professores/escola/<int:id_escola>", methods=["GET"])
def listar_professores(id_escola):
    """
    Lista todos os professores vinculados a uma escola.

    :param id_escola: ID da escola.
    :return: JSON estruturado com a lista de professores.
    """
    controller = ControllerProfessor(id_escola=id_escola)
    resultado_json = controller.listar_professores()   # já retorna string JSON
    return make_response(resultado_json)


# ------------------ ATUALIZAR PROFESSOR ------------------
@user_rout_bp.route("/professor/<int:id_professor>", methods=["PUT"])
def atualizar_professor(id_professor):
    """
    Atualiza os dados de um professor existente.

    **JSON Body esperado**:
    {
        "nome": "João Atualizado",
        "cpf": "12345678901",
        "cargo": "Física",
        "data_nascimento": "2000-01-01",
        "nacionalidade": "Brasileiro",
        "estado_civil": "Solteiro",
        "telefone": "11999999999",
        "nome_usuario": "joao_user_atualizado",
        "senha": "mortadela123",
        "sexo": "Masculino"
    }

    :param id_professor: ID do professor a ser atualizado.
    :return: Mensagem em string de sucesso ou erro.
    """
    dados = request.json
    controller = ControllerProfessor(
        id_professor=id_professor,
        nome=dados.get("nome"),
        cpf=dados.get("cpf"),
        cargo=dados.get("cargo"),
        data_nascimento=dados.get("data_nascimento"),
        nacionalidade=dados.get("nacionalidade"),
        estado_civil=dados.get("estado_civil"),
        telefone=dados.get("telefone"),
        nome_usuario=dados.get("email"),
        senha=dados.get("senha"),
        sexo=dados.get("sexo")
    )
    resultado = controller.atualizar_professor()
    return make_response(jsonify({"mensagem": resultado}))


# ------------------ DELETAR PROFESSOR ------------------
@user_rout_bp.route("/professor/<int:id_professor>", methods=["DELETE"])
def deletar_professor(id_professor):
    """
    Remove um professor do sistema.

    :param id_professor: ID do professor a ser removido.
    :return: Mensagem em string de sucesso ou erro.
    """
    controller = ControllerProfessor(id_professor=id_professor)
    resultado = controller.deletar_professor()
    return make_response(jsonify({"mensagem": resultado}))

# ------------------ CRIAR TURMA ------------------
@user_rout_bp.route("/turma", methods=["POST"])
def criar_turma():
    """
    Cria uma nova turma.

    **JSON Body esperado**:
    ```json
    {
        "nome": "Turma A",
        "escola_id": 1,
        "id_professor": 1,
        "ids_alunos_associados": [10, 11, 12]
    }
    ```

    :return: Mensagem em string de sucesso ou erro.
    """
    dados = request.json

    controller = ControllerTurma(
        nome=dados.get("nome"),
        ano_letivo=dados.get("ano_letivo"),
        id_escola=dados.get("escola_id"),
        id_professor=dados.get("id_professor"),
        ids_alunos=dados.get("ids_alunos", [])
    )
    resultado = controller.criar_turma()
    return make_response(jsonify({"mensagem": resultado}))


# ------------------ LISTAR TURMAS POR ESCOLA ------------------
@user_rout_bp.route("/turmas/escola/<int:id_escola>", methods=["GET"])
def listar_turmas(id_escola):
    """
    Lista todas as turmas de uma escola.

    :param id_escola: ID da escola.
    :return: Mensagem em string de sucesso ou erro.
    """
    controller = ControllerTurma(id_escola=id_escola)
    resultado_json = controller.listar_turmas()  # já retorna string JSON
    return make_response(resultado_json)

# ------------------ ATUALIZAR TURMA ------------------
@user_rout_bp.route("/turma/<int:id_turma>", methods=["PUT"])
def atualizar_turma(id_turma):
    """
    Atualiza os dados de uma turma, incluindo a associação de professores e alunos.

    **JSON Body esperado**:
    ```json
    {
        "nome": "3º Ano C",
        "ano_letivo": 2025,
        "id_professor_atual": 1,
        "id_professor_anterior": 2,  
        "ids_alunos_atuais": [10, 11],
        "ids_alunos_anteriores": [10, 12]
    }
    ```

    :param id_turma: ID da turma a ser atualizada.
    :return: Mensagem em string de sucesso ou erro.
    """
    dados = request.json

    controller = ControllerTurma(
        id_turma=id_turma,
        nome=dados.get("nome"),
        ano_letivo=dados.get("ano_letivo"),
        id_professor=dados.get("id_professor_atual"),
        id_professor_anterior=dados.get("id_professor_anterior"),
        ids_alunos=dados.get("ids_alunos_atuais", []),
        ids_alunos_anteriores=dados.get("ids_alunos_anteriores", [])
    )
    resultado = controller.atualizar_turmas()
    return make_response(jsonify({"mensagem": resultado}))


# ------------------ DELETAR TURMA ------------------
@user_rout_bp.route("/turma/<int:id_turma>", methods=["DELETE"])
def deletar_turma(id_turma):
    """
    Deleta uma turma existente.

    :param id_turma: ID da turma a ser deletada.
    :return: Mensagem em string de sucesso ou erro.
    """
    controller = ControllerTurma(id_turma=id_turma)
    resultado = controller.deletar_turma()
    return make_response(jsonify({"mensagem": resultado}))

# --------------- HISTÓRICO DE AVALIAÇÕES ---------------

@user_rout_bp.route("/historico/avaliacoes/aluno/<int:id_aluno>", methods=["GET"])
def historico_avaliacoes_por_aluno(id_aluno):
    """
    Retorna o histórico de avaliações de um aluno.
    """
    controller = ControllerHistoricoAvaliacoes(id_aluno=id_aluno)
    resultado = controller.listar_historico_avaliacoes_por_aluno()
    return make_response(resultado)


@user_rout_bp.route("/historico/avaliacoes/turma/<int:id_turma>/<int:id_professor>", methods=["GET"])
def historico_avaliacoes_por_turma(id_turma, id_professor):
    """
    Retorna o histórico de avaliações de uma turma.
    """
    controller = ControllerHistoricoAvaliacoes(id_turma=id_turma, id_professor=id_professor)
    resultado = controller.listar_historico_avaliacoes_por_turma()
    return make_response(resultado)


@user_rout_bp.route("/historico/avaliacoes/escola/<int:id_escola>", methods=["GET"])
def historico_avaliacoes_por_escola(id_escola):
    """
    Retorna o histórico de avaliações de uma escola.
    """
    controller = ControllerHistoricoAvaliacoes(id_escola=id_escola)
    resultado = controller.listar_historico_avaliacoes_por_escola()
    return make_response(resultado)


@user_rout_bp.route("/historico/avaliacoes/materia/<int:id_materia>", methods=["GET"])
def historico_avaliacoes_por_materia(id_materia):
    """
    Retorna o histórico de avaliações de uma matéria.
    """
    controller = ControllerHistoricoAvaliacoes(id_materia=id_materia)
    resultado = controller.listar_historico_avaliacoes_por_materia()
    return make_response(resultado)

# --------------- RANKING DE AVALIAÇÕES ---------------

@user_rout_bp.route("/ranking/alunos", methods=["GET"])
def ranking_alunos():
    """
    Retorna o ranking geral dos alunos por média de nota.
    """
    controller = ControllerRankingAvaliacao()
    resultado = controller.ranquear_alunos_geral()
    return make_response(resultado)


@user_rout_bp.route("/ranking/turmas", methods=["GET"])
def ranking_turmas():
    """
    Retorna o ranking geral das turmas por média de nota.
    """
    controller = ControllerRankingAvaliacao()
    resultado = controller.ranquear_turmas_geral()
    return make_response(resultado)


@user_rout_bp.route("/ranking/escolas", methods=["GET"])
def ranking_escolas():
    """
    Retorna o ranking geral das escolas por média de nota.
    """
    controller = ControllerRankingAvaliacao()
    resultado = controller.ranquear_escolas_geral()
    return make_response(resultado)


@user_rout_bp.route("/ranking/materias/escola/<int:id_escola>", methods=["GET"])
def ranking_materias_por_escola(id_escola):
    """
    Retorna o ranking das matérias de uma escola por média de nota.
    """
    controller = ControllerRankingAvaliacao(id_escola=id_escola)
    resultado = controller.ranquear_materias_geral()
    return make_response(resultado)

@user_rout_bp.route("/dashboard/escola/<int:id_escola>", methods=["GET"])
def dashboard_escola(id_escola):
    """
    Rota para retornar o dashboard de uma escola específica.
    """
    controller = ControllerDashboard(id_escola=id_escola)
    dashboard = controller.gerar_dashboard_escola()
    return dashboard, 200, {"Content-Type": "application/json"}


@user_rout_bp.route("/dashboard/municipio/<int:id_municipio>", methods=["GET"])
def dashboard_municipio(id_municipio):
    """
    Rota para retornar o dashboard de um município específico.
    """
    controller = ControllerDashboard(id_municipio=id_municipio)
    dashboard = controller.gerar_dashboard_municipio()
    return dashboard, 200, {"Content-Type": "application/json"}