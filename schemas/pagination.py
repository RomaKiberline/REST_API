from typing import List, Any, Optional
from pydantic import BaseModel, Field
from .book import Book


class PaginatedBooksResponse(BaseModel):
    books: List[Book] = Field(..., description="List of books")
    total: int = Field(..., description="Total number of books")
    limit: int = Field(..., description="Number of books per page")
    offset: int = Field(..., description="Number of books skipped")
    has_next: bool = Field(..., description="Whether there are more books")
    has_prev: bool = Field(..., description="Whether there are previous books")
