"""
Root Conftest Module
Main pytest configuration with hooks and fixtures
"""
import pytest
import allure
import os
from pathlib import Path
from datetime import datetime
from typing import Generator
from playwright.sync_api import Page
from pytest_bdd import given, when, then
from config.config import config as project_config
from utils.logger import Logger
from utils.screenshot_helper import ScreenshotHelper
from utils.report_helper import ReportHelper
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.registration_page import RegistrationPage
from pages.winvinaya_foundation_page import WinVinayaFoundationPage


logger = Logger.get_logger(__name__)


# Global list to store test results for CSV reporting
test_results = []


# List of plugins to load
pytest_plugins = [
    "fixtures.browser_fixtures"
]


# ============================================================================
# Pytest Configuration Hooks
# ============================================================================

def pytest_configure(config):
    """
    Pytest configuration hook - called before test collection.
    
    Args:
        config: Pytest config object
    """
    logger.info("=" * 80)
    logger.info("PYTEST CONFIGURATION STARTED")
    logger.info("=" * 80)
    
    # Create necessary directories
    project_config.reports_dir.mkdir(parents=True, exist_ok=True)
    project_config.screenshots_dir.mkdir(parents=True, exist_ok=True)
    project_config.videos_dir.mkdir(parents=True, exist_ok=True)
    project_config.allure_results_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Environment: {project_config.environment}")
    logger.info(f"Browser: {project_config.browser}")
    logger.info(f"Base URL: {project_config.get_base_url()}")
    logger.info(f"Headless: {project_config.headless}")
    logger.info(f"Reports Directory: {project_config.reports_dir}")
    
    # Add environment info to Allure report
    env_info = {
        'Environment': project_config.environment,
        'Browser': project_config.browser,
        'Base_URL': project_config.get_base_url(),
        'Headless': str(project_config.headless),
        'Timeout': str(project_config.timeout),
        'Python_Version': os.sys.version.split()[0],
        'Execution_Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    ReportHelper.add_environment_info(env_info)
    logger.info("Pytest configuration completed")


def pytest_collection_modifyitems(config, items):
    """
    Modify test items after collection.
    
    Args:
        config: Pytest config object
        items: List of test items
    """
    logger.info(f"Collected {len(items)} test items")
    
    # Add markers to tests based on their names
    for item in items:
        # Add feature markers based on file location
        if 'login' in str(item.fspath):
            item.add_marker(pytest.mark.login)
        elif 'registration' in str(item.fspath):
            item.add_marker(pytest.mark.registration)


# ============================================================================
# BDD Hooks
# ============================================================================

# Note: pytest-bdd hooks are handled automatically by the framework


# ============================================================================
# Test Execution Hooks
# ============================================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results and take screenshots on failure.
    
    Args:
        item: Test item
        call: Test call info
    """
    outcome = yield
    report = outcome.get_result()
    
    # Only process on test call (not setup/teardown)
    if report.when == 'call':
        # Get page fixture if available
        if 'page' in item.fixturenames:
            page = item.funcargs.get('page')
            
            if report.failed and page:
                # Capture screenshot on failure
                logger.error(f"Test FAILED: {item.name}")
                
                try:
                    screenshot_helper = ScreenshotHelper()
                    screenshot_path = screenshot_helper.capture_on_failure(page, item.name)
                    
                    if screenshot_path:
                        logger.info(f"Failure screenshot saved: {screenshot_path}")
                        
                        # Attach to Allure report
                        with open(screenshot_path, 'rb') as f:
                            allure.attach(
                                f.read(),
                                name=f"failure_{item.name}",
                                attachment_type=allure.attachment_type.PNG
                            )
                except Exception as e:
                    logger.error(f"Failed to capture failure screenshot: {str(e)}")
            
            elif report.passed:
                logger.info(f"Test PASSED: {item.name}")

        # Collect result for CSV report
        test_results.append({
            'name': item.name,
            'status': report.outcome,
            'duration': report.duration,
            'error': str(report.longrepr) if report.failed else ""
        })


@pytest.fixture(scope='function', autouse=True)
def test_logger(request):
    """
    Auto-use fixture to log test start and end.
    
    Args:
        request: Pytest request object
    """
    test_name = request.node.name
    logger.info(f"Starting test: {test_name}")
    
    yield
    
    logger.info(f"Finished test: {test_name}")


# ============================================================================
# Page Object Fixtures
# ============================================================================

@pytest.fixture(scope='function')
def login_page(page: Page) -> LoginPage:
    """
    Function-scoped LoginPage fixture.
    
    Args:
        page: Page instance
        
    Returns:
        LoginPage instance
    """
    return LoginPage(page)


@pytest.fixture(scope='function')
def home_page(page: Page) -> HomePage:
    """
    Function-scoped HomePage fixture.
    
    Args:
        page: Page instance
        
    Returns:
        HomePage instance
    """
    return HomePage(page)


@pytest.fixture(scope='function')
def registration_page(page: Page) -> RegistrationPage:
    """
    Function-scoped RegistrationPage fixture.
    
    Args:
        page: Page instance
        
    Returns:
        RegistrationPage instance
    """
    return RegistrationPage(page)


@pytest.fixture(scope='function')
def winvinaya_foundation_page(page: Page) -> WinVinayaFoundationPage:
    """
    Function-scoped WinVinayaFoundationPage fixture.
    
    Args:
        page: Page instance
        
    Returns:
        WinVinayaFoundationPage instance
    """
    return WinVinayaFoundationPage(page)


# ============================================================================
# Data Fixtures
# ============================================================================

@pytest.fixture(scope='session')
def test_data():
    """
    Session-scoped test data fixture.
    
    Returns:
        Test data from configuration
    """
    return project_config.test_data


@pytest.fixture(scope='function')
def valid_user():
    """
    Function-scoped valid user fixture.
    
    Returns:
        Valid user data
    """
    return project_config.get_test_user('valid')


@pytest.fixture(scope='function')
def invalid_user():
    """
    Function-scoped invalid user fixture.
    
    Returns:
        Invalid user data
    """
    return project_config.get_test_user('invalid')


# ============================================================================
# Cleanup Hooks
# ============================================================================

def pytest_sessionfinish(session, exitstatus):
    """
    Hook called after test session finishes.
    
    Args:
        session: Pytest session
        exitstatus: Exit status code
    """
    logger.info("=" * 80)
    logger.info("TEST SESSION COMPLETED")
    logger.info(f"Exit Status: {exitstatus}")
    logger.info("=" * 80)
    
    # Generate CSV report
    if test_results:
        csv_path = ReportHelper.generate_csv_report(test_results)
        if csv_path:
            logger.info(f"Final CSV report created at: {csv_path}")
    
    # Clean up old screenshots (older than 7 days)
    try:
        ScreenshotHelper.cleanup_old_screenshots(days=7)
    except Exception as e:
        logger.error(f"Failed to cleanup old screenshots: {str(e)}")
