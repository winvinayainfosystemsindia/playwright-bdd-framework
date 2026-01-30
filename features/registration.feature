Feature: User Registration
  As a new user
  I want to register for an account
  So that I can use the application

  @smoke @registration
  Scenario: Successful registration with valid data
    Given I am on the registration page
    When I fill in the registration form with valid data
    And I submit the registration form
    Then I should see registration success message
    And I should receive a confirmation email

  @regression @registration
  Scenario: Registration with existing email
    Given I am on the registration page
    When I register with an already registered email
    Then I should see "Email already exists" error

  @regression @registration
  Scenario: Registration with invalid email format
    Given I am on the registration page
    When I enter invalid email format
    And I submit the registration form
    Then I should see email validation error

  @regression @registration
  Scenario: Registration with weak password
    Given I am on the registration page
    When I enter a weak password
    And I submit the registration form
    Then I should see password strength error
