# app/services/file_service.py
import hashlib
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.database.models import FileRecord
from app.schemas.file import UploadResponse, Certificate, VerifyResponse, VerifyRecord, VerifyLink


def register_file(db: Session, filename: str, content: bytes) -> UploadResponse:
    if not content:
        raise HTTPException(status_code=400, detail="Arquivo vazio.")

    sha256 = hashlib.sha256(content).hexdigest()

    existing = db.query(FileRecord).filter(FileRecord.hash_sha256 == sha256).first()
    if existing:
        return UploadResponse(
            certificate=Certificate(
                status="already_registered",
                record_id=existing.id,
                filename=existing.filename,
                sha256=existing.hash_sha256,
                size_bytes=existing.size,
                registered_at=existing.created_at,
                verify=VerifyLink(
                    endpoint=f"/verify/{existing.hash_sha256}",
                    url_local=f"http://127.0.0.1:8000/verify/{existing.hash_sha256}",
                ),
            )
        )

    record = FileRecord(
        filename=filename,
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
        if existing:
            return UploadResponse(
                certificate=Certificate(
                    status="already_registered",
                    record_id=existing.id,
                    filename=existing.filename,
                    sha256=existing.hash_sha256,
                    size_bytes=existing.size,
                    registered_at=existing.created_at,
                    verify=VerifyLink(
                        endpoint=f"/verify/{existing.hash_sha256}",
                        url_local=f"http://127.0.0.1:8000/verify/{existing.hash_sha256}",
                    ),
                )
            )

        # fallback (muito raro)
        return UploadResponse(
            certificate=Certificate(
                status="already_registered",
                record_id=None,
                filename=filename,
                sha256=sha256,
            )
        )

    return UploadResponse(
        certificate=Certificate(
            status="registered",
            record_id=record.id,
            filename=record.filename,
            sha256=record.hash_sha256,
            size_bytes=record.size,
            registered_at=record.created_at,
            verify=VerifyLink(
                endpoint=f"/verify/{record.hash_sha256}",
                url_local=f"http://127.0.0.1:8000/verify/{record.hash_sha256}",
            ),
        )
    )


def verify_hash(db: Session, file_hash: str) -> VerifyResponse:
    file_hash = file_hash.strip().lower()

    record = db.query(FileRecord).filter(FileRecord.hash_sha256 == file_hash).first()
    if not record:
        return VerifyResponse(
            verified=False,
            sha256=file_hash,
            message="Hash não encontrado",
            record=None,
        )

    return VerifyResponse(
        verified=True,
        sha256=record.hash_sha256,
        record=VerifyRecord(
            record_id=record.id,
            filename=record.filename,
            sha256=record.hash_sha256,
            size_bytes=record.size,
            registered_at=record.created_at,
        ),
    )