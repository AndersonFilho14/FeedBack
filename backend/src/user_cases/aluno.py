from typing import Optional
from domain.models import Aluno, Responsavel
from infra.repositories import AlunoRepository, ConsultaEscolaBanco, ConsultarProfessor, ConsultaDadosAluno, AlunoIARepository, ConsultaAlunoBanco
from config import log

from utils.validarCampos import ValidadorCampos
from utils.processIA import Aluno as AlunoIA, processIA
from infra.db.models_data import Aluno as AlunoData
from typing import Optional, List
import json
from datetime import datetime, date

class ControllerAluno:
    """Controlador responsável por coordenar operações de CRUD relacionadas a alunos."""

    def __init__(
        self,
        nome: Optional[str] = None,
        data_nascimento: Optional[str] = None,
        sexo: Optional[str] = None,
        cpf: Optional[str] = None,
        nacionalidade: Optional[str] = None,
        nome_responsavel: Optional[str] = None,
        numero_responsavel: Optional[str] = None,
        faltas: Optional[int] = 0,
        nota_score_preditivo: Optional[float] = None,
        id_escola: Optional[int] = None,
        id_turma: Optional[int] = None,
        id_aluno: Optional[int] = None,
        etnia: Optional[int] = None,
        educacao_pais: Optional[int] = None,
        tempo_estudo_semanal: Optional[float] = None,
        apoio_pais: Optional[int] = None,
        aulas_particulares: Optional[int] = None,
        extra_curriculares: Optional[int] = None,
        esportes: Optional[int] = None,
        aula_musica: Optional[int] = None,
        voluntariado: Optional[int] = None,
    ) -> None:
        self.__nome = nome
        self.__data_nascimento = data_nascimento
        self.__sexo = sexo
        self.__cpf = cpf
        self.__nacionalidade = nacionalidade
        self.__nome_responsavel = nome_responsavel
        self.__numero_responsavel = numero_responsavel
        self.__faltas = faltas
        self.__nota_score = nota_score_preditivo
        self.__id_escola = id_escola
        self.__id_turma = id_turma
        self.__id_aluno = id_aluno
        self.__etnia = etnia
        self.__educacao_pais = educacao_pais
        self.__tempo_estudo_semanal = tempo_estudo_semanal
        self.__apoio_pais = apoio_pais
        self.__aulas_particulares = aulas_particulares
        self.__extra_curriculares = extra_curriculares
        self.__esportes = esportes
        self.__aula_musica = aula_musica
        self.__voluntariado = voluntariado

    def criar_aluno(self) -> str:
        resultado = CriarAlunoNoBanco(
            nome=self.__nome,
            data_nascimento=self.__data_nascimento,
            sexo=self.__sexo,
            cpf=self.__cpf,
            nacionalidade=self.__nacionalidade,
            nome_responsavel = self.__nome_responsavel, 
            numero_responsavel= self.__numero_responsavel,
            faltas=self.__faltas,
            nota_score_preditivo=self.__nota_score,
            id_escola=self.__id_escola,
            id_turma=self.__id_turma,
            etnia=self.__etnia,
            educacao_pais=self.__educacao_pais,
            tempo_estudo_semanal=self.__tempo_estudo_semanal,
            apoio_pais=self.__apoio_pais,
            aulas_particulares=self.__aulas_particulares,
            extra_curriculares=self.__extra_curriculares,
            esportes=self.__esportes,
            aula_musica=self.__aula_musica,
            voluntariado=self.__voluntariado,
        ).executar()
        return resultado

    def listar_alunos_Escola(self) -> str:
        alunos_data = ListarAlunosNoBanco(id_escola = self.__id_escola, id_turma = None).listar_alunos_escola()
        formatter = FormatarAluno()
        alunos_dominio = formatter.formatar_aluno_data_para_dominio(alunos_data = alunos_data)
        return formatter.gerar_json(alunos_dominio = alunos_dominio)
        
    def listar_alunos_turma(self) -> str:
        alunos_data = ListarAlunosNoBanco(id_escola = None, id_turma = self.__id_turma).listar_alunos_turma()
        formatter = FormatarAluno()
        alunos_dominio = formatter.formatar_aluno_data_para_dominio(alunos_data = alunos_data)
        return formatter.gerar_json(alunos_dominio = alunos_dominio)

    def atualizar_aluno(self) -> str:
        return AtualizarAlunoNoBanco(
            id_aluno=self.__id_aluno,
            novo_nome=self.__nome,
            novo_cpf=self.__cpf,
            nova_data_nascimento=self.__data_nascimento,
            novo_sexo=self.__sexo,
            nova_nacionalidade=self.__nacionalidade, 
            novo_nome_responsavel=self.__nome_responsavel,
            novo_numero_responsavel=self.__numero_responsavel,  
            nova_etnia=self.__etnia,
            nova_educacao_pais=self.__educacao_pais,
            novo_tempo_estudo_semanal=self.__tempo_estudo_semanal,
            novo_apoio_pais=self.__apoio_pais,
            novas_aulas_particulares=self.__aulas_particulares,
            novas_extra_curriculares=self.__extra_curriculares,
            novos_esportes=self.__esportes,
            nova_aula_musica=self.__aula_musica,
            novo_voluntariado=self.__voluntariado,
        ).executar()

    def deletar_aluno(self) -> str:
        return DeletarAlunoDoBanco(id_aluno = self.__id_aluno).executar()


