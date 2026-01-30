Feature: User Authentication
  As a user
  I want to login to the application
  So that I can access my account

  Background:
    Given I am on the login page

  @smoke @login
  Scenario: Successful login with valid credentials
    When I login with valid credentials
    Then I should be redirected to the dashboard
    And I should see a welcome message

  @regression @login
  Scenario Outline: Login with invalid credentials
    When I enter email "<email>" and password "<password>"
    And I click the login button
    Then I should see error message "<error_message>"

    Examples:
      | email              | password  | error_message           |
      | invalid@test.com   | wrong123  | Invalid credentials     |
      | test@test.com      |           | Password is required    |
      |                    | pass123   | Email is required       |

  @smoke @login
  Scenario: Logout functionality
    Given I am logged in
    When I click on logout button
    Then I should be redirected to login page
