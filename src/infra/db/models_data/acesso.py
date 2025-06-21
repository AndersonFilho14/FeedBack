from sqlalchemy import Column, String, Integer, ForeignKey

from infra.db.settings.base import Base # Assumindo que este é o caminho correto para sua Base Declarativa

class Acesso(Base):
    """Tabela que gerencia os dados de acesso dos usuários à aplicação.

    Esta tabela relaciona um usuário com seu cargo e, opcionalmente,
    com um professor existente no sistema, caso o acesso seja de um professor.
    """
    __tablename__ = "acesso"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario = Column(String(50), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)


    id_cargo = Column(Integer, ForeignKey('cargo.id'), nullable=False)
    id_professor = Column(Integer, ForeignKey('professor.id'), nullable=True)

    def __repr__(self) -> str:
        return f"<Acesso id={self.id}, usuario='{self.usuario}', cargo_id={self.id_cargo}>"
