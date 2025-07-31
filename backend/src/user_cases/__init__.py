from user_cases.acesso import ControllerAcesso  # noqa: F401
from user_cases.professor import (
    ControllerProfessorAtualizarFalta,  # noqa: F401
    ControllerProfessorAlunosVinculados,  # noqa : F401
    ConsultarAlunosVinculadosAoProfessor,  # noqa : F401
    ControllerProfessorAtualizarNotaAoAluno,  # noqa: F401
    ConsultarAlunosVinculadosAoProfessorNoBanco,  # noqa : F401
    ControllerConsultarMateriaEDisciplinasVinculadasAoProfessor,  # noqa : F401
    ControllerProfessor # noqa : F401
    )
from user_cases.escola import ControllerEscola # noqa : F401
from user_cases.materia import ControllerMateria # noqa : F401
from user_cases.aluno import ControllerAluno, ControllerAlunoIA # noqa : F401
from user_cases.municipio import ControllerMunicipio # noqa : F401
from user_cases.turma import ControllerTurma # noqa : F401
from user_cases.avaliacao import ControllerRankingAvaliacao, ControllerHistoricoAvaliacoes
from user_cases.dashboard import ControllerDashboard  # noqa : F401