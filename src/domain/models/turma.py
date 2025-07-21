from typing import List

class Turma:
    def __init__(self, nome: str, ano_letivo: int, id_escola: int, id: int, ids_professores: List[int], ids_alunos = List[int]):
        self.id = id
        self.nome = nome
        self.ano_letivo = ano_letivo
        self.id_escola = id_escola
        self.ids_professores = ids_professores
        self.ids_alunos = ids_alunos