class CriarAlunoNoBanco:
    def __init__(
        self,
        nome: str,
        data_nascimento: str,
        sexo: str,
        cpf: str,
        nacionalidade: str,
        nome_responsavel: str,
        numero_responsavel: str,
        nota_score_preditivo: float,
        id_escola: int,
        etnia: int,
        educacao_pais: int = None,
        tempo_estudo_semanal: float = None,
        apoio_pais: int = None,
        aulas_particulares: int = None,
        extra_curriculares: int = None,
        esportes: int = None,
        aula_musica: int = None,
        voluntariado: int = None,
        id_turma: Optional[int] = None,
        faltas: int = 0,

    ) -> None:
        self.__data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
        self.__aluno = Aluno(
            id=0,  # Inicializado como 0, será atualizado no banco
            nome=nome,
            data_nascimento=self.__data_nascimento,
            sexo=sexo,
            cpf=cpf,
            nacionalidade=nacionalidade,
            faltas=faltas,
            nota_score_preditivo=nota_score_preditivo,
            id_escola=id_escola,
            etnia=etnia,
            educacao_pais=educacao_pais,
            tempo_estudo_semanal=tempo_estudo_semanal,
            apoio_pais=apoio_pais,
            aulas_particulares=aulas_particulares,
            extra_curriculares=extra_curriculares,
            esportes=esportes,
            aula_musica=aula_musica,
            voluntariado=voluntariado,
            id_turma=id_turma,  # Inicializado como 0, será atualizado na função de criação/edicao de turmas
            id_responsavel=0,  # Inicializado como 0, será atualizado após a inserção do responsavel no banco
        )
        self.__nota_score_preditivo = ObterNotaScorePreditivo.get_score_preditivo(self.__aluno)
        self.__aluno.nota_score_preditivo = self.__nota_score_preditivo
        self.__responsavel = Responsavel(id=0, nome=nome_responsavel, telefone=numero_responsavel)


    def executar(self) -> str:
        
        # Verifica se os atributos necessários estão todos preenchidos
        resultado =  ValidadorCampos.validar_campos_preenchidos([
            self.__aluno.nome,
            self.__aluno.cpf,
            self.__aluno.nacionalidade,
            self.__responsavel.nome, 
            self.__responsavel.telefone,
            self.__aluno.data_nascimento,  
            self.__aluno.sexo,
            self.__aluno.etnia,
            self.__aluno.educacao_pais,
            self.__aluno.tempo_estudo_semanal,
            self.__aluno.apoio_pais,
            self.__aluno.aulas_particulares,
            self.__aluno.extra_curriculares,
            self.__aluno.esportes,
            self.__aluno.aula_musica,
            self.__aluno.voluntariado,
          
        ])
        
        if resultado is not None:
            return resultado
        
        try:
            # Verifica existência da escola
            if ConsultaEscolaBanco().buscar_por_id(self.__aluno.id_escola) is None:
                return f"Escola com ID {self.__aluno.id_escola} não encontrada."
            
            # Verifica existencia de algum outro aluno com associado ao cpf fornecido
            if ConsultaAlunoBanco().buscar_por_cpf(cpf= self.__aluno.cpf) is not None:
                log.warning(f"Tentativa de cadastro com CPF já existente: {self.__aluno.cpf}")
                return "CPF já vinculado."
            
            # Verifica existência de algum professor com cpf existente
            if ConsultarProfessor(cpf=self.__aluno.cpf).get_professor_retorno_cpf() is not None:
                log.warning(f"Tentativa de cadastro com CPF já existente: {self.__aluno.cpf}")
                return "CPF já vinculado."
            
            # Validações adicionais
            resultado_cpf = ValidadorCampos.validar_cpf(self.__aluno.cpf)
            if resultado_cpf is not None:
                return resultado_cpf
            
            resultado_telefone = ValidadorCampos.validar_telefone(self.__responsavel.telefone)
            if resultado_telefone is not None:
                return resultado_telefone

            AlunoRepository().criar(self.__aluno, self.__responsavel)
            log.info(f"Aluno '{self.__aluno.nome}' criado com sucesso.")
            return "Aluno criado com sucesso"
        except Exception as e:
            log.error(f"Erro ao criar aluno: {e}")
            return "Erro ao criar aluno"


