FROM python:3.11-slim

WORKDIR /app

COPY requirements-jwt.txt .

RUN pip install --no-cache-dir -r requirements-jwt.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
