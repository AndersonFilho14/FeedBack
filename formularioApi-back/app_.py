from typing import Annotated
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import Depends, FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
import numpy as np

app = FastAPI()

class Aluno(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    idade:int
    sexo: int
    etnia: int
    educacaoPais: int
    tempoEstudoSemanal: float
    faltas: int
    apoioPais: int
    aulasParticulares: int
    extracurriculares: int
    esportes: int
    musica: int
    voluntariado: int
    notaFinal: float
    
    
engine = create_engine("sqlite:///banco.db", connect_args={"check_same_thread": False})


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
SessionDep = Annotated[Session, Depends(get_session)]
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/")
def create_aluno(aluno: Aluno):
    with Session(engine) as session:
        colunas = [
    "idade", "sexo", "etnia", "educacaoPais", "tempoEstudoSemanal", "faltas",
    "aulasParticulares", "apoioPais", "extracurriculares", "esportes",
    "musica", "voluntariado"
]

        ###
        model = joblib.load(open('modelo_preditivo_1.pkl', 'rb'))
        
        features = pd.DataFrame([[
        aluno.idade,
        aluno.sexo,
        aluno.etnia,
        aluno.educacaoPais,
        aluno.tempoEstudoSemanal,
        aluno.faltas,
        aluno.aulasParticulares,
        aluno.apoioPais,
        aluno.extracurriculares,
        aluno.esportes,
        aluno.musica,
        aluno.voluntariado,
        ]], columns=colunas)
        notaFinal = model.predict(features)
        aluno.notaFinal = notaFinal[0]
        print(aluno)
        ##

        # print(teste)
        session.add(aluno)
        session.commit()
        session.refresh(aluno)
        return aluno
@app.get("/")
def list_aluno():
    with Session(engine) as session:
        alunos = session.exec(select(Aluno)).all()
        json_compatible_data = jsonable_encoder(alunos)
        return JSONResponse(content=json_compatible_data)
@app.get("/{aluno_id}")
def find_aluno(aluno_id: int):
    with Session(engine) as session:
        aluno = session.get(Aluno, aluno_id)
        return aluno


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*']
)