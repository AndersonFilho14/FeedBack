# infra/db/settings/connection.py
from typing import Self, Optional
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from infra.db.settings.base import Base # Certifique-se de que o caminho está correto

class DBConnectionHandler:
    """Classe de conexão com o banco de dados.

    Gerencia a criação do engine e a sessão.
    """

    BANCO : str  = "sqlite:///banco.db"

    def __init__(self) -> None:
        """
        Inicializa o handler de conexão.

        Args:
            connection_string (str): A string de conexão do banco de dados.
                                     Padrão para 'sqlite:///acesso.db'.
        """
        self.__connection_string = self.BANCO
        self.__engine: Engine = self.__create_database_engine()
        self.session: Optional[Session] = None

    def __create_database_engine(self) -> Engine:
        """Cria e retorna o engine do banco de dados."""
        engine: Engine = create_engine(self.__connection_string)
        return engine

    def get_engine(self) -> Engine:
        """Retorna o engine de conexão."""
        return self.__engine

    def create_db_tables(self) -> None:
        """Cria todas as tabelas mapeadas pela Base no banco de dados.
        Chame este método apenas uma vez na inicialização da sua aplicação.
        """
        print("Tentando criar tabelas do banco de dados...")
        Base.metadata.create_all(self.__engine)
        print("Tabelas criadas ou já existentes.")

    def __enter__(self) -> Self:
        """Entra no contexto do gerenciador de conexão, criando uma nova sessão."""
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)
        self.session = SessionLocal()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Sai do contexto, fechando a sessão e tratando erros."""
        if self.session:
            self.session.close()
        if exc_type: # Se houve uma exceção, você pode querer logar ou relançar.
            print(f"Erro durante a transação: {exc_type.__name__}: {exc_val}")
            # Em um cenário real, você pode querer logar e talvez levantar a exceção novamente
            # raise exc_type(exc_val) from exc_tb