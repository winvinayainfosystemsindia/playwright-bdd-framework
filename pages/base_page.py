"""
Base Page Module
Provides base page class with common page operations
"""
from typing import Optional, List
from playwright.sync_api import Page, Locator, expect
from config.config import config
from utils.logger import Logger
from utils.screenshot_helper import ScreenshotHelper


logger = Logger.get_logger(__name__)


class BasePage:
    """
    Base Page class containing common page operations.
    All page objects should inherit from this class.
    """
    
    def __init__(self, page: Page):
        """
        Initialize Base Page.
        
        Args:
            page: Playwright Page instance
        """
        self.page = page
        self.timeout = config.get_timeout()
        self.screenshot_helper = ScreenshotHelper()
    
    # Navigation Methods
    
    def navigate_to(self, url: str) -> None:
        """
        Navigate to specified URL.
        
        Args:
            url: URL to navigate to
        """
        try:
            logger.info(f"Navigating to: {url}")
            self.page.goto(url, wait_until='domcontentloaded', timeout=self.timeout)
            logger.info(f"Successfully navigated to: {url}")
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {str(e)}")
            self.screenshot_helper.capture_screenshot(self.page, f"navigation_error_{url.split('/')[-1]}")
            raise
    
    def get_current_url(self) -> str:
        """
        Get current page URL.
        
        Returns:
            Current URL
        """
        url = self.page.url
        logger.debug(f"Current URL: {url}")
        return url
    
    def get_title(self) -> str:
        """
        Get page title.
        
        Returns:
            Page title
        """
        title = self.page.title()
        logger.debug(f"Page title: {title}")
        return title
    
    def reload_page(self) -> None:
        """Reload current page."""
        logger.info("Reloading page")
        self.page.reload(wait_until='domcontentloaded')
    
    def go_back(self) -> None:
        """Navigate back in browser history."""
        logger.info("Navigating back")
        self.page.go_back(wait_until='domcontentloaded')
    
    def go_forward(self) -> None:
        """Navigate forward in browser history."""
        logger.info("Navigating forward")
        self.page.go_forward(wait_until='domcontentloaded')
    
    # Wait Methods
    
    def wait_for_element(self, selector: str, state: str = 'visible', timeout: Optional[int] = None) -> Locator:
        """
        Wait for element to reach specified state.
        
        Args:
            selector: Element selector
            state: Element state (visible, hidden, attached, detached)
            timeout: Custom timeout in milliseconds
            
        Returns:
            Locator instance
        """
        timeout = timeout or self.timeout
        try:
            logger.debug(f"Waiting for element: {selector} (state: {state})")
            locator = self.page.locator(selector)
            locator.wait_for(state=state, timeout=timeout)
            return locator
        except Exception as e:
            logger.error(f"Element not found: {selector} - {str(e)}")
            self.screenshot_helper.capture_screenshot(self.page, f"element_not_found")
            raise
    
    def wait_for_url(self, url: str, timeout: Optional[int] = None) -> None:
        """
        Wait for URL to match pattern.
        
        Args:
            url: URL pattern to wait for
            timeout: Custom timeout in milliseconds
        """
        timeout = timeout or self.timeout
        try:
            logger.debug(f"Waiting for URL: {url}")
            self.page.wait_for_url(url, timeout=timeout)
            logger.info(f"URL matched: {url}")
        except Exception as e:
            logger.error(f"URL did not match {url}: {str(e)}")
            raise
    
    def wait_for_load_state(self, state: str = 'load', timeout: Optional[int] = None) -> None:
        """
        Wait for page load state.
        
        Args:
            state: Load state (load, domcontentloaded, networkidle)
            timeout: Custom timeout in milliseconds
        """
        timeout = timeout or self.timeout
        logger.debug(f"Waiting for load state: {state}")
        self.page.wait_for_load_state(state, timeout=timeout)
    
    def wait_for_timeout(self, timeout: int) -> None:
        """
        Wait for specified timeout.
        
        Args:
            timeout: Timeout in milliseconds
        """
        logger.debug(f"Waiting for {timeout}ms")
        self.page.wait_for_timeout(timeout)
    
    # Element Interaction Methods
    
    def click(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Click on element.
        
        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds
        """
        timeout = timeout or self.timeout
        try:
            logger.info(f"Clicking element: {selector}")
            locator = self.page.locator(selector)
            locator.click(timeout=timeout)
            logger.info(f"Successfully clicked: {selector}")
        except Exception as e:
            logger.error(f"Failed to click {selector}: {str(e)}")
            self.screenshot_helper.capture_screenshot(self.page, f"click_error")
            raise
    
    def double_click(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Double click on element.
        
        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds
        """
        timeout = timeout or self.timeout
        logger.info(f"Double clicking element: {selector}")
        self.page.locator(selector).dblclick(timeout=timeout)
    
    def fill(self, selector: str, value: str, timeout: Optional[int] = None) -> None:
        """
        Fill input field with value.
        
        Args:
            selector: Element selector
            value: Value to fill
            timeout: Custom timeout in milliseconds
        """
        timeout = timeout or self.timeout
        try:
            logger.info(f"Filling element {selector} with value: {value}")
            locator = self.page.locator(selector)
            locator.fill(value, timeout=timeout)
            logger.info(f"Successfully filled: {selector}")
        except Exception as e:
            logger.error(f"Failed to fill {selector}: {str(e)}")
            self.screenshot_helper.capture_screenshot(self.page, f"fill_error")
            raise
    
    def type(self, selector: str, text: str, delay: int = 100, timeout: Optional[int] = None) -> None:
        """
        Type text into element with delay.
        
        Args:
            selector: Element selector
            text: Text to type
            delay: Delay between keystrokes in milliseconds
            timeout: Custom timeout in milliseconds
        """
        timeout = timeout or self.timeout
        logger.info(f"Typing into element: {selector}")
        self.page.locator(selector).type(text, delay=delay, timeout=timeout)
    
    def clear(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Clear input field.
        
        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds
        """
        timeout = timeout or self.timeout
        logger.info(f"Clearing element: {selector}")
        self.page.locator(selector).clear(timeout=timeout)
    
    def select_option(self, selector: str, value: str, timeout: Optional[int] = None) -> None:
        """
        Select option from dropdown.
        
        Args:
            selector: Element selector
            value: Option value to select
            timeout: Custom timeout in milliseconds
        """
        timeout = timeout or self.timeout
        logger.info(f"Selecting option {value} in {selector}")
        self.page.locator(selector).select_option(value, timeout=timeout)
    
    def check(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Check checkbox or radio button.
        
        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds
        """
        timeout = timeout or self.timeout
        logger.info(f"Checking element: {selector}")
        self.page.locator(selector).check(timeout=timeout)
    
    def uncheck(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Uncheck checkbox.
        
        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds
        """
        timeout = timeout or self.timeout
        logger.info(f"Unchecking element: {selector}")
        self.page.locator(selector).uncheck(timeout=timeout)
    
    def hover(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        Hover over element.
        
        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds
        """
        timeout = timeout or self.timeout
        logger.info(f"Hovering over element: {selector}")
        self.page.locator(selector).hover(timeout=timeout)
    
    # Element Query Methods
    
    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """
        Get text content of element.
        
        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds
            
        Returns:
            Element text content
        """
        timeout = timeout or self.timeout
        text = self.page.locator(selector).text_content(timeout=timeout)
        logger.debug(f"Text from {selector}: {text}")
        return text or ""
    
    def get_attribute(self, selector: str, attribute: str, timeout: Optional[int] = None) -> Optional[str]:
        """
        Get element attribute value.
        
        Args:
            selector: Element selector
            attribute: Attribute name
            timeout: Custom timeout in milliseconds
            
        Returns:
            Attribute value
        """
        timeout = timeout or self.timeout
        value = self.page.locator(selector).get_attribute(attribute, timeout=timeout)
        logger.debug(f"Attribute {attribute} from {selector}: {value}")
        return value
    
    def is_visible(self, selector: str, timeout: Optional[int] = None) -> bool:
        """
        Check if element is visible.
        
        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds
            
        Returns:
            True if visible, False otherwise
        """
        timeout = timeout or self.timeout
        try:
            visible = self.page.locator(selector).is_visible(timeout=timeout)
            logger.debug(f"Element {selector} visible: {visible}")
            return visible
        except:
            return False
    
    def is_enabled(self, selector: str, timeout: Optional[int] = None) -> bool:
        """
        Check if element is enabled.
        
        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds
            
        Returns:
            True if enabled, False otherwise
        """
        timeout = timeout or self.timeout
        enabled = self.page.locator(selector).is_enabled(timeout=timeout)
        logger.debug(f"Element {selector} enabled: {enabled}")
        return enabled
    
    def is_checked(self, selector: str, timeout: Optional[int] = None) -> bool:
        """
        Check if checkbox/radio is checked.
        
        Args:
            selector: Element selector
            timeout: Custom timeout in milliseconds
            
        Returns:
            True if checked, False otherwise
        """
        timeout = timeout or self.timeout
        checked = self.page.locator(selector).is_checked(timeout=timeout)
        logger.debug(f"Element {selector} checked: {checked}")
        return checked
    
    def get_element_count(self, selector: str) -> int:
        """
        Get count of elements matching selector.
        
        Args:
            selector: Element selector
            
        Returns:
            Number of matching elements
        """
        count = self.page.locator(selector).count()
        logger.debug(f"Element count for {selector}: {count}")
        return count
    
    # Screenshot Methods
    
    def capture_screenshot(self, name: Optional[str] = None) -> None:
        """
        Capture screenshot of current page.
        
        Args:
            name: Screenshot name
        """
        self.screenshot_helper.capture_screenshot(self.page, name)
    
    def capture_element_screenshot(self, selector: str, name: Optional[str] = None) -> None:
        """
        Capture screenshot of specific element.
        
        Args:
            selector: Element selector
            name: Screenshot name
        """
        self.screenshot_helper.capture_element_screenshot(self.page, selector, name)
    
    # Assertion Methods
    
    def assert_url_contains(self, expected: str) -> None:
        """
        Assert that URL contains expected text.
        
        Args:
            expected: Expected text in URL
        """
        logger.info(f"Asserting URL contains: {expected}")
        expect(self.page).to_have_url(expected, timeout=self.timeout)
    
    def assert_title_contains(self, expected: str) -> None:
        """
        Assert that title contains expected text.
        
        Args:
            expected: Expected text in title
        """
        logger.info(f"Asserting title contains: {expected}")
        expect(self.page).to_have_title(expected, timeout=self.timeout)
    
    def assert_element_visible(self, selector: str) -> None:
        """
        Assert that element is visible.
        
        Args:
            selector: Element selector
        """
        logger.info(f"Asserting element visible: {selector}")
        expect(self.page.locator(selector)).to_be_visible(timeout=self.timeout)
    
    def assert_element_text(self, selector: str, expected: str) -> None:
        """
        Assert element text matches expected.
        
        Args:
            selector: Element selector
            expected: Expected text
        """
        logger.info(f"Asserting element {selector} has text: {expected}")
        expect(self.page.locator(selector)).to_have_text(expected, timeout=self.timeout)
