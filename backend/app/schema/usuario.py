from datetime import datetime

from pydantic import EmailStr, field_validator, ValidationError
from sqlalchemy import true
from sqlmodel import SQLModel, Field


class UsuarioBase(SQLModel):

    email : EmailStr = Field(unique=True, index=True)
    nome : str
    perfil : str
    status : str #troquei o literal pois SQLModel não aceita literal


    @field_validator("status")
    def validate_status(cls,v):
        permitido = ["Online","Offline","Aparecer Offline","Ausente"]
        if v not in permitido:
            raise ValueError(f"deve ser um dos status a sequir {permitido}")
        return v

class Usuario(UsuarioBase,table = True):
    id: int | None = Field(default=None,
                           primary_key=True)
    criado_em: datetime = Field(default_factory=datetime.now)
    atualizado_em: datetime = Field(default_factory=datetime.now)


class UsuarioCreate(UsuarioBase):
    pass