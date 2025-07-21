from user_cases.professor import ControllerProfessor
from user_cases.aluno import ControllerAluno
from user_cases.turma import ControllerTurma
from user_cases.materia import ControllerMateria
from user_cases.municipio import ControllerMunicipio
from user_cases.escola import ControllerEscola
from user_cases.avaliacao import ControllerRankingAvaliacao, ControllerHistoricoDesempenho

ID_ESCOLA_TESTE = 1

# Funções de criação:

def test_criar_escola():
    controller = ControllerEscola(
        nome="Escola Modelo",
        id_escola=1,
        id_municipio=1,
    )
    resposta = controller.criar_escola()
    print(resposta)


def test_criar_professor():
    controller=ControllerProfessor(
        nome="João Teste",
        cpf="12245674980",
        cargo="Matemática",
        id_escola=ID_ESCOLA_TESTE,
        email="joao.teste@escola.com",
        senha="senhaForteJoao2025",
        telefone="1234567890",
        data_nascimento="2000-01-01",
        nacionalidade="Brasileiro",
        estado_civil="Solteiro",
        sexo="Masculino",
    )
    resposta = controller.criar_professor()
    print(resposta)


def test_criar_turma():
    controller = ControllerTurma(
        nome="3º Ano B",
        ano_letivo=2025,
        id_escola=ID_ESCOLA_TESTE
    )
    resposta = controller.criar_turma()
    print(resposta)


def test_criar_aluno():
    controller = ControllerAluno(
        nome= "Maria teste",
        cpf="98765432100",
        faltas=0,
        nota_score_preditivo=8.5,
        id_escola=ID_ESCOLA_TESTE,
        nome_responsavel="João da Silva",
        numero_responsavel="1234567890",
        sexo="Feminino",
        data_nascimento="2008-05-15",
        nacionalidade="Brasileira",
    )
    resposta = controller.criar_aluno()
    print(resposta)

def test_criar_materia():
    controller = ControllerMateria(
        nome="História",
        id_disciplina=1,
        id_professor=1
    )
    resposta = controller.criar_materia()
    print("Resultado da criação da matéria:", resposta)

def test_criar_municipio():
    controller = ControllerMunicipio(
        nome="São João do Teste 2",
        estado="TesteLand",
        regiao="Centro-Teste"
    )
    resposta = controller.criar_municipio()
    print(resposta)

# Funções de listagem:

def test_listar_escolas():
    controller = ControllerEscola(id_municipio=1)

    resposta = controller.listar_escolas()
    print(resposta)

def test_listar_professores():
    controller = ControllerProfessor(id_escola=ID_ESCOLA_TESTE)
    resposta_json = controller.listar_professores()
    print(resposta_json)

def test_listar_turmas():
    controller = ControllerTurma(id_escola=1)
    resultado = controller.listar_turmas()
    print(resultado)

def test_listar_alunos_escola():
    controller = ControllerAluno(id_escola=ID_ESCOLA_TESTE)
    resultado = controller.listar_alunos_Escola()
    print(resultado)

def test_listar_alunos_turma():
    controller = ControllerAluno(id_turma=1)
    resultado = controller.listar_alunos_turma()
    print(resultado)

def test_listar_materias():
    """Testa a listagem de matérias de uma escola."""
    controller = ControllerMateria(id_professor=1)
    resposta_json = controller.listar_materias()
    print(resposta_json)

def test_listar_municipios():
    controller = ControllerMunicipio()
    resposta_json = controller.listar_municipios()
    print(resposta_json)


# Funções de atualização:

def test_atualizar_escola():
    controller = ControllerEscola(
        id_escola=4,  # Substitua pelo ID real
        nome="Escola Modelo Atualizada",
        id_municipio=2
    )
    resposta = controller.atualizar_escola()
    print(resposta)


def test_atualizar_professor():
    controller = ControllerProfessor(
        id_professor= 5,  # ajuste para um ID válido
        nome="João Teste Atualizado",
        cpf="12245674980",
        cargo="Matemática",
        id_escola=ID_ESCOLA_TESTE,
        email="joao.teste@escola.com",
        senha="senhaForteJoao2025",
        telefone="1234567890",
        data_nascimento="2000-01-01",
        nacionalidade="Brasileiro",
        estado_civil="Solteiro",
        sexo="Masculino",
    )
    resposta = controller.atualizar_professor()
    print(resposta)

def test_atualizar_aluno():
    controller = ControllerAluno(
        id_aluno=25,  # ajuste para um ID válido
        nome="Maria atualizada",
        cpf="98765432100",
        faltas=0,
        nota_score_preditivo=8.5,
        id_escola=ID_ESCOLA_TESTE,
        nome_responsavel="João da Silva",
        numero_responsavel="1234567890",
        sexo="Feminino",
        data_nascimento="2008-05-15",
        nacionalidade="Brasileira",
    )
    resposta = controller.atualizar_aluno()
    print(resposta)

