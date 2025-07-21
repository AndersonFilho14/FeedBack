from infra import DBConnectionHandler
from infra.db.models_data import Turma as TurmaData
from infra.db.models_data import Professor as ProfessorData
from infra.db.models_data import Aluno as AlunoData
from infra.db.models_data import ProfessorTurma as ProfessorTurma
from infra.db.models_data import Avaliacao as AvaliacaoData
from domain.models import Turma
from typing import List, Optional

class TurmaRepository:
    def criar(self, turma: Turma) -> None:
        """Insere uma nova turma no banco."""
        turma_orm = TurmaData(nome = turma.nome, ano_letivo = turma.ano_letivo, id_escola = turma.id_escola)
        
        with DBConnectionHandler() as session:
            session.add(turma_orm)
            session.commit()
           
            # Atualiza os alunos com o ID da nova turma
            if turma.ids_alunos:
                session.query(AlunoData).filter(AlunoData.id.in_(turma.ids_alunos)) \
                    .update({AlunoData.id_turma: turma_orm.id}, synchronize_session=False)
                
            # Atualiza as avaliações desses alunos com o novo id_turma
            session.query(AvaliacaoData).filter(AvaliacaoData.id_aluno.in_(turma.ids_alunos)) \
                .update({AvaliacaoData.id_turma: turma_orm.id}, synchronize_session=False)

            # Cria os vínculos na tabela professor_turma
            for id_professor in turma.ids_professores:
                professor_turma = ProfessorTurma(
                    id_professor=id_professor,
                    id_turma=turma_orm.id
                )
                session.add(professor_turma)

            session.commit()

    def listar_por_escola(self, id_escola: int) -> List[TurmaData]:
        """Retorna lista de turmas filtradas por escola."""
        with DBConnectionHandler() as session:
            turmas = session.query(TurmaData).filter(TurmaData.id_escola == id_escola).all()
            return turmas

    def atualizar(self, id_turma: int, novo_nome, ids_professores_atuais: List[int],
                   ids_alunos_atuais: List[int], ids_professores_anteriores: List[int],
                   ids_alunos_anteriores: List[int]) -> bool:
        """Atualiza os dados da turma com base no ID. Retorna True se atualizado, False se não encontrado."""
        with DBConnectionHandler() as session:
            turma = session.query(TurmaData).filter(TurmaData.id == id_turma).first()
            if not turma:
                return False
            turma.nome = novo_nome
            session.commit()

            # ---------------- PROFESSORES ----------------
            set_atuais_prof = set(ids_professores_atuais)
            set_anteriores_prof = set(ids_professores_anteriores)

            profs_a_remover = set_anteriores_prof - set_atuais_prof
            profs_a_adicionar = set_atuais_prof - set_anteriores_prof

            for id_prof in profs_a_remover:
                session.query(ProfessorTurma).filter_by(id_turma=id_turma, id_professor=id_prof).delete()

            for id_prof in profs_a_adicionar:
                novo_vinculo = ProfessorTurma(id_turma=id_turma, id_professor=id_prof)
                session.add(novo_vinculo)

            # ---------------- ALUNOS ----------------
            set_atuais_alunos = set(ids_alunos_atuais)
            set_anteriores_alunos = set(ids_alunos_anteriores)

            alunos_a_remover = set_anteriores_alunos - set_atuais_alunos
            alunos_a_adicionar = set_atuais_alunos - set_anteriores_alunos

            # Desassociar alunos removidos
            if alunos_a_remover:
                session.query(AlunoData).filter(AlunoData.id.in_(alunos_a_remover)).update(
                    {AlunoData.id_turma: None}, synchronize_session=False
                )

                # Também desassociar as avaliações desses alunos
                session.query(AvaliacaoData).filter(AvaliacaoData.id_aluno.in_(alunos_a_remover)) \
                    .update({AvaliacaoData.id_turma: None}, synchronize_session=False)

            # Associar alunos novos à turma
            if alunos_a_adicionar:
                session.query(AlunoData).filter(AlunoData.id.in_(alunos_a_adicionar)).update(
                    {AlunoData.id_turma: id_turma}, synchronize_session=False
                )

                # Atualiza as avaliações desses alunos com o novo id_turma
                session.query(AvaliacaoData).filter(AvaliacaoData.id_aluno.in_(alunos_a_adicionar)) \
                    .update({AvaliacaoData.id_turma: id_turma}, synchronize_session=False)

            session.commit()
            return True

    def deletar(self, id_turma: int) -> bool:
        """Deleta a turma pelo id. Remove vínculos com professores e alunos. 
        Também zera o id_turma nas avaliações associadas. Retorna True se deletado, False se não encontrado."""
        with DBConnectionHandler() as session:
            turma = session.query(TurmaData).filter(TurmaData.id == id_turma).first()
            if not turma:
                return False

            # 1. Remover vínculos na tabela professor_turma
            session.query(ProfessorTurma).filter_by(id_turma=id_turma).delete()

            # 2. Buscar IDs dos alunos dessa turma
            alunos_na_turma = session.query(AlunoData.id).filter(AlunoData.id_turma == id_turma).all()
            ids_alunos = [aluno.id for aluno in alunos_na_turma]

            if ids_alunos:
                # 3. Desassociar alunos da turma
                session.query(AlunoData).filter(AlunoData.id.in_(ids_alunos)) \
                    .update({AlunoData.id_turma: None}, synchronize_session=False)

                # 4. Desassociar avaliações dos alunos
                session.query(AvaliacaoData).filter(AvaliacaoData.id_aluno.in_(ids_alunos)) \
                    .update({AvaliacaoData.id_turma: None}, synchronize_session=False)

            # 5. Por fim, deletar a turma
            session.delete(turma)
            session.commit()
            return True
            
class ConsultaTurmaBanco:
    """Classe resonsável por fazer consultas para validar alguns atributos no banco"""
    
    def buscar_por_id(self, id_turma: int) -> Optional[TurmaData]:
        """Busca a turma pelo ID. Retorna a turma se encontrada, ou None se não existir."""
        with DBConnectionHandler() as session:
            return session.query(TurmaData).filter_by(id=id_turma).first()

class ListarAssociadosDaTurma:
    def __init__(self, id_turma: int) -> None:
        self.__id_turma = id_turma

    def listar_professores_associados(self) -> List[ProfessorData]:
        """
        Retorna uma lista de professores vinculados à turma informada.
        """
        with DBConnectionHandler() as session:
            professores = (
                session.query(ProfessorData)
                .join(ProfessorTurma, ProfessorTurma.id_professor == ProfessorData.id)
                .filter(ProfessorTurma.id_turma == self.__id_turma)
                .all()
            )
            return professores

    def listar_alunos_associados(self) -> List[AlunoData]:
        """Retorna uma lista de alunos vinculados a esta turma."""
        with DBConnectionHandler() as session:
            alunos = (
                session.query(AlunoData)
                .filter(AlunoData.id_turma == self.__id_turma)
                .all()
            )
            return alunos