from typing import Optional
from user_cases.avaliacao import ControllerRankingAvaliacao, ControllerHistoricoAvaliacoes

class ControllerDashboard:
    """Classe responsável por gerar dashboards para escolas e municípios."""

    def __init__(self, id_escola: Optional[int] = None, id_municipio: Optional[int] = None) -> None:
        """Inicializa o controlador de dashboard com o ID da escola ou município."""
        self.id_escola = id_escola
        self.id_municipio = id_municipio

    def gerar_dashboard_escola(self) -> str:
        """ Gera o dashboard para a escola, incluindo informações sobre alunos, faltas e notas."""
    
    def gerar_dashboard_municipio(self) -> str:
        """
        Gera o dashboard para o município contendo informações agregadas de várias escolas associadas a ele.
        """
        return "Dashboard do Município"
    
