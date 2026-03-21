// Створення бази даних library_db та користувача
db = db.getSiblingDB('library_db');

// Створення користувача для library_db
db.createUser({
  user: 'mongo_admin',
  pwd: 'password',
  roles: [
    {
      role: 'readWrite',
      db: 'library_db'
    }
  ]
});

// Створення початкових індексів
db.books.createIndex({ "title": 1 });
db.books.createIndex({ "author": 1 });
db.books.createIndex({ "year": 1 });
db.books.createIndex({ "status": 1 });

print('Database library_db initialized successfully');
