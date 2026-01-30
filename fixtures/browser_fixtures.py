"""
Browser Fixtures Module
Pytest fixtures for browser management
"""
import pytest
from typing import Generator
from playwright.sync_api import Browser, BrowserContext, Page
from utils.browser_manager import BrowserManager
from config.config import config
from utils.logger import Logger


logger = Logger.get_logger(__name__)


@pytest.fixture(scope='session')
def browser_manager() -> Generator[BrowserManager, None, None]:
    """
    Session-scoped browser manager fixture.
    
    Yields:
        BrowserManager instance
    """
    logger.info("Creating browser manager (session scope)")
    manager = BrowserManager()
    yield manager
    logger.info("Cleaning up browser manager")
    manager.cleanup()


@pytest.fixture(scope='function')
def browser(browser_manager: BrowserManager) -> Generator[Browser, None, None]:
    """
    Function-scoped browser fixture.
    
    Args:
        browser_manager: BrowserManager instance
        
    Yields:
        Browser instance
    """
    logger.info("Launching browser")
    browser = browser_manager.launch_browser()
    yield browser
    logger.info("Closing browser")
    browser_manager.close_browser()


@pytest.fixture(scope='function')
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """
    Function-scoped browser context fixture.
    
    Args:
        browser: Browser instance
        
    Yields:
        BrowserContext instance
    """
    logger.info("Creating browser context")
    
    # Create context with base URL
    ctx = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        ignore_https_errors=True,
        base_url=config.get_base_url()
    )
    
    # Configure video recording if enabled
    if config.video in ['on', 'retain-on-failure', 'on_failure']:
        ctx._impl_obj._options['record_video_dir'] = str(config.videos_dir)
    
    yield ctx
    
    logger.info("Closing browser context")
    ctx.close()


@pytest.fixture(scope='function')
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """
    Function-scoped page fixture.
    
    Args:
        context: BrowserContext instance
        
    Yields:
        Page instance
    """
    logger.info("Creating new page")
    
    page = context.new_page()
    page.set_default_timeout(config.get_timeout())
    
    yield page
    
    logger.info("Closing page")
    page.close()


@pytest.fixture(scope='session')
def base_url() -> str:
    """
    Session-scoped base URL fixture.
    
    Returns:
        Base URL from configuration
    """
    return config.get_base_url()
