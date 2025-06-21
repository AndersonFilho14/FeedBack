class Acesso:

    def __init__(self, id:int, user: str, password: str) -> None:
        if None in [user, password]:
            raise ValueError("Valor nulo em credenciais, validar informação")

        self.id: str = id
        self.user: str = user
        self.senha: str = password
