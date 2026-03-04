from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status, Depends
from uuid import UUID
from sqlalchemy.orm import Session

from schemas.book import Book, BookCreate, BookStatus
from schemas.pagination import PaginatedBooksResponse
from services.book_service import BookService
from database import get_db


router = APIRouter(prefix="/books", tags=["books"])


def get_book_service(db: Session = Depends(get_db)) -> BookService:
    return BookService(db)


@router.get("/", response_model=PaginatedBooksResponse, status_code=200)
def get_all_books(
    limit: int = Query(100, ge=1, le=1000, description="Number of books to return"),
    offset: int = Query(0, ge=0, description="Number of books to skip"),
    status: Optional[BookStatus] = Query(None, description="Filter by book status"),
    author: Optional[str] = Query(None, description="Filter by author (partial match)"),
    sort_by: str = Query("title", description="Sort by field (title or year)"),
    ascending: bool = Query(True, description="Sort order (ascending or descending)"),
    book_service: BookService = Depends(get_book_service)
):
    """
    Get all books with optional filtering, sorting, and pagination.
    
    - **limit**: Number of books to return (1-1000, default: 100)
    - **offset**: Number of books to skip (default: 0)
    - **status**: Filter books by availability status
    - **author**: Filter books by author (case-insensitive partial match)
    - **sort_by**: Sort field - either 'title' or 'year'
    - **ascending**: Sort order - True for ascending, False for descending
    """
    if sort_by not in ["title", "year"]:
        raise HTTPException(
            status_code=400,
            detail="sort_by must be either 'title' or 'year'"
        )
    
    result = book_service.get_all_books(
        limit=limit,
        offset=offset,
        status=status,
        author=author,
        sort_by=sort_by,
        ascending=ascending
    )
    
    return PaginatedBooksResponse(**result)


@router.get("/{book_id}", response_model=Book, status_code=200)
def get_book_by_id(
    book_id: str,
    book_service: BookService = Depends(get_book_service)
):
    """
    Get a specific book by its ID.
    
    - **book_id**: UUID of the book to retrieve
    """
    try:
        UUID(book_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid book ID format"
        )
    
    book = book_service.get_book_by_id(book_id)
    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    return book


@router.post("/", response_model=Book, status_code=201)
def create_book(
    book_data: BookCreate,
    book_service: BookService = Depends(get_book_service)
):
    """
    Create a new book.
    
    - **title**: Book title (required)
    - **author**: Book author (required)
    - **description**: Book description (optional)
    - **status**: Book status (available or borrowed, defaults to available)
    - **year**: Publication year (required, between 1000 and 2100)
    """
    book = book_service.create_book(book_data)
    return book


@router.delete("/{book_id}", status_code=204)
def delete_book(
    book_id: str,
    book_service: BookService = Depends(get_book_service)
):
    """
    Delete a book by its ID.
    
    - **book_id**: UUID of the book to delete
    This operation is idempotent - deleting a non-existent book returns the same response.
    """
    try:
        UUID(book_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid book ID format"
        )
    
    book_service.delete_book(book_id)
    return None
