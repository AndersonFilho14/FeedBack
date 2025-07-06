from datetime import date

from config import log
from domain import Acesso, Avaliacao

from infra.repositories.acesso_data import ConsultarAcesso, ConsultarUser
from infra.repositories import (
    ConsultarProfessor,
    ConsultarAlunosVinculadosAoProfessorNoBanco,
)
from user_cases import (
    ControllerProfessorAtualizarFalta,
    ControllerProfessorAlunosVinculados,
    ConsultarAlunosVinculadosAoProfessor,
    ControllerProfessorAdicionarNotaAoAluo,
    ConsultarAlunosVinculadosAoProfessorNoBanco,  # noqa: F811
)

from infra.repositories.professor_data import AtualizarQuantidadeDeFaltasParaAluno, ConsultarDisciplinasEMateriasVinculadasAoProfessor, AdicionarNotaParaAluno
from infra.repositories.aluno_data import ConsultarTurma

from infra.db.models_data import (
    Acesso as AcessoData,  # noqa: F401
    Cargo as CargoData,  # noqa: F401
    Professor as ProfessorData,
    Escola as EscolaData,  # noqa: F401
    Municipio as MunicipioData,  # noqa: F401
)

from user_cases.acesso import ControllerAcesso


def test_conexao_acesso():
    acesso = Acesso(user="prof_alfa", password="senha123")
    acesso_data = ConsultarAcesso(user_acessar=acesso)
    retorno = acesso_data.get_retorno_banco()
    log.trace(retorno)
    log.debug(f"retorno = {type(retorno.id_user)}, reto {type(retorno.nome_cargo)}")


def test_consultar_user():
    consulta = ConsultarUser(
        id_usuario=1, tabela_no_banco=ProfessorData
    ).consultar_user()
    log.debug(f"retorno = {consulta}, reto {type(consulta)}")


def test_controller_acesso():
    user_name = "prof_alfa"
    passworld = "senha123"
    retorno = ControllerAcesso(
        user_name=user_name, passworld=passworld
    ).return_user_ou_texto()
    log.debug(retorno)


def test_consultar_professor():
    id_professor = 1
    retorno = ConsultarProfessor(id_professor=id_professor).get_professor_retorno()
    log.debug(f"retorno = {retorno} de tipo {type(retorno)}")


def test_alunos_vinculado_ao_professor():
    id_professor = 1
    retorno = ConsultarAlunosVinculadosAoProfessorNoBanco(
        professor_id=id_professor
    ).get_alunos()
    log.debug(f"retorno = {retorno} de tipo {type(retorno)}")


def test_ControllerProfessor():
    id_professor = 1
    retorno = ControllerProfessorAlunosVinculados(
        id_professor=id_professor
    ).fluxo_para_consultar_professor_e_seus_alunos()
    log.debug(f"retorno = {retorno} de tipo {type(retorno)}")


def test_ConsultarAlunosVinculadosAoProfessor():
    id_professor = 1
    lista_alunos = ConsultarAlunosVinculadosAoProfessor(
        id_professor=id_professor
    ).get_alunos_vinculados()
    log.debug(f"retorno = {lista_alunos} de tipo {type(lista_alunos)}")
    log.debug(len(lista_alunos))


def test_consultar_se_aluno_esta_vinculado_ao_professor():
    retorno = AtualizarQuantidadeDeFaltasParaAluno(
        id_professor=1, id_aluno=1, nova_quantidade_de_faltas=2
    ).fluxo_atualizar_falta_aluno()
    log.debug(retorno)
    log.debug(type(retorno))


def testar_controller_atualizar_quantidade_de_faltas():
    id_professor = "1"
    id_aluno = "1"
    faltas = "1"
    controller = ControllerProfessorAtualizarFalta(
        id_professor=id_professor, id_aluno=id_aluno, nova_quantidade_de_faltas=faltas
    ).fluxo_crud_de_nota_do_aluno()
    log.debug(controller)
    log.debug(type(controller))

def test_consultar_materia_e_disciplinas_vinculadas_ao_professor():
    id_professor = 1
    disicplinas_e_materia = ConsultarDisciplinasEMateriasVinculadasAoProfessor(id_professor= id_professor).consultar()
    log.debug(disicplinas_e_materia)
    log.debug(type(disicplinas_e_materia))

def test_adicionar_nota_banco():
    ava = Avaliacao(id= 0, tipo_avaliacao= "3Va", data_avaliacao= date(2025, 4, 21), nota= 8.3, id_aluno=1, id_professor=1, id_disciplina=1, id_materia=1, id_turma=3)
    adicionar = AdicionarNotaParaAluno(id_aluno=ava.id_aluno, id_professor=ava.id_professor, tipo_avaliacao= ava.tipo_avaliacao, nota=ava.nota, data_avaliacao= ava.data_avaliacao, id_disciplina= ava.id_disciplina, id_materia= ava.id_materia, id_turma= ava.id_turma)
    retorno = adicionar.adicionar_nota()
    log.trace(retorno)
    log.trace(type(retorno))

def test_ControllerProfessorAdicionarNotaAoAluo():
    post =  {"id_professor" : "1", "tipo_avaliacao": "2", "nota": "3", "id_aluno": "4", "id_materia": "5"}
    controller = ControllerProfessorAdicionarNotaAoAluo(post= post)
    retorno = controller.fluxo_para_adicionar()
    log.debug(retorno)
    log.debug(type(retorno))

def test_consultar_turma_do_aluno():
    retorno = ConsultarTurma(id_aluno= 700).get_id_turma()
    log.debug(retorno)
    log.debug(type(retorno))

if __name__ == "__main__":
    test_consultar_turma_do_aluno()
