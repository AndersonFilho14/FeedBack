import json
from typing import Optional
from config import log
from utils.validarCampos import ValidadorCampos

from domain.models.escola import Escola
from infra.repositories import EscolaRepository, ConsultaBancoMunicipio
from infra.db.models_data import Escola as Escola_data
from typing import List
 
    
class ControllerEscola:
    """Controlador responsável por coordenar operações relacionadas a escola"""

    def __init__(self, nome: Optional[str] = None, id_municipio: Optional[int] = None, id_escola: Optional[int] = None) -> None:
        self.__nome = nome
        self.__id_municipio = id_municipio
        self.__id_escola = id_escola

    def criar_escola(self) -> str:
        """Cria uma nova escola no banco de dados."""
        resultado = CriarEscolaNoBanco(nome = self.__nome, id_municipio = self.__id_municipio).executar()
        return resultado

    def listar_escolas(self) -> list[dict]:
        """Lista todas as escolas do banco de dados para um determinado município."""
        escolas_data = ListarEscolasDoBanco(id_municipio = self.__id_municipio).executar()
        formatter = FormatarEscola()
        escolas_dominio = formatter.formatar_escola_data_para_dominio(escolas_data = escolas_data)
        return formatter.gerar_json(escolas_dominio = escolas_dominio)

    def atualizar_escola(self) -> str:
        """Atualiza o nome e o município da escola com o ID informado."""
        return AtualizarEscolaNoBanco(id_escola = self.__id_escola, novo_nome = self.__nome, novo_id_municipio = self.__id_municipio).executar()

    def deletar_escola(self) -> str:
        """Remove uma escola do banco pelo ID."""
        return DeletarEscolaDoBanco(id_escola = self.__id_escola).executar()


class CriarEscolaNoBanco:
    def __init__(self,  nome: str, id_municipio: int):
        self.__escola = Escola(nome = nome, id_municipio = id_municipio, id = 0)

    def executar(self) -> str:
        
        # Validação dos campos obrigatórios
        resultado = ValidadorCampos.validar_campos_preenchidos([
            self.__escola.nome,
            self.__escola.id_municipio
        ])
        
        if resultado is not None:
            return resultado
        
        try:
            # Verifica existência do município antes de criar a escola
            if ConsultaBancoMunicipio().buscar_por_id(self.__escola.id_municipio) is None:
                return f"Município com ID {self.__escola.id_municipio} não encontrado."
            
            else:
                EscolaRepository().criar(self.__escola)
                log.info(f"Escola '{self.__escola.nome}' criada com sucesso.")
                return "Escola criada com sucesso"
        except Exception as e:
            log.error(f"Erro ao criar escola: {e}")
            return "Erro ao criar escola"


class ListarEscolasDoBanco:
    def __init__(self, id_municipio: int):
        self.__id_municipio = id_municipio

    def executar(self) -> list[dict]:
        try:
            escolas = EscolaRepository().listar_por_municipio(self.__id_municipio)
            log.debug(f"{len(escolas)} escolas encontradas no município {self.__id_municipio}.")
            return escolas
        except Exception as e:
            log.error(f"Erro ao listar escolas do município {self.__id_municipio}: {e}")
            return []


class AtualizarEscolaNoBanco:
    def __init__(self, id_escola: int, novo_nome: str, novo_id_municipio: int):
        self.__id = id_escola
        self.__novo_nome = novo_nome
        self.__novo_id_municipio = novo_id_municipio

    def executar(self) -> str:
        
        # Valida se todos os campos estão preenchidos
        resultado = ValidadorCampos.validar_campos_preenchidos([
            self.__id,
            self.__novo_nome,
            self.__novo_id_municipio
        ])
        
        if resultado is not None:
            return resultado
        
        try:
            # Verifica existência do município antes de atualizar a escola
            if ConsultaBancoMunicipio().buscar_por_id(self.__novo_id_municipio) is None:
                return f"Município com ID {self.__novo_id_municipio} não encontrado."
            
            atualizado = EscolaRepository().atualizar(self.__id, self.__novo_nome, self.__novo_id_municipio)
            if atualizado:
                log.info(f"Escola {self.__id} atualizada para '{self.__novo_nome}', município {self.__novo_id_municipio}.")
                return "Escola atualizada com sucesso"
            else:
                return "Escola não encontrada"
        except Exception as e:
            log.error(f"Erro ao atualizar escola: {e}")
            return "Erro ao atualizar escola"


class DeletarEscolaDoBanco:
    def __init__(self, id_escola: int):
        self.__id = id_escola

    def executar(self) -> str:
        try:
            deletado = EscolaRepository().deletar(self.__id)
            if deletado:
                log.info(f"Escola {self.__id} deletada.")
                return "Escola deletada com sucesso"
            else:
                return "Escola não encontrada"
        except Exception as e:
            log.error(f"Erro ao deletar escola: {e}")
            return "Erro ao deletar escola"
        
class FormatarEscola:
    """Classe responsável por converter EscolaData (ORM) em Escola (domínio) e gerar JSON formatado."""

    def formatar_escola_data_para_dominio(self, escolas_data: List[Escola_data]) -> List[Escola]:
        escolas_dom = []
        for escola in escolas_data:
            escola_dom = Escola(
                id=escola.id,
                nome=escola.nome,
                id_municipio=escola.id_municipio
            )
            escolas_dom.append(escola_dom)
        return escolas_dom

    def gerar_json(self, escolas_dominio: List[Escola]) -> str:
        lista = [
            {
                "id": escola.id,
                "nome": escola.nome,
                "id_municipio": escola.id_municipio
            }
            for escola in escolas_dominio
        ]
        return json.dumps({"escolas": lista}, ensure_ascii=False, indent=4)