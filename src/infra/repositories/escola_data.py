from infra import DBConnectionHandler
from infra.db.models_data import Escola as EscolaData
from domain.models import Escola
from typing import List, Optional

class EscolaRepository:
          
    def criar(self, escola_dom: Escola) -> None:
        """Insere uma nova escola no banco."""
        escola_orm = EscolaData(nome = escola_dom.nome, id_municipio = escola_dom.id_municipio)
        
        with DBConnectionHandler() as session:
            session.add(escola_orm)
            session.commit()

    def listar_por_municipio(self, id_municipio: int) -> List[EscolaData]:
        """Retorna lista de escolas filtradas por município."""
        with DBConnectionHandler() as session:
            escolas = session.query(EscolaData).filter(EscolaData.id_municipio == id_municipio).all()
            return escolas

    def atualizar(self, id_escola: int, novo_nome: str, novo_id_municipio: int) -> bool:
        """Atualiza os dados da escola com base no ID. Retorna True se for atualizada, False se não encontrada."""
        with DBConnectionHandler() as session:
            escola = session.query(EscolaData).filter(EscolaData.id == id_escola).first()
            if not escola:
                return False
            else:
                escola.nome = novo_nome
                escola.id_municipio = novo_id_municipio
                session.commit()
                return True

    def deletar(self, id_escola: int) -> bool:
        """Deleta a escola pelo id. Retorna True se deletado, False se não encontrado."""
        with DBConnectionHandler() as session:
            escola = session.query(EscolaData).filter(EscolaData.id == id_escola).first()
            if not escola:
                return False
            else:
                session.delete(escola)
                session.commit()
                return True
    
            
class ConsultaEscolaBanco:
    """Classe resonsável por fazer consultas para validar alguns atributos no banco"""
    
    def buscar_por_id(self, id_escola: int) -> Optional[EscolaData]:
        with DBConnectionHandler() as session:
            return session.query(EscolaData).filter_by(id = id_escola).first()