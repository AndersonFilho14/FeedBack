from datetime import date

class Avaliacao:
    """
    Representa uma avaliação com seus dados.
    Esta classe valida os tipos de dados recebidos em sua inicialização.
    """
    def __init__(
        self,
        id: int,
        tipo_avaliacao: str,
        data_avaliacao: date,
        nota: float,
        id_aluno: int,
        id_professor: int,
        id_disciplina: int,
        id_materia: int,
        id_turma: int,
    ) -> None:

        # --- Bloco de Validação de Tipos ---

        # Valida campos que devem ser strings
        if not isinstance(tipo_avaliacao, str):
            raise ValueError(f"O campo 'tipo_avaliacao' deve ser uma string (str), mas recebeu {type(tipo_avaliacao).__name__}")

        # Valida campos que devem ser inteiros
        for campo_nome, valor in {
            "id": id, "id_aluno": id_aluno, "id_professor": id_professor,
            "id_disciplina": id_disciplina, "id_materia": id_materia, "id_turma": id_turma
        }.items():
            if not isinstance(valor, int):
                raise ValueError(f"O campo '{campo_nome}' deve ser um inteiro (int), mas recebeu {type(valor).__name__}")

        # Valida campo que deve ser float
        if not isinstance(nota, float):
             raise ValueError(f"O campo 'nota' deve ser um número decimal (float), mas recebeu {type(nota).__name__}")

        # Valida campo que deve ser do tipo data
        if not isinstance(data_avaliacao, date):
            raise ValueError(f"O campo 'data_avaliacao' deve ser um objeto data (date), mas recebeu {type(data_avaliacao).__name__}")


        # --- Atribuição dos Atributos ---
        self.id = id
        self.tipo_avaliacao = tipo_avaliacao
        self.data_avaliacao = data_avaliacao
        self.nota = nota
        self.id_aluno = id_aluno
        self.id_professor = id_professor
        self.id_disciplina = id_disciplina
        self.id_materia = id_materia
        self.id_turma = id_turma

    def __repr__(self) -> str:
        """
        Retorna uma representação em string do objeto, útil para debugging.
        """
        return (
            f"<Avaliacao id={self.id}, aluno_id={self.id_aluno}, "
            f"tipo='{self.tipo_avaliacao}', nota={self.nota}>"
        )
