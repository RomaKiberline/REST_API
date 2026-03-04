from typing import Dict, List
from uuid import uuid4
from datetime import datetime

from schemas.book import BookStatus


class BookModel:
    def __init__(
        self,
        title: str,
        author: str,
        description: str = None,
        status: BookStatus = BookStatus.AVAILABLE,
        year: int = None
    ):
        self.id = str(uuid4())
        self.title = title
        self.author = author
        self.description = description
        self.status = status
        self.year = year
        self.created_at = datetime.now()
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "description": self.description,
            "status": self.status.value,
            "year": self.year,
            "created_at": self.created_at.isoformat()
        }
