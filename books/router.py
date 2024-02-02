import os
from typing import List, Sequence

from fastapi import HTTPException, APIRouter, Depends, UploadFile, File
from fastapi.responses import FileResponse
from sqlmodel import Session, select

from auth.token_service import verify_access_token
from books.schema import Book, BookInput
from db.config import get_session

router = APIRouter(prefix="/api/books")

covers_directory = "covers"


@router.post("/", status_code=201)
def create_book(book: BookInput, session: Session = Depends(get_session)) -> Book:
    new_book = Book.model_validate(book)
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return new_book


@router.put("/{book_id}")
def update_book(book_id: int, updated_book: BookInput, session: Session = Depends(get_session)) -> Book:
    book = get_book(book_id, session)
    for key, value in updated_book.dict().items():
        setattr(book, key, value)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@router.get("/")
def read_books(session: Session = Depends(get_session)) -> Sequence[Book]:
    books = session.exec(select(Book)).all()
    return books


@router.get("/{book_id}")
def read_book(book_id: int, session: Session = Depends(get_session)) -> Book:
    return get_book(book_id, session)


@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, session: Session = Depends(get_session)):
    book = get_book(book_id, session)
    session.delete(book)
    session.commit()


@router.get("/{book_id}/cover")
def get_book_cover(book_id: int, session: Session = Depends(get_session)) -> FileResponse:
    book = get_book(book_id, session)
    file_path = get_cover_filepath(book_id, book.cover_file_name)
    return FileResponse(file_path, headers={"Content-Disposition": f"attachment; filename={book.cover_file_name}"})


@router.post("/{book_id}/cover", status_code=204, dependencies=[Depends(verify_access_token)])
def save_book_cover(book_id: int, cover: UploadFile = File(...), session: Session = Depends(get_session)):
    book = get_book(book_id, session)
    book.cover_file_name = cover.filename
    save_cover(cover, book_id)
    session.commit()


def get_book(book_id, session):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


def save_cover(cover: UploadFile, book_id: int):
    if not os.path.exists(covers_directory):
        os.makedirs(covers_directory)
    file_path = get_cover_filepath(book_id, cover.filename)

    with open(file_path, "wb") as file_object:
        file_object.write(cover.file.read())

    return file_path


def get_cover_filepath(book_id: int, original_cover_filename: str):
    return os.path.join(covers_directory, f"{str(book_id)}_{original_cover_filename}")