class ListarAlunosNoBanco:
    def __init__(self, id_escola: Optional[int], id_turma: Optional[int]):
        self.__id_escola = id_escola
        self.__id_turma = id_turma

    def listar_alunos_escola(self) -> list[AlunoData]:       
        try:
            alunos = AlunoRepository().listar_por_escola(self.__id_escola)
            log.debug(f"{len(alunos)} alunos encontrados na escola {self.__id_escola}.")
            return alunos
        except Exception as e:
            log.error(f"Erro ao listar alunos: {e}")
            return []
        
    def listar_alunos_turma(self) -> list[AlunoData]:
        try:
            alunos = AlunoRepository().listar_por_turma(self.__id_turma)
            log.debug(f"{len(alunos)} alunos encontrados na turma {self.__id_turma}.")
            return alunos
        except Exception as e:
            log.error(f"Erro ao listar alunos: {e}")
            return []

class AtualizarAlunoNoBanco:
    def __init__(
        self,
        id_aluno: int,
        novo_nome: str,
        novo_cpf: str,
        nova_data_nascimento: str,
        novo_sexo: str,
        nova_nacionalidade: str,
        novo_nome_responsavel: str,
        novo_numero_responsavel: str,
        nova_etnia: int,
        nova_educacao_pais: int,
        novo_tempo_estudo_semanal: float,
        novo_apoio_pais: int,
        novas_aulas_particulares: int,
        novas_extra_curriculares: int,
        novos_esportes: int,
        nova_aula_musica: int,
        novo_voluntariado: int,
    ):
        self.__id = id_aluno
        self.__novo_nome = novo_nome
        self.__novo_cpf = novo_cpf
        self.__nova_data_nascimento = nova_data_nascimento
        self.__novo_sexo = novo_sexo
        self.__nova_nacionalidade = nova_nacionalidade
        self.__novo_nome_responsavel = novo_nome_responsavel
        self.__novo_numero_responsavel = novo_numero_responsavel
        self.__nova_etnia = nova_etnia
        self.__nova_educacao_pais = nova_educacao_pais
        self.__novo_tempo_estudo_semanal = novo_tempo_estudo_semanal
        self.__novo_apoio_pais = novo_apoio_pais
        self.__novas_aulas_particulares = novas_aulas_particulares
        self.__novas_extra_curriculares = novas_extra_curriculares
        self.__novos_esportes = novos_esportes
        self.__nova_aula_musica = nova_aula_musica
        self.__novo_voluntariado = novo_voluntariado

    def executar(self) -> str:
        
        # Verifica se os atributos necessários estão todos preenchidos
        resultado = ValidadorCampos.validar_campos_preenchidos([
            self.__id,
            self.__novo_nome,
            self.__novo_cpf,
            self.__nova_data_nascimento,
            self.__novo_sexo,
            self.__nova_nacionalidade,
            self.__novo_nome_responsavel,
            self.__novo_numero_responsavel,
            self.__nova_etnia,
            self.__nova_educacao_pais,
            self.__novo_tempo_estudo_semanal,
            self.__novo_apoio_pais,
            self.__novas_aulas_particulares,
            self.__novas_extra_curriculares,
            self.__novos_esportes,
            self.__nova_aula_musica,
            self.__novo_voluntariado
        ])
        if resultado is not None:
            return resultado
        
        try:
            
            # Verifica existencia de algum aluno com cpf existente
            if ConsultaAlunoBanco().buscar_por_cpf_e_id(id=self.__id, cpf=self.__novo_cpf):
                log.warning(f"Tentativa de cadastro com CPF já existente: {self.__novo_cpf}")
                return "CPF já vinculado."
            
            # Verifica existência de algum professor com cpf existente
            if ConsultarProfessor(id_professor = self.__id, cpf = self.__novo_cpf).get_professor_retorno_cpf_e_id():
                log.warning(f"Tentativa de cadastro com CPF já existente: {self.__novo_cpf}")
                return "CPF já vinculado."
            
            # Validações adicionais
            resultado_cpf = ValidadorCampos.validar_cpf(self.__novo_cpf)
            if resultado_cpf is not None:
                return resultado_cpf

            resultado_telefone = ValidadorCampos.validar_telefone(self.__novo_numero_responsavel)
            if resultado_telefone is not None:
                return resultado_telefone

            data_nascimento = datetime.strptime(self.__nova_data_nascimento, "%Y-%m-%d").date() if isinstance(self.__nova_data_nascimento, str) else self.__nova_data_nascimento
            if data_nascimento is None:
                return "Data de nascimento inválida."

            atualizado = AlunoRepository().atualizar(
                id_aluno=self.__id,
                novo_nome=self.__novo_nome,
                novo_cpf=self.__novo_cpf,
                novo_nome_responsavel=self.__novo_nome_responsavel,
                novo_numero_responsavel=self.__novo_numero_responsavel,
                nova_data_nascimento=data_nascimento,
                novo_sexo=self.__novo_sexo,
                nova_nacionalidade=self.__nova_nacionalidade,
                nova_etnia=self.__nova_etnia,
                nova_educacao_pais=self.__nova_educacao_pais,
                novo_tempo_estudo_semanal=self.__novo_tempo_estudo_semanal,
                novo_apoio_pais=self.__novo_apoio_pais,
                novas_aulas_particulares=self.__novas_aulas_particulares,
                novas_extra_curriculares=self.__novas_extra_curriculares,
                novos_esportes=self.__novos_esportes,
                nova_aula_musica=self.__nova_aula_musica,
                novo_voluntariado=self.__novo_voluntariado
            )
            if atualizado:
                log.info(f"Aluno {self.__id} atualizado com sucesso.")
                return "Aluno atualizado com sucesso"
            else:
                return "Aluno não encontrado"
        except Exception as e:
            log.error(f"Erro ao atualizar aluno: {e}")
            return "Erro ao atualizar aluno"


