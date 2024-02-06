Feature: Search Books
As a user
I want to search for books by name and/or author
So that I can find the books I'm interested in

Scenario: Search for a book by name and author
Given there are books in the database
When I search for a book by name puszcz and author sienkiewicz
Then I should find the book W pustyni i w puszczy