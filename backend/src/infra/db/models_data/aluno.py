from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from infra.db.settings.base import Base


class Aluno(Base):
    """
    Representa a tabela 'aluno' no banco de dados.

    Esta tabela armazena informações pessoais, educacionais e comportamentais dos alunos,
    sendo utilizada para análises acadêmicas e preditivas de desempenho.

    Atributos:
        id (int): Identificador único do aluno (chave primária).
        nome (str): Nome completo do aluno.
        cpf (str): Cadastro de Pessoa Física (CPF) do aluno. Deve ser único.
        faltas (int): Número de faltas acumuladas pelo aluno. Valor padrão é 0.
        nota_score_preditivo (float): Score preditivo de desempenho (pode ser nulo inicialmente).
        id_escola (int): Chave estrangeira referenciando a escola do aluno.
        id_turma (int): Chave estrangeira referenciando a turma do aluno (pode ser nula).
        id_responsavel (int): Chave estrangeira referenciando o responsável pelo aluno.
        data_nascimento (date): Data de nascimento do aluno.
        sexo (str): Sexo do aluno (ex: 'Masculino', 'Feminino', etc.).
        nacionalidade (str): Nacionalidade do aluno.
        etnia (int): Código representando a etnia do aluno.
        educacaoPais (int): Nível de escolaridade dos pais.
        tempoEstudoSemanal (float): Tempo médio de estudo semanal do aluno (em horas).
        apoioPais (int): Indicador se os pais oferecem apoio educacional (0 = não, 1 = sim).
        aulasParticulares (int): Indicador se o aluno faz aulas particulares (0 = não, 1 = sim).
        extraCurriculares (int): Indicador se participa de atividades extracurriculares.
        esportes (int): Indicador se pratica esportes regularmente.
        aulaMusica (int): Indicador se participa de aulas de música.
        voluntariado (int): Indicador se participa de atividades de voluntariado.

    Métodos:
        __repr__: Retorna uma representação legível do objeto para depuração.
    """

    __tablename__ = "aluno"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    faltas = Column(Integer, default=0, nullable=False)
    nota_score_preditivo = Column(Float, nullable=True)  # Pode ser nulo no início
    id_escola = Column(Integer, ForeignKey("escola.id"), nullable=False)
    id_turma = Column(Integer, ForeignKey("turma.id"))
    id_responsavel = Column(Integer, ForeignKey("responsavel.id"), nullable=False)
    data_nascimento = Column(Date)
    sexo = Column(String(20))
    nacionalidade = Column(String(50))
    etnia = Column(Integer)
    educacaoPais = Column(Integer)
    tempoEstudoSemanal = Column(Float)
    apoioPais = Column(Integer)
    aulasParticulares = Column(Integer)
    extraCurriculares = Column(Integer)
    esportes = Column(Integer)
    aulaMusica = Column(Integer)
    voluntariado = Column(Integer)


    def __repr__(self) -> str:
        return f"<Aluno id={self.id}, nome='{self.nome}'>"