class DeletarAlunoDoBanco:
    def __init__(self, id_aluno: int):
        self.__id = id_aluno

    def executar(self) -> str:
        try:
            deletado = AlunoRepository().deletar(self.__id)
            if deletado:
                log.info(f"Aluno {self.__id} deletado.")
                return "Aluno deletado com sucesso"
            else:
                return "Aluno não encontrado"
        except Exception as e:
            log.error(f"Erro ao deletar aluno: {e}")
            return "Erro ao deletar aluno"
        

class ObterNotaScorePreditivo:
    """Classe responsável por obter a nota de um aluno a partir de seu ID."""
    
    def get_score_preditivo(aluno: Aluno) -> str:
        """Obtém o score preditivo de um aluno."""
        try:
            aluno_ia = ObterNotaScorePreditivo._criar_aluno_ia(aluno)
            nota_predita = processIA(aluno_ia)
            log.info(f"Score preditivo para o aluno {aluno.id} ({aluno.nome}): {nota_predita}")
            return nota_predita
        except Exception as e:
            log.error(f"Erro ao obter score preditivo: {e}")
            return "Erro ao obter score preditivo"

    def _criar_aluno_ia(aluno: Aluno) -> AlunoIA:
        """Cria um objeto AlunoIA a partir de um objeto Aluno."""
        idade = ObterNotaScorePreditivo._calcular_idade(aluno.data_nascimento)
        return AlunoIA(
            id=aluno.id,
            nome=aluno.nome,
            idade=idade,
            sexo=1 if aluno.sexo.lower() == 'masculino' else 0,
            etnia=aluno.etnia,
            educacaoPais=aluno.educacao_pais,
            tempoEstudoSemanal=aluno.tempo_estudo_semanal,
            faltas=aluno.faltas,
            apoioPais=aluno.apoio_pais,
            aulasParticulares=aluno.aulas_particulares,
            extraCurriculares=aluno.extra_curriculares,
            esportes=aluno.esportes,
            aulaMusica=aluno.aula_musica,
            voluntariado=aluno.voluntariado,
            notaFinal=""
        )
    
    def _calcular_idade(data_nascimento: date) -> int:
        """Calcula a idade do aluno com base na data de nascimento."""
        hoje = date.today()
        return hoje.year - data_nascimento.year - (
            (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day)
    )
    

