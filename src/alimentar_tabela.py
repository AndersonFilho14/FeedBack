import random
from datetime import date, timedelta
from sqlalchemy.exc import IntegrityError # Import IntegrityError

# Importa o handler de conexão e as classes do seu modelo
from infra.db.settings.connection import DBConnectionHandler
from infra.db.models_data import (
    Acesso,
    Professor,
    Cargo,
    Turma,
    Aluno,
    Avaliacao,
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
    with DBConnectionHandler() as session:
        # 2. Popular Cargos (essencial para Acesso)
        print("Populando cargos...")
        cargos_para_criar = ["Professor", "Escola", "Municipio"]

        # Use um dicionário para armazenar os objetos Cargo criados/encontrados
        cargos_existentes = {}

        for cargo_nome in cargos_para_criar:
            # Tenta encontrar o cargo existente
            cargo = session.query(Cargo).filter_by(nome_cargo=cargo_nome).first()
            if not cargo:
                # Se não existir, cria um novo
                cargo = Cargo(nome_cargo=cargo_nome)
                session.add(cargo)
                session.commit() # Comita individualmente para que o ID seja gerado imediatamente
                session.refresh(cargo)
                print(f"Cargo '{cargo_nome}' criado (ID: {cargo.id}).")
            else:
                print(f"Cargo '{cargo_nome}' já existe (ID: {cargo.id}).")
            cargos_existentes[cargo_nome] = cargo

        # Atribua os objetos Cargo encontrados/criados às suas variáveis
        cargo_professor = cargos_existentes["Professor"]
        cargo_escola = cargos_existentes["Escola"]
        cargo_municipio = cargos_existentes["Municipio"]


        # 2.1 Popular acesso
        print("Populando acessos...")
        # Verifica e cria acessos apenas se não existirem
        acesso_prof_exists = session.query(Acesso).filter_by(usuario="prof_alfa").first()
        if not acesso_prof_exists:
            acesso_professor_obj = Acesso(
                usuario="prof_alfa", senha="senha123", id_user="1", id_cargo=cargo_professor.id
            )
            session.add(acesso_professor_obj)
            print("Acesso 'prof_alfa' criado.")
        else:
            print("Acesso 'prof_alfa' já existe.")

        acesso_escola_exists = session.query(Acesso).filter_by(usuario="escola_alfa").first()
        if not acesso_escola_exists:
            acesso_escola_obj = Acesso(
                usuario="escola_alfa", senha="senha123", id_user="1", id_cargo=cargo_escola.id
            )
            session.add(acesso_escola_obj)
            print("Acesso 'escola_alfa' criado.")
        else:
            print("Acesso 'escola_alfa' já existe.")

        acesso_municipio_exists = session.query(Acesso).filter_by(usuario="municipio_alfa").first()
        if not acesso_municipio_exists:
            acesso_municipio_obj = Acesso(
                usuario="municipio_alfa", senha="senha123", id_user="1", id_cargo=cargo_municipio.id
            )
            session.add(acesso_municipio_obj)
            print("Acesso 'municipio_alfa' criado.")
        else:
            print("Acesso 'municipio_alfa' já existe.")

        session.commit() # Comita os acessos

        # 3. Criar Municípios
        print("Criando municípios...")
        municipio_a = session.query(Municipio).filter_by(nome="Cidade Alpha").first()
        if not municipio_a:
            municipio_a = Municipio(nome="Cidade Alpha", regiao="Metropolitana", estado="Pernambuco")
            session.add(municipio_a)
            session.commit()
            session.refresh(municipio_a)
            print(f"Município '{municipio_a.nome}' criado (ID: {municipio_a.id}).")
        else:
            print(f"Município '{municipio_a.nome}' já existe (ID: {municipio_a.id}).")

        municipio_b = session.query(Municipio).filter_by(nome="Cidade Beta").first()
        if not municipio_b:
            municipio_b = Municipio(nome="Cidade Beta", regiao="Interior", estado="Pernambuco")
            session.add(municipio_b)
            session.commit()
            session.refresh(municipio_b)
            print(f"Município '{municipio_b.nome}' criado (ID: {municipio_b.id}).")
        else:
            print(f"Município '{municipio_b.nome}' já existe (ID: {municipio_b.id}).")

        # 4. Criar Escolas (duas por município)
        print("Criando escolas...")
        escolas_list = []
        escola_a1 = session.query(Escola).filter_by(nome="Escola Primaria Alpha I").first()
        if not escola_a1:
            escola_a1 = Escola(nome="Escola Primaria Alpha I", id_municipio=municipio_a.id)
            session.add(escola_a1)
            session.commit()
            session.refresh(escola_a1)
        escolas_list.append(escola_a1)

        escola_a2 = session.query(Escola).filter_by(nome="Escola Secundária Alpha II").first()
        if not escola_a2:
            escola_a2 = Escola(nome="Escola Secundária Alpha II", id_municipio=municipio_a.id)
            session.add(escola_a2)
            session.commit()
            session.refresh(escola_a2)
        escolas_list.append(escola_a2)

        escola_b1 = session.query(Escola).filter_by(nome="Escola Municipal Beta I").first()
        if not escola_b1:
            escola_b1 = Escola(nome="Escola Municipal Beta I", id_municipio=municipio_b.id)
            session.add(escola_b1)
            session.commit()
            session.refresh(escola_b1)
        escolas_list.append(escola_b1)

        escola_b2 = session.query(Escola).filter_by(nome="Escola Estadual Beta II").first()
        if not escola_b2:
            escola_b2 = Escola(nome="Escola Estadual Beta II", id_municipio=municipio_b.id)
            session.add(escola_b2)
            session.commit()
            session.refresh(escola_b2)
        escolas_list.append(escola_b2)
        print("Escolas criadas (ou já existiam).")

        # 5. Criar Turmas (duas por escola)
        print("Criando turmas...")
        turmas = []
        for escola in escolas_list:
            turma1_name = f"1º Ano - {escola.nome[-2:]} A"
            turma2_name = f"1º Ano - {escola.nome[-2:]} B"

            turma1 = session.query(Turma).filter_by(nome=turma1_name, id_escola=escola.id).first()
            if not turma1:
                turma1 = Turma(nome=turma1_name, ano_letivo=2025, id_escola=escola.id)
                session.add(turma1)
            turmas.append(turma1)

            turma2 = session.query(Turma).filter_by(nome=turma2_name, id_escola=escola.id).first()
            if not turma2:
                turma2 = Turma(nome=turma2_name, ano_letivo=2025, id_escola=escola.id)
                session.add(turma2)
            turmas.append(turma2)
        session.commit()
        # Garante que todos os objetos turma têm seus IDs após o commit
        for turma in turmas:
            session.refresh(turma)
        print("Turmas criadas (ou já existiam).")

        # 6. Criar Disciplinas
        print("Criando disciplinas...")
        portugues = session.query(Disciplina).filter_by(nome_disciplina="Português").first()
        if not portugues:
            portugues = Disciplina(nome_disciplina="Português")
            session.add(portugues)
            session.commit()
            session.refresh(portugues)
        print(f"Disciplina '{portugues.nome_disciplina}' criada (ou já existia) (ID: {portugues.id}).")

        matematica = session.query(Disciplina).filter_by(nome_disciplina="Matemática").first()
        if not matematica:
            matematica = Disciplina(nome_disciplina="Matemática")
            session.add(matematica)
            session.commit()
            session.refresh(matematica)
        print(f"Disciplina '{matematica.nome_disciplina}' criada (ou já existia) (ID: {matematica.id}).")


        # 7. Criar Professores
        print("Criando professores (4 por escola, 2 por matéria por turma)...")
        professores = []
        cpf_counter = 1000

        turmas_por_escola = {escola.id: [] for escola in escolas_list}
        for turma in turmas:
            turmas_por_escola[turma.id_escola].append(turma)

        for escola in escolas_list:
            escola_turmas = turmas_por_escola[escola.id]
            # Assumimos que cada escola terá 2 turmas para este exemplo
            turma_a = escola_turmas[0]
            turma_b = escola_turmas[1]

            # Professores de Português para esta escola
            prof_port_1_name = f"Prof. Português 1 - {escola.nome[-2:]}"
            prof_port_1 = session.query(Professor).filter_by(nome=prof_port_1_name, id_escola=escola.id).first()
            if not prof_port_1:
                prof_port_1 = Professor(
                    nome=prof_port_1_name,
                    cpf=f"{cpf_counter:011d}",
                    cargo="Professor de Português",
                    id_escola=escola.id,
                    data_nascimento=date(1980, 5, 15),
                    sexo="Feminino",
                    nacionalidade="Brasileira",
                    estado_civil="Casado(a)",
                    telefone="81999990001",
                )
                session.add(prof_port_1)
                session.commit() # Comita individualmente para ter o ID
                session.refresh(prof_port_1)
            professores.append(prof_port_1)
            cpf_counter += 1

            prof_port_2_name = f"Prof. Português 2 - {escola.nome[-2:]}"
            prof_port_2 = session.query(Professor).filter_by(nome=prof_port_2_name, id_escola=escola.id).first()
            if not prof_port_2:
                prof_port_2 = Professor(
                    nome=prof_port_2_name,
                    cpf=f"{cpf_counter:011d}",
                    cargo="Professor de Português",
                    id_escola=escola.id,
                    data_nascimento=date(1982, 8, 20),
                    sexo="Feminino",
                    nacionalidade="Brasileira",
                    estado_civil="Solteiro(a)",
                    telefone="81999990002",
                )
                session.add(prof_port_2)
                session.commit()
                session.refresh(prof_port_2)
            professores.append(prof_port_2)
            cpf_counter += 1

            # Professores de Matemática para esta escola
            prof_mat_1_name = f"Prof. Matemática 1 - {escola.nome[-2:]}"
            prof_mat_1 = session.query(Professor).filter_by(nome=prof_mat_1_name, id_escola=escola.id).first()
            if not prof_mat_1:
                prof_mat_1 = Professor(
                    nome=prof_mat_1_name,
                    cpf=f"{cpf_counter:011d}",
                    cargo="Professor de Matemática",
                    id_escola=escola.id,
                    data_nascimento=date(1975, 3, 10),
                    sexo="Masculino",
                    nacionalidade="Brasileira",
                    estado_civil="Casado(a)",
                    telefone="81999990003",
                )
                session.add(prof_mat_1)
                session.commit()
                session.refresh(prof_mat_1)
            professores.append(prof_mat_1)
            cpf_counter += 1

            prof_mat_2_name = f"Prof. Matemática 2 - {escola.nome[-2:]}"
            prof_mat_2 = session.query(Professor).filter_by(nome=prof_mat_2_name, id_escola=escola.id).first()
            if not prof_mat_2:
                prof_mat_2 = Professor(
                    nome=prof_mat_2_name,
                    cpf=f"{cpf_counter:011d}",
                    cargo="Professor de Matemática",
                    id_escola=escola.id,
                    data_nascimento=date(1985, 11, 25),
                    sexo="Masculino",
                    nacionalidade="Brasileira",
                    estado_civil="Solteiro(a)",
                    telefone="81999990004",
                )
                session.add(prof_mat_2)
                session.commit()
                session.refresh(prof_mat_2)
            professores.append(prof_mat_2)
            cpf_counter += 1
        print("Professores criados (ou já existiam).")

        # Recarrega o dicionário professores_por_escola_e_disciplina com os objetos atualizados
        professores_por_escola_e_disciplina = {escola.id: {'Português': [], 'Matemática': []} for escola in escolas_list}
        for prof in professores:
            if "Português" in prof.cargo:
                professores_por_escola_e_disciplina[prof.id_escola]['Português'].append(prof)
            elif "Matemática" in prof.cargo:
                professores_por_escola_e_disciplina[prof.id_escola]['Matemática'].append(prof)

        # 8. Criar Tabela de Relação Professor-Turma
        print("Vinculando professores às turmas (um professor por turma por matéria)...")
        prof_turma_data = []
        for escola in escolas_list:
            escola_turmas = sorted(turmas_por_escola[escola.id], key=lambda t: t.nome)

            # Atribuir professores de Português
            if len(escola_turmas) >= 2 and len(professores_por_escola_e_disciplina[escola.id]['Português']) >= 2:
                prof_port_turma_a = professores_por_escola_e_disciplina[escola.id]['Português'][0]
                prof_port_turma_b = professores_por_escola_e_disciplina[escola.id]['Português'][1]

                # Verifica se a relação já existe antes de adicionar
                if not session.query(ProfessorTurma).filter_by(id_professor=prof_port_turma_a.id, id_turma=escola_turmas[0].id).first():
                    prof_turma_data.append(ProfessorTurma(id_professor=prof_port_turma_a.id, id_turma=escola_turmas[0].id))
                if not session.query(ProfessorTurma).filter_by(id_professor=prof_port_turma_b.id, id_turma=escola_turmas[1].id).first():
                    prof_turma_data.append(ProfessorTurma(id_professor=prof_port_turma_b.id, id_turma=escola_turmas[1].id))

            # Atribuir professores de Matemática
            if len(escola_turmas) >= 2 and len(professores_por_escola_e_disciplina[escola.id]['Matemática']) >= 2:
                prof_mat_turma_a = professores_por_escola_e_disciplina[escola.id]['Matemática'][0]
                prof_mat_turma_b = professores_por_escola_e_disciplina[escola.id]['Matemática'][1]

                # Verifica se a relação já existe antes de adicionar
                if not session.query(ProfessorTurma).filter_by(id_professor=prof_mat_turma_a.id, id_turma=escola_turmas[0].id).first():
                    prof_turma_data.append(ProfessorTurma(id_professor=prof_mat_turma_a.id, id_turma=escola_turmas[0].id))
                if not session.query(ProfessorTurma).filter_by(id_professor=prof_mat_turma_b.id, id_turma=escola_turmas[1].id).first():
                    prof_turma_data.append(ProfessorTurma(id_professor=prof_mat_turma_b.id, id_turma=escola_turmas[1].id))

        session.add_all(prof_turma_data)
        session.commit()
        print("Professores vinculados às turmas (ou já estavam vinculados).")

        # 9. Criar Matérias (tópicos dentro das disciplinas)
        print("Criando matérias...")
        materia_port_name = "Gramática"
        materia_port_1 = session.query(Materia).filter_by(nome_materia=materia_port_name, id_disciplina=portugues.id).first()
        if not materia_port_1:
            materia_port_1 = Materia(
                nome_materia=materia_port_name,
                id_disciplina=portugues.id,
                id_professor=professores_por_escola_e_disciplina[escola_a1.id]['Português'][0].id,
            )
            session.add(materia_port_1)
            session.commit()
            session.refresh(materia_port_1)
        print(f"Matéria '{materia_port_name}' criada (ou já existia).")

        materia_mat_name = "Álgebra"
        materia_mat_1 = session.query(Materia).filter_by(nome_materia=materia_mat_name, id_disciplina=matematica.id).first()
        if not materia_mat_1:
            materia_mat_1 = Materia(
                nome_materia=materia_mat_name,
                id_disciplina=matematica.id,
                id_professor=professores_por_escola_e_disciplina[escola_a1.id]['Matemática'][0].id,
            )
            session.add(materia_mat_1)
            session.commit()
            session.refresh(materia_mat_1)
        print(f"Matéria '{materia_mat_name}' criada (ou já existia).")

        # 10. Criar Responsáveis
        print("Criando responsáveis...")
        responsaveis = []
        for i in range(len(turmas) * 3):
            responsavel_name = f"Responsavel {i + 1}"
            responsavel = session.query(Responsavel).filter_by(nome=responsavel_name).first()
            if not responsavel:
                responsavel = Responsavel(
                    nome=responsavel_name,
                    telefone="telefone responsavel",
                )
                session.add(responsavel)
                session.commit()
                session.refresh(responsavel)
            responsaveis.append(responsavel)
        print("Responsáveis criados (ou já existiam).")


        # 11. Criar Alunos (três por turma)
        print("Criando alunos...")
        alunos = []
        responsaveis_disponiveis = list(responsaveis)
        random.shuffle(responsaveis_disponiveis)
        global_aluno_count = 0
        for turma_idx, turma in enumerate(turmas):
            for j in range(3):
                global_aluno_count += 1
                aluno_name = f"Aluno {global_aluno_count} - {turma.nome}"
                aluno = session.query(Aluno).filter_by(nome=aluno_name, id_turma=turma.id).first()

                if not aluno:
                    idade_aluno = random.randint(6, 8)
                    ano_nascimento = 2025 - idade_aluno
                    mes_nascimento = random.randint(1, 12)
                    dia_nascimento = random.randint(1, 28)

                    aluno = Aluno(
                        nome=aluno_name,
                        cpf=f"{600 + global_aluno_count:09d}01",
                        data_nascimento=date(ano_nascimento, mes_nascimento, dia_nascimento),
                        sexo=random.choice(["Masculino", "Feminino"]),
                        nacionalidade="Brasileira",
                        faltas=random.randint(0, 2),
                        nota_score_preditivo=random.uniform(5.0, 9.5),
                        id_escola=turma.id_escola,
                        id_turma=turma.id,
                        id_responsavel=responsaveis_disponiveis.pop().id if responsaveis_disponiveis else None,
                    )
                    session.add(aluno)
                    session.commit()
                    session.refresh(aluno)
                alunos.append(aluno)
        print("Alunos criados (ou já existiam).")

        # 12. Criar Avaliações (com lógica de notas)
        print("Gerando avaliações...")
        avaliacoes_para_adicionar = []
        for aluno_obj in session.query(Aluno).all(): # Renomeado para evitar conflito com 'aluno' do loop anterior
            escola_do_aluno = session.query(Escola).filter_by(id=aluno_obj.id_escola).one()
            municipio_da_escola = session.query(Municipio).filter_by(id=escola_do_aluno.id_municipio).one()
            is_municipio_a = municipio_da_escola.nome == "Cidade Alpha"

            professores_da_turma = (
                session.query(Professor)
                .join(ProfessorTurma)
                .filter(ProfessorTurma.id_turma == aluno_obj.id_turma)
                .all()
            )

            professor_portugues_turma = next((p for p in professores_da_turma if "Português" in p.cargo), None)
            professor_matematica_turma = next((p for p in professores_da_turma if "Matemática" in p.cargo), None)

            portugues = session.query(Disciplina).filter_by(nome_disciplina="Português").one()
            matematica = session.query(Disciplina).filter_by(nome_disciplina="Matemática").one()

            materia_port_1 = session.query(Materia).filter(Materia.id_disciplina == portugues.id).first()
            materia_mat_1 = session.query(Materia).filter(Materia.id_disciplina == matematica.id).first()

            avaliacao_tipos = ["1Va", "2Va", "3Va", "4Va"]
            datas_avaliacao_port = {
                "1Va": date(2025, 4, random.randint(15, 28)),
                "2Va": date(2025, 6, random.randint(15, 28)),
                "3Va": date(2025, 9, random.randint(1, 15)),
                "4Va": date(2025, 11, random.randint(10, 25)),
            }
            datas_avaliacao_mat = {
                "1Va": date(2025, 4, random.randint(15, 28)),
                "2Va": date(2025, 6, random.randint(15, 28)),
                "3Va": date(2025, 9, random.randint(1, 15)),
                "4Va": date(2025, 11, random.randint(10, 25)),
            }


            # --- Avaliações de Português ---
            if professor_portugues_turma and materia_port_1:
                nota_base_port = random.uniform(8.0, 10.0) if is_municipio_a else random.uniform(6.0, 8.5)
                for tipo_avaliacao in avaliacao_tipos:
                    # Verifica se a avaliação já existe para evitar duplicatas
                    existing_avaliacao = session.query(Avaliacao).filter_by(
                        id_aluno=aluno_obj.id,
                        id_disciplina=portugues.id,
                        tipo_avaliacao=tipo_avaliacao
                    ).first()

                    if not existing_avaliacao:
                        nota = round(min(10.0, nota_base_port * random.uniform(0.85, 1.15)), 2)
                        if tipo_avaliacao == "1Va": nota = round(nota_base_port, 2)

                        avaliacoes_para_adicionar.append(Avaliacao(
                            tipo_avaliacao=tipo_avaliacao,
                            data_avaliacao=datas_avaliacao_port[tipo_avaliacao],
                            nota=nota,
                            id_aluno=aluno_obj.id,
                            id_professor=professor_portugues_turma.id,
                            id_disciplina=portugues.id,
                            id_materia=materia_port_1.id,
                            id_turma=aluno_obj.id_turma,
                        ))

            # --- Avaliações de Matemática ---
            if professor_matematica_turma and materia_mat_1:
                nota_base_mat = random.uniform(8.0, 10.0) if not is_municipio_a else random.uniform(6.0, 8.5)
                for tipo_avaliacao in avaliacao_tipos:
                    # Verifica se a avaliação já existe para evitar duplicatas
                    existing_avaliacao = session.query(Avaliacao).filter_by(
                        id_aluno=aluno_obj.id,
                        id_disciplina=matematica.id,
                        tipo_avaliacao=tipo_avaliacao
                    ).first()

                    if not existing_avaliacao:
                        nota = round(min(10.0, nota_base_mat * random.uniform(0.85, 1.15)), 2)
                        if tipo_avaliacao == "1Va": nota = round(nota_base_mat, 2)

                        avaliacoes_para_adicionar.append(Avaliacao(
                            tipo_avaliacao=tipo_avaliacao,
                            data_avaliacao=datas_avaliacao_mat[tipo_avaliacao],
                            nota=nota,
                            id_aluno=aluno_obj.id,
                            id_professor=professor_matematica_turma.id,
                            id_disciplina=matematica.id,
                            id_materia=materia_mat_1.id,
                            id_turma=aluno_obj.id_turma,
                        ))

        session.add_all(avaliacoes_para_adicionar)
        try:
            session.commit()
            print("Avaliações geradas com sucesso.")
        except IntegrityError as e:
            session.rollback()
            print(f"Aviso: Algumas avaliações já existiam e não foram adicionadas novamente. Erro: {e}")


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