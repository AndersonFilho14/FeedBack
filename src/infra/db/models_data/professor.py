from sqlalchemy import Column, Integer, String, Date, ForeignKey
from infra.db.settings.base import Base


class Professor(Base):
    """
    Tabela que armazena os dados dos professores.

    Atributos:
        id (int): Identificador único do professor.
        nome (str): Nome completo do professor.
        cpf (str): CPF do professor.
        cargo (str): Cargo ou função do professor.
        id_escola (int): Chave estrangeira para a tabela Escola.
    """

    __tablename__ = "professor"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    cargo = Column(String(100), nullable=True)  # Pode ser nulo se o cargo for genérico
    id_escola = Column(Integer, ForeignKey("escola.id"), nullable=False)
    data_nascimento = Column(Date, nullable=True)
    sexo = Column(String(20), nullable=True)
    nacionalidade = Column(String(50), nullable=True)
    estado_civil = Column(String(20), nullable=True)
    telefone = Column(String(20), nullable=True)
    email = Column(String(120), nullable=True)
    senha = Column(String(255), nullable=False)
    
    def __repr__(self) -> str:
        return f"<Professor id={self.id}, nome='{self.nome}'>"
