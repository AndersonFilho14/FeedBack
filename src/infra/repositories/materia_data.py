from infra import DBConnectionHandler

from typing import List, Dict

from domain.models import Materia
from infra.db.models_data import Materia as MateriaData

class MateriaRepository:
    def criar(self, materia: Materia) -> None:
        """Insere uma nova matéria no banco."""
        
        # Convertendo materia de domain para materia de infra
        materia_orm = MateriaData(nome_materia = materia.nome,
                                  id_disciplina = materia.id_disciplina,
                                  id_professor = materia.id_professor)
        with DBConnectionHandler() as session:
            session.add(materia_orm)
            session.commit()

    def listar_por_professor(self, id_professor: int) -> List[Dict]:
        """Retorna lista de matérias atribuídas a um professor específico."""
        with DBConnectionHandler() as session:
            materias = session.query(MateriaData).filter(MateriaData.id_professor == id_professor).all()
            return [{"id": m.id, "nome": m.nome, "id_professor": m.id_professor} for m in materias]

    def atualizar(self, id_materia: int, novo_nome: str, novo_id_professor: int) -> bool:
        """Atualiza os dados da matéria com base no ID. Retorna True se atualizado, False se não encontrado."""
        
        with DBConnectionHandler() as session:
            materia = session.query(MateriaData).filter(MateriaData.id == id_materia).first()
            if not materia:
                return False
            materia.nome = novo_nome
            materia.id_professor = novo_id_professor
            session.commit()
            return True

    def deletar(self, id_materia: int) -> bool:
        """Deleta a matéria pelo id. Retorna True se deletado, False se não encontrado."""
        with DBConnectionHandler() as session:
            materia = session.query(MateriaData).filter(MateriaData.id == id_materia).first()
            if not materia:
                return False
            session.delete(materia)
            session.commit()
            return True