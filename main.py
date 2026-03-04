from fastapi import FastAPI
from api.books import router as books_router

app = FastAPI(
    title="Library API",
    description="A simple library management API built with FastAPI",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url=None
)

app.include_router(books_router)


@app.get("/")
async def root():
    return {"message": "Welcome to Library API", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
