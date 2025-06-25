class Professor:
    def __init__(
        self, id: int, nome: str, cpf: str, cargo: str, id_escola: int
    ) -> None:
        for item in [nome, cpf, cargo]:
            if not isinstance(item, str):
                raise ValueError("O valor não é str")

        for item in [id, id_escola]:
            if not isinstance(item, int):
                raise ValueError("O valor não é int")

        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.cargo = cargo
        self.id_escola = id_escola

    def __repr__(self) -> str:
        return f"<Professor id={self.id}, nome='{self.nome}'>"
