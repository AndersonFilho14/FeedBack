from infra import DBConnectionHandler
from infra.db.models_data import Turma as TurmaData
from domain.models import Turma
from typing import List, Optional

class TurmaRepository:
    def criar(self, turma: Turma) -> None:
        """Insere uma nova turma no banco."""
        turma_orm = TurmaData(nome = turma.nome, ano_letivo = turma.ano_letivo, id_escola = turma.id_escola)
        with DBConnectionHandler() as session:
            session.add(turma_orm)
            session.commit()

    def listar_por_escola(self, id_escola: int) -> List[TurmaData]:
        """Retorna lista de turmas filtradas por escola."""
        with DBConnectionHandler() as session:
            turmas = session.query(TurmaData).filter(TurmaData.id_escola == id_escola).all()
            return turmas

    def atualizar(self, id_turma: int, novo_nome: str, novo_ano_letivo: int, novo_id_escola: int) -> bool:
        """Atualiza os dados da turma com base no ID. Retorna True se atualizado, False se não encontrado."""
        with DBConnectionHandler() as session:
            turma = session.query(TurmaData).filter(TurmaData.id == id_turma).first()
            if not turma:
                return False
            turma.nome = novo_nome
            turma.ano_letivo = novo_ano_letivo
            turma.id_escola = novo_id_escola
            session.commit()
            return True

    def deletar(self, id_turma: int) -> bool:
        """Deleta a turma pelo id. Retorna True se deletado, False se não encontrado."""
        with DBConnectionHandler() as session:
            turma = session.query(TurmaData).filter(TurmaData.id == id_turma).first()
            if not turma:
                return False
            session.delete(turma)
            session.commit()
            return True
        
class ConsultaBancoTurma:
    """Classe resonsável por fazer consultas para validar alguns atributos no banco"""
    
    def buscar_por_id(self, id_turma: int) -> Optional[TurmaData]:
        """Busca a turma pelo ID. Retorna a turma se encontrada, ou None se não existir."""
        with DBConnectionHandler() as session:
            return session.query(TurmaData).filter_by(id=id_turma).first()