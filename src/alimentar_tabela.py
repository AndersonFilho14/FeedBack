import random
from datetime import date

# Importa o handler de conexão e as classes do seu modelo
from infra.db.settings.connection import DBConnectionHandler
from infra.db.models_data import (
    Acesso, Professor, Cargo, Turma, Aluno, Avaliacao, # noqa : F401
    Disciplina, Escola, Materia, Municipio,
    ProfessorTurma, Responsavel
)

def popular_dados():
    """
    Popula o banco de dados com dados de exemplo, seguindo as especificações.
    """
    # A sessão do SQLAlchemy é obtida através do DBConnectionHandler
    with DBConnectionHandler() as session:


        # Se o seu DBConnectionHandler já chama Base.metadata.create_all(engine)
        # ao ser inicializado, esta linha não é necessária aqui.
        # Caso contrário, adicione uma chamada para criar as tabelas aqui.

        # 2. Popular Cargos (essencial para Acesso)
        print("Populando cargos...")
        cargo_professor = Cargo(nome_cargo="Professor")
        cargo_aluno = Cargo(nome_cargo="Aluno")
        cargo_responsavel = Cargo(nome_cargo="Responsavel")
        cargo_coordenador = Cargo(nome_cargo="Coordenador")
        session.add_all([cargo_professor, cargo_aluno, cargo_responsavel, cargo_coordenador])
        session.commit()
        # Após o commit, os IDs são gerados. Precisamos refresh para ter certeza que os objetos têm IDs.
        session.refresh(cargo_professor)
        session.refresh(cargo_aluno)
        session.refresh(cargo_responsavel)
        session.refresh(cargo_coordenador)

        # 3. Criar Municípios
        print("Criando municípios...")
        municipio_a = Municipio(nome="Cidade Alpha", regiao="Metropolitana", estado="Pernambuco")
        municipio_b = Municipio(nome="Cidade Beta", regiao="Interior", estado="Pernambuco")
        session.add_all([municipio_a, municipio_b])
        session.commit()
        session.refresh(municipio_a)
        session.refresh(municipio_b)
        print(f"Municípios criados: {municipio_a.nome} (ID: {municipio_a.id}), {municipio_b.nome} (ID: {municipio_b.id})")

        # 4. Criar Escolas (duas por município)
        print("Criando escolas...")
        escola_a1 = Escola(nome="Escola Primaria Alpha I", id_municipio=municipio_a.id)
        escola_a2 = Escola(nome="Escola Secundária Alpha II", id_municipio=municipio_a.id)
        escola_b1 = Escola(nome="Escola Municipal Beta I", id_municipio=municipio_b.id)
        escola_b2 = Escola(nome="Escola Estadual Beta II", id_municipio=municipio_b.id)
        session.add_all([escola_a1, escola_a2, escola_b1, escola_b2])
        session.commit()
        session.refresh(escola_a1)
        session.refresh(escola_a2)
        session.refresh(escola_b1)
        session.refresh(escola_b2)
        print("Escolas criadas.")

        # 5. Criar Turmas (duas por escola)
        print("Criando turmas...")
        turmas = []
        escolas_list = [escola_a1, escola_a2, escola_b1, escola_b2]
        for escola in escolas_list: # Removi 'i' desnecessário no loop externo, pois 'j' está no interno.
            turma1 = Turma(nome=f"1º Ano - {escola.nome[-2:]}", ano_letivo=2025, id_escola=escola.id)
            turma2 = Turma(nome=f"2º Ano - {escola.nome[-2:]}", ano_letivo=2025, id_escola=escola.id)
            turmas.extend([turma1, turma2])
        session.add_all(turmas)
        session.commit()
        for turma in turmas:
            session.refresh(turma)
        print("Turmas criadas.")

        # 6. Criar Disciplinas
        print("Criando disciplinas...")
        portugues = Disciplina(nome_disciplina="Português")
        matematica = Disciplina(nome_disciplina="Matemática")
        session.add_all([portugues, matematica])
        session.commit()
        session.refresh(portugues)
        session.refresh(matematica)
        print(f"Disciplinas criadas: {portugues.nome_disciplina} (ID: {portugues.id}), {matematica.nome_disciplina} (ID: {matematica.id})")

        # 7. Criar Professores (Matemática e Português)
        print("Criando professores...")
        prof_portugues1 = Professor(nome="Prof. Ana Silva", cpf="11122233344", cargo="Professor de Português", id_escola=escola_a1.id)
        prof_portugues2 = Professor(nome="Prof. Bia Costa", cpf="22233344455", cargo="Professor de Português", id_escola=escola_b1.id)
        prof_matematica1 = Professor(nome="Prof. Carlos Santos", cpf="33344455566", cargo="Professor de Matemática", id_escola=escola_a2.id)
        prof_matematica2 = Professor(nome="Prof. Daniel Pereira", cpf="44455566677", cargo="Professor de Matemática", id_escola=escola_b2.id)
        session.add_all([prof_portugues1, prof_portugues2, prof_matematica1, prof_matematica2])
        session.commit()
        session.refresh(prof_portugues1)
        session.refresh(prof_portugues2)
        session.refresh(prof_matematica1)
        session.refresh(prof_matematica2)
        print("Professores criados.")

        # 8. Criar Tabela de Relação Professor-Turma
        print("Vinculando professores às turmas...")
        prof_turma_data = []
        prof_turma_data.append(ProfessorTurma(id_professor=prof_portugues1.id, id_turma=turmas[0].id))
        prof_turma_data.append(ProfessorTurma(id_professor=prof_portugues1.id, id_turma=turmas[1].id))
        prof_turma_data.append(ProfessorTurma(id_professor=prof_matematica1.id, id_turma=turmas[2].id))
        prof_turma_data.append(ProfessorTurma(id_professor=prof_matematica1.id, id_turma=turmas[3].id))
        prof_turma_data.append(ProfessorTurma(id_professor=prof_portugues2.id, id_turma=turmas[4].id))
        prof_turma_data.append(ProfessorTurma(id_professor=prof_portugues2.id, id_turma=turmas[5].id))
        prof_turma_data.append(ProfessorTurma(id_professor=prof_matematica2.id, id_turma=turmas[6].id))
        prof_turma_data.append(ProfessorTurma(id_professor=prof_matematica2.id, id_turma=turmas[7].id))
        session.add_all(prof_turma_data)
        session.commit()
        print("Professores vinculados às turmas.")

        # 9. Criar Matérias (tópicos dentro das disciplinas)
        print("Criando matérias...")
        materia_port_1 = Materia(nome_materia="Gramática", id_disciplina=portugues.id, id_professor=prof_portugues1.id)
        materia_port_2 = Materia(nome_materia="Interpretação de Texto", id_disciplina=portugues.id, id_professor=prof_portugues2.id)
        materia_mat_1 = Materia(nome_materia="Álgebra", id_disciplina=matematica.id, id_professor=prof_matematica1.id)
        materia_mat_2 = Materia(nome_materia="Geometria", id_disciplina=matematica.id, id_professor=prof_matematica2.id)
        session.add_all([materia_port_1, materia_port_2, materia_mat_1, materia_mat_2])
        session.commit()
        session.refresh(materia_port_1)
        session.refresh(materia_port_2)
        session.refresh(materia_mat_1)
        session.refresh(materia_mat_2)
        print("Matérias criadas.")

        # 10. Criar Responsáveis
        print("Criando responsáveis...")
        responsaveis = []
        for i in range(len(turmas) * 3):
            responsaveis.append(Responsavel(
                nome=f"Responsavel {i+1}",
                cpf=f"{500+i:09d}00",
                parentesco=random.choice(["Mãe", "Pai", "Avó"])
            ))
        session.add_all(responsaveis)
        session.commit()
        for resp in responsaveis:
            session.refresh(resp)
        print("Responsáveis criados.")

        # 11. Criar Alunos (três por turma)
        print("Criando alunos...")
        alunos = []
        responsavel_idx = 0
        global_aluno_count = 0 # Adicionado um contador global para o nome do aluno
        for turma_idx, turma in enumerate(turmas): # Usei 'turma_idx' para evitar conflito com 'i' no f-string
            for j in range(3): # 'j' está corretamente definido aqui
                global_aluno_count += 1
                aluno = Aluno(
                    nome=f"Aluno {global_aluno_count} - {turma.nome}", # Usando o contador global
                    cpf=f"{600+global_aluno_count:09d}01",
                    idade=random.randint(6, 8),
                    faltas=random.randint(0, 2),
                    nota_score_preditivo=random.uniform(5.0, 9.5),
                    id_escola=turma.id_escola,
                    id_turma=turma.id,
                    id_responsavel=responsaveis[responsavel_idx].id
                )
                alunos.append(aluno)
                responsavel_idx += 1
        session.add_all(alunos)
        session.commit()
        for aluno in alunos:
            session.refresh(aluno)
        print("Alunos criados.")

        # 12. Criar Avaliações (com lógica de notas)
        print("Gerando avaliações...")
        for aluno in alunos:
            escola_do_aluno = session.query(Escola).filter_by(id=aluno.id_escola).first()
            municipio_da_escola = session.query(Municipio).filter_by(id=escola_do_aluno.id_municipio).first()

            is_municipio_a = municipio_da_escola.nome == "Cidade Alpha"

            # --- Lógica para o Professor de Português ---
            # Vamos garantir que sempre tenhamos um professor de português
            # Podemos usar os professores que já criamos e associá-los de forma mais flexível.
            # Se o aluno é da escola A1 ou A2 (Cidade Alpha), usa prof_portugues1.
            # Se o aluno é da escola B1 ou B2 (Cidade Beta), usa prof_portugues2.
            if escola_do_aluno.id == escola_a1.id or escola_do_aluno.id == escola_a2.id:
                professor_portugues_para_avaliacao = prof_portugues1
            else:
                professor_portugues_para_avaliacao = prof_portugues2

            # Avaliação de Português
            nota_port = random.uniform(8.0, 10.0) if is_municipio_a else random.uniform(6.0, 8.5)

            avaliacao_portugues = Avaliacao(
                tipo_avaliacao="Prova Mensal",
                data_avaliacao=date(2025, random.randint(3, 5), random.randint(1, 28)),
                nota_1=round(nota_port, 2),
                nota_2=round(random.uniform(nota_port * 0.9, nota_port * 1.1), 2),
                nota_3=round(random.uniform(nota_port * 0.9, nota_port * 1.1), 2),
                nota_4=round(random.uniform(nota_port * 0.9, nota_port * 1.1), 2),
                id_aluno=aluno.id,
                # AGORA SABEMOS QUE professor_portugues_para_avaliacao TEM UM OBJETO VÁLIDO
                id_professor=professor_portugues_para_avaliacao.id,
                id_disciplina=portugues.id,
                id_materia=random.choice([materia_port_1, materia_port_2]).id,
                id_turma=aluno.id_turma
            )
            session.add(avaliacao_portugues)

            # --- Lógica para o Professor de Matemática ---
            # Mesma lógica, mas para matemática.
            if escola_do_aluno.id == escola_a1.id or escola_do_aluno.id == escola_a2.id:
                professor_matematica_para_avaliacao = prof_matematica1
            else:
                professor_matematica_para_avaliacao = prof_matematica2

            # Avaliação de Matemática
            nota_mat = random.uniform(8.0, 10.0) if not is_municipio_a else random.uniform(6.0, 8.5)

            avaliacao_matematica = Avaliacao(
                tipo_avaliacao="Prova Bimestral",
                data_avaliacao=date(2025, random.randint(3, 5), random.randint(1, 28)),
                nota_1=round(nota_mat, 2),
                nota_2=round(random.uniform(nota_mat * 0.9, nota_mat * 1.1), 2),
                nota_3=round(random.uniform(nota_mat * 0.9, nota_mat * 1.1), 2),
                nota_4=round(random.uniform(nota_mat * 0.9, nota_mat * 1.1), 2),
                id_aluno=aluno.id,
                # AGORA SABEMOS QUE professor_matematica_para_avaliacao TEM UM OBJETO VÁLIDO
                id_professor=professor_matematica_para_avaliacao.id,
                id_disciplina=matematica.id,
                id_materia=random.choice([materia_mat_1, materia_mat_2]).id,
                id_turma=aluno.id_turma
            )
            session.add(avaliacao_matematica)
        session.commit()
        print("Avaliações geradas com sucesso.")

        # Exemplo de consulta para verificar (agora com JOINs explícitos)
        print("\n--- Verificando dados (amostra) ---")
        print("\nAlunos da Cidade Alpha com notas de Português:")
        # Para consultar, precisamos de JOINs manuais no ORM
        alunos_alpha_query = session.query(Aluno, Escola, Municipio). \
            join(Escola, Aluno.id_escola == Escola.id). \
            join(Municipio, Escola.id_municipio == Municipio.id). \
            filter(Municipio.nome == "Cidade Alpha").all()

        for aluno_obj, escola_obj, municipio_obj in alunos_alpha_query:
            # Buscar a turma separadamente, se Aluno.turma não for um relationship
            turma_do_aluno = session.query(Turma).filter_by(id=aluno_obj.id_turma).first()

            avaliacoes_portugues_aluno = session.query(Avaliacao, Disciplina, Turma). \
                join(Disciplina, Avaliacao.id_disciplina == Disciplina.id). \
                join(Turma, Avaliacao.id_turma == Turma.id). \
                filter(Avaliacao.id_aluno == aluno_obj.id, Disciplina.nome_disciplina == "Português").first()

            if avaliacoes_portugues_aluno:
                avaliacao, disciplina, turma_da_avaliacao = avaliacoes_portugues_aluno
                # Usar turma_do_aluno.nome para ter certeza que é o nome da turma do aluno
                print(f"- {aluno_obj.nome} (Escola: {escola_obj.nome}, Turma: {turma_do_aluno.nome}) - Português: {avaliacao.nota_1}")

        print("\nAlunos da Cidade Beta com notas de Matemática:")
        alunos_beta_query = session.query(Aluno, Escola, Municipio). \
            join(Escola, Aluno.id_escola == Escola.id). \
            join(Municipio, Escola.id_municipio == Municipio.id). \
            filter(Municipio.nome == "Cidade Beta").all()

        for aluno_obj, escola_obj, municipio_obj in alunos_beta_query:
            # Buscar a turma separadamente
            turma_do_aluno = session.query(Turma).filter_by(id=aluno_obj.id_turma).first()

            avaliacoes_matematica_aluno = session.query(Avaliacao, Disciplina, Turma). \
                join(Disciplina, Avaliacao.id_disciplina == Disciplina.id). \
                join(Turma, Avaliacao.id_turma == Turma.id). \
                filter(Avaliacao.id_aluno == aluno_obj.id, Disciplina.nome_disciplina == "Matemática").first()

            if avaliacoes_matematica_aluno:
                avaliacao, disciplina, turma_da_avaliacao = avaliacoes_matematica_aluno
                print(f"- {aluno_obj.nome} (Escola: {escola_obj.nome}, Turma: {turma_do_aluno.nome}) - Matemática: {avaliacao.nota_1}")

        print("\nPopulação de dados concluída!")

if __name__ == "__main__":
    try:
        popular_dados()
    except Exception as exception:
        print(f"Erro ao popular os dados. Tipo de erro: {str(exception)}")
        # Removendo 'raise exception' para que o script termine após a mensagem de erro,
        # sem mostrar todo o traceback se for um erro conhecido.
        # Se você ainda precisar do traceback completo para depuração, pode adicionar de volta.
        # raise exception
