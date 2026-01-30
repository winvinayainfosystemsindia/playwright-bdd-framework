"""
Registration Page Module
Page Object Model for Registration page
"""
from typing import Dict
from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.logger import Logger


logger = Logger.get_logger(__name__)


class RegistrationPage(BasePage):
    """Registration Page Object class."""
    
    # Locators
    FIRST_NAME_INPUT = "#firstName"
    LAST_NAME_INPUT = "#lastName"
    EMAIL_INPUT = "#email"
    PASSWORD_INPUT = "#password"
    CONFIRM_PASSWORD_INPUT = "#confirmPassword"
    PHONE_INPUT = "#phone"
    ADDRESS_INPUT = "#address"
    TERMS_CHECKBOX = "#terms"
    REGISTER_BUTTON = "button[type='submit']"
    SUCCESS_MESSAGE = ".success-message"
    ERROR_MESSAGE = ".error-message"
    EMAIL_ERROR = "#email-error"
    PASSWORD_ERROR = "#password-error"
    LOGIN_LINK = "a[href*='login']"
    
    def __init__(self, page: Page):
        """
        Initialize Registration Page.
        
        Args:
            page: Playwright Page instance
        """
        super().__init__(page)
        self.url = f"{self.page.context.browser.contexts[0]._impl_obj._options.get('baseURL', 'https://example.com')}/register"
    
    def navigate(self) -> None:
        """Navigate to registration page."""
        logger.info("Navigating to registration page")
        self.navigate_to(self.url)
    
    def enter_first_name(self, first_name: str) -> None:
        """
        Enter first name.
        
        Args:
            first_name: First name
        """
        logger.info(f"Entering first name: {first_name}")
        self.fill(self.FIRST_NAME_INPUT, first_name)
    
    def enter_last_name(self, last_name: str) -> None:
        """
        Enter last name.
        
        Args:
            last_name: Last name
        """
        logger.info(f"Entering last name: {last_name}")
        self.fill(self.LAST_NAME_INPUT, last_name)
    
    def enter_email(self, email: str) -> None:
        """
        Enter email address.
        
        Args:
            email: Email address
        """
        logger.info(f"Entering email: {email}")
        self.fill(self.EMAIL_INPUT, email)
    
    def enter_password(self, password: str) -> None:
        """
        Enter password.
        
        Args:
            password: Password
        """
        logger.info("Entering password")
        self.fill(self.PASSWORD_INPUT, password)
    
    def enter_confirm_password(self, password: str) -> None:
        """
        Enter confirm password.
        
        Args:
            password: Confirm password
        """
        logger.info("Entering confirm password")
        self.fill(self.CONFIRM_PASSWORD_INPUT, password)
    
    def enter_phone(self, phone: str) -> None:
        """
        Enter phone number.
        
        Args:
            phone: Phone number
        """
        logger.info(f"Entering phone: {phone}")
        self.fill(self.PHONE_INPUT, phone)
    
    def enter_address(self, address: str) -> None:
        """
        Enter address.
        
        Args:
            address: Address
        """
        logger.info(f"Entering address: {address}")
        self.fill(self.ADDRESS_INPUT, address)
    
    def accept_terms(self) -> None:
        """Accept terms and conditions."""
        logger.info("Accepting terms and conditions")
        self.check(self.TERMS_CHECKBOX)
    
    def click_register_button(self) -> None:
        """Click register button."""
        logger.info("Clicking register button")
        self.click(self.REGISTER_BUTTON)
    
    def register_user(self, user_data: Dict[str, str]) -> None:
        """
        Register user with provided data.
        
        Args:
            user_data: Dictionary containing user registration data
        """
        logger.info(f"Registering user with email: {user_data.get('email')}")
        
        if 'first_name' in user_data:
            self.enter_first_name(user_data['first_name'])
        
        if 'last_name' in user_data:
            self.enter_last_name(user_data['last_name'])
        
        if 'email' in user_data:
            self.enter_email(user_data['email'])
        
        if 'password' in user_data:
            self.enter_password(user_data['password'])
            # Confirm password with same password if not provided
            confirm_pwd = user_data.get('confirm_password', user_data['password'])
            self.enter_confirm_password(confirm_pwd)
        
        if 'phone' in user_data:
            self.enter_phone(user_data['phone'])
        
        if 'address' in user_data:
            self.enter_address(user_data['address'])
        
        # Accept terms by default
        if user_data.get('accept_terms', True):
            self.accept_terms()
    
    def submit_registration_form(self) -> None:
        """Submit registration form."""
        logger.info("Submitting registration form")
        self.click_register_button()
    
    def get_success_message(self) -> str:
        """
        Get success message text.
        
        Returns:
            Success message text
        """
        logger.info("Getting success message")
        return self.get_text(self.SUCCESS_MESSAGE)
    
    def get_error_message(self) -> str:
        """
        Get error message text.
        
        Returns:
            Error message text
        """
        logger.info("Getting error message")
        return self.get_text(self.ERROR_MESSAGE)
    
    def get_email_error(self) -> str:
        """
        Get email field error message.
        
        Returns:
            Email error message
        """
        return self.get_text(self.EMAIL_ERROR)
    
    def get_password_error(self) -> str:
        """
        Get password field error message.
        
        Returns:
            Password error message
        """
        return self.get_text(self.PASSWORD_ERROR)
    
    def is_success_message_displayed(self) -> bool:
        """
        Check if success message is displayed.
        
        Returns:
            True if success message is visible
        """
        return self.is_visible(self.SUCCESS_MESSAGE, timeout=5000)
    
    def is_error_message_displayed(self) -> bool:
        """
        Check if error message is displayed.
        
        Returns:
            True if error message is visible
        """
        return self.is_visible(self.ERROR_MESSAGE, timeout=5000)
    
    def verify_registration_success(self) -> bool:
        """
        Verify registration was successful.
        
        Returns:
            True if registration successful
        """
        logger.info("Verifying registration success")
        try:
            # Check for success message or redirect
            if self.is_success_message_displayed():
                logger.info("Registration successful - success message displayed")
                return True
            
            # Check if redirected to login or dashboard
            current_url = self.get_current_url()
            if 'login' in current_url.lower() or 'dashboard' in current_url.lower():
                logger.info("Registration successful - redirected")
                return True
            
            return False
        except Exception as e:
            logger.error(f"Registration verification failed: {str(e)}")
            return False
    
    def click_login_link(self) -> None:
        """Click login link."""
        logger.info("Clicking login link")
        self.click(self.LOGIN_LINK)
    
    def is_on_registration_page(self) -> bool:
        """
        Verify if currently on registration page.
        
        Returns:
            True if on registration page
        """
        current_url = self.get_current_url()
        return 'register' in current_url.lower() or 'signup' in current_url.lower()
