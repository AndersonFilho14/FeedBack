import joblib
import numpy as np


class Aluno:
    id: int | None
    nome: str
    idade:int
    sexo: int
    etnia: int
    educacaoPais: int
    tempoEstudoSemanal: float
    faltas: int
    apoioPais: int
    aulasParticulares: int
    extraCurriculares: int
    esportes: int
    aulaMusica: int
    voluntariado: int
    notaFinal: str


def processIA(aluno: Aluno) -> str:
    try:
        model = joblib.load(open('RNA_model.pkl', 'rb'))
        
        features = np.array([[
       int(aluno.idade),
    int(aluno.sexo),
    int(aluno.etnia),
    int(aluno.educacaoPais),
    int(aluno.tempoEstudoSemanal),
    int(aluno.faltas),
    int(aluno.aulasParticulares),
    int(aluno.apoioPais),
    int(aluno.extraCurriculares),
    int(aluno.esportes),
    int(aluno.aulaMusica),
    int(aluno.voluntariado)
        ]])
        notaFinal = model.predict(features)
        mapeamento = {0: 'A', 1: 'B', 2:'C', 3:'D', 4:'F'}
        nota_predita = mapeamento.get(notaFinal[0])
        return nota_predita

    except Exception as e:
        return f"Erro: {str(e)}"
