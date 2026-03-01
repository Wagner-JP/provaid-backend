from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .connection import Base


class FileRecord(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    hash_sha256 = Column(String, unique=True, nullable=False)
    size = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)