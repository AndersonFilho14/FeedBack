from flask import Blueprint, make_response, jsonify, request

from user_cases import (
    ControllerAcesso,
    ControllerProfessorAtualizarFalta,
    ControllerProfessorAlunosVinculados,
    ControllerProfessorAdicionarNotaAoAluo,  # noqa F401
    ControllerConsultarMateriaEDisciplinasVinculadasAoProfessor,
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


@user_rout_bp.route(
    "/professor/atualizar_quantidade_de_faltas_para_aluno/<string:id_professor>/<string:id_aluno>/<string:faltas>",
    methods=["GET"],
)
def professor_atualizar_quantidade_de_faltas_para_unico_aluno(
    id_professor: str, id_aluno: str, faltas: str
) -> str:
    """Atualiza a quantidade de faltas de um aluno específico.

    .. warning::
        Este endpoint utiliza o método GET para uma operação de escrita,
        o que não é uma prática recomendada. O ideal seria migrar para
        um método PUT ou POST, com os dados enviados no corpo da requisição.

    :param id_professor: O ID do professor que está atualizando a falta.
    :param id_aluno: O ID do aluno que terá as faltas atualizadas.
    :param faltas: A nova quantidade total de faltas a ser registrada.
    :return: Uma resposta JSON confirmando o sucesso ou a falha da operação.
    """
    controller = ControllerProfessorAtualizarFalta(
        id_professor=id_professor, id_aluno=id_aluno, nova_quantidade_de_faltas=faltas
    )
    retorno = controller.fluxo_crud_de_nota_do_aluno()
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

@user_rout_bp.route("/professor/adicionar_nota", methods=["POST"])
def prof_aplicar_nota_a_aluno():
    """Endpoint para que um professor adicione uma nota de avaliação a um aluno.

    Esta rota recebe um payload JSON com os detalhes da avaliação, passa
    para um controller que orquestra a validação e a inserção dos dados,
    e retorna o resultado da operação em formato JSON.

    **JSON Body Esperado:**
    ```json
    {
        "id_professor": 1,
        "id_aluno": 1,
        "id_materia": 1,
        "id_disciplina": 1,
        "tipo_avaliacao": "1Va",
        "nota": 8.5
    }
    ```

    :return: Uma resposta JSON contendo o resultado da operação.
             - Em caso de sucesso (201 Created), retorna: `{"sucesso": "mensagem"}`
             - Em caso de falha (400 Bad Request), retorna: `{"erro": "mensagem"}`
    """
    post: dict = request.json
    controller = ControllerProfessorAdicionarNotaAoAluo(post= post)
    retorno = controller.fluxo_para_adicionar()
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
