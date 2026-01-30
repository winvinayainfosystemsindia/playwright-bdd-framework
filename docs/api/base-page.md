# BasePage API Reference

Complete API documentation for the `BasePage` class.

## Overview

`BasePage` is the foundation class for all page objects. It provides common methods for interacting with web pages using Playwright.

**Location:** `pages/base_page.py`

---

## Constructor

### `__init__(page: Page)`

Initialize the base page.

**Parameters:**
- `page` (Page): Playwright Page instance

**Example:**
```python
class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
```

---

## Navigation Methods

### `navigate_to(url: str) -> None`

Navigate to specified URL.

**Parameters:**
- `url` (str): URL to navigate to

**Example:**
```python
self.navigate_to("https://example.com/login")
```

### `get_current_url() -> str`

Get current page URL.

**Returns:** Current URL as string

**Example:**
```python
current_url = self.get_current_url()
```

### `get_title() -> str`

Get page title.

**Returns:** Page title as string

**Example:**
```python
title = self.get_title()
```

### `reload_page() -> None`

Reload current page.

### `go_back() -> None`

Navigate back in browser history.

### `go_forward() -> None`

Navigate forward in browser history.

---

## Wait Methods

### `wait_for_element(selector: str, state: str = 'visible', timeout: Optional[int] = None) -> Locator`

Wait for element to reach specified state.

**Parameters:**
- `selector` (str): Element selector
- `state` (str): Element state ('visible', 'hidden', 'attached', 'detached')
- `timeout` (int, optional): Custom timeout in milliseconds

**Returns:** Locator instance

**Example:**
```python
element = self.wait_for_element("#submit-btn", "visible")
```

### `wait_for_url(url: str, timeout: Optional[int] = None) -> None`

Wait for URL to match pattern.

**Parameters:**
- `url` (str): URL pattern
- `timeout` (int, optional): Timeout in milliseconds

**Example:**
```python
self.wait_for_url("**/dashboard")
```

### `wait_for_load_state(state: str = 'load', timeout: Optional[int] = None) -> None`

Wait for page load state.

**Parameters:**
- `state` (str): Load state ('load', 'domcontentloaded', 'networkidle')
- `timeout` (int, optional): Timeout in milliseconds

---

## Element Interaction Methods

### `click(selector: str, timeout: Optional[int] = None) -> None`

Click on element.

**Parameters:**
- `selector` (str): Element selector
- `timeout` (int, optional): Timeout in milliseconds

**Example:**
```python
self.click("button[type='submit']")
```

### `fill(selector: str, value: str, timeout: Optional[int] = None) -> None`

Fill input field with value.

**Parameters:**
- `selector` (str): Element selector
- `value` (str): Value to fill
- `timeout` (int, optional): Timeout in milliseconds

**Example:**
```python
self.fill("#email", "test@example.com")
```

### `type(selector: str, text: str, delay: int = 100, timeout: Optional[int] = None) -> None`

Type text with delay between keystrokes.

**Parameters:**
- `selector` (str): Element selector
- `text` (str): Text to type
- `delay` (int): Delay in milliseconds (default: 100)
- `timeout` (int, optional): Timeout in milliseconds

### `clear(selector: str, timeout: Optional[int] = None) -> None`

Clear input field.

### `select_option(selector: str, value: str, timeout: Optional[int] = None) -> None`

Select option from dropdown.

**Example:**
```python
self.select_option("#country", "USA")
```

### `check(selector: str, timeout: Optional[int] = None) -> None`

Check checkbox or radio button.

### `uncheck(selector: str, timeout: Optional[int] = None) -> None`

Uncheck checkbox.

### `hover(selector: str, timeout: Optional[int] = None) -> None`

Hover over element.

---

## Element Query Methods

### `get_text(selector: str, timeout: Optional[int] = None) -> str`

Get text content of element.

**Returns:** Element text

**Example:**
```python
message = self.get_text(".success-message")
```

### `get_attribute(selector: str, attribute: str, timeout: Optional[int] = None) -> Optional[str]`

Get element attribute value.

**Parameters:**
- `selector` (str): Element selector
- `attribute` (str): Attribute name

**Returns:** Attribute value or None

**Example:**
```python
href = self.get_attribute("a.link", "href")
```

### `is_visible(selector: str, timeout: Optional[int] = None) -> bool`

Check if element is visible.

**Returns:** True if visible, False otherwise

**Example:**
```python
if self.is_visible(".error-message"):
    # Handle error
```

### `is_enabled(selector: str, timeout: Optional[int] = None) -> bool`

Check if element is enabled.

**Returns:** True if enabled, False otherwise

### `is_checked(selector: str, timeout: Optional[int] = None) -> bool`

Check if checkbox/radio is checked.

**Returns:** True if checked, False otherwise

### `get_element_count(selector: str) -> int`

Get count of elements matching selector.

**Returns:** Number of matching elements

**Example:**
```python
item_count = self.get_element_count(".product-item")
```

---

## Screenshot Methods

### `capture_screenshot(name: Optional[str] = None) -> None`

Capture screenshot of current page.

**Parameters:**
- `name` (str, optional): Screenshot name

**Example:**
```python
self.capture_screenshot("login_page")
```

### `capture_element_screenshot(selector: str, name: Optional[str] = None) -> None`

Capture screenshot of specific element.

**Parameters:**
- `selector` (str): Element selector
- `name` (str, optional): Screenshot name

---

## Assertion Methods

### `assert_url_contains(expected: str) -> None`

Assert that URL contains expected text.

**Parameters:**
- `expected` (str): Expected text in URL

**Example:**
```python
self.assert_url_contains("/dashboard")
```

### `assert_title_contains(expected: str) -> None`

Assert that title contains expected text.

### `assert_element_visible(selector: str) -> None`

Assert that element is visible.

**Example:**
```python
self.assert_element_visible(".welcome-message")
```

### `assert_element_text(selector: str, expected: str) -> None`

Assert element text matches expected.

**Parameters:**
- `selector` (str): Element selector
- `expected` (str): Expected text

---

## Properties

### `page`
Playwright Page instance

### `timeout`
Default timeout in milliseconds

### `screenshot_helper`
ScreenshotHelper instance

---

## Usage Example

```python
from playwright.sync_api import Page
from pages.base_page import BasePage

class ProductPage(BasePage):
    # Locators
    SEARCH_BOX = "#search"
    SEARCH_BUTTON = "button[type='submit']"
    RESULTS = ".product-item"
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = "https://example.com/products"
    
    def search_product(self, query: str) -> None:
        """Search for product."""
        self.fill(self.SEARCH_BOX, query)
        self.click(self.SEARCH_BUTTON)
        self.wait_for_element(self.RESULTS, "visible")
    
    def get_result_count(self) -> int:
        """Get number of search results."""
        return self.get_element_count(self.RESULTS)
    
    def verify_results_displayed(self) -> None:
        """Verify search results are displayed."""
        self.assert_element_visible(self.RESULTS)
```

---

## Best Practices

1. **Always use BasePage methods** instead of direct Playwright calls
2. **Add logging** for important actions
3. **Use descriptive selector names** as class constants
4. **Handle errors gracefully** with try-except when needed
5. **Use waits** instead of hard-coded sleeps

---

## Related Documentation

- [Page Object Model Guide](../page-object-model.md)
- [Writing Tests](../writing-tests.md)
- [Usage Guide](../usage.md)
