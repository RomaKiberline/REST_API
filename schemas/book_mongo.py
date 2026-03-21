from pydantic import BaseModel, Field
from pydantic_mongo import ObjectIdField
from typing import Optional
from datetime import datetime
from enum import Enum
from bson import ObjectId

class BookStatus(str, Enum):
    available = "available"
    borrowed = "borrowed"

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    status: BookStatus = BookStatus.available
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
    id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True

class BookResponse(BaseModel):
    id: str
    title: str
    author: str
    description: Optional[str]
    status: BookStatus
    year: int
    created_at: datetime

    class Config:
        from_attributes = True
