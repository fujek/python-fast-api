from pytest_bdd import scenario, given, when, then, parsers
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel, select
import pytest

from author.schema import Author
from books.schema import Book
from library import app
from fastapi.testclient import TestClient


# Fixture for initializing the database
@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def session(db):
    with Session(db) as session:
        yield session


# Fixture for obtaining a test client
@pytest.fixture
def client():
    return TestClient(app)


# Test scenario
@scenario("test_search_books.feature", "Search for a book by name and author")
def test_search_books():
    pass


# Fixture for adding books to the database
@given("there are books in the database")
def given_there_are_books_in_the_database(session):
    # Adding an author
    author = Author(name="Henryk Sienkiewicz")
    session.add(author)
    session.commit()
    # Adding books
    book1 = Book(name="W pustyni i w puszczy", author_id=author.id, isbn='123-123',
                 description="Book description")
    book2 = Book(name="Potop", author_id=author.id, isbn='233-123',
                 description="Book description")
    session.add(book1)
    session.add(book2)
    session.commit()


# Fixture for searching books
@when(parsers.parse("I search for a book by name {book_name} and author {author_name}"),
      target_fixture="request_result")
def when_i_search_for_a_book_by_name_and_author(client, book_name, author_name):
    response = client.get(f"/api/books?name={book_name}&author={author_name}")
    return response.json()


# Check if the book is found
@then(parsers.parse("I should find the book {expected_book}"))
def then_i_should_find_the_book(expected_book, request_result):
    assert len(request_result) == 1
    found_book = Book.model_validate(request_result[0])
    assert found_book.name == expected_book
