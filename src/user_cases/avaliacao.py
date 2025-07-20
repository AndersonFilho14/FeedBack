import json

from typing import List, Dict, Optional
from collections import defaultdict

from infra.repositories.avaliacao_data import AvaliacaoRepository
from domain.models.avaliacao import Avaliacao
from infra.db.models_data import Avaliacao as AvaliacaoData
from infra.repositories import ConsultaAlunoBanco, ConsultaEscolaBanco, ConsultaTurmaBanco, ConsultaMateriaBanco, ConsultarProfessor

class ControllerRankingAvaliacao:
    """Classe responsável por gerar rankings de desempenho por aluno, turma, escola e matéria."""

    def ranquear_alunos(self) -> str:
        """Ranqueia todos os alunos com base na média das avaliações."""
        avaliacoes_data = AvaliacaoRepository().buscar_todas()
        avaliacoes_dom = FormatarAvaliacao().formatar_avaliacao_data_para_dominio(avaliacoes_data)
        ranking = RanquearAvaliacao.raquear_avaliacoes(avaliacoes_dom, criterio = "id_aluno")
        return FormatarAvaliacao().gerar_json_ranqueado(ranking = ranking, criterio = "ranking_alunos")

    def ranquear_turmas(self) -> str:
        """Ranqueia todas as turmas com base na média das avaliações."""
        avaliacoes_data = AvaliacaoRepository().buscar_todas()
        avaliacoes_dom = FormatarAvaliacao().formatar_avaliacao_data_para_dominio(avaliacoes_data)
        ranking = RanquearAvaliacao.raquear_avaliacoes(avaliacoes_dom, criterio = "id_turma")
        return FormatarAvaliacao().gerar_json_ranqueado(ranking = ranking, criterio = "ranking_turmas")

    def ranquear_escolas(self) -> str:
        """Ranqueia todas as escolas com base na média das avaliações."""
        avaliacoes_data = AvaliacaoRepository().buscar_todas()
        avaliacoes_dom = FormatarAvaliacao().formatar_avaliacao_data_para_dominio(avaliacoes_data)
        ranking = RanquearAvaliacao.raquear_por_escola(avaliacoes_dom)
        return FormatarAvaliacao().gerar_json_ranqueado(ranking = ranking, criterio = "ranking_escolas")
    
    def ranquear_materias(self) -> str:
        """Retorna JSON ranqueado com as disciplinas de uma escola por média de nota."""
        avaliacoes_data = AvaliacaoRepository().buscar_todas()
        avaliacoes_dom = FormatarAvaliacao().formatar_avaliacao_data_para_dominio(avaliacoes_data)
        ranking = RanquearAvaliacao.raquear_avaliacoes(avaliacoes_dom, "id_materia")
        return FormatarAvaliacao().gerar_json_ranqueado(ranking = ranking, criterio = "ranking_materias")


class RanquearAvaliacao:
    """Classe para calcular médias e ranquear por aluno, turma ou escola."""

    def raquear_avaliacoes(avaliacoes: List[Avaliacao], criterio: str) -> List[Dict]:
        """Ranqueia com base no critério (id_turma, id_aluno, id_disciplina)."""
        agrupado = defaultdict(list)
        for avaliacao in avaliacoes:
            chave_do_grupo = getattr(avaliacao, criterio)
            agrupado[chave_do_grupo].append(avaliacao)

        medias = RanquearAvaliacao._calcular_media(agrupado)
        return sorted(medias, key=lambda x: x["media"], reverse=True)
    
    def raquear_por_escola(avaliacoes: List[Avaliacao]) -> List[Dict]:
        """Ranqueia avaliações por escola, associando aluno → escola."""
    
        agrupado = defaultdict(list)

        for avaliacao in avaliacoes:
            aluno = ConsultaAlunoBanco(id_aluno = avaliacao.id_aluno).buscar_aluno_por_id()
            if aluno:
                id_escola = aluno.id_escola
                agrupado[id_escola].append(avaliacao)

        medias = RanquearAvaliacao._calcular_media(agrupado)
        return sorted(medias, key=lambda x: x["media"], reverse=True)
    
    def _calcular_media(agrupado: Dict[int, List[Avaliacao]]) -> List[Dict]:
        """Calcula a média e quantidade de avaliações de cada grupo."""
        resultado = []
        for id_grupo, avaliacoes in agrupado.items():
            total = len(avaliacoes)
            media = round(sum(a.nota for a in avaliacoes) / total, 2)
            resultado.append({
                "id": id_grupo,
                "media": media,
                "quantidade_avaliacoes": total
            })
        return sorted(resultado, key=lambda x: x["media"], reverse=True)


