Feature: Add Author
  As a user
  I want to add a new author to the database
  So that I can associate books with the author

  Scenario: Add a new author
    Given the system is empty
    When I add a new author with name Henryk Sienkiewicz
    Then the author Henryk Sienkiewicz should be in the system
