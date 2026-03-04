from typing import Dict, List, Optional
from uuid import UUID

from models.book import BookModel
from repository.book_repository import BookRepository
from schemas.book import BookCreate, BookStatus


class BookService:
    def __init__(self):
        self.repository = BookRepository()
    
    async def create_book(self, book_data: BookCreate) -> Dict:
        book = BookModel(
            title=book_data.title,
            author=book_data.author,
            description=book_data.description,
            status=book_data.status,
            year=book_data.year
        )
        return await self.repository.add_book(book)
    
    async def get_all_books(
        self,
        status: Optional[BookStatus] = None,
        author: Optional[str] = None,
        sort_by: str = "title",
        ascending: bool = True
    ) -> List[Dict]:
        books = await self.repository.filter_books(status=status, author=author)
        return await self.repository.sort_books(books, sort_by, ascending)
    
    async def get_book_by_id(self, book_id: str) -> Optional[Dict]:
        return await self.repository.get_book_by_id(book_id)
    
    async def delete_book(self, book_id: str) -> bool:
        return await self.repository.delete_book(book_id)