class ControllerHistoricoDesempenho:
    """Classe responsável por listar o histórico de avaliações por aluno, turma, escola ou matéria."""

    def __init__(self, id_aluno: Optional[int] = None,
                       id_turma: Optional[int] = None,
                       id_escola: Optional[int] = None,
                       id_professor: Optional[int] = None,) -> None:
                       
        self.__id_aluno = id_aluno
        self.__id_turma = id_turma
        self.__id_escola = id_escola
        self.__id_professor = id_professor

    def listar_historico_avaliacoes_por_aluno(self) -> str:
        """Retorna JSON com avaliações de um aluno."""
        avaliacoes_data = AvaliacaoRepository().buscar_por_aluno(self.__id_aluno)
        avaliacoes_dom = FormatarAvaliacao().formatar_avaliacao_data_para_dominio(avaliacoes_data)
        return FormatarAvaliacao().gerar_json(avaliacoes_dom)

    def listar_historico_avaliacoes_por_turma(self) -> str:
        """Retorna JSON com avaliações de uma turma."""
        avaliacoes_data = AvaliacaoRepository().buscar_por_turma(self.__id_turma, self.__id_professor)
        avaliacoes_dom = FormatarAvaliacao().formatar_avaliacao_data_para_dominio(avaliacoes_data)
        return FormatarAvaliacao().gerar_json(avaliacoes_dom)

    def listar_historico_avaliacoes_por_escola(self) -> str:
        """Retorna JSON com avaliações de uma escola."""
        avaliacoes_data = AvaliacaoRepository().buscar_por_escola(self.__id_escola)
        avaliacoes_dom = FormatarAvaliacao().formatar_avaliacao_data_para_dominio(avaliacoes_data)
        return FormatarAvaliacao().gerar_json(avaliacoes_dom)
    

