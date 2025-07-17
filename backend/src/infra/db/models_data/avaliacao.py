from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from infra.db.settings.base import Base


class Avaliacao(Base):
    """
    Tabela que armazena o resultado de uma avaliação específica do aluno.

    Atributos:
        id (int): Identificador único da avaliação.
        tipo_avaliacao (str): Tipo de avaliação, ex: "1Va", "2Va".
        data_avaliacao (Date): Data em que a avaliação foi aplicada.
        nota (float): Pontuação obtida na avaliação.
        id_aluno (int): Chave estrangeira para a tabela Aluno.
        id_professor (int): Chave estrangeira para a tabela Professor.
        id_disciplina (int): Chave estrangeira para a tabela Disciplina.
        id_materia (int): Chave estrangeira para a tabela Materia (tópico específico).
        id_turma (int): Chave estrangeira para a tabela Turma.
    """

    __tablename__ = "avaliacao"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo_avaliacao = Column(String(5), nullable=False)
    data_avaliacao = Column(Date, nullable=False)
    nota = Column(Float, nullable=False)  # Coluna única para a nota
    id_aluno = Column(Integer, ForeignKey("aluno.id"), nullable=False)
    id_professor = Column(Integer, ForeignKey("professor.id"), nullable=False)
    id_disciplina = Column(Integer, ForeignKey("disciplina.id"), nullable=False)
    id_materia = Column(Integer, ForeignKey("materia.id"), nullable=False)
    id_turma = Column(Integer, ForeignKey("turma.id"), nullable=False)

    def __repr__(self) -> str:
        return f"<Avaliacao id={self.id}, aluno_id={self.id_aluno}, tipo='{self.tipo_avaliacao}', nota={self.nota}>"
