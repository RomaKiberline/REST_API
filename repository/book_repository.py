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
    
    def get_all_books(
        self,
        limit: int = 100,
        offset: int = 0,
        status: Optional[BookStatus] = None,
        author: Optional[str] = None,
        sort_by: str = "title",
        ascending: bool = True
    ) -> List[Book]:
        query = self.db.query(Book)
        
        # Apply filters
        if status:
            query = query.filter(Book.status == status)
        
        if author:
            query = query.filter(
                Book.author.ilike(f"%{author}%")
            )
        
        # Apply sorting
        if sort_by == "title":
            order_column = Book.title
        elif sort_by == "year":
            order_column = Book.year
        else:
            order_column = Book.title
        
        if ascending:
            query = query.order_by(asc(order_column))
        else:
            query = query.order_by(desc(order_column))
        
        # Apply pagination
        return query.offset(offset).limit(limit).all()
    
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
