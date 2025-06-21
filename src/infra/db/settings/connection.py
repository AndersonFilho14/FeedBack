# infra/db/settings/connection.py
from typing import Optional

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

from infra.db.models_data import Acesso, Professor, Cargo, Turma, Aluno, Avaliacao, Coordenacao, Disciplina, Escola, Materia, Municipio, ProfessorTurma, Responsavel  # noqa: F401

from infra.db.settings.base import Base

class DBConnectionHandler:
    """
    Gerencia a conexão com o banco de dados SQLite, criando o engine e as sessões.

    Esta classe lida com a inicialização do banco de dados e a criação de tabelas
    baseadas nos modelos definidos que herdam de `Base`. Ela também implementa
    o protocolo de gerenciador de contexto para facilitar o uso de sessões do SQLAlchemy.

    Atributos:
        BANCO (str): A string de conexão para o banco de dados SQLite. Por padrão,
                     o arquivo do banco de dados será 'banco.db' criado no diretório
                     onde o script de execução for rodado.
    """

    BANCO : str  = "sqlite:///banco.db"

    def __init__(self) -> None:
        """
        Inicializa o handler de conexão com o banco de dados.

        Configura a string de conexão, cria o engine do banco de dados e inicializa
        a sessão como None. Durante a criação do engine, as tabelas são criadas
        no banco de dados se ainda não existirem, baseadas nos modelos importados
        (Acesso, Professor, Cargo).
        """
        self.__connection_string = self.BANCO
        self.__engine: Engine = self.__create_database_engine()
        self.session: Optional[Session] = None

    def __create_database_engine(self) -> Engine:
        """
        Cria e retorna o engine do banco de dados.

        Este método é responsável por configurar o motor de conexão com o banco de dados
        e garantir que todas as tabelas mapeadas pelos modelos que herdam de `Base`
        sejam criadas no banco, caso ainda não existam.

        Returns:
            Engine: O objeto Engine do SQLAlchemy configurado para a conexão.
        """
        engine: Engine = create_engine(self.__connection_string)
        Base.metadata.create_all(engine)
        return engine


    def __enter__(self) -> Session:
        """
        Entra no contexto do gerenciador de conexão.

        Quando usado com a instrução 'with', este método cria uma nova sessão
        do SQLAlchemy e a disponibiliza para operações de banco de dados.

        Returns:
            Session: A sessão do SQLAlchemy para interagir com o banco de dados.
        """
        SessionLocal = sessionmaker(autocommit=False, bind=self.__engine)
        self.session = SessionLocal()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Sai do contexto do gerenciador de conexão.

        Este método é automaticamente chamado ao sair do bloco 'with'.
        Ele garante que a sessão do SQLAlchemy seja fechada, liberando os recursos
        do banco de dados. Ele também pode ser usado para tratar exceções que
        ocorreram dentro do bloco 'with'.

        Args:
            exc_type (Optional[Type[BaseException]]): O tipo da exceção, se houver.
            exc_val (Optional[BaseException]): A instância da exceção, se houver.
            exc_tb (Optional[TracebackType]): O traceback da exceção, se houver.
        """
        if self.session:
            self.session.close()
