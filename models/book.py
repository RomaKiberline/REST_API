from sqlalchemy import Column, String, Integer, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
import uuid

from schemas.book import BookStatus

Base = declarative_base()


class Book(Base):
    __tablename__ = "books"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=True)
    status = Column(Enum(BookStatus), default=BookStatus.AVAILABLE, nullable=False)
    year = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "id": str(self.id),
            "title": self.title,
            "author": self.author,
            "description": self.description,
            "status": self.status.value if self.status else None,
            "year": self.year,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