class ControllerAlunoIA:
    """Controlador responsável por coletar dados de alunos relacionados à IA."""

    def obter_distribuicao_notas_ia_escola(id_escola: int) -> str:
        """
        Retorna um JSON com a contagem de notas preditivas dos alunos de uma escola.
        """
        distribuicao = AlunoIARepository.contar_notas_ia_por_escola(id_escola)
        return json.dumps({"distribuicao_por_escola": distribuicao}, ensure_ascii=False, indent=4)


    def obter_distribuicao_notas_ia_geral(id_escola: Optional[int] = None) -> str:
        """
        Retorna um JSON com a contagem de notas preditivas dos alunos (geral).
        """
        distribuicao = AlunoIARepository.contar_notas_ia_geral()
        return json.dumps({"distribuicao_geral": distribuicao}, ensure_ascii=False, indent=4)


    def obter_distribuicao_notas_por_sexo_escola(id_escola: int) -> str:
        """
        Retorna um JSON com a contagem de notas preditivas dos alunos por sexo.
        """
        distribuicao = AlunoIARepository.contar_notas_ia_por_sexo_escola(id_escola)
        return json.dumps({"distribuicao_por_sexo": distribuicao}, ensure_ascii=False, indent=4)


    def obter_distribuicao_notas_por_sexo_geral() -> str:
        """
        Retorna um JSON com a contagem de notas preditivas dos alunos por sexo (geral, sem filtro de escola).
        """
        distribuicao = AlunoIARepository.contar_notas_ia_por_sexo_geral()
        return json.dumps({"distribuicao_por_sexo": distribuicao}, ensure_ascii=False, indent=4)


    def obter_qtd_alunos_por_esporte_escola(id_escola: int) -> str:
        """
        Retorna a contagem de alunos que participam ou não de esportes na escola.

        Exemplo:
        {
            "esportes": {
                "Participa": 7,
                "Não participa": 5
            }
        }
        """
        dados = AlunoIARepository.contar_alunos_por_esporte_escola(id_escola)
        return json.dumps({"esportes": dados}, ensure_ascii=False, indent=4)


    def obter_qtd_alunos_por_esporte_geral() -> str:
        """
        Retorna a contagem de alunos que participam ou não de esportes em todas as escolas.

        Exemplo:
        {
            "esportes": {
                "Participa": 15,
                "Não participa": 9
            }
        }
        """
        dados = AlunoIARepository.contar_alunos_por_esporte_geral()
        return json.dumps({"esportes": dados}, ensure_ascii=False, indent=4)


    def obter_qtd_alunos_por_extra_curricular_escola(id_escola: int) -> str:
        """
        Retorna a contagem de alunos que fazem ou não fazem aulas extracurriculares na escola.

        Exemplo:
        {
            "extraCurriculares": {
                "Faz": 6,
                "Não faz": 8
            }
        }
        """
        dados = AlunoIARepository.contar_alunos_por_extracurriculares_escola(id_escola)
        return json.dumps({"extraCurriculares": dados}, ensure_ascii=False, indent=4)


    def obter_qtd_alunos_por_extra_curricular_geral() -> str:
        """
        Retorna a contagem de alunos que fazem ou não fazem aulas extracurriculares em geral.

        Exemplo:
        {
            "extraCurriculares": {
                "Faz": 12,
                "Não faz": 18
            }
        }
        """
        dados = AlunoIARepository.contar_alunos_por_extracurriculares_geral()
        return json.dumps({"extraCurriculares": dados}, ensure_ascii=False, indent=4)


    def obter_qtd_alunos_por_aula_musica_escola(id_escola: int) -> str:
        """
        Retorna a contagem de alunos que fazem ou não fazem aula de música na escola.

        Exemplo:
        {
            "aulaMusica": {
                "Faz": 5,
                "Não faz": 9
            }
        }
        """
        dados = AlunoIARepository.contar_alunos_por_aula_musica_escola(id_escola)
        return json.dumps({"aulaMusica": dados}, ensure_ascii=False, indent=4)


    def obter_qtd_alunos_por_aula_musica_geral() -> str:
        """
        Retorna a contagem de alunos que fazem ou não fazem aula de música em geral.

        Exemplo:
        {
            "aulaMusica": {
                "Faz": 14,
                "Não faz": 16
            }
        }
        """
        dados = AlunoIARepository.contar_alunos_por_aula_musica_geral()
        return json.dumps({"aulaMusica": dados}, ensure_ascii=False, indent=4)


    def obter_qtd_alunos_por_aulas_particulares_escola(id_escola: int) -> str:
        """
        Retorna a contagem de alunos que fazem ou não fazem aulas particulares na escola.

        Exemplo:
        {
            "aulasParticulares": {
                "Faz": 4,
                "Não faz": 10
            }
        }
        """
        dados = AlunoIARepository.contar_alunos_por_aulas_particulares_escola(id_escola)
        return json.dumps({"aulasParticulares": dados}, ensure_ascii=False, indent=4)


    def obter_qtd_alunos_por_aulas_particulares_geral() -> str:
        """
        Retorna a contagem de alunos que fazem ou não fazem aulas particulares em geral.

        Exemplo:
        {
            "aulasParticulares": {
                "Faz": 12,
                "Não faz": 18
            }
        }
        """
        dados = AlunoIARepository.contar_alunos_por_aulas_particulares_geral()
        return json.dumps({"aulasParticulares": dados}, ensure_ascii=False, indent=4)
    

