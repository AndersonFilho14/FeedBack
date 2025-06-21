from config import log

from domain import Acesso

class ControllerAcesso:
    def __init__(self, user_name: str, passworld: str)->None:
        log.trace("Iniciando a validação do logger")
        Acesso(user= user_name, password= passworld)
        log.trace("Não levantou error")
