from typing import List, Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ASCENDING, DESCENDING
from bson import ObjectId
from schemas.book_mongo import Book, BookCreate, BookUpdate, BookStatus

class BookMongoRepository:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database.books
        self.collection.create_index([("title", ASCENDING)])
        self.collection.create_index([("author", ASCENDING)])
        self.collection.create_index([("year", ASCENDING)])
        self.collection.create_index([("status", ASCENDING)])

    async def create_book(self, book_data: BookCreate) -> Book:
        """Створення нової книги"""
        book_dict = book_data.model_dump()
        result = await self.collection.insert_one(book_dict)
        book_dict["id"] = str(result.inserted_id)
        return Book(**book_dict)

    async def get_book_by_id(self, book_id: str) -> Optional[Book]:
        """Отримання книги за ID"""
        try:
            book = await self.collection.find_one({"_id": ObjectId(book_id)})
            if book:
                book["id"] = str(book["_id"])
                return Book(**book)
            return None
        except Exception:
            return None

    async def get_all_books(
        self,
        limit: int = 100,
        offset: int = 0,
        status: Optional[BookStatus] = None,
        author: Optional[str] = None,
        sort_by: str = "title",
        ascending: bool = True
    ) -> List[Book]:
        """Отримання всіх книг з пагінацією, фільтрацією та сортуванням"""
        query = {}
        
        # Фільтрація
        if status:
            query["status"] = status
        if author:
            query["author"] = {"$regex": author, "$options": "i"}

        # Сортування
        sort_field = sort_by if sort_by in ["title", "author", "year", "created_at"] else "title"
        sort_order = ASCENDING if ascending else DESCENDING

        # Отримання даних
        cursor = self.collection.find(query).sort(sort_field, sort_order).skip(offset).limit(limit)
        books = []
        async for book in cursor:
            book["id"] = str(book["_id"])
            books.append(Book(**book))
        
        return books

    async def count_books(
        self,
        status: Optional[BookStatus] = None,
        author: Optional[str] = None
    ) -> int:
        """Підрахунок загальної кількості книг"""
        query = {}
        
        if status:
            query["status"] = status
        if author:
            query["author"] = {"$regex": author, "$options": "i"}

        return await self.collection.count_documents(query)

    async def update_book(self, book_id: str, book_data: BookUpdate) -> Optional[Book]:
        """Оновлення книги"""
        try:
            update_data = {k: v for k, v in book_data.model_dump().items() if v is not None}
            if not update_data:
                return await self.get_book_by_id(book_id)

            await self.collection.update_one(
                {"_id": ObjectId(book_id)},
                {"$set": update_data}
            )
            return await self.get_book_by_id(book_id)
        except Exception:
            return None

    async def delete_book(self, book_id: str) -> bool:
        """Видалення книги"""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(book_id)})
            return result.deleted_count > 0
        except Exception:
            return False

    async def book_exists(self, book_id: str) -> bool:
        """Перевірка існування книги"""
        book = await self.get_book_by_id(book_id)
        return book is not None
