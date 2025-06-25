from typing import Optional


class Materia:
    def __init__(self, nome: str, id_professor: int, id_disciplina: int, id_materia: Optional[int] = None) -> None:
        self.id_materia = id_materia
        self.nome = nome
        self.id_disciplina = id_disciplina
        self.id_professor = id_professor

