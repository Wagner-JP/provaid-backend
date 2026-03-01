from fastapi import FastAPI

from app.database.connection import engine
from app.database.models import Base
from app.routes.files import router as files_router

app = FastAPI(
    title="ProvaID API",
    description="Plataforma de certificação e verificação de autenticidade de conteúdos digitais (SHA-256).",
    version="1.0.0",
)

# Cria as tabelas no banco automaticamente (mais pra frente trocamos por migrations)
Base.metadata.create_all(bind=engine)

@app.get("/", summary="Status da API")
def root():
    return {"message": "ProvaID API rodando 🚀"}

# liga as rotas
app.include_router(files_router)