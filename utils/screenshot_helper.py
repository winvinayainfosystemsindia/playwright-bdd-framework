"""
Screenshot Helper Module
Provides screenshot capture and management functionality
"""
import allure
from pathlib import Path
from datetime import datetime
from typing import Optional
from playwright.sync_api import Page
from config.config import config
from utils.logger import Logger


logger = Logger.get_logger(__name__)


class ScreenshotHelper:
    """
    Screenshot Helper class for capturing and managing screenshots.
    Integrates with Allure reporting.
    """
    
    @staticmethod
    def capture_screenshot(
        page: Page,
        name: Optional[str] = None,
        attach_to_allure: bool = True,
        full_page: bool = False
    ) -> Optional[Path]:
        """
        Capture screenshot of the current page.
        
        Args:
            page: Playwright Page instance
            name: Screenshot name (auto-generated if not provided)
            attach_to_allure: Whether to attach screenshot to Allure report
            full_page: Whether to capture full page screenshot
            
        Returns:
            Path to saved screenshot or None if failed
        """
        try:
            # Generate screenshot name
            if not name:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                name = f"screenshot_{timestamp}"
            
            # Ensure .png extension
            if not name.endswith('.png'):
                name = f"{name}.png"
            
            # Create screenshot path
            screenshot_path = config.screenshots_dir / name
            
            # Capture screenshot
            screenshot_bytes = page.screenshot(
                path=str(screenshot_path),
                full_page=full_page
            )
            
            logger.info(f"Screenshot captured: {screenshot_path}")
            
            # Attach to Allure report
            if attach_to_allure:
                allure.attach(
                    screenshot_bytes,
                    name=name,
                    attachment_type=allure.attachment_type.PNG
                )
                logger.debug(f"Screenshot attached to Allure report: {name}")
            
            return screenshot_path
            
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {str(e)}")
            return None
    
    @staticmethod
    def capture_element_screenshot(
        page: Page,
        selector: str,
        name: Optional[str] = None,
        attach_to_allure: bool = True
    ) -> Optional[Path]:
        """
        Capture screenshot of a specific element.
        
        Args:
            page: Playwright Page instance
            selector: Element selector
            name: Screenshot name
            attach_to_allure: Whether to attach to Allure report
            
        Returns:
            Path to saved screenshot or None if failed
        """
        try:
            # Generate screenshot name
            if not name:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                name = f"element_screenshot_{timestamp}"
            
            if not name.endswith('.png'):
                name = f"{name}.png"
            
            screenshot_path = config.screenshots_dir / name
            
            # Locate element and capture screenshot
            element = page.locator(selector)
            screenshot_bytes = element.screenshot(path=str(screenshot_path))
            
            logger.info(f"Element screenshot captured: {screenshot_path}")
            
            # Attach to Allure report
            if attach_to_allure:
                allure.attach(
                    screenshot_bytes,
                    name=name,
                    attachment_type=allure.attachment_type.PNG
                )
            
            return screenshot_path
            
        except Exception as e:
            logger.error(f"Failed to capture element screenshot: {str(e)}")
            return None
    
    @staticmethod
    def capture_on_failure(page: Page, test_name: str) -> Optional[Path]:
        """
        Capture screenshot on test failure.
        
        Args:
            page: Playwright Page instance
            test_name: Name of the failed test
            
        Returns:
            Path to saved screenshot or None if failed
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_name = f"FAILED_{test_name}_{timestamp}.png"
        
        logger.warning(f"Test failed, capturing screenshot: {screenshot_name}")
        
        return ScreenshotHelper.capture_screenshot(
            page=page,
            name=screenshot_name,
            attach_to_allure=True,
            full_page=True
        )
    
    @staticmethod
    def cleanup_old_screenshots(days: int = 7) -> None:
        """
        Clean up screenshots older than specified days.
        
        Args:
            days: Number of days to retain screenshots
        """
        try:
            current_time = datetime.now()
            screenshot_dir = config.screenshots_dir
            
            if not screenshot_dir.exists():
                return
            
            deleted_count = 0
            for screenshot_file in screenshot_dir.glob('*.png'):
                file_modified_time = datetime.fromtimestamp(screenshot_file.stat().st_mtime)
                age_days = (current_time - file_modified_time).days
                
                if age_days > days:
                    screenshot_file.unlink()
                    deleted_count += 1
            
            if deleted_count > 0:
                logger.info(f"Cleaned up {deleted_count} old screenshots (older than {days} days)")
                
        except Exception as e:
            logger.error(f"Failed to cleanup old screenshots: {str(e)}")
