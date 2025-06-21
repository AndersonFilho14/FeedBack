from sqlalchemy import Column, Integer, String, ForeignKey
from infra.db.settings.base import Base

class Materia(Base):
    """
    Tabela que define tópicos ou unidades de conteúdo dentro de uma disciplina.

    Atributos:
        id (int): Identificador único do tópico/matéria.
        nome_materia (str): Nome do tópico ou unidade (ex: "Álgebra", "Gramática").
        id_disciplina (int): Chave estrangeira para a tabela Disciplina.
        id_professor (int): Chave estrangeira para o professor responsável por esta matéria/conteúdo.
    """
    __tablename__ = "materia"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_materia = Column(String(100), nullable=False)
    id_disciplina = Column(Integer, ForeignKey('disciplina.id'), nullable=False)
    id_professor = Column(Integer, ForeignKey('professor.id'), nullable=False)

    def __repr__(self) -> str:
        return f"<Materia id={self.id}, nome='{self.nome_materia}'>"
