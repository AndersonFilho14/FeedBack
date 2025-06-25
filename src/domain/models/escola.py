from typing import Optional

class Escola:
    def __init__(self, nome: str, id_municipio: int, id: Optional[int] = None):
        self.id = id
        self.nome = nome
        self.id_municipio = id_municipio