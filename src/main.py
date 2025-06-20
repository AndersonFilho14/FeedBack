# Exemplo de uso para inicialização (em um arquivo de configuração/main.py)
from infra.db.settings.connection import DBConnectionHandler

from infra.db.entites import Acesso, Professor, Cargo  # Exemplo: importa seu modelo Acesso


def insert_new_acesso(nome: str,user: str, password: str):
    # Passamos a string de conexão no construtor
    # Isso pode ser feito uma vez e o objeto DBConnectionHandler pode ser reutilizado
    # ou criado a cada operação se preferir, mas sem o create_db_tables no __init__.
    # Se você quiser um singleton para o handler, pode implementar um padrão.
    db_handler = DBConnectionHandler()

    with db_handler as db_connection:
        try:
            new_prof = Professor(nome=nome)
            db_connection.session.add(new_prof)
            db_connection.session.flush()

            new_acesso = Acesso(user=user, senha=password, professor_id = new_prof.id)
            db_connection.session.add(new_acesso)

            db_connection.session.commit()
            print(f"Dados inseridos com sucesso: {new_acesso}")
        except Exception as e:
            db_connection.session.rollback()
            print(f"Erro ao inserir dados: {e}")

def insert_cargos():

    db_handler = DBConnectionHandler()

    with db_handler as db_connection:
        try:
            new_prof = Cargo(cargo="cordenacao")
            db_connection.session.add(new_prof)
            db_connection.session.commit()

            new_prof = Cargo(cargo="professor")
            db_connection.session.add(new_prof)
            db_connection.session.commit()

            print(f"Dados inseridos com sucesso:")
        except Exception as e:
            db_connection.session.rollback()
            print(f"Erro ao inserir dados: {e}")

def get_all_acessos():
    db_handler = DBConnectionHandler()
    with db_handler as db_connection:
        try:
            acessos = db_connection.session.query(Acesso.autor_id).all()
            print("\nRegistros de Acesso:")
            for acesso in acessos:
                print(acesso)
            return acessos
        except Exception as e:
            print(f"Erro ao buscar dados: {e}")
            return []

if __name__ == "__main__":
    # Garante que as tabelas existam antes de tentar operar
    db_handler_init = DBConnectionHandler()
    db_handler_init.create_db_tables()
