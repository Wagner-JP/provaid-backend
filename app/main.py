import os
print("CAMINHO ATUAL:", os.getcwd())

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import engine, Base
from app.routes.files import router as files_router
from app.routes.auth import router as auth_router

app = FastAPI(
    title="ProvaID API",
    description="Plataforma de certificação e verificação de autenticidade de conteúdos digitais (SHA-256).",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(files_router)
app.include_router(auth_router)


@app.get("/", tags=["Health"])
def root():
    return {"message": "ProvaID API rodando 🚀"}


Base.metadata.create_all(bind=engine)