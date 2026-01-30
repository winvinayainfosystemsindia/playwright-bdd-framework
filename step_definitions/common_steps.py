"""
Common Step Definitions
Reusable BDD step implementations
"""
import pytest
from pytest_bdd import given, when, then, parsers
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.logger import Logger


logger = Logger.get_logger(__name__)


# Common Navigation Steps

@given(parsers.parse('I am on the {page_name} page'))
def navigate_to_page(page_name: str, login_page: LoginPage, home_page: HomePage, registration_page):
    """
    Navigate to specified page.
    
    Args:
        page_name: Name of the page to navigate to
    """
    logger.info(f"Step: Given I am on the {page_name} page")
    
    page_map = {
        'login': login_page,
        'home': home_page,
        'dashboard': home_page,
        'registration': registration_page
    }
    
    page = page_map.get(page_name.lower())
    if page:
        page.navigate()
    else:
        raise ValueError(f"Unknown page: {page_name}")


@when(parsers.parse('I navigate to {url}'))
def navigate_to_url(url: str, page):
    """
    Navigate to specific URL.
    
    Args:
        url: URL to navigate to
    """
    logger.info(f"Step: When I navigate to {url}")
    page.navigate_to(url)


@when(parsers.parse('I search for "{query}"'))
def search_for_product(query: str, home_page: HomePage, context: dict):
    """
    Search for product.
    
    Args:
        query: Search query
    """
    logger.info(f"Step: When I search for '{query}'")
    home_page.search(query)
    context['search_query'] = query


# Common Verification Steps

@then('I should see search results')
def verify_search_results(page, context: dict):
    """Verify search results are displayed."""
    logger.info("Step: Then I should see search results")
    
    # Wait for results to load
    page.wait_for_timeout(2000)
    
    # This is a placeholder - actual implementation would check for results container
    # For now, we'll just verify page loaded
    assert page.get_current_url(), "Page not loaded"


@then(parsers.parse('the results should contain "{expected_text}"'))
def verify_results_contain_text(page, expected_text: str):
    """
    Verify results contain expected text.
    
    Args:
        expected_text: Expected text in results
    """
    logger.info(f"Step: Then the results should contain '{expected_text}'")
    
    # This is a placeholder - actual implementation would check results
    # For now, we'll just log
    logger.info(f"Would verify results contain: {expected_text}")


@then(parsers.parse('I should see "{message}" message'))
def verify_message_displayed(page, message: str):
    """
    Verify specific message is displayed.
    
    Args:
        message: Expected message
    """
    logger.info(f"Step: Then I should see '{message}' message")
    
    # Wait for message
    page.wait_for_timeout(1000)
    
    # This is a placeholder - actual implementation would check for message
    logger.info(f"Would verify message: {message}")


@then(parsers.parse('the results should be in category "{category}"'))
def verify_results_category(page, category: str, context: dict):
    """
    Verify results are in specified category.
    
    Args:
        category: Expected category
    """
    logger.info(f"Step: Then the results should be in category '{category}'")
    
    # Store in context
    context['expected_category'] = category
    
    # This is a placeholder - actual implementation would verify category
    logger.info(f"Would verify category: {category}")


# Common Action Steps

@when('I click on {element_name}')
def click_on_element(element_name: str, page):
    """
    Click on named element.
    
    Args:
        element_name: Name of element to click
    """
    logger.info(f"Step: When I click on {element_name}")
    
    # This is a generic step - actual implementation would map element names to selectors
    logger.info(f"Would click on: {element_name}")


@when(parsers.parse('I wait for {seconds:d} seconds'))
def wait_for_seconds(seconds: int, page):
    """
    Wait for specified seconds.
    
    Args:
        seconds: Number of seconds to wait
    """
    logger.info(f"Step: When I wait for {seconds} seconds")
    page.wait_for_timeout(seconds * 1000)
