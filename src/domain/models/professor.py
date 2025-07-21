from datetime import date

class Professor:
    def __init__(
        self, id: int,
        nome: str,
        cpf: str,
        cargo: str,
        id_escola: int,
        data_nascimento: date,
        sexo: str,
        nacionalidade: str,
        estado_civil: str,
        telefone: str,
        email: str,
        senha: str
    ) -> None:
        for item in [nome, cpf, cargo, sexo, nacionalidade, 
                     estado_civil, telefone, email, senha]:
            if not isinstance(item, str):
                raise ValueError("O valor não é str")

        for item in [id, id_escola]:
            if not isinstance(item, int):
                raise ValueError("O valor não é int")
            
        if not isinstance(data_nascimento, date):
            raise ValueError("data_nascimento deve ser um objeto do tipo `date`")

        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.cargo = cargo
        self.id_escola = id_escola
        self.data_nascimento = data_nascimento
        self.sexo = sexo
        self.nacionalidade = nacionalidade
        self.estado_civil = estado_civil
        self.telefone = telefone
        self.email = email
        self.senha = senha

    def __repr__(self) -> str:
        return f"<Professor id={self.id}, nome='{self.nome}', cpf='{self.cpf}', cargo='{self.cargo}', id_escola={self.id_escola}, data_nascimento={self.data_nascimento}, sexo='{self.sexo}', nacionalidade='{self.nacionalidade}', estado_civil='{self.estado_civil}', telefone='{self.telefone}', email='{self.email}', senha='{self.senha}'>"
