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
from config.config import config
from utils.logger import Logger
from utils.screenshot_helper import ScreenshotHelper
from utils.report_helper import ReportHelper
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.registration_page import RegistrationPage


logger = Logger.get_logger(__name__)


# ============================================================================
# Pytest Configuration Hooks
# ============================================================================

def pytest_configure(config_obj):
    """
    Pytest configuration hook - called before test collection.
    
    Args:
        config_obj: Pytest config object
    """
    logger.info("=" * 80)
    logger.info("PYTEST CONFIGURATION STARTED")
    logger.info("=" * 80)
    
    # Create necessary directories
    config.reports_dir.mkdir(parents=True, exist_ok=True)
    config.screenshots_dir.mkdir(parents=True, exist_ok=True)
    config.videos_dir.mkdir(parents=True, exist_ok=True)
    config.allure_results_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Environment: {config.environment}")
    logger.info(f"Browser: {config.browser}")
    logger.info(f"Base URL: {config.get_base_url()}")
    logger.info(f"Headless: {config.headless}")
    logger.info(f"Reports Directory: {config.reports_dir}")
    
    # Add environment info to Allure report
    env_info = {
        'Environment': config.environment,
        'Browser': config.browser,
        'Base_URL': config.get_base_url(),
        'Headless': str(config.headless),
        'Timeout': str(config.timeout),
        'Python_Version': os.sys.version.split()[0],
        'Execution_Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    ReportHelper.add_environment_info(env_info)
    logger.info("Pytest configuration completed")


def pytest_collection_modifyitems(config_obj, items):
    """
    Modify test items after collection.
    
    Args:
        config_obj: Pytest config object
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

@pytest.fixture
def pytest_bdd_before_scenario(request):
    """
    Hook called before each BDD scenario.
    
    Args:
        request: Pytest request object
    """
    scenario_name = request.node.name
    logger.info("=" * 80)
    logger.info(f"SCENARIO STARTED: {scenario_name}")
    logger.info("=" * 80)


@pytest.fixture
def pytest_bdd_after_scenario(request, page: Page):
    """
    Hook called after each BDD scenario.
    
    Args:
        request: Pytest request object
        page: Page instance
    """
    scenario_name = request.node.name
    logger.info("=" * 80)
    logger.info(f"SCENARIO COMPLETED: {scenario_name}")
    logger.info("=" * 80)


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
    return config.test_data


@pytest.fixture(scope='function')
def valid_user():
    """
    Function-scoped valid user fixture.
    
    Returns:
        Valid user data
    """
    return config.get_test_user('valid')


@pytest.fixture(scope='function')
def invalid_user():
    """
    Function-scoped invalid user fixture.
    
    Returns:
        Invalid user data
    """
    return config.get_test_user('invalid')


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
    
    # Clean up old screenshots (older than 7 days)
    try:
        ScreenshotHelper.cleanup_old_screenshots(days=7)
    except Exception as e:
        logger.error(f"Failed to cleanup old screenshots: {str(e)}")
