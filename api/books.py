from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from uuid import UUID

from schemas.book import Book, BookCreate, BookStatus
from services.book_service import BookService


router = APIRouter(prefix="/books", tags=["books"])
book_service = BookService()


@router.get("/", response_model=List[Book], status_code=200)
async def get_all_books(
    status: Optional[BookStatus] = Query(None, description="Filter by book status"),
    author: Optional[str] = Query(None, description="Filter by author (partial match)"),
    sort_by: str = Query("title", description="Sort by field (title or year)"),
    ascending: bool = Query(True, description="Sort order (ascending or descending)")
):
    """
    Get all books with optional filtering and sorting.
    
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
    
    books = await book_service.get_all_books(
        status=status,
        author=author,
        sort_by=sort_by,
        ascending=ascending
    )
    return books


@router.get("/{book_id}", response_model=Book, status_code=200)
async def get_book_by_id(book_id: str):
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
    
    book = await book_service.get_book_by_id(book_id)
    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    return book


@router.post("/", response_model=Book, status_code=201)
async def create_book(book_data: BookCreate):
    """
    Create a new book.
    
    - **title**: Book title (required)
    - **author**: Book author (required)
    - **description**: Book description (optional)
    - **status**: Book status (available or borrowed, defaults to available)
    - **year**: Publication year (required, between 1000 and 2100)
    """
    book = await book_service.create_book(book_data)
    return book


@router.delete("/{book_id}", status_code=204)
async def delete_book(book_id: str):
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
    
    await book_service.delete_book(book_id)
    return None
