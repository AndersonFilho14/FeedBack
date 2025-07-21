import random
from datetime import date

# Importa o handler de conexão e as classes do seu modelo
from infra.db.settings.connection import DBConnectionHandler
from infra.db.models_data import (
    Acesso,
    Professor,
    Cargo,
    Turma,
    Aluno,
    Avaliacao,  # noqa : F401
    Disciplina,
    Escola,
    Materia,
    Municipio,
    ProfessorTurma,
    Responsavel,
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
        cargo_escola = Cargo(nome_cargo="Escola")
        cargo_municipio = Cargo(nome_cargo="Municipio")
        session.add_all([cargo_professor, cargo_escola, cargo_municipio])
        session.commit()
        # Após o commit, os IDs são gerados. Precisamos refresh para ter certeza que os objetos têm IDs.
        session.refresh(cargo_professor)
        session.refresh(cargo_escola)
        session.refresh(cargo_municipio)

        # 2.1 Popular acesso
        acesso_professor = Acesso(
            usuario="prof_alfa", senha="senha123", id_user="1", id_cargo=1
        )
        acesso_escola = Acesso(
            usuario="escola_alfa", senha="senha123", id_user="1", id_cargo=2
        )
        acesso_municipio = Acesso(
            usuario="municipio_alfa", senha="senha123", id_user="1", id_cargo=3
        )
        session.add_all([acesso_professor, acesso_escola, acesso_municipio])
        session.commit()
        # Após o commit, os IDs são gerados. Precisamos refresh para ter certeza que os objetos têm IDs.
        session.refresh(cargo_professor)
        session.refresh(cargo_escola)
        session.refresh(cargo_municipio)

        # 3. Criar Municípios
        print("Criando municípios...")
        municipio_a = Municipio(
            nome="Cidade Alpha", regiao="Metropolitana", estado="Pernambuco"
        )
        municipio_b = Municipio(
            nome="Cidade Beta", regiao="Interior", estado="Pernambuco"
        )
        session.add_all([municipio_a, municipio_b])
        session.commit()
        session.refresh(municipio_a)
        session.refresh(municipio_b)
        print(
            f"Municípios criados: {municipio_a.nome} (ID: {municipio_a.id}), {municipio_b.nome} (ID: {municipio_b.id})"
        )

        # 4. Criar Escolas (duas por município)
        print("Criando escolas...")
        escola_a1 = Escola(nome="Escola Primaria Alpha I", id_municipio=municipio_a.id)
        escola_a2 = Escola(
            nome="Escola Secundária Alpha II", id_municipio=municipio_a.id
        )
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
        for escola in (
            escolas_list
        ):  # Removi 'i' desnecessário no loop externo, pois 'j' está no interno.
            turma1 = Turma(
                nome=f"1º Ano - {escola.nome[-2:]}",
                ano_letivo=2025,
                id_escola=escola.id,
            )
            turma2 = Turma(
                nome=f"2º Ano - {escola.nome[-2:]}",
                ano_letivo=2025,
                id_escola=escola.id,
            )
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
        print(
            f"Disciplinas criadas: {portugues.nome_disciplina} (ID: {portugues.id}), {matematica.nome_disciplina} (ID: {matematica.id})"
        )

        # 7. Criar Professores (Matemática e Português)
        prof_portugues1 = Professor(
            nome="Prof. Ana Silva",
            cpf="11122233344",
            cargo="Professor de Português",
            id_escola=escola_a1.id,
            data_nascimento=date(1980, 5, 20),
            sexo="feminino",
            nacionalidade="Brasileira",
            estado_civil="Casada",
            telefone="(81) 98888-1111",
            email="ana.silva@escola.com",
            senha="senhaForteAna2025"
        )

        prof_portugues2 = Professor(
            nome="Prof. Bia Costa",
            cpf="22233344455",
            cargo="Professor de Português",
            id_escola=escola_b1.id,
            data_nascimento=date(1983, 3, 14),
            sexo="feminino",
            nacionalidade="Brasileira",
            estado_civil="Solteira",
            telefone="(81) 97777-2222",
            email="bia.costa@escola.com",
            senha="senhaForteBia2025"
        )

        prof_matematica1 = Professor(
            nome="Prof. Carlos Santos",
            cpf="33344455566",
            cargo="Professor de Matemática",
            id_escola=escola_a2.id,
            data_nascimento=date(1985, 9, 15),
            sexo="masculino",
            nacionalidade="Brasileiro",
            estado_civil="Solteiro",
            telefone="(81) 91234-5678",
            email="carlos.santos@escola.com",
            senha="senhaForteCarlos2025"
        )

        prof_matematica2 = Professor(
            nome="Prof. Daniel Pereira",
            cpf="44455566677",
            cargo="Professor de Matemática",
            id_escola=escola_b2.id,
            data_nascimento=date(1982, 11, 30),
            sexo="masculino",
            nacionalidade="Brasileiro",
            estado_civil="Casado",
            telefone="(81) 93456-7890",
            email="daniel.pereira@escola.com",
            senha="senhaForteDaniel2025"
        )
        session.add_all(
            [prof_portugues1, prof_portugues2, prof_matematica1, prof_matematica2]
        )
        session.commit()
        session.refresh(prof_portugues1)
        session.refresh(prof_portugues2)
        session.refresh(prof_matematica1)
        session.refresh(prof_matematica2)
        print("Professores criados.")

        # 8. Criar Tabela de Relação Professor-Turma
        print("Vinculando professores às turmas...")
        prof_turma_data = []
        prof_turma_data.append(
            ProfessorTurma(id_professor=prof_portugues1.id, id_turma=turmas[0].id)
        )
        prof_turma_data.append(
            ProfessorTurma(id_professor=prof_portugues1.id, id_turma=turmas[1].id)
        )
        prof_turma_data.append(
            ProfessorTurma(id_professor=prof_matematica1.id, id_turma=turmas[2].id)
        )
        prof_turma_data.append(
            ProfessorTurma(id_professor=prof_matematica1.id, id_turma=turmas[3].id)
        )
        prof_turma_data.append(
            ProfessorTurma(id_professor=prof_portugues2.id, id_turma=turmas[4].id)
        )
        prof_turma_data.append(
            ProfessorTurma(id_professor=prof_portugues2.id, id_turma=turmas[5].id)
        )
        prof_turma_data.append(
            ProfessorTurma(id_professor=prof_matematica2.id, id_turma=turmas[6].id)
        )
        prof_turma_data.append(
            ProfessorTurma(id_professor=prof_matematica2.id, id_turma=turmas[7].id)
        )
        session.add_all(prof_turma_data)
        session.commit()
        print("Professores vinculados às turmas.")

        # 9. Criar Matérias (tópicos dentro das disciplinas)
        print("Criando matérias...")
        materia_port_1 = Materia(
            nome_materia="Gramática",
            id_disciplina=portugues.id,
            id_professor=prof_portugues1.id,
        )
        materia_port_2 = Materia(
            nome_materia="Interpretação de Texto",
            id_disciplina=portugues.id,
            id_professor=prof_portugues2.id,
        )
        materia_mat_1 = Materia(
            nome_materia="Álgebra",
            id_disciplina=matematica.id,
            id_professor=prof_matematica1.id,
        )
        materia_mat_2 = Materia(
            nome_materia="Geometria",
            id_disciplina=matematica.id,
            id_professor=prof_matematica2.id,
        )
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
            responsaveis.append(
                Responsavel(
                    nome=f"Responsável {i + 1}",
                    telefone=f"(81) 9{random.randint(1000,9999)}-{random.randint(1000,9999)}"
                )
            )
        session.add_all(responsaveis)
        session.commit()
        for resp in responsaveis:
            session.refresh(resp)
        print("Responsáveis criados.")

        # 11. Criar Alunos (três por turma)
        print("Criando alunos...")
        alunos = []
        responsavel_idx = 0
        global_aluno_count = 0  # Adicionado um contador global para o nome do aluno
        for turma_idx, turma in enumerate(turmas):
            for j in range(3):
                global_aluno_count += 1
                aluno = Aluno(
                    nome=f"Aluno {global_aluno_count} - {turma.nome}",
                    cpf=f"{600 + global_aluno_count:09d}01",
                    faltas=random.randint(0, 2),
                    nota_score_preditivo=random.uniform(5.0, 9.5),
                    id_escola=turma.id_escola,
                    id_turma=turma.id,
                    id_responsavel=responsaveis[responsavel_idx].id,
                    data_nascimento=date(2015, random.randint(1, 12), random.randint(1, 28)),
                    sexo=random.choice(["masculino", "feminino"]),
                    nacionalidade="Brasileiro",
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
        avaliacoes_para_adicionar = []
        for aluno in session.query(Aluno).all():
            escola_do_aluno = session.query(Escola).filter_by(id=aluno.id_escola).one()
            municipio_da_escola = session.query(Municipio).filter_by(id=escola_do_aluno.id_municipio).one()
            is_municipio_a = municipio_da_escola.nome == "Cidade Alpha"

            # Determina os professores corretos para o aluno
            prof_portugues1 = session.query(Professor).filter(Professor.nome.contains("Ana Silva")).one()
            prof_portugues2 = session.query(Professor).filter(Professor.nome.contains("Bia Costa")).one()
            prof_matematica1 = session.query(Professor).filter(Professor.nome.contains("Carlos Santos")).one()
            prof_matematica2 = session.query(Professor).filter(Professor.nome.contains("Daniel Pereira")).one()
            portugues = session.query(Disciplina).filter_by(nome_disciplina="Português").one()
            matematica = session.query(Disciplina).filter_by(nome_disciplina="Matemática").one()
            materia_port_1 = session.query(Materia).filter(Materia.nome_materia == "Gramática").one()
            materia_port_2 = session.query(Materia).filter(Materia.nome_materia == "Interpretação de Texto").one()
            materia_mat_1 = session.query(Materia).filter(Materia.nome_materia == "Álgebra").one()
            materia_mat_2 = session.query(Materia).filter(Materia.nome_materia == "Geometria").one()


            if escola_do_aluno.id_municipio == municipio_a.id:
                professor_portugues = prof_portugues1
                professor_matematica = prof_matematica1
            else:
                professor_portugues = prof_portugues2
                professor_matematica = prof_matematica2

            # --- Avaliações de Português (1Va e 2Va) ---
            nota_base_port = random.uniform(8.0, 10.0) if is_municipio_a else random.uniform(6.0, 8.5)
            avaliacoes_para_adicionar.append(Avaliacao(
                tipo_avaliacao="1Va",
                data_avaliacao=date(2025, 4, random.randint(15, 28)),
                nota=round(nota_base_port, 2),
                id_aluno=aluno.id,
                id_professor=professor_portugues.id,
                id_disciplina=portugues.id,
                id_materia=random.choice([materia_port_1.id, materia_port_2.id]),
                id_turma=aluno.id_turma,
            ))
            avaliacoes_para_adicionar.append(Avaliacao(
                tipo_avaliacao="2Va",
                data_avaliacao=date(2025, 6, random.randint(15, 28)),
                nota=round(min(10.0, nota_base_port * random.uniform(0.9, 1.1)), 2),
                id_aluno=aluno.id,
                id_professor=professor_portugues.id,
                id_disciplina=portugues.id,
                id_materia=random.choice([materia_port_1.id, materia_port_2.id]),
                id_turma=aluno.id_turma,
            ))
            avaliacoes_para_adicionar.append(Avaliacao(
                tipo_avaliacao="3Va",
                data_avaliacao=date(2025, 8, random.randint(15, 28)),
                nota=round(min(10.0, nota_base_port * random.uniform(0.85, 1.05)), 2),
                id_aluno=aluno.id,
                id_professor=professor_portugues.id,
                id_disciplina=portugues.id,
                id_materia=random.choice([materia_port_1.id, materia_port_2.id]),
                id_turma=aluno.id_turma,
            ))
            avaliacoes_para_adicionar.append(Avaliacao(
                tipo_avaliacao="4Va",
                data_avaliacao=date(2025, 10, random.randint(15, 28)),
                nota=round(min(10.0, nota_base_port * random.uniform(0.8, 1.0)), 2),
                id_aluno=aluno.id,
                id_professor=professor_portugues.id,
                id_disciplina=portugues.id,
                id_materia=random.choice([materia_port_1.id, materia_port_2.id]),
                id_turma=aluno.id_turma,
            ))

            # --- Avaliações de Matemática (1Va e 2Va) ---
            nota_base_mat = random.uniform(8.0, 10.0) if not is_municipio_a else random.uniform(6.0, 8.5)
            avaliacoes_para_adicionar.append(Avaliacao(
                tipo_avaliacao="1Va",
                data_avaliacao=date(2025, 4, random.randint(15, 28)),
                nota=round(nota_base_mat, 2),
                id_aluno=aluno.id,
                id_professor=professor_matematica.id,
                id_disciplina=matematica.id,
                id_materia=random.choice([materia_mat_1.id, materia_mat_2.id]),
                id_turma=aluno.id_turma,
            ))
            avaliacoes_para_adicionar.append(Avaliacao(
                tipo_avaliacao="2Va",
                data_avaliacao=date(2025, 6, random.randint(15, 28)),
                nota=round(min(10.0, nota_base_mat * random.uniform(0.9, 1.1)), 2),
                id_aluno=aluno.id,
                id_professor=professor_matematica.id,
                id_disciplina=matematica.id,
                id_materia=random.choice([materia_mat_1.id, materia_mat_2.id]),
                id_turma=aluno.id_turma,
            ))
            avaliacoes_para_adicionar.append(Avaliacao(
                tipo_avaliacao="3Va",
                data_avaliacao=date(2025, 8, random.randint(15, 28)),
                nota=round(min(10.0, nota_base_mat * random.uniform(0.85, 1.05)), 2),
                id_aluno=aluno.id,
                id_professor=professor_matematica.id,
                id_disciplina=matematica.id,
                id_materia=random.choice([materia_mat_1.id, materia_mat_2.id]),
                id_turma=aluno.id_turma,
            ))
            avaliacoes_para_adicionar.append(Avaliacao(
                tipo_avaliacao="4Va",
                data_avaliacao=date(2025, 10, random.randint(15, 28)),
                nota=round(min(10.0, nota_base_mat * random.uniform(0.8, 1.0)), 2),
                id_aluno=aluno.id,
                id_professor=professor_matematica.id,
                id_disciplina=matematica.id,
                id_materia=random.choice([materia_mat_1.id, materia_mat_2.id]),
                id_turma=aluno.id_turma,
            ))

        session.add_all(avaliacoes_para_adicionar)
        session.commit()
        print("Avaliações geradas com sucesso.")

        # --- Verificação de Dados Atualizada ---
        print("\n--- Verificando dados (amostra) ---")
        portugues = session.query(Disciplina).filter_by(nome_disciplina="Português").one()
        matematica = session.query(Disciplina).filter_by(nome_disciplina="Matemática").one()

        print("\nAlunos da Cidade Alpha com notas de Português:")
        alunos_alpha_query = (
            session.query(Aluno).join(Escola).join(Municipio).filter(Municipio.nome == "Cidade Alpha")
        )
        for aluno_obj in alunos_alpha_query:
            turma_do_aluno = session.query(Turma).filter_by(id=aluno_obj.id_turma).one()
            avaliacoes = (
                session.query(Avaliacao)
                .filter(Avaliacao.id_aluno == aluno_obj.id, Avaliacao.id_disciplina == portugues.id)
                .order_by(Avaliacao.tipo_avaliacao)
                .all()
            )
            notas_str = ", ".join([f"{ava.tipo_avaliacao}: {ava.nota}" for ava in avaliacoes])
            print(f"- {aluno_obj.nome} (Turma: {turma_do_aluno.nome}) - Português: {notas_str}")

        print("\nAlunos da Cidade Beta com notas de Matemática:")
        alunos_beta_query = (
            session.query(Aluno).join(Escola).join(Municipio).filter(Municipio.nome == "Cidade Beta")
        )
        for aluno_obj in alunos_beta_query:
            turma_do_aluno = session.query(Turma).filter_by(id=aluno_obj.id_turma).one()
            avaliacoes = (
                session.query(Avaliacao)
                .filter(Avaliacao.id_aluno == aluno_obj.id, Avaliacao.id_disciplina == matematica.id)
                .order_by(Avaliacao.tipo_avaliacao)
                .all()
            )
            notas_str = ", ".join([f"{ava.tipo_avaliacao}: {ava.nota}" for ava in avaliacoes])
            print(f"- {aluno_obj.nome} (Turma: {turma_do_aluno.nome}) - Matemática: {notas_str}")

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
