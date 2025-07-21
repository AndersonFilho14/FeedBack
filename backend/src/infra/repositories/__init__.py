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

from infra.repositories.aluno_data import ConsultarTurma, AlunoRepository, ConsultaAlunoBanco  # noqa : F401
from infra.repositories.escola_data import EscolaRepository, ConsultaEscolaBanco # noqa : F401
from infra.repositories.materia_data import MateriaRepository, ConsultaMateriaBanco # noqa : F401
from infra.repositories.municipio_data import MunicipioRepository, ConsultaMunicipioBanco # noqa : F401
from infra.repositories.turma_data import TurmaRepository, ConsultaTurmaBanco, ListarAssociadosDaTurma # noqa : F401
from infra.repositories.avaliacao_data import AvaliacaoRepository  # noqa : F401