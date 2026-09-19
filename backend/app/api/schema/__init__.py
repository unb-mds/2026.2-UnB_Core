from fastapi import FastAPI

from backend.app.api.schema.publicacao_institucional import publicacao_router
app = FastAPI()

app.include_router(router=publicacao_router,prefix="/publicacao")