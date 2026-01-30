# Framework Usage Guide

Comprehensive guide on using the Playwright BDD Test Automation Framework.

## 📖 Table of Contents

1. [Running Tests](#running-tests)
2. [Writing Tests](#writing-tests)
3. [Page Objects](#page-objects)
4. [Test Data](#test-data)
5. [Configuration](#configuration)
6. [Reporting](#reporting)
7. [Best Practices](#best-practices)

---

## 🚀 Running Tests

### Basic Execution

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with detailed output
pytest -vv
```

### Run by Markers

```bash
# Smoke tests
pytest -m smoke

# Regression tests
pytest -m regression

# Login tests
pytest -m login

# Multiple markers
pytest -m "smoke and login"
pytest -m "smoke or regression"
```

### Run Specific Tests

```bash
# Run specific feature
pytest --features features/login.feature

# Run specific step file
pytest step_definitions/login_steps.py

# Run specific test by name
pytest -k "test_successful_login"
```

### Parallel Execution

```bash
# Auto-detect CPU cores
pytest -n auto

# Specify number of workers
pytest -n 4

# Distribute by file
pytest -n 4 --dist loadfile
```

### Browser Selection

```bash
# Chromium (default)
pytest

# Firefox
BROWSER=firefox pytest

# WebKit
BROWSER=webkit pytest
```

### Headless Mode

```bash
# Headless
HEADLESS=true pytest

# Headed (see browser)
HEADLESS=false pytest
```

### Environment Selection

```bash
# Development
ENVIRONMENT=dev pytest

# QA
ENVIRONMENT=qa pytest

# Production
ENVIRONMENT=prod pytest
```

### Retry Failed Tests

```bash
# Retry failed tests 3 times
pytest --reruns 3

# Retry with delay
pytest --reruns 3 --reruns-delay 2
```

### Stop on Failure

```bash
# Stop on first failure
pytest -x

# Stop after 3 failures
pytest --maxfail=3
```

---

## ✍️ Writing Tests

### 1. Create Feature File

**Location:** `features/my_feature.feature`

```gherkin
Feature: User Profile Management
  As a logged-in user
  I want to manage my profile
  So that I can keep my information updated

  Background:
    Given I am logged in
    And I am on the profile page

  @smoke @profile
  Scenario: Update profile name
    When I update my name to "John Doe"
    And I click save button
    Then I should see success message
    And my name should be updated

  @regression @profile
  Scenario Outline: Update profile with different data
    When I update my <field> to "<value>"
    And I click save button
    Then I should see success message

    Examples:
      | field    | value           |
      | name     | Jane Smith      |
      | email    | jane@test.com   |
      | phone    | +1234567890     |
```

### 2. Create Page Object

**Location:** `pages/profile_page.py`

```python
from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.logger import Logger

logger = Logger.get_logger(__name__)

class ProfilePage(BasePage):
    """Profile Page Object."""
    
    # Locators
    NAME_INPUT = "#name"
    EMAIL_INPUT = "#email"
    PHONE_INPUT = "#phone"
    SAVE_BUTTON = "button[type='submit']"
    SUCCESS_MESSAGE = ".success-message"
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.base_url}/profile"
    
    def navigate(self) -> None:
        """Navigate to profile page."""
        logger.info("Navigating to profile page")
        self.navigate_to(self.url)
    
    def update_name(self, name: str) -> None:
        """Update profile name."""
        logger.info(f"Updating name to: {name}")
        self.fill(self.NAME_INPUT, name)
    
    def update_email(self, email: str) -> None:
        """Update profile email."""
        logger.info(f"Updating email to: {email}")
        self.fill(self.EMAIL_INPUT, email)
    
    def click_save(self) -> None:
        """Click save button."""
        logger.info("Clicking save button")
        self.click(self.SAVE_BUTTON)
    
    def get_success_message(self) -> str:
        """Get success message text."""
        return self.get_text(self.SUCCESS_MESSAGE)
    
    def is_success_message_displayed(self) -> bool:
        """Check if success message is displayed."""
        return self.is_visible(self.SUCCESS_MESSAGE)
```

### 3. Create Step Definitions

**Location:** `step_definitions/profile_steps.py`

```python
from pytest_bdd import scenarios, given, when, then, parsers
from pages.profile_page import ProfilePage
from utils.logger import Logger

logger = Logger.get_logger(__name__)

# Load scenarios
scenarios('../features/my_feature.feature')

# Given Steps
@given('I am on the profile page')
def navigate_to_profile(profile_page: ProfilePage):
    """Navigate to profile page."""
    logger.info("Step: Given I am on the profile page")
    profile_page.navigate()

# When Steps
@when(parsers.parse('I update my name to "{name}"'))
def update_name(profile_page: ProfilePage, name: str):
    """Update profile name."""
    logger.info(f"Step: When I update my name to '{name}'")
    profile_page.update_name(name)

@when(parsers.parse('I update my {field} to "{value}"'))
def update_field(profile_page: ProfilePage, field: str, value: str):
    """Update profile field."""
    logger.info(f"Step: When I update my {field} to '{value}'")
    
    if field == 'name':
        profile_page.update_name(value)
    elif field == 'email':
        profile_page.update_email(value)

@when('I click save button')
def click_save(profile_page: ProfilePage):
    """Click save button."""
    logger.info("Step: When I click save button")
    profile_page.click_save()

# Then Steps
@then('I should see success message')
def verify_success_message(profile_page: ProfilePage):
    """Verify success message is displayed."""
    logger.info("Step: Then I should see success message")
    assert profile_page.is_success_message_displayed(), \
        "Success message not displayed"

@then(parsers.parse('my name should be updated'))
def verify_name_updated(profile_page: ProfilePage):
    """Verify name was updated."""
    logger.info("Step: Then my name should be updated")
    # Add verification logic
    pass
```

### 4. Add Page Fixture

**Location:** `conftest.py`

```python
@pytest.fixture(scope='function')
def profile_page(page: Page) -> ProfilePage:
    """Profile page fixture."""
    return ProfilePage(page)
```

### 5. Run Your Test

```bash
pytest step_definitions/profile_steps.py -v
```

---

## 📄 Page Objects

### BasePage Methods

All page objects inherit from `BasePage` which provides:

**Navigation:**
- `navigate_to(url)` - Navigate to URL
- `reload_page()` - Reload current page
- `go_back()` - Navigate back
- `go_forward()` - Navigate forward

**Element Interactions:**
- `click(selector)` - Click element
- `fill(selector, value)` - Fill input field
- `type(selector, text, delay)` - Type with delay
- `select_option(selector, value)` - Select dropdown option
- `check(selector)` - Check checkbox
- `hover(selector)` - Hover over element

**Element Queries:**
- `get_text(selector)` - Get element text
- `get_attribute(selector, attr)` - Get attribute value
- `is_visible(selector)` - Check if visible
- `is_enabled(selector)` - Check if enabled
- `get_element_count(selector)` - Count elements

**Waits:**
- `wait_for_element(selector, state)` - Wait for element
- `wait_for_url(url)` - Wait for URL
- `wait_for_load_state(state)` - Wait for page load

**Screenshots:**
- `capture_screenshot(name)` - Capture screenshot
- `capture_element_screenshot(selector, name)` - Element screenshot

**Assertions:**
- `assert_url_contains(text)` - Assert URL
- `assert_element_visible(selector)` - Assert visibility
- `assert_element_text(selector, text)` - Assert text

---

## 📊 Test Data

### YAML Data Files

**Location:** `config/test_data/users.yml`

```yaml
users:
  valid:
    email: testuser@example.com
    password: Test@123456
    first_name: John
    last_name: Doe
  
  admin:
    email: admin@example.com
    password: Admin@123456
    role: administrator
```

**Usage in tests:**

```python
from config.config import config

# Get test user
user = config.get_test_user('valid')
email = user['email']
password = user['password']
```

### Dynamic Data with Faker

```python
from utils.data_reader import fake_data_generator

# Generate user
user = fake_data_generator.generate_user()

# Generate specific data
email = fake_data_generator.generate_email()
password = fake_data_generator.generate_password()
name = fake_data_generator.generate_name()
```

---

## ⚙️ Configuration

### Environment Variables (.env)

```env
# Environment
ENVIRONMENT=dev

# Browser
BROWSER=chromium
HEADLESS=false
SLOW_MO=0

# Application
BASE_URL=https://example.com
TIMEOUT=30000

# Recording
VIDEO=on_failure
SCREENSHOT=only-on-failure

# Logging
LOG_LEVEL=INFO
```

### Environment-Specific Configs

**Location:** `config/environments/dev.yml`

```yaml
base_url: https://dev.example.com
timeout: 30000
api_url: https://api-dev.example.com
```

**Available environments:**
- `dev.yml` - Development
- `qa.yml` - QA/Testing
- `prod.yml` - Production

---

## 📊 Reporting

### HTML Report

```bash
pytest --html=reports/report.html --self-contained-html
```

Open `reports/report.html` in browser.

### Allure Report

```bash
# Generate results
pytest --alluredir=reports/allure-results

# Serve report
allure serve reports/allure-results

# Generate static report
allure generate reports/allure-results -o reports/allure-report
```

### Logs

Logs are automatically created in `reports/` with timestamps:
- `test_execution_YYYYMMDD_HHMMSS.log`

---

## ✅ Best Practices

### 1. Use Descriptive Names

```python
# Good
def test_user_can_login_with_valid_credentials():
    pass

# Avoid
def test1():
    pass
```

### 2. Keep Steps Atomic

```gherkin
# Good
When I enter email "test@example.com"
And I enter password "password123"
And I click login button

# Avoid
When I login with credentials
```

### 3. Use Page Objects

```python
# Good
login_page.login(email, password)

# Avoid
page.fill("#email", email)
page.fill("#password", password)
page.click("button")
```

### 4. Add Proper Logging

```python
logger.info(f"Logging in with email: {email}")
```

### 5. Use Markers

```gherkin
@smoke @login
Scenario: Successful login
```

### 6. Handle Waits Properly

```python
# Good - Use explicit waits
self.wait_for_element(selector, 'visible')

# Avoid - Hard-coded sleeps
time.sleep(5)
```

---

## 🔍 Debugging

### Run with Debug Output

```bash
pytest -vv -s
```

### Run Single Test

```bash
pytest -k "test_name" -vv
```

### Capture Screenshots

Screenshots are automatically captured on failure in `reports/screenshots/`

### View Logs

Check `reports/test_execution_*.log` for detailed logs

---

## 📚 Next Steps

- [Architecture Overview](architecture.md)
- [API Reference](api/base-page.md)
- [CI/CD Integration](ci-cd-integration.md)
- [Troubleshooting](troubleshooting.md)
