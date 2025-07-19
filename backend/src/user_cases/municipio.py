import json
from typing import Optional, List

from domain.models import Municipio
from infra.repositories import MunicipioRepository
from infra.db.models_data import Municipio as MunicipioData
from config import log
from utils.validarCampos import ValidadorCampos

class ControllerMunicipio:
    """Controlador responsável por coordenar operações relacionadas a municípios."""

    def __init__(self, nome: Optional[str] = None, estado: Optional[str] = None,
                 regiao: Optional[str] = None, id_municipio: Optional[int] = None):
        self.__nome = nome
        self.__estado = estado
        self.__regiao = regiao
        self.__id_municipio = id_municipio

    def criar_municipio(self) -> str:
        """Cria um novo município no banco de dados."""
        return CriarMunicipioNoBanco(self.__nome, self.__estado, self.__regiao).executar()

    def listar_municipios(self) -> str:
        """Lista todos os municípios cadastrados no banco."""
        municipios_data = ListarMunicipiosNoBanco().executar()
        municipios_dom = FormatarMunicipio().data_para_dominio(municipios_data)
        return FormatarMunicipio().gerar_json(municipios_dom)

    def atualizar_municipio(self) -> str:
        """Atualiza os dados do município com base no ID."""
        return AtualizarMunicipioNoBanco(self.__id_municipio, self.__nome, self.__estado, self.__regiao).executar()

    def deletar_municipio(self) -> str:
        """Remove um município do banco pelo ID."""
        return DeletarMunicipioDoBanco(self.__id_municipio).executar()


class CriarMunicipioNoBanco:
    def __init__(self, nome: str, estado: str, regiao: str):
        self.__municipio = Municipio(nome=nome, estado=estado, regiao=regiao)

    def executar(self) -> str:
        
        # Validação de campos obrigatórios
        resultado = ValidadorCampos.validar_campos_preenchidos([
            self.__municipio.nome,
            self.__municipio.estado,
            self.__municipio.regiao
        ])
        
        if resultado is not None:
            return resultado
        
        try:
            MunicipioRepository().criar(self.__municipio)
            log.info(f"Município '{self.__municipio.nome}' criado com sucesso.")
            return "Município criado com sucesso"
        except Exception as e:
            log.error(f"Erro ao criar município: {e}")
            return "Erro ao criar município"


class ListarMunicipiosNoBanco:
    def executar(self) -> List[MunicipioData]:
        try:
            municipios = MunicipioRepository().listar()
            log.debug(f"{len(municipios)} municípios encontrados.")
            return municipios
        except Exception as e:
            log.error(f"Erro ao listar municípios: {e}")
            return []


class AtualizarMunicipioNoBanco:
    def __init__(self, id_municipio: int, novo_nome: str, novo_estado: str, nova_regiao: str):
        self.__id = id_municipio
        self.__novo_nome = novo_nome
        self.__novo_estado = novo_estado
        self.__nova_regiao = nova_regiao

    def executar(self) -> str:
        
        # Validação dos campos obrigatórios
        resultado = ValidadorCampos.validar_campos_preenchidos([
            self.__id,
            self.__novo_nome,
            self.__novo_estado,
            self.__nova_regiao
        ])
        
        if resultado is not None:
            return resultado
        
        try:
            atualizado = MunicipioRepository().atualizar(
                id_municipio=self.__id,
                novo_nome=self.__novo_nome,
                novo_estado=self.__novo_estado,
                nova_regiao=self.__nova_regiao
            )
            if atualizado:
                log.info(f"Município {self.__id} atualizado com sucesso.")
                return "Município atualizado com sucesso"
            else:
                return "Município não encontrado"
        except Exception as e:
            log.error(f"Erro ao atualizar município: {e}")
            return "Erro ao atualizar município"


class DeletarMunicipioDoBanco:
    def __init__(self, id_municipio: int):
        self.__id = id_municipio

    def executar(self) -> str:
        try:
            deletado = MunicipioRepository().deletar(self.__id)
            if deletado:
                log.info(f"Município {self.__id} deletado.")
                return "Município deletado com sucesso"
            else:
                return "Município não encontrado"
        except Exception as e:
            log.error(f"Erro ao deletar município: {e}")
            return "Erro ao deletar município"


class FormatarMunicipio:
    """Classe responsável por converter MunicipioData → Municipio → JSON"""

    def data_para_dominio(self, municipios_data: List[MunicipioData]) -> List[Municipio]:
        municipios_dom = []
        for municipio in municipios_data:
            municipio = Municipio(
                id_municipio=municipio.id,
                nome=municipio.nome,
                estado=municipio.estado,
                regiao=municipio.regiao or ""
            )
            municipios_dom.append(municipio)
        return municipios_dom

    def gerar_json(self, municipios_dom: List[Municipio]) -> str:
        lista = [
            {
                "id": municipio.id,
                "nome": municipio.nome,
                "estado": municipio.estado,
                "regiao": municipio.regiao
            }
            for municipio in municipios_dom
        ]
        return json.dumps({"municipios": lista}, ensure_ascii=False, indent=4)