class FormatarAluno:
    """Classe responsável por formatar AlunoData → Aluno (domínio) → JSON."""

    def formatar_aluno_data_para_dominio(self, alunos_data: List[AlunoData]) -> List[Aluno]:
        lista_alunos = []
        for aluno in alunos_data:

            lista_alunos.append(

                Aluno(
                    id=aluno.id,
                    nome=aluno.nome,
                    cpf=aluno.cpf,
                    faltas=aluno.faltas,
                    nota_score_preditivo=aluno.nota_score_preditivo,
                    data_nascimento=aluno.data_nascimento,
                    sexo=aluno.sexo,
                    nacionalidade=aluno.nacionalidade,
                    id_escola=aluno.id_escola,
                    id_turma=aluno.id_turma,
                    id_responsavel=aluno.id_responsavel,
                    etnia=aluno.etnia,
                    educacao_pais=aluno.educacaoPais,
                    tempo_estudo_semanal=aluno.tempoEstudoSemanal,
                    apoio_pais=aluno.apoioPais,
                    aulas_particulares=aluno.aulasParticulares,
                    extra_curriculares=aluno.extraCurriculares,
                    esportes=aluno.esportes,
                    aula_musica=aluno.aulaMusica,
                    voluntariado=aluno.voluntariado,
                )
            )
        return lista_alunos

    def gerar_json(self, alunos_dominio: List[Aluno]) -> str:
        alunos_json = []
        for aluno in alunos_dominio:
            dados_aluno = ConsultaDadosAluno(aluno.id)
            nome_responsavel = dados_aluno.nome_responsavel()
            numero_responsavel = dados_aluno.numero_responsavel()
            nome_turma = dados_aluno.nome_turma()
            nome_escola = dados_aluno.nome_escola()
            alunos_json.append(    
                {
                    "id": aluno.id,
                    "nome": aluno.nome,
                    "cpf": aluno.cpf,
                    "faltas": aluno.faltas,
                    "nota_score_preditivo": aluno.nota_score_preditivo,
                    "data_nascimento": aluno.data_nascimento.strftime("%Y-%m-%d") if aluno.data_nascimento else None,
                    "sexo": aluno.sexo,
                    "nome_responsavel": nome_responsavel,
                    "numero_responsavel": numero_responsavel,
                    "nome_turma": nome_turma,
                    "nome_escola": nome_escola,
                    "nacionalidade": aluno.nacionalidade,
                    "id_escola": aluno.id_escola,
                    "id_turma": aluno.id_turma,
                    "id_responsavel": aluno.id_responsavel,
                    "etnia": aluno.etnia,
                    "educacao_pais": aluno.educacao_pais,
                    "tempo_estudo_semanal": aluno.tempo_estudo_semanal,
                    "apoio_pais": aluno.apoio_pais,
                    "aulas_particulares": aluno.aulas_particulares,
                    "extra_curriculares": aluno.extra_curriculares,
                    "esportes": aluno.esportes,
                    "aula_musica": aluno.aula_musica,
                    "voluntariado": aluno.voluntariado,
                }
            )

        return json.dumps({"alunos": alunos_json}, ensure_ascii=False, indent=4)