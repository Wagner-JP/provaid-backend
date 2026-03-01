from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import engine
from app.database.models import Base
from app.routes.files import router as files_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="ProvaID API",
        description="Plataforma de certificação e verificação de autenticidade de conteúdos digitais (SHA-256).",
        version="1.0.0",
    )

    # ✅ CORS (necessário para o frontend conseguir chamar a API)
    # Em produção, troque "*" pelo domínio do seu frontend (ex: https://provai.app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ✅ Rotas
    app.include_router(files_router, tags=["Files"])

    # ✅ Healthcheck / Status
    @app.get("/", summary="Status da API", tags=["Health"])
    def root():
        return {"message": "ProvaID API rodando 🚀"}

    return app


app = create_app()

# ✅ Criação de tabelas
# Obs: OK para DEV. Em produção, prefira migrations (Alembic).
Base.metadata.create_all(bind=engine)