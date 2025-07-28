from infra import DBConnectionHandler
from infra.db.models_data import Escola as EscolaData, Acesso as AcessoData, Cargo as CargoData
from domain.models import Escola
from typing import List, Optional

class EscolaRepository:
          
    def criar(self, escola_dom: Escola) -> None:
        """Insere uma nova escola no banco."""
        escola_orm = EscolaData(nome = escola_dom.nome, id_municipio = escola_dom.id_municipio)
        
        with DBConnectionHandler() as session:
            session.add(escola_orm)
            session.commit()
            session.refresh(escola_orm)

            # Criando o acesso do usuário
            cargo = session.query(CargoData).filter(CargoData.nome_cargo == "Escola").first()
            if not cargo:
                raise ValueError("Cargo 'Escola' não encontrado no banco de dados.")
            
            acesso = AcessoData( usuario = escola_dom.nome_usuario,
                                 senha = escola_dom.senha,
                                 id_user = escola_orm.id, 
                                 id_cargo = cargo.id)
            session.add(acesso)
            session.commit()

    def listar_por_municipio(self, id_municipio: int) -> List[EscolaData]:
        """Retorna lista de escolas filtradas por município."""
        with DBConnectionHandler() as session:
            escolas = session.query(EscolaData).filter(EscolaData.id_municipio == id_municipio).all()
            return escolas

    def atualizar(self, id_escola: int, novo_nome: str, novo_id_municipio: int,
                   novo_nome_usuario: str, nova_senha: str ) -> bool:
        """Atualiza os dados da escola com base no ID. Retorna True se for atualizada, False se não encontrada."""
        
        with DBConnectionHandler() as session:
            escola = session.query(EscolaData).filter(EscolaData.id == id_escola).first()
            if not escola:
                return False
            else:
                escola.nome = novo_nome
                escola.id_municipio = novo_id_municipio
                session.commit()

                # Atualizando o acesso do usuário
                acesso = session.query(AcessoData).filter(AcessoData.id_user == id_escola).first()
                acesso.usuario = novo_nome_usuario
                acesso.senha = nova_senha
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

                acesso = session.query(AcessoData).filter(AcessoData.id_user == id_escola).first()
                session.delete(acesso)
                session.commit()    
                return True
    
            
class ConsultaEscolaBanco:
    """Classe resonsável por fazer consultas para validar alguns atributos no banco"""
    
    def buscar_por_id(self, id_escola: int) -> Optional[EscolaData]:
        with DBConnectionHandler() as session:
            return session.query(EscolaData).filter_by(id = id_escola).first()
    
    def buscar_acesso(self, id_escola: int, id_cargo: Optional[int] = None) -> Optional[AcessoData]:
        with DBConnectionHandler() as session:
            query = session.query(AcessoData).filter_by(id_user=id_escola)

            if id_cargo is not None:
                query = query.filter_by(id_cargo=id_cargo)

            return query.first()

    