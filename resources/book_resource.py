from flask import request, jsonify
from flask_restful import Resource
from models.flask_book import FlaskBook, flask_books_list
from datetime import datetime

class BookListResource(Resource):
    def get(self):
        """
        Отримати список всіх книг
        ---
        responses:
          200:
            description: Список книг успішно отримано
            schema:
              type: array
              items:
                $ref: '#/definitions/Book'
        """
        return [book.to_dict() for book in flask_books_list]
    
    def post(self):
        """
        Створити нову книгу
        ---
        parameters:
          - name: book
            in: body
            required: true
            schema:
              type: object
              required:
                - title
                - author
                - year
              properties:
                title:
                  type: string
                  example: "Назва книги"
                author:
                  type: string
                  example: "Автор книги"
                description:
                  type: string
                  example: "Опис книги"
                year:
                  type: integer
                  example: 2024
                status:
                  type: string
                  enum: [available, borrowed]
                  example: "available"
        responses:
          201:
            description: Книга успішно створена
            schema:
              $ref: '#/definitions/Book'
          400:
            description: Помилка валідації
        """
        data = request.get_json()
        
        # Валідація
        if not data or not all(k in data for k in ['title', 'author', 'year']):
            return {'error': 'Відсутні обов\'язкові поля: title, author, year'}, 400
        
        # Створення нової книги
        new_book = FlaskBook(
            title=data['title'],
            author=data['author'],
            description=data.get('description', ''),
            year=data['year'],
            status=data.get('status', 'available')
        )
        
        flask_books_list.append(new_book)
        
        return new_book.to_dict(), 201

class BookResource(Resource):
    def get(self, book_id):
        """
        Отримати книгу за ID
        ---
        parameters:
          - name: book_id
            in: path
            required: true
            type: integer
            description: ID книги
        responses:
          200:
            description: Книга успішно знайдена
            schema:
              $ref: '#/definitions/Book'
          404:
            description: Книга не знайдена
        """
        book = next((book for book in flask_books_list if book.id == book_id), None)
        if not book:
            return {'error': 'Книга не знайдена'}, 404
        return book.to_dict()
    
    def put(self, book_id):
        """
        Оновити книгу за ID
        ---
        parameters:
          - name: book_id
            in: path
            required: true
            type: integer
            description: ID книги
          - name: book
            in: body
            required: true
            schema:
              type: object
              properties:
                title:
                  type: string
                author:
                  type: string
                description:
                  type: string
                year:
                  type: integer
                status:
                  type: string
                  enum: [available, borrowed]
        responses:
          200:
            description: Книга успішно оновлена
            schema:
              $ref: '#/definitions/Book'
          404:
            description: Книга не знайдена
          400:
            description: Помилка валідації
        """
        book = next((book for book in flask_books_list if book.id == book_id), None)
        if not book:
            return {'error': 'Книга не знайдена'}, 404
        
        data = request.get_json()
        if not data:
            return {'error': 'Відсутні дані для оновлення'}, 400
        
        # Оновлення полів
        if 'title' in data:
            book.title = data['title']
        if 'author' in data:
            book.author = data['author']
        if 'description' in data:
            book.description = data['description']
        if 'year' in data:
            book.year = data['year']
        if 'status' in data:
            book.status = data['status']
        
        book.updated_at = datetime.now()
        
        return book.to_dict()
    
    def delete(self, book_id):
        """
        Видалити книгу за ID
        ---
        parameters:
          - name: book_id
            in: path
            required: true
            type: integer
            description: ID книги
        responses:
          204:
            description: Книга успішно видалена
          404:
            description: Книга не знайдена
        """
        global flask_books_list
        book_index = next((i for i, book in enumerate(flask_books_list) if book.id == book_id), None)
        
        if book_index is None:
            return {'error': 'Книга не знайдена'}, 404
        
        del flask_books_list[book_index]
        return '', 204
