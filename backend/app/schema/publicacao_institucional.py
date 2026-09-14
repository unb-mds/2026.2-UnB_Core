from datetime import datetime

from pydantic import field_validator, HttpUrl
from sqlmodel import SQLModel, Field, AutoString


class PublicacaoInstitucionalBase(SQLModel):
    fonte_id: int
    titulo: str
    resumo: str
    categoria: str
    unidade_responsavel: str
    curso_id: int | None = None
    url_oficial: HttpUrl =   Field(unique=True, index=True, sa_type=AutoString)
    url_oficial : str = str(url_oficial)
    publicado_em: datetime | None = None
    prazo_inicio: datetime | None = None
    prazo_fim: datetime | None = None
    estado: str = "nao_verificada"
    ultima_verificacao: datetime | None = None

    @field_validator("estado")
    @classmethod
    def validar_estado(cls, valor: str) -> str:
        estados_permitidos = [
            "ativa",
            "encerrada",
            "cancelada",
            "desatualizada",
            "nao_verificada",
            "sem_prazo",
        ]

        if valor not in estados_permitidos:
            raise ValueError(
                f"estado deve ser um dos seguintes: {estados_permitidos}"
            )

        return valor


class PublicacaoInstitucional(
    PublicacaoInstitucionalBase,
    table=True,
):
    id: int | None = Field(default=None, primary_key=True)


class PublicacaoInstitucionalCreate(PublicacaoInstitucionalBase):
    pass
