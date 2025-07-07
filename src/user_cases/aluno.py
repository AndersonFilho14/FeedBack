from typing import Optional
from domain.models import Aluno
from infra.repositories import AlunoRepository, ConsultaBancoEscola, ConsultaBancoTurma, ConsultaBancoAluno, ConsultarProfessor
from config import log

from utils.validarCampos import ValidadorCampos
from infra.db.models_data import Aluno as AlunoData
from typing import Optional, List
import json

class ControllerAluno:
    """Controlador responsável por coordenar operações de CRUD relacionadas a alunos."""

    def __init__(
        self,
        nome: Optional[str] = None,
        cpf: Optional[str] = None,
        idade: Optional[int] = None,
        faltas: Optional[int] = 0,
        nota_score_preditivo: Optional[float] = None,
        id_escola: Optional[int] = None,
        id_turma: Optional[int] = None,
        id_responsavel: Optional[int] = None,
        id_aluno: Optional[int] = None,
    ) -> None:
        self.__nome = nome
        self.__cpf = cpf
        self.__idade = idade
        self.__faltas = faltas
        self.__nota_score = nota_score_preditivo
        self.__id_escola = id_escola
        self.__id_turma = id_turma
        self.__id_responsavel = id_responsavel
        self.__id_aluno = id_aluno

    def criar_aluno(self) -> str:
        resultado = CriarAlunoNoBanco(
            nome = self.__nome,
            cpf = self.__cpf,
            idade = self.__idade,
            faltas = self.__faltas,
            nota_score_preditivo = self.__nota_score,
            id_escola = self.__id_escola,
            id_turma = self.__id_turma,
            id_responsavel = self.__id_responsavel, 
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
            id_aluno = self.__id_aluno,
            novo_nome = self.__nome,
            novo_cpf= self.__cpf,
            nova_idade = self.__idade,
            novas_faltas = self.__faltas,
            novo_id_turma = self.__id_turma,
            novo_id_responsavel = self.__id_responsavel
        ).executar()

    def deletar_aluno(self) -> str:
        return DeletarAlunoDoBanco(id_aluno = self.__id_aluno).executar()


class CriarAlunoNoBanco:
    def __init__(
        self,
        nome: str,
        cpf: str,
        idade: int,
        faltas: int,
        nota_score_preditivo: Optional[float],
        id_escola: int,
        id_turma: int,
        id_responsavel: int
    ):
        self.__aluno = Aluno(
            nome = nome,
            cpf = cpf,
            idade = idade,
            faltas = faltas,
            nota_score_preditivo = nota_score_preditivo,
            id_escola = id_escola,
            id_turma = id_turma,
            id_responsavel = id_responsavel,
            id = 0
        )

    def executar(self) -> str:
        
        # Verifica se os atributos necessários estão todos preenchidos
        resultado =  ValidadorCampos.validar_campos_preenchidos([
                        self.__aluno.nome,
            self.__aluno.cpf,
            self.__aluno.idade,
            self.__aluno.id_escola,
            self.__aluno.id_turma,
            self.__aluno.id_responsavel
        ])
        
        if resultado is not None:
            return resultado
        
        try:
            # Verifica existência da escola
            if ConsultaBancoEscola().buscar_por_id(self.__aluno.id_escola) is None:
                return f"Escola com ID {self.__aluno.id_escola} não encontrada."
            
            # Verifica existência da turma
            if ConsultaBancoTurma().buscar_por_id(self.__aluno.id_turma) is None:
                return f"Turma com ID {self.__aluno.id_turma} não encontrada."
            
            # Verifica existencia de algum outro aluno com associado ao cpf fornecido
            if ConsultaBancoAluno().buscar_por_cpf(cpf= self.__aluno.cpf) is not None:
                log.warning(f"Tentativa de cadastro com CPF já existente: {self.__aluno.cpf}")
                return "CPF já vinculado."
            
            # Verifica existência de algum professor com cpf existente
            if ConsultarProfessor(id_professor=0).get_professor_retorno_cpf(cpf=self.__aluno.cpf) is not None:
                log.warning(f"Tentativa de cadastro com CPF já existente: {self.__aluno.cpf}")
                return "CPF já vinculado."
            
            else:
                AlunoRepository().criar(self.__aluno)
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
    def __init__(self, id_aluno: int, novo_nome: str, novo_cpf: str, nova_idade: int, novas_faltas: int, novo_id_turma: int, novo_id_responsavel: int):
        self.__id = id_aluno
        self.__novo_nome = novo_nome
        self.__novo_cpf = novo_cpf
        self.__nova_idade = nova_idade
        self.__novas_faltas = novas_faltas
        self.__novo_id_turma = novo_id_turma
        self.__novo_id_responsavel = novo_id_responsavel

    def executar(self) -> str:
        
        # Verifica se os atributos necessários estão todos preenchidos
        resultado = ValidadorCampos.validar_campos_preenchidos([
            self.__id,
            self.__novo_nome,
            self.__novo_cpf,
            self.__nova_idade,
            self.__novas_faltas,
            self.__novo_id_turma,
            self.__novo_id_responsavel
        ])
        
        if resultado is not None:
            return resultado
        
        try:
            # Verifica existência da turma
            if ConsultaBancoTurma().buscar_por_id(self.__novo_id_turma) is None:
                return f"Turma com ID {self.__novo_id_turma} não encontrada."
            
            # Verifica existencia de algum aluno com cpf existente
            if ConsultaBancoAluno().buscar_por_cpf_e_id(cpf=self.__novo_cpf, id = self.__id):
                log.warning(f"Tentativa de cadastro com CPF já existente: {self.__novo_cpf}")
                return "CPF já vinculado."
            
            # Verifica existência de algum professor com cpf existente
            if ConsultarProfessor(id_professor = self.__id).get_professor_retorno_cpf_e_id(cpf = self.__novo_cpf, id = self.__id):
                log.warning(f"Tentativa de cadastro com CPF já existente: {self.__novo_cpf}")
                return "CPF já vinculado."
            
            else:
                atualizado = AlunoRepository().atualizar(
                    id_aluno = self.__id,
                    novo_nome = self.__novo_nome,
                    nova_idade = self.__nova_idade,
                    novas_faltas = self.__novas_faltas,
                    novo_id_turma = self.__novo_id_turma,
                    novo_id_responsavel = self.__novo_id_responsavel, 
                    novo_cpf = self.__novo_cpf
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
        return [
            Aluno(
                id = aluno.id,
                nome = aluno.nome,
                cpf = aluno.cpf,
                idade = aluno.idade,
                faltas = aluno.faltas,
                nota_score_preditivo = aluno.nota_score_preditivo,
                id_escola = aluno.id_escola,
                id_turma = aluno.id_turma,
                id_responsavel = aluno.id_responsavel
            )
            for aluno in alunos_data
        ]

    def gerar_json(self, alunos_dominio: List[Aluno]) -> str:
        alunos_json = [
            {
                "id": a.id,
                "nome": a.nome,
                "cpf": a.cpf,
                "idade": a.idade,
                "faltas": a.faltas,
                "nota_score_preditivo": a.nota_score_preditivo,
                "id_escola": a.id_escola,
                "id_turma": a.id_turma,
                "id_responsavel": a.id_responsavel
            }
            for a in alunos_dominio
        ]
        return json.dumps({"alunos": alunos_json}, ensure_ascii=False, indent=4)