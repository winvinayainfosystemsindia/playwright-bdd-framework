"""
Registration Step Definitions
BDD step implementations for registration feature
"""
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from pages.registration_page import RegistrationPage
from config.config import config
from utils.logger import Logger
from utils.data_reader import fake_data_generator


logger = Logger.get_logger(__name__)

# Load scenarios from feature file
scenarios('../features/registration.feature')


# Given Steps

@given('I am on the registration page')
def navigate_to_registration_page(registration_page: RegistrationPage):
    """Navigate to registration page."""
    logger.info("Step: Given I am on the registration page")
    registration_page.navigate()
    assert registration_page.is_on_registration_page(), "Not on registration page"


# When Steps

@when('I fill in the registration form with valid data')
def fill_registration_form_with_valid_data(registration_page: RegistrationPage, context: dict):
    """Fill registration form with valid data."""
    logger.info("Step: When I fill in the registration form with valid data")
    
    # Generate fake user data
    user_data = fake_data_generator.generate_user()
    
    # Store in context for later use
    context['registration_data'] = user_data
    
    # Fill registration form
    registration_page.register_user(user_data)


@when('I submit the registration form')
def submit_registration_form(registration_page: RegistrationPage):
    """Submit registration form."""
    logger.info("Step: When I submit the registration form")
    registration_page.submit_registration_form()


@when('I register with an already registered email')
def register_with_existing_email(registration_page: RegistrationPage, context: dict):
    """Register with existing email."""
    logger.info("Step: When I register with an already registered email")
    
    # Get existing user data
    user = config.get_test_user('existing_user')
    
    # Generate new user data but use existing email
    user_data = fake_data_generator.generate_user()
    user_data['email'] = user['email']
    
    # Store in context
    context['registration_data'] = user_data
    
    # Fill and submit form
    registration_page.register_user(user_data)
    registration_page.submit_registration_form()


@when('I enter invalid email format')
def enter_invalid_email_format(registration_page: RegistrationPage, context: dict):
    """Enter invalid email format."""
    logger.info("Step: When I enter invalid email format")
    
    # Generate user data with invalid email
    user_data = fake_data_generator.generate_user()
    user_data['email'] = 'invalid-email-format'
    
    # Store in context
    context['registration_data'] = user_data
    
    # Fill registration form
    registration_page.register_user(user_data)


@when('I enter a weak password')
def enter_weak_password(registration_page: RegistrationPage, context: dict):
    """Enter weak password."""
    logger.info("Step: When I enter a weak password")
    
    # Generate user data with weak password
    user_data = fake_data_generator.generate_user()
    user_data['password'] = '123'  # Weak password
    
    # Store in context
    context['registration_data'] = user_data
    
    # Fill registration form
    registration_page.register_user(user_data)


# Then Steps

@then('I should see registration success message')
def verify_registration_success_message(registration_page: RegistrationPage):
    """Verify registration success message."""
    logger.info("Step: Then I should see registration success message")
    
    # Wait for success message
    registration_page.wait_for_timeout(2000)
    
    # Verify success
    assert registration_page.verify_registration_success(), \
        "Registration success message not displayed"


@then('I should receive a confirmation email')
def verify_confirmation_email(context: dict):
    """Verify confirmation email (placeholder)."""
    logger.info("Step: Then I should receive a confirmation email")
    
    # This is a placeholder - in real scenario, you would verify email
    # For now, we'll just log and pass
    logger.info("Email verification would happen here in real scenario")
    
    # Store verification status in context
    context['email_verified'] = True


@then(parsers.parse('I should see "{error_message}" error'))
def verify_specific_error_message(registration_page: RegistrationPage, error_message: str):
    """
    Verify specific error message.
    
    Args:
        error_message: Expected error message
    """
    logger.info(f"Step: Then I should see '{error_message}' error")
    
    # Wait for error message
    registration_page.wait_for_timeout(1000)
    
    # Check if error message is displayed
    assert registration_page.is_error_message_displayed(), "Error message not displayed"
    
    # Get actual error message
    actual_message = registration_page.get_error_message()
    
    # Verify error message contains expected text
    assert error_message.lower() in actual_message.lower(), \
        f"Expected '{error_message}' in error message, but got '{actual_message}'"


@then('I should see email validation error')
def verify_email_validation_error(registration_page: RegistrationPage):
    """Verify email validation error."""
    logger.info("Step: Then I should see email validation error")
    
    # Wait for error
    registration_page.wait_for_timeout(1000)
    
    # Check for email error or general error
    has_error = (
        registration_page.is_error_message_displayed() or
        registration_page.is_visible(registration_page.EMAIL_ERROR, timeout=2000)
    )
    
    assert has_error, "Email validation error not displayed"


@then('I should see password strength error')
def verify_password_strength_error(registration_page: RegistrationPage):
    """Verify password strength error."""
    logger.info("Step: Then I should see password strength error")
    
    # Wait for error
    registration_page.wait_for_timeout(1000)
    
    # Check for password error or general error
    has_error = (
        registration_page.is_error_message_displayed() or
        registration_page.is_visible(registration_page.PASSWORD_ERROR, timeout=2000)
    )
    
    assert has_error, "Password strength error not displayed"
