from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from services.book_mongo_service import BookMongoService
from schemas.book_mongo import BookCreate, BookUpdate, BookResponse, BookStatus
from mongodb.client import MongoDB

router = APIRouter(prefix="/books", tags=["books"])

async def get_book_mongo_service():
    return BookMongoService()

@router.get("/", response_model=dict, status_code=200)
async def get_all_books(
    limit: int = Query(100, ge=1, le=1000, description="Number of books to return"),
    offset: int = Query(0, ge=0, description="Number of books to skip"),
    status: Optional[BookStatus] = Query(None, description="Filter by book status"),
    author: Optional[str] = Query(None, description="Filter by author (partial match)"),
    sort_by: str = Query("title", description="Sort by field (title, author, year, or created_at)"),
    ascending: bool = Query(True, description="Sort order (ascending or descending)"),
    book_service: BookMongoService = Depends(get_book_mongo_service)
):
    """
    Get all books with optional filtering, sorting, and limit-offset pagination.
    """
    if sort_by not in ["title", "author", "year", "created_at"]:
        raise HTTPException(
            status_code=400,
            detail="sort_by must be one of 'title', 'author', 'year', or 'created_at'"
        )
    
    result = await book_service.get_all_books(
        limit=limit,
        offset=offset,
        status=status,
        author=author,
        sort_by=sort_by,
        ascending=ascending
    )
    
    return {
        "books": [book.model_dump() for book in result["books"]],
        "total": result["total"],
        "limit": result["limit"],
        "offset": result["offset"],
        "has_next": result["has_next"],
        "has_prev": result["has_prev"]
    }

@router.get("/{book_id}", response_model=BookResponse, status_code=200)
async def get_book_by_id(
    book_id: str,
    book_service: BookMongoService = Depends(get_book_mongo_service)
):
    """
    Get a specific book by its ID.
    """
    book = await book_service.get_book_by_id(book_id)
    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    return book

@router.post("/", response_model=BookResponse, status_code=201)
async def create_book(
    book_data: BookCreate,
    book_service: BookMongoService = Depends(get_book_mongo_service)
):
    """
    Create a new book.
    """
    book = await book_service.create_book(book_data)
    return book

@router.put("/{book_id}", response_model=BookResponse, status_code=200)
async def update_book(
    book_id: str,
    book_data: BookUpdate,
    book_service: BookMongoService = Depends(get_book_mongo_service)
):
    """
    Update an existing book.
    """
    book = await book_service.update_book(book_id, book_data)
    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    return book

@router.delete("/{book_id}", status_code=204)
async def delete_book(
    book_id: str,
    book_service: BookMongoService = Depends(get_book_mongo_service)
):
    """
    Delete a book by its ID.
    """
    success = await book_service.delete_book(book_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )
    return None
