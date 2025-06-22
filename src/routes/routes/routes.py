from flask import Blueprint

from user_cases import ControllerAcesso
user_rout_bp = Blueprint("user_routes", __name__)


@user_rout_bp.route("/acesso/<string:user_name>/<string:passworld>", methods=["GET"])
def login(user_name: str, passworld: str) -> str:
    informacao = ControllerAcesso(user_name= user_name, passworld= passworld).return_user_ou_texto()
    return informacao
