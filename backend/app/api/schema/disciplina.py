import re

from fastapi import APIRouter,HTTPException
from pydantic import AfterValidator, validator
from sqlmodel import SQLModel, Field, Session, create_engine
from typing import Literal, Annotated,Optional
from datetime import datetime
from curso import Curso,CursoGet

def codigoDisciplina(value: str) ->str:
    upper = value.upper()
    upper = upper.replace("-", "")
    departamento = re.split(r'(\d+)', upper)[0]
    try:
        codigo = re.split(r'(\d+)', upper)[1]
    except IndexError:
        raise ValueError("falta departamento ou codigo da disciplina")
    if(departamento == "" or codigo == ''):
        raise ValueError("falta departamento ou codigo da disciplina")
    departamentos_validos = ["CIC","MAT","FCTE","FGA"] # troca isso para um database com todos os codgios de disciplina no sigaa
    if departamento not in departamentos_validos:
        raise ValueError("Departamento Não valido")

    if  0<int(codigo)<9999:
         return departamento + "-" + codigo
    else:
        raise ValueError("codigo não valido")

class DisciplinaBase(SQLModel):
    codigo: Annotated[str, AfterValidator(codigoDisciplina)]
    nome: str
    periodo: datetime
    ativo : bool


class Disciplina(DisciplinaBase,table = True):
    id: int | None = Field(default=None,
                           primary_key=True)

    #curso_id : list[int]  = Field(default=[], sa_column=Column(ARRAY(Integer)))  #removi temporarimente,pois usa postgresql
    #obs tambem da para colocar o curso_id como uma string,so tem que criar uma função que faz isso automaticamente

class DisciplinaCreate(DisciplinaBase):
    pass

# router
disciplina_router = APIRouter()

#databae
sqlite_file_name = "Disciplinas.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)

@disciplina_router.get("/{curso_id}")
async def GetListaCurso(curso_id : int):
    with Session(engine) as session:
        cursoProcurado =  session.get(Curso,curso_id)
        if not cursoProcurado:
            raise HTTPException(status_code=404,
                                detail=f"não foi encontrado um curso com id {curso_id} ")
        curso = CursoGet.model_validate(cursoProcurado)
        return curso

@disciplina_router.get("/{curso_id}/disciplina")
async def GetListaDisciplina():
    with Session(engine) as session:
        #precisar implementar o curso_id dentro da class Disciplina para isso funcionar.
        pass





