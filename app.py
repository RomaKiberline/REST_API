from flask import Flask
from flask_restful import Api
from flasgger import Swagger
from resources.book_resource import BookResource, BookListResource

app = Flask(__name__)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger_template = {
    "info": {
        "title": "Library API",
        "description": "API для управління бібліотекою книг",
        "version": "1.0.0",
        "contact": {
            "developer": "Student",
            "email": "student@pnu.edu.ua"
        }
    },
    "security": [
        {
            "BearerAuth": []
        }
    ]
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

api = Api(app)

api.add_resource(BookListResource, '/api/books')
api.add_resource(BookResource, '/api/books/<int:book_id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
