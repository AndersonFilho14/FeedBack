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
    ControllerProfessorAtualizarNotaAoAluno,
    ConsultarAlunosVinculadosAoProfessorNoBanco,  # noqa: F811
)

from infra.repositories.professor_data import AtualizarQuantidadeDeFaltasParaAluno, ConsultarDisciplinasEMateriasVinculadasAoProfessor, AtualizarNotaParaAluno
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
    print (retorno)


def test_ControllerProfessor():
    id_professor = 1
    retorno = ControllerProfessorAlunosVinculados(
        id_professor=id_professor
    ).fluxo_para_consultar_professor_e_seus_alunos()
    log.debug(f"retorno = {retorno} de tipo {type(retorno)}")
    print(retorno)


def test_ConsultarAlunosVinculadosAoProfessor():
    id_professor = 1
    lista_alunos = ConsultarAlunosVinculadosAoProfessor(
        id_professor=id_professor
    ).get_alunos_vinculados()
    log.debug(f"retorno = {lista_alunos} de tipo {type(lista_alunos)}")
    log.debug(len(lista_alunos))
    print(lista_alunos)


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
    ).processar_faltas_para_alunos()()
    log.debug(controller)
    log.debug(type(controller))

def test_consultar_materia_e_disciplinas_vinculadas_ao_professor():
    id_professor = 1
    disicplinas_e_materia = ConsultarDisciplinasEMateriasVinculadasAoProfessor(id_professor= id_professor).consultar()
    log.debug(disicplinas_e_materia)
    log.debug(type(disicplinas_e_materia))

def test_atualizar_nota_banco():
    lista_notas_alunos = [
        {"nota": 8.5, "id_avaliacao": 1},
        {"nota": 7.0, "id_avaliacao": 2},
        {"nota": 9.0, "id_avaliacao": 3},
    ]
    adicionar = ControllerProfessorAtualizarNotaAoAluno(notas_alunos=lista_notas_alunos)
    retorno = adicionar.atualizar_notas()
    print(retorno)


def test_ControllerProfessorAdicionarNotaAoAluno():
    post =  {"id_professor" : "1", "tipo_avaliacao": "2", "nota": "3", "id_aluno": "4", "id_materia": "5"}
    controller = ControllerProfessorAtualizarNotaAoAluno(post= post)
    retorno = controller.fluxo_para_atualizar_notas()
    log.debug(retorno)
    log.debug(type(retorno))

def test_consultar_turma_do_aluno():
    retorno = ConsultarTurma(id_aluno= 700).get_id_turma()
    log.debug(retorno)
    log.debug(type(retorno))

def teste_controller_atualizar_faltas():
    print("\n=== Teste: Atualizar Faltas de Alunos ===")

    # Suponha que esses IDs existam no banco
    id_professor = "1"
    lista_de_faltas = [
        {"id_aluno": 1, "faltas": 2},
        {"id_aluno": 2, "faltas": 0},
        {"id_aluno": 3, "faltas": 4},
    ]

    controller = ControllerProfessorAtualizarFalta(
        id_professor=id_professor,
        faltas_alunos=lista_de_faltas
    )

    resultados = controller.processar_faltas_para_alunos()
    print(resultados)

if __name__ == "__main__":
    test_atualizar_nota_banco()