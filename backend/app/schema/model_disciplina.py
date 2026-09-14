import re

from pydantic import AfterValidator, validator
from sqlmodel import SQLModel, Field
from typing import Literal, Annotated,Optional
from datetime import datetime

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
    periodo: datetime = Field(default_factory=datetime.now)
    ativo : bool

class Disciplina(DisciplinaBase,table = True):
    id: int | None = Field(default=None,
                           primary_key=True)

    #curso_id : list[int]  = Field(default=[], sa_column=Column(ARRAY(Integer)))  #removi temporarimente,pois usa postgresql

class DisciplinaCreate(DisciplinaBase):
    pass
