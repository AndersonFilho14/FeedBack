class Aluno:
    def __init__(
        self,
        id: int,
        nome: str,
        cpf: str,
        idade: int,
        faltas: int,
        nota_score_preditivo: float,
        id_escola: int,
        id_turma: int,
        id_responsavel: int,
    ) -> None:
        """Model de aluno

        :param int id: id l
        :param str nome: _description_
        :param str cpf: _description_
        :param int idade: _description_
        :param int faltas: _description_
        :param float nota_score_preditivo: _description_
        :param int id_escola: _description_
        :param int id_turma: _description_
        :param int id_responsavel: _description_
        :raises ValueError: _description_
        :raises ValueError: _description_
        """

        for item in [id, idade, faltas, id_escola, id_turma, id_responsavel]:
            if not isinstance(item, int):
                raise ValueError(
                    "Valor ao para fazer aluno invalido. Deveria ser um inteiro"
                )

        for item in [nome, cpf]:
            if not isinstance(item, str):
                raise ValueError(
                    "Valor ao para fazer aluno invalido. Deveria ser um string"
                )

        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.idade = idade
        self.faltas = faltas
        self.nota_score_preditivo = nota_score_preditivo
        self.id_escola = id_escola
        self.id_turma = id_turma
        self.id_responsavel = id_responsavel

    def __repr__(self):
        return f"< Aluno : id = {self.id} | nome = {self.nome} | cpf = {self.cpf} | idade = {self.idade} | faltas = {self.faltas} | nota_score_preditivo = {self.nota_score_preditivo} | id_escola = {self.id_escola} | id_turma = {self.id_turma} | id_responsavel = {self.id_responsavel} > "
