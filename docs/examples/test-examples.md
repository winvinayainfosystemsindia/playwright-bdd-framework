# Test Examples

Comprehensive examples of writing tests in the framework.

## 📝 Table of Contents

1. [Simple Login Test](#simple-login-test)
2. [Data-Driven Test](#data-driven-test)
3. [Multi-Step Test](#multi-step-test)
4. [API + UI Test](#api--ui-test)
5. [Custom Fixtures](#custom-fixtures)

---

## 1. Simple Login Test

### Feature File: `features/simple_login.feature`

```gherkin
Feature: Simple Login
  
  @smoke
  Scenario: User logs in successfully
    Given I am on the login page
    When I enter email "test@example.com"
    And I enter password "password123"
    And I click login button
    Then I should be on the dashboard
```

### Step Definitions: `step_definitions/simple_login_steps.py`

```python
from pytest_bdd import scenarios, given, when, then, parsers

scenarios('../features/simple_login.feature')

@given('I am on the login page')
def on_login_page(login_page):
    login_page.navigate()

@when(parsers.parse('I enter email "{email}"'))
def enter_email(login_page, email):
    login_page.enter_email(email)

@when(parsers.parse('I enter password "{password}"'))
def enter_password(login_page, password):
    login_page.enter_password(password)

@when('I click login button')
def click_login(login_page):
    login_page.click_login_button()

@then('I should be on the dashboard')
def verify_dashboard(home_page):
    assert home_page.is_on_home_page()
```

---

## 2. Data-Driven Test

### Feature File: `features/login_variations.feature`

```gherkin
Feature: Login Variations
  
  @regression
  Scenario Outline: Login with different users
    Given I am on the login page
    When I login as "<user_type>"
    Then I should see "<expected_page>"
    
    Examples:
      | user_type | expected_page |
      | admin     | admin_panel   |
      | user      | dashboard     |
      | guest     | limited_view  |
```

### Step Definitions: `step_definitions/login_variations_steps.py`

```python
from pytest_bdd import scenarios, given, when, then, parsers
from config.config import config

scenarios('../features/login_variations.feature')

@when(parsers.parse('I login as "{user_type}"'))
def login_as_user_type(login_page, user_type):
    user = config.get_test_user(user_type)
    login_page.login(user['email'], user['password'])

@then(parsers.parse('I should see "{expected_page}"'))
def verify_page(page, expected_page):
    current_url = page.url
    assert expected_page in current_url
```

---

## 3. Multi-Step Test

### Feature File: `features/user_journey.feature`

```gherkin
Feature: Complete User Journey
  
  @smoke
  Scenario: New user registration and first purchase
    # Registration
    Given I am on the registration page
    When I fill registration form with:
      | field      | value              |
      | first_name | John               |
      | last_name  | Doe                |
      | email      | john@example.com   |
      | password   | SecurePass123!     |
    And I submit registration
    Then I should see registration success
    
    # Login
    When I navigate to login page
    And I login with registered credentials
    Then I should be logged in
    
    # Shopping
    When I search for "laptop"
    And I add first item to cart
    And I proceed to checkout
    Then I should see checkout page
```

### Step Definitions: `step_definitions/user_journey_steps.py`

```python
from pytest_bdd import scenarios, given, when, then, parsers

scenarios('../features/user_journey.feature')

@when('I fill registration form with:')
def fill_registration(registration_page, datatable, context):
    user_data = {}
    for row in datatable:
        user_data[row['field']] = row['value']
    
    context['user_data'] = user_data
    registration_page.register_user(user_data)

@when('I login with registered credentials')
def login_with_registered(login_page, context):
    user_data = context['user_data']
    login_page.login(user_data['email'], user_data['password'])

@when(parsers.parse('I search for "{query}"'))
def search_product(home_page, query):
    home_page.search(query)

@when('I add first item to cart')
def add_to_cart(product_page):
    product_page.add_first_item_to_cart()
```

---

## 4. API + UI Test

### Feature File: `features/api_ui_test.feature`

```gherkin
Feature: API and UI Integration
  
  @integration
  Scenario: Create user via API and verify in UI
    Given I create a user via API
    When I login with the created user
    Then I should see user profile
    And profile data should match API data
```

### Step Definitions: `step_definitions/api_ui_steps.py`

```python
from pytest_bdd import scenarios, given, when, then
import requests

scenarios('../features/api_ui_test.feature')

@given('I create a user via API')
def create_user_via_api(context, base_url):
    # API call to create user
    user_data = {
        'email': 'apiuser@example.com',
        'password': 'ApiPass123!',
        'name': 'API User'
    }
    
    response = requests.post(
        f"{base_url}/api/users",
        json=user_data
    )
    
    assert response.status_code == 201
    context['api_user'] = user_data
    context['api_response'] = response.json()

@when('I login with the created user')
def login_with_api_user(login_page, context):
    user = context['api_user']
    login_page.login(user['email'], user['password'])

@then('profile data should match API data')
def verify_profile_matches_api(profile_page, context):
    api_data = context['api_response']
    ui_name = profile_page.get_user_name()
    
    assert ui_name == api_data['name']
```

---

## 5. Custom Fixtures

### Fixture File: `conftest.py` (add to existing)

```python
import pytest
from utils.data_reader import fake_data_generator

@pytest.fixture
def random_user():
    """Generate random user data."""
    return fake_data_generator.generate_user()

@pytest.fixture
def authenticated_page(login_page, home_page, valid_user):
    """Return page with authenticated session."""
    login_page.navigate()
    login_page.login(valid_user['email'], valid_user['password'])
    return home_page

@pytest.fixture
def test_product():
    """Return test product data."""
    return {
        'name': 'Test Laptop',
        'price': 999.99,
        'category': 'Electronics'
    }
```

### Usage in Tests:

```python
from pytest_bdd import scenarios, given, when, then

scenarios('../features/custom_fixture_test.feature')

@given('I am logged in with random user')
def login_random_user(login_page, random_user):
    login_page.navigate()
    login_page.login(random_user['email'], random_user['password'])

@when('I am on authenticated dashboard')
def on_dashboard(authenticated_page):
    # Page is already authenticated
    assert authenticated_page.is_logged_in()

@when('I add test product to cart')
def add_test_product(cart_page, test_product):
    cart_page.add_product(test_product['name'])
```

---

## 6. Screenshot Example

### Capture Screenshots in Tests:

```python
from pytest_bdd import scenarios, when, then

scenarios('../features/screenshot_test.feature')

@when('I perform complex action')
def complex_action(page, login_page):
    # Capture before action
    login_page.capture_screenshot("before_action")
    
    # Perform action
    login_page.click("#complex-button")
    
    # Capture after action
    login_page.capture_screenshot("after_action")

@then('I verify with screenshot')
def verify_with_screenshot(login_page):
    # Capture element screenshot
    login_page.capture_element_screenshot(
        ".result-container",
        "result_verification"
    )
```

---

## 7. Parallel Execution Example

### Feature File: `features/parallel_test.feature`

```gherkin
Feature: Parallel Execution Tests
  
  @parallel
  Scenario: Test 1 - Independent test
    Given I am on page A
    When I perform action A
    Then I see result A
  
  @parallel
  Scenario: Test 2 - Independent test
    Given I am on page B
    When I perform action B
    Then I see result B
```

### Run in Parallel:

```bash
# Run with 4 workers
pytest -m parallel -n 4

# Run with auto-detection
pytest -m parallel -n auto
```

---

## 8. Retry Example

### Feature with Flaky Test:

```gherkin
Feature: Flaky Test Example
  
  @flaky
  Scenario: Test with network dependency
    Given I am on the page
    When I wait for external API
    Then I should see API data
```

### Run with Retry:

```bash
# Retry failed tests 3 times
pytest -m flaky --reruns 3 --reruns-delay 1
```

---

## 9. Custom Markers Example

### Add to `pytest.ini`:

```ini
markers =
    smoke: Smoke tests
    regression: Regression tests
    integration: Integration tests
    flaky: Tests that may fail intermittently
    slow: Slow running tests
```

### Use in Features:

```gherkin
@smoke @integration
Scenario: Important integration test
  # Test steps
```

### Run:

```bash
pytest -m "smoke and integration"
pytest -m "smoke or regression"
pytest -m "not slow"
```

---

## 10. Complete Example

### Feature: `features/complete_example.feature`

```gherkin
Feature: Complete E2E Example
  
  Background:
    Given the application is running
    And test data is prepared
  
  @smoke @e2e
  Scenario: Complete user workflow
    # Registration
    Given I am on registration page
    When I register with valid data
    Then registration should succeed
    
    # Email verification (mocked)
    When I verify email
    Then account should be activated
    
    # Login
    When I login with registered account
    Then I should be on dashboard
    
    # Profile update
    When I update my profile
    Then changes should be saved
    
    # Logout
    When I logout
    Then I should be on login page
```

This example demonstrates the complete capabilities of the framework!

---

## Related Documentation

- [Writing Tests Guide](../writing-tests.md)
- [Usage Guide](../usage.md)
- [API Reference](../api/base-page.md)
