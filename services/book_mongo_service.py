from typing import List, Dict, Any, Optional
from mongodb.book_repository import BookMongoRepository
from mongodb.client import MongoDB
from schemas.book_mongo import Book, BookCreate, BookUpdate, BookStatus, BookResponse

class BookMongoService:
    def __init__(self):
        database = MongoDB.get_database()
        self.repository = BookMongoRepository(database)

    async def create_book(self, book_data: BookCreate) -> BookResponse:
        """Створення нової книги"""
        book = await self.repository.create_book(book_data)
        return BookResponse(
            id=str(book.id),
            title=book.title,
            author=book.author,
            description=book.description,
            status=book.status,
            year=book.year,
            created_at=book.created_at
        )

    async def get_book_by_id(self, book_id: str) -> Optional[BookResponse]:
        """Отримання книги за ID"""
        book = await self.repository.get_book_by_id(book_id)
        if not book:
            return None
        return BookResponse(
            id=str(book.id),
            title=book.title,
            author=book.author,
            description=book.description,
            status=book.status,
            year=book.year,
            created_at=book.created_at
        )

    async def get_all_books(
        self,
        limit: int = 100,
        offset: int = 0,
        status: Optional[BookStatus] = None,
        author: Optional[str] = None,
        sort_by: str = "title",
        ascending: bool = True
    ) -> Dict[str, Any]:
        """Отримання всіх книг з пагінацією"""
        books = await self.repository.get_all_books(
            limit=limit,
            offset=offset,
            status=status,
            author=author,
            sort_by=sort_by,
            ascending=ascending
        )
        
        total_count = await self.repository.count_books(
            status=status,
            author=author
        )

        book_responses = [
            BookResponse(
                id=str(book.id),
                title=book.title,
                author=book.author,
                description=book.description,
                status=book.status,
                year=book.year,
                created_at=book.created_at
            ) for book in books
        ]

        return {
            "books": book_responses,
            "total": total_count,
            "limit": limit,
            "offset": offset,
            "has_next": offset + limit < total_count,
            "has_prev": offset > 0
        }

    async def update_book(self, book_id: str, book_data: BookUpdate) -> Optional[BookResponse]:
        """Оновлення книги"""
        book = await self.repository.update_book(book_id, book_data)
        if not book:
            return None
        return BookResponse(
            id=str(book.id),
            title=book.title,
            author=book.author,
            description=book.description,
            status=book.status,
            year=book.year,
            created_at=book.created_at
        )

    async def delete_book(self, book_id: str) -> bool:
        """Видалення книги"""
        return await self.repository.delete_book(book_id)

    async def book_exists(self, book_id: str) -> bool:
        """Перевірка існування книги"""
        return await self.repository.book_exists(book_id)
