"""
Login Page Module
Page Object Model for Login page
"""
from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.logger import Logger


logger = Logger.get_logger(__name__)


class LoginPage(BasePage):
    """Login Page Object class."""
    
    # Locators
    EMAIL_INPUT = "#email"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button[type='submit']"
    ERROR_MESSAGE = ".error-message"
    FORGOT_PASSWORD_LINK = "a[href*='forgot-password']"
    REMEMBER_ME_CHECKBOX = "#remember-me"
    SIGNUP_LINK = "a[href*='signup']"
    
    def __init__(self, page: Page):
        """
        Initialize Login Page.
        
        Args:
            page: Playwright Page instance
        """
        super().__init__(page)
        self.url = f"{self.page.context.browser.contexts[0]._impl_obj._options.get('baseURL', 'https://example.com')}/login"
    
    def navigate(self) -> None:
        """Navigate to login page."""
        logger.info("Navigating to login page")
        self.navigate_to(self.url)
    
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
    
    def click_login_button(self) -> None:
        """Click login button."""
        logger.info("Clicking login button")
        self.click(self.LOGIN_BUTTON)
    
    def login(self, email: str, password: str) -> None:
        """
        Perform login with credentials.
        
        Args:
            email: Email address
            password: Password
        """
        logger.info(f"Logging in with email: {email}")
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
    
    def get_error_message(self) -> str:
        """
        Get error message text.
        
        Returns:
            Error message text
        """
        logger.info("Getting error message")
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_error_message_displayed(self) -> bool:
        """
        Check if error message is displayed.
        
        Returns:
            True if error message is visible
        """
        return self.is_visible(self.ERROR_MESSAGE, timeout=5000)
    
    def is_login_successful(self) -> bool:
        """
        Check if login was successful by verifying URL change.
        
        Returns:
            True if login successful
        """
        try:
            self.wait_for_url("**/dashboard", timeout=10000)
            logger.info("Login successful - redirected to dashboard")
            return True
        except:
            logger.warning("Login failed - not redirected to dashboard")
            return False
    
    def click_forgot_password(self) -> None:
        """Click forgot password link."""
        logger.info("Clicking forgot password link")
        self.click(self.FORGOT_PASSWORD_LINK)
    
    def click_remember_me(self) -> None:
        """Click remember me checkbox."""
        logger.info("Clicking remember me checkbox")
        self.check(self.REMEMBER_ME_CHECKBOX)
    
    def click_signup_link(self) -> None:
        """Click signup link."""
        logger.info("Clicking signup link")
        self.click(self.SIGNUP_LINK)
    
    def is_on_login_page(self) -> bool:
        """
        Verify if currently on login page.
        
        Returns:
            True if on login page
        """
        current_url = self.get_current_url()
        return 'login' in current_url.lower()
