from typing import List, Optional
from uuid import UUID
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc

from models.book import Book
from schemas.book import BookStatus


class BookRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def add_book(self, book: Book) -> Book:
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book
    
    def get_all_books_cursor(
        self,
        limit: int = 100,
        cursor: Optional[str] = None,
        status: Optional[BookStatus] = None,
        author: Optional[str] = None,
        sort_by: str = "created_at",
        ascending: bool = True
    ) -> tuple[List[Book], Optional[str]]:
        query = self.db.query(Book)
        
        # Apply filters
        if status:
            query = query.filter(Book.status == status)
        
        if author:
            query = query.filter(
                Book.author.ilike(f"%{author}%")
            )
        
        if sort_by == "title":
            order_columns = [Book.title, Book.id]
        elif sort_by == "year":
            order_columns = [Book.year, Book.id]
        elif sort_by == "created_at":
            order_columns = [Book.created_at, Book.id]
        else:
            order_columns = [Book.created_at, Book.id]
        
        if cursor:
            try:
                cursor_uuid = UUID(cursor)
                if ascending:
                    # For ascending order, get items after cursor
                    query = query.filter(Book.id > cursor_uuid)
                else:
                    # For descending order, get items before cursor
                    query = query.filter(Book.id < cursor_uuid)
            except ValueError:
                # Invalid cursor, ignore it
                pass
        
        # Apply sorting
        if ascending:
            for col in order_columns:
                query = query.order_by(asc(col))
        else:
            for col in order_columns:
                query = query.order_by(desc(col))
        
        # Apply limit (get one extra to determine if there's a next page)
        books = query.limit(limit + 1).all()
        
        # Determine next cursor
        next_cursor = None
        has_next = len(books) > limit
        if has_next:
            books = books[:-1]
            if books:
                next_cursor = str(books[-1].id)
        
        return books, next_cursor
    
    def get_book_by_id(self, book_id: str) -> Optional[Book]:
        try:
            uuid.UUID(book_id)
            return self.db.query(Book).filter(Book.id == book_id).first()
        except ValueError:
            return None
    
    def delete_book(self, book_id: str) -> bool:
        try:
            uuid.UUID(book_id)
            book = self.db.query(Book).filter(Book.id == book_id).first()
            if book:
                self.db.delete(book)
                self.db.commit()
                return True
            return False
        except ValueError:
            return False
    
    def count_books(
        self,
        status: Optional[BookStatus] = None,
        author: Optional[str] = None
    ) -> int:
        query = self.db.query(Book)
        
        if status:
            query = query.filter(Book.status == status)
        
        if author:
            query = query.filter(
                Book.author.ilike(f"%{author}%")
            )
        
        return query.count()
