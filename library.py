import time
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from sqlmodel import SQLModel

from db import engine
from routers import books, authors

app = FastAPI(title="Library")

app.include_router(authors.router)
app.include_router(books.router)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    uvicorn.run('library:app', reload=True)