from typing import List, Optional
from infra import DBConnectionHandler
from infra.db.models_data import Municipio as MunicipioData
from domain.models import Municipio


class MunicipioRepository:
    """Persistência e consultas de municípios."""

    def criar(self, municipio_dom: Municipio) -> None:
        """Insere um novo município no banco."""
        municipio_orm = MunicipioData(
            nome=municipio_dom.nome,
            regiao=municipio_dom.regiao,
            estado=municipio_dom.estado
        )
        with DBConnectionHandler() as session:
            session.add(municipio_orm)
            session.commit()

    def listar(self) -> List[MunicipioData]:
        """Retorna todos os municípios."""
        with DBConnectionHandler() as session:
            return session.query(MunicipioData).all()

    def atualizar(self, id_municipio: int, novo_nome: str, nova_regiao: str, novo_estado: str) -> bool:
        """Atualiza o município pelo ID. Retorna True se atualizado, False se não encontrado."""
        with DBConnectionHandler() as session:
            municipio = session.query(MunicipioData).filter_by(id=id_municipio).first()
            if not municipio:
                return False
            municipio.nome = novo_nome
            municipio.regiao = nova_regiao
            municipio.estado = novo_estado
            session.commit()
            return True

    def deletar(self, id_municipio: int) -> bool:
        """Deleta o município pelo ID. Retorna True se deletado, False se não encontrado."""
        with DBConnectionHandler() as session:
            municipio = session.query(MunicipioData).filter_by(id=id_municipio).first()
            if not municipio:
                return False
            session.delete(municipio)
            session.commit()
            return True


class ConsultaMunicipioBanco:
    """Classe resonsável por fazer consultas para validar alguns atributos no banco"""
    
    def buscar_por_id(self, id_municipio: int) -> Optional[MunicipioData]:
        """Busca o município pelo ID. Retorna o objeto ou None se não existir."""
        with DBConnectionHandler() as session:
            return session.query(MunicipioData).filter_by(id=id_municipio).first()
