from config import log  # noqa : F401

from infra.repositories import ConsultarAcesso, ConsultarUser  # noqa : F401
from infra.db.models_data import (
    Professor as ProfessorData,  # noqa : F401
    Escola as EscolaData,  # noqa : F401
    Municipio as MunicipioData,) # noqa : F401


class VisualizarAlunos:
    def __init__(
        self,
    ):
        pass
