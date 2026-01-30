"""
Browser Manager Module
Implements Factory pattern for browser management
"""
from typing import Optional, Dict, Any
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright
from config.config import config
from utils.logger import Logger


logger = Logger.get_logger(__name__)


class BrowserManager:
    """
    Browser Manager class implementing Factory pattern.
    Manages browser lifecycle and provides browser instances.
    """
    
    def __init__(self):
        """Initialize Browser Manager."""
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self._browser_type = config.browser
        self._headless = config.headless
        self._slow_mo = config.slow_mo
        
    def start_playwright(self) -> Playwright:
        """
        Start Playwright instance.
        
        Returns:
            Playwright instance
        """
        if not self.playwright:
            self.playwright = sync_playwright().start()
            logger.info("Playwright started successfully")
        return self.playwright
    
    def launch_browser(self, browser_type: Optional[str] = None, **kwargs) -> Browser:
        """
        Launch browser using Factory pattern.
        
        Args:
            browser_type: Browser type (chromium, firefox, webkit)
            **kwargs: Additional browser launch arguments
            
        Returns:
            Browser instance
        """
        if not self.playwright:
            self.start_playwright()
        
        browser_type = browser_type or self._browser_type
        
        # Default browser arguments
        launch_args = {
            'headless': kwargs.get('headless', self._headless),
            'slow_mo': kwargs.get('slow_mo', self._slow_mo),
            'args': kwargs.get('args', [
                '--start-maximized',
                '--disable-blink-features=AutomationControlled'
            ])
        }
        
        # Merge with custom kwargs
        launch_args.update({k: v for k, v in kwargs.items() if k not in ['headless', 'slow_mo', 'args']})
        
        # Factory pattern - select browser
        if browser_type.lower() == 'chromium':
            self.browser = self.playwright.chromium.launch(**launch_args)
            logger.info(f"Chromium browser launched (headless={launch_args['headless']})")
        elif browser_type.lower() == 'firefox':
            self.browser = self.playwright.firefox.launch(**launch_args)
            logger.info(f"Firefox browser launched (headless={launch_args['headless']})")
        elif browser_type.lower() == 'webkit':
            self.browser = self.playwright.webkit.launch(**launch_args)
            logger.info(f"WebKit browser launched (headless={launch_args['headless']})")
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")
        
        return self.browser
    
    def create_context(self, **kwargs) -> BrowserContext:
        """
        Create browser context with configuration.
        
        Args:
            **kwargs: Context options
            
        Returns:
            BrowserContext instance
        """
        if not self.browser:
            self.launch_browser()
        
        # Default context options
        context_options = {
            'viewport': kwargs.get('viewport', {'width': 1920, 'height': 1080}),
            'ignore_https_errors': kwargs.get('ignore_https_errors', True),
            'record_video_dir': None,
            'record_video_size': kwargs.get('record_video_size', {'width': 1920, 'height': 1080})
        }
        
        # Configure video recording based on settings
        if config.video in ['on', 'retain-on-failure', 'on_failure']:
            context_options['record_video_dir'] = str(config.videos_dir)
        
        # Merge with custom kwargs
        context_options.update({k: v for k, v in kwargs.items() if k not in context_options})
        
        self.context = self.browser.new_context(**context_options)
        logger.info("Browser context created with viewport: {}".format(context_options['viewport']))
        
        return self.context
    
    def create_page(self) -> Page:
        """
        Create a new page in the browser context.
        
        Returns:
            Page instance
        """
        if not self.context:
            self.create_context()
        
        self.page = self.context.new_page()
        
        # Set default timeout
        self.page.set_default_timeout(config.get_timeout())
        
        logger.info(f"New page created with timeout: {config.get_timeout()}ms")
        
        return self.page
    
    def get_browser(self) -> Browser:
        """
        Get current browser instance or create new one.
        
        Returns:
            Browser instance
        """
        if not self.browser:
            self.launch_browser()
        return self.browser
    
    def get_context(self) -> BrowserContext:
        """
        Get current browser context or create new one.
        
        Returns:
            BrowserContext instance
        """
        if not self.context:
            self.create_context()
        return self.context
    
    def get_page(self) -> Page:
        """
        Get current page or create new one.
        
        Returns:
            Page instance
        """
        if not self.page:
            self.create_page()
        return self.page
    
    def close_page(self) -> None:
        """Close current page."""
        if self.page:
            self.page.close()
            logger.info("Page closed")
            self.page = None
    
    def close_context(self) -> None:
        """Close browser context."""
        if self.context:
            self.context.close()
            logger.info("Browser context closed")
            self.context = None
            self.page = None
    
    def close_browser(self) -> None:
        """Close browser."""
        if self.browser:
            self.browser.close()
            logger.info("Browser closed")
            self.browser = None
            self.context = None
            self.page = None
    
    def stop_playwright(self) -> None:
        """Stop Playwright instance."""
        if self.playwright:
            self.playwright.stop()
            logger.info("Playwright stopped")
            self.playwright = None
    
    def cleanup(self) -> None:
        """Clean up all browser resources."""
        logger.info("Starting browser cleanup...")
        self.close_page()
        self.close_context()
        self.close_browser()
        self.stop_playwright()
        logger.info("Browser cleanup completed")
