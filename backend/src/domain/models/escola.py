from typing import Optional


class Escola:
    def __init__(self, nome: str, id_municipio: int, id: int, nome_usuario: Optional[str] = None, senha: Optional[str] = None):
        self.id = id
        self.nome = nome
        self.id_municipio = id_municipio
        self.nome_usuario = nome_usuario
        self.senha = senha
