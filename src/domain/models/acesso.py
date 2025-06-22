from typing import Optional


class Acesso:
    def __init__(self, user: str, password: str) -> None:
        if None in [user, password]:
            raise ValueError("Valor nulo em credenciais, validar informação")

        self.user: str = user
        self.senha: str = password
        self.id_user: Optional[int] = None
        self.nome_cargo: Optional[str] = None

    def __repr__(self) -> str:
        return f"<Acesso user={self.user}, cargo='{self.nome_cargo}'>"
