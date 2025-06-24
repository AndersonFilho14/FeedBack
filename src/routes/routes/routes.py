from flask import Blueprint

from user_cases import ControllerAcesso, ControllerProfessorAlunosVinculados

user_rout_bp = Blueprint("user_routes", __name__)


@user_rout_bp.route("/acesso/<string:user_name>/<string:passworld>", methods=["GET"])
def login(user_name: str, passworld: str) -> str:
    informacao = ControllerAcesso(
        user_name=user_name, passworld=passworld
    ).return_user_ou_texto()
    return informacao


@user_rout_bp.route("/professor/visualizar_alunos/<string:id_professor>", methods=["GET"])
def professor_visualizar_alunos_vinculados_a_ele(id_professor: str) -> str:
    retorno = ControllerProfessorAlunosVinculados(
        id_professor=id_professor
    ).fluxo_para_consultar_professor_e_seus_alunos()
    return retorno


# prof aplicar falta a aluno
# prof aplicar nota a aluno
#
