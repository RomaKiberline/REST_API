from enum import Enum
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field


class BookStatus(str, Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    status: BookStatus = BookStatus.AVAILABLE
    year: int = Field(..., ge=1000, le=2100)


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[BookStatus] = None
    year: Optional[int] = Field(None, ge=1000, le=2100)


class Book(BookBase):
    id: str
    created_at: str

    model_config = {"from_attributes": True}


# Cursor Pagination Schemas
class CursorPaginatedBooksResponse(BaseModel):
    books: List[Book]
    next_cursor: Optional[str] = None
    has_next: bool = False
    limit: int
