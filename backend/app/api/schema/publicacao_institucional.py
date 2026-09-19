from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import field_validator, HttpUrl
from sqlmodel import SQLModel, Field, AutoString,Session, create_engine,select

publicacao_router = APIRouter()

sqlite_file_name = "database_publicaco_institucional.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)
class PublicacaoInstitucionalBase(SQLModel):
    fonte_id: int
    titulo: str
    resumo: str
    categoria: str
    unidade_responsavel: str
    curso_id: int | None = None
    url_oficial: HttpUrl =   Field(unique=True, index=True, sa_type=AutoString)
    url_oficial : str = str(url_oficial)
    publicado_em: datetime | None = None #Vai sempre deixar a verificação como None
    prazo_inicio: datetime | None = None # mesmo problema do de cima
    prazo_fim: datetime | None = None # mesmo problema
    estado: str = "nao_verificada"
    ultima_verificacao: datetime | None = None #mesmo problama

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

class PublicacaoInstitucionalGet(SQLModel):
    publicacao_id : int = Field(default = None,foreign_key="PublicacaoInstitucional.id")
    fonte_id: int
    titulo: str
    resumo: str
    categoria: str
    unidade_responsavel: str
    url_oficial: str

@publicacao_router.get("/{publicacao_id}")
async def get_publicacao(publicacao_id: int):
    with Session(engine) as session:
        publicacao = session.get(PublicacaoInstitucional,publicacao_id)
        if not publicacao:
            raise HTTPException(status_code=404,
                                detail=f"publicação com Id {publicacao_id} não existe")
        return publicacao


@publicacao_router.post("/criar")
async def post_publicacao(publicacao: PublicacaoInstitucionalCreate):
    with Session(engine) as session:
        if not publicacao:
            raise HTTPException(status_code=422,
                                detail="Erro de entrada, faltou parametro ou tipo errado")# colocar mais detalhes depois
        publicacao_db = PublicacaoInstitucional.model_validate(publicacao)
        session.add(publicacao_db)
        session.commit()
        session.refresh(publicacao_db)
        return publicacao_db