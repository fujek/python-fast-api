import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session

from auth.router import router as auth_router, pwd_context
from auth.schema import User, UserRole
from author.router import router as author_router
from books.router import router as books_router
from borrow.router import router as borrow_router
from db.config import engine

app = FastAPI(title="Library")

app.include_router(author_router, tags=['Authors'])
app.include_router(books_router, tags=['Books'])
app.include_router(auth_router, tags=['Auth'])
app.include_router(borrow_router, tags=['Borrowings'])

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
    # with Session(engine) as session:
    #     user = User()
    #     user.username = 'damian'
    #     user.password = pwd_context.hash('test')
    #     user.role = UserRole.ADMIN
    #     session.add(user)
    #     session.commit()


if __name__ == "__main__":
    uvicorn.run('library:app', reload=True)
