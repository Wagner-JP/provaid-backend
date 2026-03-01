from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services.file_service import register_file, verify_hash
from app.schemas.file import UploadResponse, VerifyResponse

router = APIRouter(tags=["Arquivos"])


@router.post(
    "/upload",
    summary="Registrar arquivo",
    description="Registra um arquivo, gera hash SHA-256 e retorna um certificado digital.",
    response_model=UploadResponse
)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    content = await file.read()
    return register_file(db=db, filename=file.filename, content=content)


@router.get(
    "/verify/{file_hash}",
    summary="Verificar hash",
    description="Verifica se um hash SHA-256 já foi registrado e retorna os metadados.",
    response_model=VerifyResponse
)
def verify_file(
    file_hash: str,
    db: Session = Depends(get_db)
):
    return verify_hash(db=db, file_hash=file_hash)