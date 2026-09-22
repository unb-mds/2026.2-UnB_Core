from sqlmodel import SQLModel, Field


class CursoBase(SQLModel):
    nome: str
    sigla: str
    ativo: bool = True


class Curso(CursoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class CursoCreate(CursoBase):
    pass

class CursoGet(SQLModel):
    sigla : str | None
    nome : str | None
