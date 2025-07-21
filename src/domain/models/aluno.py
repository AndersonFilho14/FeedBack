from datetime import date

class Aluno:
    def __init__(
        self,
        id: int,
        nome: str,
        data_nascimento: date,
        sexo: str,
        cpf: str,
        nacionalidade: str,
        faltas: int,
        nota_score_preditivo: float,
        id_escola: int,
        id_turma: int,
        id_responsavel: int,
    ) -> None:
        """Model de aluno com validações de tipo."""

        for item in [id, faltas, id_escola, id_turma, id_responsavel]:
            if not isinstance(item, int):
                raise ValueError("Valor inválido: esperado inteiro")

        for item in [nome, cpf, sexo, nacionalidade]:
            if not isinstance(item, str):
                raise ValueError("Valor inválido: esperado string")

        if not isinstance(data_nascimento, date):
            raise ValueError("data_nascimento deve ser um objeto do tipo `date`")

        self.id = id
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.sexo = sexo
        self.cpf = cpf
        self.nacionalidade = nacionalidade
        self.faltas = faltas
        self.nota_score_preditivo = nota_score_preditivo
        self.id_escola = id_escola
        self.id_turma = id_turma
        self.id_responsavel = id_responsavel

    def __repr__(self):
        return (
            f"<Aluno id={self.id} | nome={self.nome} | cpf={self.cpf}"
            f"| faltas={self.faltas} | nota_score_preditivo={self.nota_score_preditivo} "
            f"| id_escola={self.id_escola} | id_turma={self.id_turma} | id_responsavel={self.id_responsavel} "
            f"| data_nascimento={self.data_nascimento} | sexo={self.sexo} | nacionalidade={self.nacionalidade} "
        )
