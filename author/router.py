from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from auth.token_service import verify_access_token
from author.schema import AuthorInput, Author
from books.schema import Book
from db.config import get_session

router = APIRouter(prefix="/api/authors")


@router.post("/", response_model=Author, status_code=201, dependencies=[Depends(verify_access_token)])
def create_author(author: AuthorInput, session: Session = Depends(get_session)):
    new_author = Author.model_validate(author)
    session.add(new_author)
    session.commit()
    session.refresh(new_author)
    return new_author


@router.put("/{author_id}", response_model=Author, dependencies=[Depends(verify_access_token)])
def update_author(author_id: int, updated_author: AuthorInput, session: Session = Depends(get_session)):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    for key, value in updated_author.dict().items():
        setattr(author, key, value)
    session.add(author)
    session.commit()
    session.refresh(author)
    return author


@router.get("/", response_model=List[Author])
def read_authors(session: Session = Depends(get_session)):
    authors = session.exec(select(Author)).all()
    return authors


@router.get("/{author_id}", response_model=Author)
def read_author(author_id: int, session: Session = Depends(get_session)):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.delete("/{author_id}", status_code=204, dependencies=[Depends(verify_access_token)])
def delete_author(author_id: int, session: Session = Depends(get_session)):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    session.delete(author)
    session.commit()


@router.get("/{author_id}/books")
def get_author_books(author_id: int, session: Session = Depends(get_session)):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    query = select(Book).where(Book.author == author)
    return session.exec(query).all()
