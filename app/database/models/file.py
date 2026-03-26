from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from app.database.connection import Base


class FileRecord(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    hash_sha256 = Column(String, unique=True, index=True, nullable=False)
    size = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)