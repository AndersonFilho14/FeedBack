from flask import Blueprint, make_response, jsonify

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
    informacao: str = ControllerAcesso(
        user_name=user_name, passworld=passworld
    ).return_user_ou_texto()
    return informacao


@user_rout_bp.route(
    "/professor/visualizar_alunos/<string:id_professor>", methods=["GET"]
)
def professor_visualizar_alunos_vinculados_a_ele(id_professor: str) -> str:
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
    controller = ControllerProfessorAtualizarFalta(
        id_professor=id_professor, id_aluno=id_aluno, nova_quantidade_de_faltas=faltas
    )
    retorno = controller.fluxo_crud_de_nota_do_aluno()
    return retorno

@user_rout_bp.route('/materia_e_disciplina_que_o_professor_ensina/<string:id_professor>', methods=['GET'])
def consultar_materia_e_disciplina_do_professor(id_professor: str):
    consultar = ControllerConsultarMateriaEDisciplinasVinculadasAoProfessor(id_professor=id_professor)
    retorno = consultar.fluxo_para_consultar()
    print(retorno)
    print(type(retorno))
    return make_response(jsonify(retorno))

# @user_rout_bp.route("/professor/adicionar_nota", methods=["POST"])
# def prof_aplicar_nota_a_aluno():
#     post: dict = request.json
#     controller = ControllerProfessorAdicionarNotaAoAluo(post= post)
#     controller.fluxo_para_adicionar()
#     retorno = "Retorno ainda não feito para prof_aplicar_nota_a_aluno"
#     return make_response(jsonify(retorno))
#


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
