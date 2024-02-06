from pytest_bdd import scenario, given, when, then, parsers
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel, select
from fastapi.testclient import TestClient
import pytest

from author.schema import Author
from library import app


# Fixture for initializing the database
@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


# Test scenario
@scenario("test_add_author.feature", "Add a new author")
def test_add_author():
    pass


# Fixture for obtaining a test client
@pytest.fixture
def client():
    return TestClient(app)


# Fixture for clearing the database
@given("the system is empty")
def given_the_system_is_empty(db):
    pass  # Nothing to do here, as the database is already empty


# Fixture for adding a new author
@when(parsers.parse("I add a new author with name {author_name}"))
def when_i_add_a_new_author_with_name(client, author_name):
    response = client.post("api/authors", json={"name": author_name})
    return response


# Check if the author is in the database
@then(parsers.parse("the author {expected_author_name} should be in the system"))
def then_the_author_should_be_in_the_database(client, expected_author_name):
    authors = client.get("api/authors").json()
    assert len(authors) == 1
    author = Author.model_validate(authors[0])
    assert author.name == expected_author_name
