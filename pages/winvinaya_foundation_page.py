"""
WinVinaya Foundation Page Module
Page object for WinVinaya Foundation website
"""
from pages.base_page import BasePage
from utils.logger import Logger


logger = Logger.get_logger(__name__)


class WinVinayaFoundationPage(BasePage):
    """
    Page Object for WinVinaya Foundation website.
    Contains locators and methods for interacting with the page.
    """
    
    # Page URL
    URL = "https://winvinayafoundation.org"
    
    # Locators
    MAIN_HEADING = "h1"
    LOGO = "img[alt*='WinVinaya'], img[alt*='logo']"
    NAVIGATION = "nav"
    
    def __init__(self, page):
        """
        Initialize WinVinaya Foundation Page.
        
        Args:
            page: Playwright Page instance
        """
        super().__init__(page)
        logger.info("WinVinaya Foundation Page initialized")
    
    def navigate(self) -> None:
        """Navigate to WinVinaya Foundation website."""
        logger.info(f"Navigating to WinVinaya Foundation: {self.URL}")
        self.navigate_to(self.URL)
        self.wait_for_load_state('domcontentloaded')
        logger.info("Successfully navigated to WinVinaya Foundation")
    
    def is_page_loaded(self) -> bool:
        """
        Check if page is loaded successfully.
        
        Returns:
            True if page is loaded, False otherwise
        """
        try:
            # Wait for content to be loaded
            self.wait_for_load_state('domcontentloaded', timeout=10000)
            title = self.get_title()
            logger.info(f"Page loaded. Current title: '{title}'")
            return True
        except Exception as e:
            logger.error(f"Page not loaded properly: {str(e)}")
            return False
    
    def get_page_title(self) -> str:
        """
        Get the page title.
        
        Returns:
            Page title as string
        """
        # Wait for title to be populated
        self.page.wait_for_function("document.title !== ''", timeout=5000)
        title = self.get_title()
        logger.info(f"Page title: {title}")
        return title
    
    def is_page_title_present(self) -> bool:
        """
        Check if page title is present and not empty.
        
        Returns:
            True if title is present, False otherwise
        """
        title = self.get_page_title()
        is_present = bool(title and len(title.strip()) > 0)
        logger.info(f"Page title present: {is_present}")
        return is_present
    
    def verify_title_contains(self, expected_text: str) -> bool:
        """
        Verify that page title contains expected text.
        
        Args:
            expected_text: Text that should be in the title
            
        Returns:
            True if title contains expected text, False otherwise
        """
        title = self.get_page_title()
        contains = expected_text.lower() in title.lower()
        logger.info(f"Title '{title}' contains '{expected_text}': {contains}")
        return contains
    
    def is_main_heading_visible(self) -> bool:
        """
        Check if main heading is visible.
        
        Returns:
            True if visible, False otherwise
        """
        try:
            return self.is_visible(self.MAIN_HEADING, timeout=5000)
        except:
            return False
    
    def get_main_heading_text(self) -> str:
        """
        Get main heading text. Handles multiple H1 elements.
        
        Returns:
            Joined text of all H1 elements
        """
        try:
            headings = self.page.locator(self.MAIN_HEADING)
            count = headings.count()
            texts = []
            for i in range(count):
                texts.append(headings.nth(i).inner_text())
            
            combined_text = " ".join(texts)
            logger.info(f"Combined H1 text: {combined_text}")
            return combined_text
        except Exception as e:
            logger.error(f"Failed to get main heading text: {str(e)}")
            return ""
