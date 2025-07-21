from typing import Optional
from domain.models import Aluno, Responsavel
from infra.repositories import AlunoRepository, ConsultaEscolaBanco, ConsultaTurmaBanco, ConsultaAlunoBanco, ConsultarProfessor, ConsultaDadosAluno
from config import log

from utils.validarCampos import ValidadorCampos
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
        ).executar()

    def deletar_aluno(self) -> str:
        return DeletarAlunoDoBanco(id_aluno = self.__id_aluno).executar()


class CriarAlunoNoBanco:
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
    ) -> None:

        # Conversão segura da data de nascimento
        if isinstance(data_nascimento, str):
            try:
                self.__data_nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Formato inválido para data_nascimento. Use 'YYYY-MM-DD'.")
        else:
            self.__data_nascimento = data_nascimento  # já convertido ou None


        self.__aluno = Aluno(
            id=0,  # Inicializado como 0, será atualizado no banco
            nome=nome,
            data_nascimento= self.__data_nascimento,
            sexo=sexo,
            cpf=cpf,
            nacionalidade=nacionalidade,
            faltas=faltas,
            nota_score_preditivo=nota_score_preditivo,
            id_escola=id_escola,
            id_turma=0,  # Inicializado como 0, será atualizado na função de criação/edicao de turmas
            id_responsavel=0,  # Inicializado como 0, será atualizado após a inserção do responsavel no banco
        )
        self.__responsavel = Responsavel(id =0, nome=nome_responsavel, telefone=numero_responsavel)



    def executar(self) -> str:
        
        # Verifica se os atributos necessários estão todos preenchidos
        resultado =  ValidadorCampos.validar_campos_preenchidos([
            self.__aluno.nome,
            self.__aluno.cpf,
            self.__aluno.nacionalidade,
            self.__responsavel.nome, 
            self.__responsavel.telefone,
            self.__aluno.data_nascimento,   
        ])
        
        if resultado is not None:
            return resultado
        
        try:
            # Verifica existência da escola
            if ConsultaEscolaBanco().buscar_por_id(self.__aluno.id_escola) is None:
                return f"Escola com ID {self.__aluno.id_escola} não encontrada."
            
            # Verifica existencia de algum outro aluno com associado ao cpf fornecido
            if ConsultaAlunoBanco(cpf= self.__aluno.cpf).buscar_por_cpf() is not None:
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
    ):
        self.__id = id_aluno
        self.__novo_nome = novo_nome
        self.__novo_cpf = novo_cpf
        self.__nova_data_nascimento = nova_data_nascimento
        self.__novo_sexo = novo_sexo
        self.__nova_nacionalidade = nova_nacionalidade
        self.__novo_nome_responsavel = novo_nome_responsavel
        self.__novo_numero_responsavel = novo_numero_responsavel

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
        ])
        if resultado is not None:
            return resultado
        
        try:
            
            # Verifica existencia de algum aluno com cpf existente
            if ConsultaAlunoBanco(id_aluno=self.__id, cpf=self.__novo_cpf).buscar_por_cpf_e_id():
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
                    id_responsavel=aluno.id_responsavel
                )
            )
        return lista_alunos

    def gerar_json(self, alunos_dominio: List[Aluno]) -> str:
        alunos_json = []
        for aluno in alunos_dominio:
            dados_aluno = ConsultaDadosAluno(aluno.id)
            nome_responsavel = dados_aluno.nome_responsavel()
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
                    "nome_turma": nome_turma,
                    "nome_escola": nome_escola,
                    "nacionalidade": aluno.nacionalidade,
                    "id_escola": aluno.id_escola,
                    "id_turma": aluno.id_turma,     
                    "id_responsavel": aluno.id_responsavel
                }
            )

        return json.dumps({"alunos": alunos_json}, ensure_ascii=False, indent=4)