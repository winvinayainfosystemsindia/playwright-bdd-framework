Feature: Product Search
  As a user
  I want to search for products
  So that I can find items I'm interested in

  Background:
    Given I am logged in
    And I am on the home page

  @smoke @search
  Scenario: Search for existing product
    When I search for "Laptop"
    Then I should see search results
    And the results should contain "Laptop"

  @regression @search
  Scenario: Search with no results
    When I search for "NonExistentProduct12345"
    Then I should see "No results found" message

  @regression @search
  Scenario Outline: Search for different product categories
    When I search for "<product>"
    Then I should see search results
    And the results should be in category "<category>"

    Examples:
      | product      | category     |
      | Laptop       | Electronics  |
      | Smartphone   | Electronics  |
      | Headphones   | Accessories  |
