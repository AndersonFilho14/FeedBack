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
        for escola in escolas_list:
            turma1 = Turma(
                nome=f"1º Ano - {escola.nome[-2:]} A",
                ano_letivo=2025,
                id_escola=escola.id,
            )
            turma2 = Turma(
                nome=f"1º Ano - {escola.nome[-2:]} B",
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

        # 7. Criar Professores
        print("Criando professores (4 por escola, 2 por matéria por turma)...")
        professores = []
        # Mapeamento para garantir CPF único e nomes descritivos
        cpf_counter = 1000
        
        # Obtenha as turmas e agrupe-as por escola para facilitar a atribuição
        turmas_por_escola = {escola.id: [] for escola in escolas_list}
        for turma in turmas:
            turmas_por_escola[turma.id_escola].append(turma)

        for escola in escolas_list:
            escola_turmas = turmas_por_escola[escola.id]
            # Assumimos que cada escola terá 2 turmas para este exemplo
            turma_a = escola_turmas[0]
            turma_b = escola_turmas[1]

            # Professores de Português para esta escola
            prof_port_1 = Professor(
                nome=f"Prof. Português 1 - {escola.nome[-2:]}",
                cpf=f"{cpf_counter:011d}",
                cargo="Professor de Português",
                id_escola=escola.id,
            )
            cpf_counter += 1
            prof_port_2 = Professor(
                nome=f"Prof. Português 2 - {escola.nome[-2:]}",
                cpf=f"{cpf_counter:011d}",
                cargo="Professor de Português",
                id_escola=escola.id,
            )
            cpf_counter += 1

            # Professores de Matemática para esta escola
            prof_mat_1 = Professor(
                nome=f"Prof. Matemática 1 - {escola.nome[-2:]}",
                cpf=f"{cpf_counter:011d}",
                cargo="Professor de Matemática",
                id_escola=escola.id,
            )
            cpf_counter += 1
            prof_mat_2 = Professor(
                nome=f"Prof. Matemática 2 - {escola.nome[-2:]}",
                cpf=f"{cpf_counter:011d}",
                cargo="Professor de Matemática",
                id_escola=escola.id,
            )
            cpf_counter += 1

            professores.extend([prof_port_1, prof_port_2, prof_mat_1, prof_mat_2])

        session.add_all(professores)
        session.commit()
        for prof in professores:
            session.refresh(prof)
        print("Professores criados.")

        # 8. Criar Tabela de Relação Professor-Turma
        print("Vinculando professores às turmas (um professor por turma por matéria)...")
        prof_turma_data = []
        professores_por_escola_e_disciplina = {escola.id: {'Português': [], 'Matemática': []} for escola in escolas_list}
        
        for prof in professores:
            if "Português" in prof.cargo:
                professores_por_escola_e_disciplina[prof.id_escola]['Português'].append(prof)
            elif "Matemática" in prof.cargo:
                professores_por_escola_e_disciplina[prof.id_escola]['Matemática'].append(prof)

        for escola in escolas_list:
            escola_turmas = sorted(turmas_por_escola[escola.id], key=lambda t: t.nome) # Ordenar para garantir consistência
            
            # Atribuir professores de Português
            if len(escola_turmas) >= 2 and len(professores_por_escola_e_disciplina[escola.id]['Português']) >= 2:
                prof_port_turma_a = professores_por_escola_e_disciplina[escola.id]['Português'][0]
                prof_port_turma_b = professores_por_escola_e_disciplina[escola.id]['Português'][1]
                
                prof_turma_data.append(ProfessorTurma(id_professor=prof_port_turma_a.id, id_turma=escola_turmas[0].id))
                prof_turma_data.append(ProfessorTurma(id_professor=prof_port_turma_b.id, id_turma=escola_turmas[1].id))
            
            # Atribuir professores de Matemática
            if len(escola_turmas) >= 2 and len(professores_por_escola_e_disciplina[escola.id]['Matemática']) >= 2:
                prof_mat_turma_a = professores_por_escola_e_disciplina[escola.id]['Matemática'][0]
                prof_mat_turma_b = professores_por_escola_e_disciplina[escola.id]['Matemática'][1]
                
                prof_turma_data.append(ProfessorTurma(id_professor=prof_mat_turma_a.id, id_turma=escola_turmas[0].id))
                prof_turma_data.append(ProfessorTurma(id_professor=prof_mat_turma_b.id, id_turma=escola_turmas[1].id))
                
        session.add_all(prof_turma_data)
        session.commit()
        print("Professores vinculados às turmas.")

        # 9. Criar Matérias (tópicos dentro das disciplinas)
        print("Criando matérias...")
        materia_port_1 = Materia(
            nome_materia="Gramática",
            id_disciplina=portugues.id,
            id_professor=professores_por_escola_e_disciplina[escola_a1.id]['Português'][0].id, # Exemplo: um professor de Português da Escola Alpha I
        )
        materia_mat_1 = Materia(
            nome_materia="Álgebra",
            id_disciplina=matematica.id,
            id_professor=professores_por_escola_e_disciplina[escola_a1.id]['Matemática'][0].id, # Exemplo: um professor de Matemática da Escola Alpha I
        )
        session.add_all([materia_port_1, materia_mat_1]) # Use colchetes para passar múltiplos objetos
        session.commit()
        session.refresh(materia_port_1)
        session.refresh(materia_mat_1)
        print("Matérias criadas.")

        # 10. Criar Responsáveis
        print("Criando responsáveis...")
        responsaveis = []
        for i in range(len(turmas) * 3):
            responsaveis.append(
                Responsavel(
                    nome=f"Responsavel {i + 1}",
                    telefone=f"{500 + i:09d}00",
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
        global_aluno_count = 0
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

            # Obter os professores associados à turma do aluno
            professores_da_turma = (
                session.query(Professor)
                .join(ProfessorTurma)
                .filter(ProfessorTurma.id_turma == aluno.id_turma)
                .all()
            )
            
            # Filtrar professores por disciplina
            professor_portugues_turma = next((p for p in professores_da_turma if "Português" in p.cargo), None)
            professor_matematica_turma = next((p for p in professores_da_turma if "Matemática" in p.cargo), None)

            # Obter as disciplinas
            portugues = session.query(Disciplina).filter_by(nome_disciplina="Português").one()
            matematica = session.query(Disciplina).filter_by(nome_disciplina="Matemática").one()
            
            # Obter as matérias (exemplo, você pode precisar de mais lógica aqui se tiver várias matérias por disciplina)
            materia_port_1 = session.query(Materia).filter(Materia.id_disciplina == portugues.id).first()
            materia_mat_1 = session.query(Materia).filter(Materia.id_disciplina == matematica.id).first()

            # --- Avaliações de Português (1Va e 2Va) ---
            if professor_portugues_turma and materia_port_1:
                nota_base_port = random.uniform(8.0, 10.0) if is_municipio_a else random.uniform(6.0, 8.5)
                avaliacoes_para_adicionar.append(Avaliacao(
                    tipo_avaliacao="1Va",
                    data_avaliacao=date(2025, 4, random.randint(15, 28)),
                    nota=round(nota_base_port, 2),
                    id_aluno=aluno.id,
                    id_professor=professor_portugues_turma.id,
                    id_disciplina=portugues.id,
                    id_materia=materia_port_1.id,
                    id_turma=aluno.id_turma,
                ))
                avaliacoes_para_adicionar.append(Avaliacao(
                    tipo_avaliacao="2Va",
                    data_avaliacao=date(2025, 6, random.randint(15, 28)),
                    nota=round(min(10.0, nota_base_port * random.uniform(0.9, 1.1)), 2),
                    id_aluno=aluno.id,
                    id_professor=professor_portugues_turma.id,
                    id_disciplina=portugues.id,
                    id_materia=materia_port_1.id,
                    id_turma=aluno.id_turma,
                ))

            # --- Avaliações de Matemática (1Va e 2Va) ---
            if professor_matematica_turma and materia_mat_1:
                nota_base_mat = random.uniform(8.0, 10.0) if not is_municipio_a else random.uniform(6.0, 8.5)
                avaliacoes_para_adicionar.append(Avaliacao(
                    tipo_avaliacao="1Va",
                    data_avaliacao=date(2025, 4, random.randint(15, 28)),
                    nota=round(nota_base_mat, 2),
                    id_aluno=aluno.id,
                    id_professor=professor_matematica_turma.id,
                    id_disciplina=matematica.id,
                    id_materia=materia_mat_1.id,
                    id_turma=aluno.id_turma,
                ))
                avaliacoes_para_adicionar.append(Avaliacao(
                    tipo_avaliacao="2Va",
                    data_avaliacao=date(2025, 6, random.randint(15, 28)),
                    nota=round(min(10.0, nota_base_mat * random.uniform(0.9, 1.1)), 2),
                    id_aluno=aluno.id,
                    id_professor=professor_matematica_turma.id,
                    id_disciplina=matematica.id,
                    id_materia=materia_mat_1.id,
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