class FormatarAvaliacao:
    """Formata AvaliacaoData → Avaliacao (domínio) → JSON."""

    def formatar_avaliacao_data_para_dominio(self, avaliacoes_data: List[AvaliacaoData]) -> List[Avaliacao]:
        """Converte uma lista de AvaliacaoData (ORM) para Avaliacao (domínio)."""
        avaliacoes_dom = []
        for avaliacao in avaliacoes_data:
            avaliacao = Avaliacao(
                id = avaliacao.id,
                tipo_avaliacao = avaliacao.tipo_avaliacao,
                data_avaliacao = avaliacao.data_avaliacao,
                nota = avaliacao.nota,
                id_aluno = avaliacao.id_aluno,
                id_professor = avaliacao.id_professor,
                id_disciplina = avaliacao.id_disciplina,
                id_materia = avaliacao.id_materia,
                id_turma = avaliacao.id_turma
            )
            avaliacoes_dom.append(avaliacao)
        return avaliacoes_dom

    def gerar_json(self, avaliacoes_dominio: List[Avaliacao]) -> str:
        """Gera JSON com lista de avaliações formatadas, incluindo nomes associados."""
        lista = []

        for avaliacao in avaliacoes_dominio:
            aluno = ConsultaAlunoBanco(id_aluno=avaliacao.id_aluno).buscar_aluno_por_id()
            professor = ConsultarProfessor(id_professor=avaliacao.id_professor).get_professor_retorno()
            disciplina = ConsultaMateriaBanco().buscar_disciplina_por_id(id_disciplina=avaliacao.id_disciplina)
            materia = ConsultaMateriaBanco().buscar_materia_por_id(avaliacao.id_materia)
            turma = ConsultaTurmaBanco().buscar_por_id(avaliacao.id_turma)

            nome_aluno = aluno.nome if aluno else "Desconhecido"
            nome_professor = professor.nome if professor else "Desconhecido"
            nome_disciplina = disciplina.nome_disciplina if disciplina else "Desconhecida"
            nome_materia = materia.nome_materia if materia else "Desconhecida"
            nome_turma = turma.nome if turma else "Desconhecida"
            escola = ConsultaEscolaBanco().buscar_por_id(aluno.id_escola)
            nome_escola = escola.nome if escola else "Desconhecida"


            lista.append({
                "id": avaliacao.id,
                "tipo_avaliacao": avaliacao.tipo_avaliacao,
                "data_avaliacao": avaliacao.data_avaliacao.isoformat(),
                "nota": avaliacao.nota,
                "id_aluno": avaliacao.id_aluno,
                "nome_aluno": nome_aluno,
                "nome_professor": nome_professor,
                "nome_disciplina": nome_disciplina,
                "nome_materia": nome_materia,
                "nome_turma": nome_turma,
                "nome_escola": nome_escola
            })

        return json.dumps({"avaliacoes": lista}, ensure_ascii=False, indent=4)
    
    def gerar_json_ranqueado(self, ranking: List[Dict], criterio: str, nome: str = "ranking") -> str:
        """Gera JSON com a lista ranqueada, incluindo nomes e quantidade de avaliações."""

        lista_formatada = []

        if criterio == "ranking_alunos":
            for item in ranking:
                aluno = ConsultaAlunoBanco(id_aluno=item["id"]).buscar_aluno_por_id()
                
                if aluno is not None:
                    turma = ConsultaTurmaBanco().buscar_por_id(aluno.id_turma)
                    escola = ConsultaEscolaBanco().buscar_por_id(aluno.id_escola)
                    
                    if turma and escola is not None:
                        lista_formatada.append({
                            "id": aluno.id,
                            "nome_aluno": aluno.nome,
                            "nome_turma": turma.nome if turma else "Desconhecida",
                            "nome_escola": escola.nome if escola else "Desconhecida",
                            "media": item["media"],
                            "quantidade_avaliacoes": item["quantidade_avaliacoes"]
                        })

        elif criterio == "ranking_turmas":
            for item in ranking:
                turma = ConsultaTurmaBanco().buscar_por_id(item["id"])

                if turma is not None:
                    escola = ConsultaEscolaBanco().buscar_por_id(turma.id_escola)

                    if escola is not None: 
                        lista_formatada.append({
                            "id": turma.id,
                            "nome_turma": turma.nome,
                            "nome_escola": escola.nome if escola else "Desconhecida",
                            "media": item["media"],
                            "quantidade_avaliacoes": item["quantidade_avaliacoes"]
                        })

        elif criterio == "ranking_escolas":

            for item in ranking:
                escola = ConsultaEscolaBanco().buscar_por_id(item["id"])
                if escola is not None:
                    lista_formatada.append({
                        "id": escola.id,
                        "nome_escola": escola.nome,
                        "media": item["media"],
                        "quantidade_avaliacoes": item["quantidade_avaliacoes"]
                    })

        elif criterio == "ranking_materias":
            for item in ranking:
                materia = ConsultaMateriaBanco().buscar_materia_por_id(item["id"])
                if materia is not None:
                    lista_formatada.append({
                        "id": materia.id,
                        "nome_materia": materia.nome_materia,
                        "media": item["media"],
                        "quantidade_avaliacoes": item["quantidade_avaliacoes"]
                    })
        
        return json.dumps({nome: lista_formatada}, ensure_ascii=False, indent=4)
