from typing import Optional, Any

from infra import DBConnectionHandler

from domain import Acesso
from infra.db.models_data import (
    Acesso as AcessoData,
    Cargo as CargoData,
    Professor as ProfessorData,
    Escola as EscolaData,
    Municipio as MunicipioData,
)


class ConsultarAcesso:
    """Handles user access queries and data retrieval."""

    def __init__(self, user_acessar: Acesso) -> None:
        """Initializes the connection handler with user access data."""
        self.__acesso: Acesso = user_acessar
        self.__retorno: Optional[Any] = None  # Initialize __retorno to None
        self.__consultar_user_de_acesso()

    def __consultar_user_de_acesso(self) -> None:
        """Executes the database query to find user access and cargo information."""
        with DBConnectionHandler() as session:
            retorno_query = (
                session.query(
                    AcessoData.id_user,
                    CargoData.nome_cargo,
                )
                .join(CargoData, AcessoData.id_cargo == CargoData.id)
                .filter(
                    AcessoData.usuario == self.__acesso.user,
                    AcessoData.senha == self.__acesso.senha,
                )
                .first()
            )
        self.__retorno = retorno_query

    def get_retorno_banco(self) -> Optional[Acesso]:
        """Returns the retrieved user access and cargo data as a dictionary."""
        # Now, self.__retorno is guaranteed to exist (even if it's None)
        if self.__retorno:
            self.__acesso.id_user = self.__retorno.id_user
            self.__acesso.nome_cargo = self.__retorno.nome_cargo
            return self.__acesso
        return None


class ConsultarUser:
    """Handles querying user data from specified database tables."""

    def __init__(
        self,
        id_usuario: int,
        tabela_no_banco: ProfessorData | EscolaData | MunicipioData,
    ) -> None:
        """Initializes the class with a user ID and the target database table."""
        self.__id_usuario = id_usuario
        self.__tabela_no_banco = tabela_no_banco

    def consultar_user(self) -> str | None:
        """Queries the database for the user's name based on their ID and table."""
        with DBConnectionHandler() as session:
            retorno = session.query(self.__tabela_no_banco.nome).filter(
                self.__tabela_no_banco.id == self.__id_usuario
            )
        if retorno:
            return retorno[0][0]
        raise ValueError("Erro na consulta do banco. Pessoa não encontrada no")
