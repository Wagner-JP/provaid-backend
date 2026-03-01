from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import hashlib

from app.database.connection import engine, get_db
from app.database.models import Base, FileRecord

app = FastAPI()

# Cria as tabelas no banco automaticamente
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "ProvaID API rodando 🚀"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Arquivo vazio.")

    sha256 = hashlib.sha256(content).hexdigest()

    # evita duplicação
    existing = db.query(FileRecord).filter(FileRecord.hash_sha256 == sha256).first()
    if existing:
        return {
            "message": "Arquivo já registrado",
            "exists": True,
            "id": existing.id,
            "filename": existing.filename,
            "hash": existing.hash_sha256,
            "size": existing.size,
            "created_at": existing.created_at,
        }

    record = FileRecord(
        filename=file.filename,
        hash_sha256=sha256,
        size=len(content),
    )

    try:
        db.add(record)
        db.commit()
        db.refresh(record)
    except IntegrityError:
        db.rollback()
        existing = db.query(FileRecord).filter(FileRecord.hash_sha256 == sha256).first()
        return {
            "message": "Arquivo já registrado",
            "exists": True,
            "id": existing.id if existing else None,
            "filename": existing.filename if existing else file.filename,
            "hash": sha256,
        }

    return {
        "message": "Arquivo registrado com sucesso",
        "exists": False,
        "id": record.id,
        "filename": record.filename,
        "hash": record.hash_sha256,
        "size": record.size,
        "created_at": record.created_at,
    }


@app.get("/verify/{file_hash}")
def verify_file(file_hash: str, db: Session = Depends(get_db)):
    file_hash = file_hash.strip().lower()

    record = db.query(FileRecord).filter(FileRecord.hash_sha256 == file_hash).first()
    if not record:
        return {"exists": False, "message": "Hash não encontrado"}

    return {
        "exists": True,
        "id": record.id,
        "filename": record.filename,
        "hash": record.hash_sha256,
        "size": record.size,
        "created_at": record.created_at,
    }