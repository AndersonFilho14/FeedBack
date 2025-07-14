class Municipio:

    def __init__(self, nome: str, estado: str, regiao: str, id_municipio: int):
        self.id = id_municipio
        self.nome = nome
        self.estado = estado
        self.regiao = regiao