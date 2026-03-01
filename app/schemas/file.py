from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class VerifyLink(BaseModel):
    endpoint: str
    url_local: str


class Certificate(BaseModel):
    provider: str = "ProvaID"
    version: str = "1.0"
    record_id: Optional[int] = None
    status: str  # "registered" | "already_registered"
    filename: Optional[str] = None
    sha256: str
    size_bytes: Optional[int] = None
    registered_at: Optional[datetime] = None
    verify: Optional[VerifyLink] = None


class UploadResponse(BaseModel):
    certificate: Certificate


class VerifyRecord(BaseModel):
    record_id: int
    filename: str
    sha256: str
    size_bytes: int
    registered_at: datetime

    # pydantic v2 + SQLAlchemy
    model_config = {"from_attributes": True}


class VerifyResponse(BaseModel):
    verified: bool
    provider: str = "ProvaID"
    version: str = "1.0"
    sha256: str
    message: Optional[str] = None
    record: Optional[VerifyRecord] = None