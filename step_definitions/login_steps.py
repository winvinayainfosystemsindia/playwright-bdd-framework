"""
Login Step Definitions
BDD step implementations for login feature
"""
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from pages.login_page import LoginPage
from pages.home_page import HomePage
from config.config import config
from utils.logger import Logger


logger = Logger.get_logger(__name__)

# Load scenarios from feature file
scenarios('../features/login.feature')


# Given Steps

@given('I am on the login page')
def navigate_to_login_page(login_page: LoginPage):
    """Navigate to login page."""
    logger.info("Step: Given I am on the login page")
    login_page.navigate()
    assert login_page.is_on_login_page(), "Not on login page"


@given('I am logged in')
def user_is_logged_in(login_page: LoginPage, home_page: HomePage):
    """Login with valid credentials."""
    logger.info("Step: Given I am logged in")
    
    # Get valid user credentials
    user = config.get_test_user('valid')
    
    # Navigate to login page
    login_page.navigate()
    
    # Perform login
    login_page.login(user['email'], user['password'])
    
    # Verify login successful
    assert home_page.verify_successful_login(), "Login failed"


# When Steps

@when('I login with valid credentials')
def login_with_valid_credentials(login_page: LoginPage):
    """Login with valid credentials."""
    logger.info("Step: When I login with valid credentials")
    
    # Get valid user credentials
    user = config.get_test_user('valid')
    
    # Perform login
    login_page.login(user['email'], user['password'])


@when(parsers.parse('I enter email "{email}" and password "{password}"'))
def enter_email_and_password(login_page: LoginPage, email: str, password: str):
    """
    Enter email and password.
    
    Args:
        email: Email address
        password: Password
    """
    logger.info(f"Step: When I enter email '{email}' and password")
    
    if email:
        login_page.enter_email(email)
    
    if password:
        login_page.enter_password(password)


@when('I click the login button')
def click_login_button(login_page: LoginPage):
    """Click login button."""
    logger.info("Step: When I click the login button")
    login_page.click_login_button()


@when('I click on logout button')
def click_logout_button(home_page: HomePage):
    """Click logout button."""
    logger.info("Step: When I click on logout button")
    home_page.logout()


# Then Steps

@then('I should be redirected to the dashboard')
def verify_redirected_to_dashboard(home_page: HomePage):
    """Verify redirection to dashboard."""
    logger.info("Step: Then I should be redirected to the dashboard")
    assert home_page.is_on_home_page(), "Not redirected to dashboard"


@then('I should see a welcome message')
def verify_welcome_message(home_page: HomePage):
    """Verify welcome message is displayed."""
    logger.info("Step: Then I should see a welcome message")
    assert home_page.is_welcome_message_displayed(), "Welcome message not displayed"


@then(parsers.parse('I should see error message "{error_message}"'))
def verify_error_message(login_page: LoginPage, error_message: str, context: dict):
    """
    Verify error message is displayed.
    
    Args:
        error_message: Expected error message
    """
    logger.info(f"Step: Then I should see error message '{error_message}'")
    
    # Wait a bit for error message to appear
    login_page.wait_for_timeout(1000)
    
    # Check if error message is displayed
    assert login_page.is_error_message_displayed(), f"Error message not displayed"
    
    # Get actual error message
    actual_message = login_page.get_error_message()
    
    # Store in context for debugging
    context['error_message'] = actual_message
    
    # Verify error message contains expected text
    assert error_message.lower() in actual_message.lower(), \
        f"Expected '{error_message}' in error message, but got '{actual_message}'"


@then('I should be redirected to login page')
def verify_redirected_to_login_page(login_page: LoginPage):
    """Verify redirection to login page."""
    logger.info("Step: Then I should be redirected to login page")
    
    # Wait for redirect
    login_page.wait_for_timeout(2000)
    
    # Verify on login page
    assert login_page.is_on_login_page(), "Not redirected to login page"
