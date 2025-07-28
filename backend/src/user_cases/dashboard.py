import json
from typing import Optional
from user_cases.avaliacao import ControllerRankingAvaliacao
from user_cases.aluno import ControllerAlunoIA

class ControllerDashboard:
    """Classe responsável por gerar dashboards para escolas e municípios."""

    def __init__(self, id_escola: Optional[int] = None, id_municipio: Optional[int] = None) -> None:
        """Inicializa o controlador de dashboard com o ID da escola ou município."""
        self.id_escola = id_escola
        self.id_municipio = id_municipio

    def gerar_dashboard_escola(self) -> str:
        """Gera o dashboard para a escola, incluindo rankings e dados de IA e atividades."""

        # --- Rankings de avaliação ---
        controller = ControllerRankingAvaliacao(id_escola=self.id_escola)
        ranking_alunos = json.loads(controller.ranquear_alunos_por_escola())
        ranking_turmas = json.loads(controller.ranquear_turmas_por_escola())
        ranking_materias = json.loads(controller.ranquear_materias_por_escola())
        ranking_tipos_avaliacao = json.loads(controller.ranquear_por_tipo_avaliacao_por_escola())
        ranking_professores = json.loads(controller.ranquear_professores_por_escola())

        # --- Distribuição IA e atividades ---
        notas_ia = json.loads(ControllerAlunoIA.obter_distribuicao_notas_ia_escola(id_escola=self.id_escola))
        notas_por_sexo = json.loads(ControllerAlunoIA.obter_distribuicao_notas_por_sexo_escola(id_escola=self.id_escola))
        alunos_por_esporte = json.loads(ControllerAlunoIA.obter_qtd_alunos_por_esporte_escola(id_escola=self.id_escola))
        alunos_por_extra = json.loads(ControllerAlunoIA.obter_qtd_alunos_por_extra_curricular_escola(id_escola=self.id_escola))
        alunos_por_musica = json.loads(ControllerAlunoIA.obter_qtd_alunos_por_aula_musica_escola(id_escola=self.id_escola))
        alunos_por_particular = json.loads(ControllerAlunoIA.obter_qtd_alunos_por_aulas_particulares_escola(id_escola=self.id_escola))

        # --- JSON Final agrupado ---
        dashboard = {
            "ranking": {
                "alunos": ranking_alunos,
                "turmas": ranking_turmas,
                "materias": ranking_materias,
                "tipos_avaliacao": ranking_tipos_avaliacao,
                "professores": ranking_professores
            },
            "ia": {
                "distribuicao_notas": notas_ia,
                "por_sexo": notas_por_sexo
            },
            "atividades": {
                "esportes": alunos_por_esporte,
                "extra_curriculares": alunos_por_extra,
                "aulas_musica": alunos_por_musica,
                "aulas_particulares": alunos_por_particular
            }
        }

        return json.dumps(dashboard, ensure_ascii=False, indent=4)

    def gerar_dashboard_municipio(self) -> str:
        """
        Gera o dashboard para o município contendo informações agregadas de várias escolas associadas a ele.
        """

        # --- Rankings gerais ---
        controller = ControllerRankingAvaliacao()
        ranking_alunos = json.loads(controller.ranquear_alunos_geral())
        ranking_turmas = json.loads(controller.ranquear_turmas_geral())
        ranking_escolas = json.loads(controller.ranquear_escolas_geral())
        ranking_materias = json.loads(controller.ranquear_materias_geral())
        ranking_tipo_avaliacao = json.loads(controller.ranquear_por_tipo_avaliacao_geral())

        # --- Dados preditivos IA (gerais) ---
        notas_ia_geral = json.loads(ControllerAlunoIA.obter_distribuicao_notas_ia_geral())
        notas_ia_por_sexo = json.loads(ControllerAlunoIA.obter_distribuicao_notas_por_sexo_geral())

        # --- Participações em atividades (gerais) ---
        esporte_geral = json.loads(ControllerAlunoIA.obter_qtd_alunos_por_esporte_geral())
        extra_geral = json.loads(ControllerAlunoIA.obter_qtd_alunos_por_extra_curricular_geral())
        musica_geral = json.loads(ControllerAlunoIA.obter_qtd_alunos_por_aula_musica_geral())
        particulares_geral = json.loads(ControllerAlunoIA.obter_qtd_alunos_por_aulas_particulares_geral())

        # --- JSON Final organizado ---
        dashboard = {
            "ranking": {
                "alunos": ranking_alunos,
                "turmas": ranking_turmas,
                "escolas": ranking_escolas,
                "materias": ranking_materias,
                "tipos_avaliacao": ranking_tipo_avaliacao
            },
            "ia": {
                "distribuicao_notas": notas_ia_geral,
                "por_sexo": notas_ia_por_sexo
            },
            "atividades": {
                "esportes": esporte_geral,
                "extra_curriculares": extra_geral,
                "aulas_musica": musica_geral,
                "aulas_particulares": particulares_geral
            }
        }

        return json.dumps(dashboard, ensure_ascii=False, indent=4)
        