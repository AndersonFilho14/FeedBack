from infra.repositories.acesso_data import ConsultarAcesso  # noqa: F401
from infra.repositories.acesso_data import ConsultarUser  # noqa: F401

from infra.repositories.professor_data import (
    ConsultarProfessor,  # noqa : F401
    AdicionarNotaParaAluno,  # noqa : F401
    AtualizarQuantidadeDeFaltasParaAluno,   # noqa : F401
    ConsultarAlunosVinculadosAoProfessorNoBanco,  # noqa : F401
    ConsultarDisciplinasEMateriasVinculadasAoProfessor,   # noqa : F401
    ProfessorRepository # noqa : F401
)

from infra.repositories.aluno_data import ConsultarTurma, AlunoRepository, ConsultaBancoAluno  # noqa : F401
from infra.repositories.escola_data import EscolaRepository, ConsultaBancoEscola # noqa : F401
from infra.repositories.materia_data import MateriaRepository # noqa : F401
from infra.repositories.municipio_data import MunicipioRepository, ConsultaBancoMunicipio # noqa : F401
from infra.repositories.turma_data import TurmaRepository, ConsultaBancoTurma # noqa : F401