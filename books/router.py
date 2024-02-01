from typing import List

from fastapi import FastAPI, HTTPException, APIRouter, Depends
from sqlmodel import Session, select

from books.schema import Book, BookInput
from db.config import get_session

router = APIRouter(prefix="/api/books")


@router.post("/", response_model=Book, status_code=201)
def create_book(book: BookInput, session: Session = Depends(get_session)):
    new_book = Book.model_validate(book)
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return book


@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: BookInput, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in updated_book.dict().items():
        setattr(book, key, value)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@router.get("/", response_model=List[Book])
def read_books(session: Session = Depends(get_session)):
    books = session.exec(select(Book)).all()
    return books


@router.get("/{book_id}", response_model=Book)
def read_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
