from user_cases.professor import ControllerProfessor
from user_cases.aluno import ControllerAluno
from user_cases.aluno import ControllerAluno, ControllerAlunoIA
from user_cases.turma import ControllerTurma
from user_cases.materia import ControllerMateria
from user_cases.municipio import ControllerMunicipio
from user_cases.escola import ControllerEscola
from user_cases.avaliacao import ControllerRankingAvaliacao, ControllerHistoricoAvaliacoes

ID_ESCOLA_TESTE = 1

# Funções de criação:

def test_criar_escola():
    controller = ControllerEscola(
        nome="Escola Modelo",
        id_escola=1,
        id_municipio=1,
        nome_usuario="escola_modelo_user",
        senha="senhaForte2025"
    )
    resposta = controller.criar_escola()
    print(resposta)


def test_criar_professor():
    controller=ControllerProfessor(
        nome="João Teste",
        cpf="12245674980",
        cargo="Matemática",
        id_escola=ID_ESCOLA_TESTE,
        nome_usuario="joao_teste_user",
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
    ids_alunos = [25, 26, 27, 28]  # IDs de alunos
    controller = ControllerTurma(
        nome="3º Ano B",
        ano_letivo=2025,
        id_escola=ID_ESCOLA_TESTE,
        id_professor=1,
        ids_alunos=ids_alunos,
    )
    resposta = controller.criar_turma()
    print(resposta)


def test_criar_aluno():
    controller = ControllerAluno(
        nome= "fulano de tal",
        cpf="91765442714",
        id_escola=ID_ESCOLA_TESTE,
        nome_responsavel="João da Silva",
        numero_responsavel="1234567890",
        sexo="Feminino",
        data_nascimento="2008-05-15",
        nacionalidade="Brasileira",
        etnia=1,
        educacao_pais=1,
        tempo_estudo_semanal=10.0,
        apoio_pais=1,
        aulas_particulares=1,
        extra_curriculares=1,
        esportes=1,
        aula_musica=1,
        voluntariado=1
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
    controller = ControllerTurma(id_escola=ID_ESCOLA_TESTE)
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
        id_municipio=2, 
        nome_usuario="escola_modelo_user_atualizado",
        senha="senhaForteAtualizada2025"
    )
    resposta = controller.atualizar_escola()
    print(resposta)


def test_atualizar_professor():
    controller = ControllerProfessor(
        id_professor= 17,  # ajuste para um ID válido
        nome="João Teste Atualizado",
        cpf="12245674980",
        cargo="Matemática",
        id_escola=ID_ESCOLA_TESTE,
        nome_usuario="joao_teste_user_atualizado",
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
        id_escola=ID_ESCOLA_TESTE,
        nome_responsavel="João da Silva",
        numero_responsavel="1234567890",
        sexo="Feminino",
        data_nascimento="2008-05-15",
        nacionalidade="Brasileira",
        etnia=1,
        educacao_pais=1,
        tempo_estudo_semanal=10.0,
        apoio_pais=1,
        aulas_particulares=1,
        extra_curriculares=1,
        esportes=1,
        aula_musica=1,
        voluntariado=1
    )
    resposta = controller.atualizar_aluno()
    print(resposta)

def test_atualizar_turma():
    ids_alunos_anteriores = [4, 5]
    ids_alunos_atual = [1, 2]  # IDs de alunos atuais
    
    controller = ControllerTurma(
        id_turma=2,  # ajuste para um ID válido
        nome="3º Ano b atualizado",
        id_professor_anterior=2,
        ids_alunos_anteriores=ids_alunos_anteriores,
        id_professor=2,
        ids_alunos=ids_alunos_atual,
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
    controller = ControllerTurma(id_turma=9)
    resposta = controller.deletar_turma()
    print(resposta)

ID_ALUNO_TESTE = 1
ID_TURMA_TESTE = 1
ID_ESCOLA_TESTE = 1
ID_DISCIPLINA_TESTE = 1

# Testes de histórico de desempenho (listar avaliações)

def test_historico_por_aluno():
    controller = ControllerHistoricoAvaliacoes(id_aluno=ID_ALUNO_TESTE)
    resposta = controller.listar_historico_avaliacoes_por_aluno()
    print(resposta)

def test_historico_por_turma():
    controller = ControllerHistoricoAvaliacoes(id_turma=ID_TURMA_TESTE, id_professor=1)
    resposta = controller.listar_historico_avaliacoes_por_turma()
    print(resposta)

def test_historico_por_escola():
    controller = ControllerHistoricoAvaliacoes(id_escola=2)
    resposta = controller.listar_historico_avaliacoes_por_escola()
    print(resposta)


# Testes de ranking 

def test_ranking_por_aluno_geral():
    controller = ControllerRankingAvaliacao()
    resposta = controller.ranquear_alunos_geral()
    print(resposta)

def test_ranking_por_turma_geral():
    controller = ControllerRankingAvaliacao()
    resposta = controller.ranquear_turmas_geral()
    print(resposta)

def test_ranking_por_escola_geral():
    controller = ControllerRankingAvaliacao()
    resposta = controller.ranquear_escolas_geral()
    print(resposta)

def test_ranking_por_materia_geral():
    controller = ControllerRankingAvaliacao()
    resposta = controller.ranquear_materias_geral()
    print(resposta)

def teste_ranking_por_aluno_escola():
    controller = ControllerRankingAvaliacao(id_escola=ID_ESCOLA_TESTE)
    resposta = controller.ranquear_alunos_por_escola()
    print(resposta)

def teste_ranking_por_turma_escola():
    controller = ControllerRankingAvaliacao(id_escola=ID_ESCOLA_TESTE)
    resposta = controller.ranquear_turmas_por_escola()
    print(resposta)

def teste_ranking_por_materia_escola():
    controller = ControllerRankingAvaliacao(id_escola=ID_ESCOLA_TESTE)
    resposta = controller.ranquear_materias_por_escola()
    print(resposta)

def teste_ranking_tipo_avaliacao_geral():
    controller = ControllerRankingAvaliacao()
    resposta = controller.ranquear_por_tipo_avaliacao_geral()
    print(resposta)

def teste_ranking_tipo_avaliacao_escola():
    controller = ControllerRankingAvaliacao(id_escola=ID_ESCOLA_TESTE)
    resposta = controller.ranquear_por_tipo_avaliacao_por_escola()
    print(resposta)

def teste_ranking_professor_escola():
    controller = ControllerRankingAvaliacao(id_escola=ID_ESCOLA_TESTE)
    resposta = controller.ranquear_professores_por_escola()
    print(resposta)

# Testes relacionados aos dados da IA:

def teste_distrubuicao_notas_IA_geral():
    resultado = ControllerAlunoIA.obter_distribuicao_notas_ia_geral()
    print (resultado)

def teste_distribuicao_notas_IA_Escola():
    resultado = ControllerAlunoIA.obter_distribuicao_notas_ia_escola(id_escola = ID_ESCOLA_TESTE)
    print (resultado)

def teste_distribuicao_notas_IA_por_sexo_geral():
    resultado = ControllerAlunoIA.obter_distribuicao_notas_por_sexo_geral()
    print (resultado)

def teste_distribuicao_notas_IA_por_sexo_escola():
    resultado = ControllerAlunoIA.obter_distribuicao_notas_por_sexo_escola(ID_ESCOLA_TESTE)
    print (resultado)

def teste_distribuicao_participantes_esporte_geral():
    resultado = ControllerAlunoIA.obter_qtd_alunos_por_esporte_geral()
    print(resultado)

def teste_distribuicao_participantes_esporte_escola():
    resultado = ControllerAlunoIA.obter_qtd_alunos_por_esporte_escola(ID_ESCOLA_TESTE)
    print(resultado)

def teste_distribuicao_extra_curricular_geral():
    resultado = ControllerAlunoIA.obter_qtd_alunos_por_extra_curricular_geral()
    print(resultado)

def teste_distribuicao_extra_curricular_escola():
    resultado = ControllerAlunoIA.obter_qtd_alunos_por_extra_curricular_escola(ID_ESCOLA_TESTE)
    print(resultado)
    
def teste_distribuicao_aula_musica_escola():
    resultado = ControllerAlunoIA.obter_qtd_alunos_por_aula_musica_escola(ID_ESCOLA_TESTE)
    print(resultado)
    
def teste_distribuicao_aula_musica_geral():
    resultado = ControllerAlunoIA.obter_qtd_alunos_por_aula_musica_geral()
    print(resultado)

def teste_distribuicao_aulas_Particulares_escola():
    resultado = ControllerAlunoIA.obter_qtd_alunos_por_aulas_particulares_escola(ID_ESCOLA_TESTE)
    print(resultado)

def teste_distribuicao_aulas_Particulares_geral():
    resultado = ControllerAlunoIA.obter_qtd_alunos_por_aulas_particulares_geral()
    print(resultado)

if __name__ == "__main__":
    print("descomente a função que deseja testar")
    #test_criar_escola()
    #test_criar_professor()
    #test_criar_turma()
    #test_criar_aluno()
    #test_criar_materia()
    #test_criar_municipio() 
   
    test_listar_escolas()
    #test_listar_professores()
    #test_listar_turmas()
    #test_listar_alunos_escola()
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
    #test_deletar_escola()
    #test_deletar_professor()
    #test_deletar_turma()
    #test_deletar_aluno()
    #test_deletar_materia()
    #test_deletar_municipio()  

    #test_historico_por_aluno()
    #test_historico_por_turma()
    #test_historico_por_escola()

    #test_ranking_por_aluno_geral()
    #test_ranking_por_turma_geral()
    #test_ranking_por_escola_geral()
    #test_ranking_por_materia_geral()
    #teste_ranking_tipo_avaliacao_geral()

    #teste_ranking_por_aluno_escola()
    #teste_ranking_por_turma_escola()
    #teste_ranking_por_materia_escola()
    #teste_ranking_tipo_avaliacao_escola()
    #teste_ranking_tipo_avaliacao_escola()
    #teste_ranking_professor_escola()

    #teste_distrubuicao_notas_IA_geral()
    #teste_distribuicao_notas_IA_por_sexo_geral()
    #teste_distribuicao_participantes_esporte_geral()
    #teste_distribuicao_extra_curricular_geral()
    #teste_distribuicao_aula_musica_geral()
    #teste_distribuicao_aulas_Particulares_geral()

    #teste_distribuicao_notas_IA_Escola()
    #teste_distribuicao_notas_IA_por_sexo_escola()
    #teste_distribuicao_participantes_esporte_escola()
    #teste_distribuicao_extra_curricular_escola()
    #teste_distribuicao_aula_musica_escola()
    #teste_distribuicao_aulas_Particulares_escola()