def test_atualizar_turma():
    controller = ControllerTurma(
        id_turma=8,  # ajuste para um ID válido
        nome="3º Ano b atualizado",
    )
    resposta = controller.atualizar_turmas()
    print(resposta)


def test_atualizar_municipio():
    id_municipio_existente = 2  # ajuste com o ID real do banco

    controller = ControllerMunicipio(
        id_municipio=id_municipio_existente,
        nome="São João do Teste 2",
        estado="Pernambuco",
        regiao="Nordeste"
    )
    resposta = controller.atualizar_municipio()
    print(resposta)

def test_atualizar_materia():
    controller = ControllerMateria(
        id_materia=4,  # Substitua por um ID real de matéria existente
        nome="edf",
        id_disciplina=2,
        id_professor=3
    )
    resposta = controller.atualizar_materia()
    print(resposta)


# Funções de deletar:

def test_deletar_escola():
    controller = ControllerEscola(id_escola=5)  # Substitua pelo ID
    resposta = controller.deletar_escola()
    print(resposta)
    
def test_deletar_professor():
    controller = ControllerProfessor(id_professor=5)  # Substitua por um ID real
    resposta = controller.deletar_professor()
    print(resposta)

def test_deletar_aluno():
    controller = ControllerAluno(id_aluno=25)  # Substitua por um ID real
    resposta = controller.deletar_aluno()
    print(resposta)

def test_deletar_municipio():
    controller = ControllerMunicipio(id_municipio=5)
    resposta = controller.deletar_municipio()
    print(resposta)

def test_deletar_materia():
    controller = ControllerMateria(id_materia=6)  # Substitua por um ID real
    resposta = controller.deletar_materia()
    print(resposta)
    
def test_deletar_turma():
    controller = ControllerTurma(id_turma=1)
    resposta = controller.deletar_turma()
    print(resposta)

ID_ALUNO_TESTE = 1
ID_TURMA_TESTE = 1
ID_ESCOLA_TESTE = 1
ID_DISCIPLINA_TESTE = 1

# Testes de histórico de desempenho (listar avaliações)

def test_historico_por_aluno():
    controller = ControllerHistoricoDesempenho(id_aluno=ID_ALUNO_TESTE)
    resposta = controller.listar_historico_avaliacoes_por_aluno()
    print(resposta)

def test_historico_por_turma():
    controller = ControllerHistoricoDesempenho(id_turma=ID_TURMA_TESTE, id_professor=1)
    resposta = controller.listar_historico_avaliacoes_por_turma()
    print(resposta)

def test_historico_por_escola():
    controller = ControllerHistoricoDesempenho(id_escola=2)
    resposta = controller.listar_historico_avaliacoes_por_escola()
    print(resposta)


# Testes de ranking de desempenho (ranquear por critério)

def test_ranking_por_aluno():
    controller = ControllerRankingAvaliacao()
    resposta = controller.ranquear_alunos()
    print(resposta)

def test_ranking_por_turma():
    controller = ControllerRankingAvaliacao()
    resposta = controller.ranquear_turmas()
    print(resposta)

def test_ranking_por_escola():
    controller = ControllerRankingAvaliacao()
    resposta = controller.ranquear_escolas()
    print(resposta)

def test_ranking_por_disciplina_na_escola():
    controller = ControllerRankingAvaliacao()
    resposta = controller.ranquear_materias()
    print(resposta)


if __name__ == "__main__":
    print("descomente a função que deseja testar")
    #test_criar_escola()
    #test_criar_professor()
    #test_criar_turma()
    #test_criar_aluno()
    #test_criar_materia()
    #test_criar_municipio() 
   
    #test_listar_escolas()
    #test_listar_professores()
    #test_listar_turmas()
    test_listar_alunos_escola()
    #test_listar_alunos_turma()
    #test_listar_materias()
    #test_listar_municipios()
    
    #test_atualizar_escola()
    #test_atualizar_professor()
    #test_atualizar_turma()
    #test_atualizar_aluno()
    #test_atualizar_materia()
    #test_atualizar_municipio() 
    
    #test_deletar_escola()
    #test_deletar_professor()
    #test_deletar_turma()
    #test_deletar_aluno()
    #test_deletar_materia()
    #test_deletar_municipio()  

    #test_historico_por_aluno()
    #test_historico_por_turma()
    #test_historico_por_escola()

    #test_ranking_por_aluno()
    #test_ranking_por_turma()
    #test_ranking_por_escola()
    #test_ranking_por_disciplina_na_escola()