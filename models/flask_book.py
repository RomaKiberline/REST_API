from datetime import datetime
from typing import List, Optional

class FlaskBook:
    def __init__(self, title: str, author: str, year: int, description: str = "", status: str = "available"):
        self.id = self._generate_id()
        self.title = title
        self.author = author
        self.description = description
        self.year = year
        self.status = status
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def _generate_id(self) -> int:
        """Генерація унікального ID"""
        if not hasattr(FlaskBook, '_id_counter'):
            FlaskBook._id_counter = 1
        else:
            FlaskBook._id_counter += 1
        return FlaskBook._id_counter
    
    def to_dict(self) -> dict:
        """Конвертація в словник для JSON відповіді"""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'description': self.description,
            'year': self.year,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'FlaskBook':
        """Створення об'єкта зі словника"""
        book = cls(
            title=data['title'],
            author=data['author'],
            year=data['year'],
            description=data.get('description', ''),
            status=data.get('status', 'available')
        )
        book.id = data.get('id', book.id)
        if 'created_at' in data:
            book.created_at = datetime.fromisoformat(data['created_at'])
        if 'updated_at' in data:
            book.updated_at = datetime.fromisoformat(data['updated_at'])
        return book
    
    def update(self, **kwargs):
        """Оновлення полів книги"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()

# Список книг для зберігання в пам'яті (in-memory database)
flask_books_list: List[FlaskBook] = [
    FlaskBook(
        title="1984",
        author="George Orwell",
        description="Антиутопічний роман про тоталітарне суспільство",
        year=1949,
        status="available"
    ),
    FlaskBook(
        title="Лісова пісня",
        author="Леся Українка",
        description="Драматична поема про кохання Мавки та Лукаша",
        year=1911,
        status="available"
    ),
    FlaskBook(
        title="Кобзар",
        author="Тарас Шевченко",
        description="Збірка поезій Тараса Шевченка",
        year=1840,
        status="available"
    )
]
