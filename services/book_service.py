from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session

from models.book import Book
from repository.book_repository import BookRepository
from schemas.book import BookCreate, BookStatus


class BookService:
    def __init__(self, db: Session):
        self.repository = BookRepository(db)
    
    def create_book(self, book_data: BookCreate) -> Dict[str, Any]:
        book = Book(
            title=book_data.title,
            author=book_data.author,
            description=book_data.description,
            status=book_data.status,
            year=book_data.year
        )
        created_book = self.repository.add_book(book)
        return created_book.to_dict()
    
    def get_all_books_cursor(
        self,
        limit: int = 100,
        cursor: Optional[str] = None,
        status: Optional[BookStatus] = None,
        author: Optional[str] = None,
        sort_by: str = "created_at",
        ascending: bool = True
    ) -> Dict[str, Any]:
        books, next_cursor = self.repository.get_all_books_cursor(
            limit=limit,
            cursor=cursor,
            status=status,
            author=author,
            sort_by=sort_by,
            ascending=ascending
        )
        
        return {
            "books": [book.to_dict() for book in books],
            "next_cursor": next_cursor,
            "has_next": next_cursor is not None,
            "limit": limit
        }
    
    def get_book_by_id(self, book_id: str) -> Optional[Dict]:
        book = self.repository.get_book_by_id(book_id)
        return book.to_dict() if book else None
    
    def delete_book(self, book_id: str) -> bool:
        return self.repository.delete_book(book_id)
