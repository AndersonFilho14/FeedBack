import json
import base64

from typing import Optional

from config import log

from domain import Acesso

from infra.repositories import ConsultarAcesso, ConsultarUser
from infra.db.models_data import (
    Professor as ProfessorData,
    Escola as EscolaData,
    Municipio as MunicipioData,
)


class ControllerAcesso:
    """Controla o fluxo de acesso do usuário, desde a autenticação até a formatação do retorno."""

    def __init__(self, user_name: str, passworld: str) -> None:
        """Inicializa o controlador com o nome de usuário e senha."""
        self.__user = user_name
        self.__passworld = passworld

    def return_user_ou_texto(self) -> str:
        """Retorna os dados do usuário autenticado ou uma mensagem de erro."""
        retorno_banco: Acesso | str = BucarAcessoBanco(
            user_name=self.__user, passworld=self.__passworld
        ).buscar_banco()
        if not isinstance(retorno_banco, Acesso):
            log.debug("Não encontrou no banco")
            return retorno_banco

        usuario = BuscarQualUser(retorno_banco).consultar_quem_esta_acessando()
        return FormatarJsonRetorno(
            nome_cargo=retorno_banco.nome_cargo,
            nome_user=usuario,
            id_user=retorno_banco.id_user,
        ).gerar_json()


class BucarAcessoBanco:
    """Responsável por buscar as informações de acesso do usuário no banco de dados."""

    def __init__(self, user_name: str, passworld: str) -> None:
        """Inicializa a busca de acesso com nome de usuário e senha."""
        self.__user_acesso = Acesso(user=user_name, password=passworld)
        log.trace("Iniciando a validação do acesso")

    def buscar_banco(self) -> Acesso | str:
        """Executa a consulta ao banco de dados para validar o acesso e retorna os dados ou uma mensagem de erro."""
        retorno: Optional[Acesso] = ConsultarAcesso(
            user_acessar=self.__user_acesso
        ).get_retorno_banco()
        if not retorno:
            return "User não encontrado"
        return retorno


class BuscarQualUser:
    """Identifica o tipo de usuário e consulta seus dados específicos no banco de dados."""

    def __init__(self, acesso: Acesso):
        self.__acesso: Acesso = acesso
        self.tabela = self.__factory_qual_tabela()

    def __factory_qual_tabela(
        self,
    ) -> ProfessorData | EscolaData | MunicipioData | None:
        """Determina a tabela do banco de dados a ser consultada com base no cargo do usuário."""
        if self.__acesso.nome_cargo == "Professor":
            return ProfessorData
        if self.__acesso.nome_cargo == "Escola":
            return EscolaData
        if self.__acesso.nome_cargo == "Municipio":
            return MunicipioData

        raise ValueError("Essa tabela não foi mapeada")

    def consultar_quem_esta_acessando(self) -> str:
        """Consulta o nome do usuário na tabela correspondente ao seu cargo."""
        consulta = ConsultarUser(
            id_usuario=self.__acesso.id_user, tabela_no_banco=self.tabela
        ).consultar_user()
        return consulta


class FormatarJsonRetorno:
    """Formata os dados do usuário e cargo em uma string JSON, incluindo um token base64."""

    def __init__(self, nome_user: str, nome_cargo: str, id_user: int) -> None:
        self.__nome_user = nome_user
        self.__nome_cargo = nome_cargo
        self.__id_user = id_user

    def gerar_json(self) -> str:
        """Gera a string JSON formatada com os dados do usuário e um token base64."""
        token_base64 = base64.b64encode(self.__nome_user.encode("utf-8")).decode(
            "utf-8"
        )

        data_to_json = {
            "id_user": self.__id_user,
            "nome": self.__nome_user,
            "cargo": self.__nome_cargo,
            "token": token_base64,
        }

        return json.dumps(data_to_json, indent=4, ensure_ascii=False)
