from datetime import datetime

from pydantic import field_validator
from sqlmodel import SQLModel, Field


class FonteInstitucionalBase(SQLModel):
    nome: str
    unidade_responsavel: str
    url_base: str
    frequencia_verificacao: str
    estado: str = "ativa"
    ultima_verificacao: datetime | None = None

    @field_validator("estado")
    @classmethod
    def validar_estado(cls, valor: str) -> str:
        estados_permitidos = [
            "ativa",
            "pausada",
            "indisponivel",
        ]

        if valor not in estados_permitidos:
            raise ValueError(
                f"estado deve ser um dos seguintes: {estados_permitidos}"
            )

        return valor


class FonteInstitucional(FonteInstitucionalBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class FonteInstitucionalCreate(FonteInstitucionalBase):
    pass
