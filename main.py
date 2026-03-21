from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.books_mongo import router as books_mongo_router
from mongodb.client import MongoDB

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await MongoDB.connect_to_mongo()
    yield
    # Shutdown
    await MongoDB.close_mongo_connection()

app = FastAPI(
    title="Library API with MongoDB",
    description="A simple library management API built with FastAPI and MongoDB",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url=None,
    lifespan=lifespan
)

app.include_router(books_mongo_router)


@app.get("/")
async def root():
    return {"message": "Welcome to Library API with MongoDB", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
