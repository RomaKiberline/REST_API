from typing import Dict, List, Optional
from uuid import UUID

from models.book import BookModel
from schemas.book import BookStatus


class BookRepository:
    def __init__(self):
        self._books: List[Dict] = []
    
    async def add_book(self, book: BookModel) -> Dict:
        book_dict = book.to_dict()
        self._books.append(book_dict)
        return book_dict
    
    async def get_all_books(self) -> List[Dict]:
        return self._books.copy()
    
    async def get_book_by_id(self, book_id: str) -> Optional[Dict]:
        for book in self._books:
            if book["id"] == book_id:
                return book
        return None
    
    async def delete_book(self, book_id: str) -> bool:
        for i, book in enumerate(self._books):
            if book["id"] == book_id:
                del self._books[i]
                return True
        return False
    
    async def filter_books(
        self,
        status: Optional[BookStatus] = None,
        author: Optional[str] = None
    ) -> List[Dict]:
        filtered_books = self._books.copy()
        
        if status:
            filtered_books = [
                book for book in filtered_books 
                if book["status"] == status.value
            ]
        
        if author:
            filtered_books = [
                book for book in filtered_books 
                if author.lower() in book["author"].lower()
            ]
        
        return filtered_books
    
    async def sort_books(
        self,
        books: List[Dict],
        sort_by: str = "title",
        ascending: bool = True
    ) -> List[Dict]:
        if sort_by not in ["title", "year"]:
            return books
        
        reverse = not ascending
        return sorted(books, key=lambda x: x[sort_by], reverse=reverse)
