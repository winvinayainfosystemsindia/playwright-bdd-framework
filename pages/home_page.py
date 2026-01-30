"""
Home Page Module
Page Object Model for Home/Dashboard page
"""
from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.logger import Logger


logger = Logger.get_logger(__name__)


class HomePage(BasePage):
    """Home Page Object class."""
    
    # Locators
    WELCOME_MESSAGE = ".welcome-message"
    USER_PROFILE = "#user-profile"
    LOGOUT_BUTTON = "button[data-testid='logout']"
    NAVIGATION_MENU = ".nav-menu"
    SEARCH_BOX = "#search"
    NOTIFICATIONS_ICON = ".notifications-icon"
    SETTINGS_LINK = "a[href*='settings']"
    PROFILE_DROPDOWN = ".profile-dropdown"
    USER_NAME = ".user-name"
    
    def __init__(self, page: Page):
        """
        Initialize Home Page.
        
        Args:
            page: Playwright Page instance
        """
        super().__init__(page)
        self.url = f"{self.page.context.browser.contexts[0]._impl_obj._options.get('baseURL', 'https://example.com')}/dashboard"
    
    def navigate(self) -> None:
        """Navigate to home page."""
        logger.info("Navigating to home page")
        self.navigate_to(self.url)
    
    def get_welcome_message(self) -> str:
        """
        Get welcome message text.
        
        Returns:
            Welcome message text
        """
        logger.info("Getting welcome message")
        return self.get_text(self.WELCOME_MESSAGE)
    
    def is_welcome_message_displayed(self) -> bool:
        """
        Check if welcome message is displayed.
        
        Returns:
            True if welcome message is visible
        """
        return self.is_visible(self.WELCOME_MESSAGE, timeout=10000)
    
    def click_user_profile(self) -> None:
        """Click user profile."""
        logger.info("Clicking user profile")
        self.click(self.USER_PROFILE)
    
    def click_logout_button(self) -> None:
        """Click logout button."""
        logger.info("Clicking logout button")
        self.click(self.LOGOUT_BUTTON)
    
    def logout(self) -> None:
        """
        Perform logout action.
        Opens profile dropdown and clicks logout.
        """
        logger.info("Logging out")
        try:
            # Try to click profile dropdown first
            if self.is_visible(self.PROFILE_DROPDOWN, timeout=2000):
                self.click(self.PROFILE_DROPDOWN)
                self.wait_for_timeout(500)
        except:
            pass
        
        self.click_logout_button()
        logger.info("Logout completed")
    
    def is_logged_in(self) -> bool:
        """
        Check if user is logged in.
        
        Returns:
            True if user is logged in
        """
        try:
            return self.is_visible(self.USER_PROFILE, timeout=5000)
        except:
            return False
    
    def get_user_name(self) -> str:
        """
        Get logged in user name.
        
        Returns:
            User name text
        """
        logger.info("Getting user name")
        return self.get_text(self.USER_NAME)
    
    def search(self, query: str) -> None:
        """
        Perform search.
        
        Args:
            query: Search query
        """
        logger.info(f"Searching for: {query}")
        self.fill(self.SEARCH_BOX, query)
        self.page.keyboard.press("Enter")
    
    def click_notifications(self) -> None:
        """Click notifications icon."""
        logger.info("Clicking notifications icon")
        self.click(self.NOTIFICATIONS_ICON)
    
    def click_settings(self) -> None:
        """Click settings link."""
        logger.info("Clicking settings link")
        self.click(self.SETTINGS_LINK)
    
    def is_on_home_page(self) -> bool:
        """
        Verify if currently on home page.
        
        Returns:
            True if on home page
        """
        current_url = self.get_current_url()
        return 'dashboard' in current_url.lower() or 'home' in current_url.lower()
    
    def verify_successful_login(self) -> bool:
        """
        Verify successful login by checking multiple elements.
        
        Returns:
            True if login verification successful
        """
        logger.info("Verifying successful login")
        try:
            # Check if on home page
            if not self.is_on_home_page():
                logger.warning("Not on home page")
                return False
            
            # Check if user profile is visible
            if not self.is_visible(self.USER_PROFILE, timeout=5000):
                logger.warning("User profile not visible")
                return False
            
            logger.info("Login verification successful")
            return True
        except Exception as e:
            logger.error(f"Login verification failed: {str(e)}")
            return False
