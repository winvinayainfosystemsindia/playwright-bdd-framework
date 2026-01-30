# Architecture Overview

Complete architectural documentation for the Playwright BDD Test Automation Framework.

## 🏗️ Architecture Layers

The framework follows a **4-layer architecture** for separation of concerns and maintainability.

```
┌─────────────────────────────────────────────────────┐
│         Layer 4: Test Scenarios                     │
│  Feature Files | Test Configuration | Test Data     │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│         Layer 3: Test Logic                         │
│  Step Definitions | Fixtures | Test Helpers        │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│         Layer 2: Test Objects                       │
│  Page Objects | Component Objects | API Clients    │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│         Layer 1: Framework Core                     │
│  Browser | Config | Logger | Utils | Reporting     │
└─────────────────────────────────────────────────────┘
```

---

## 📐 Design Patterns

### 1. Page Object Model (POM)

**Purpose:** Separate page structure from test logic

**Implementation:**
```python
class LoginPage(BasePage):
    # Locators
    EMAIL_INPUT = "#email"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button[type='submit']"
    
    def login(self, email, password):
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
```

**Benefits:**
- Centralized element locators
- Reusable page methods
- Easy maintenance

### 2. Singleton Pattern

**Purpose:** Single configuration instance

**Implementation:**
```python
class Config:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

**Benefits:**
- Single source of truth
- Prevents duplicate initialization
- Global access point

### 3. Factory Pattern

**Purpose:** Dynamic browser creation

**Implementation:**
```python
def launch_browser(self, browser_type):
    if browser_type == 'chromium':
        return self.playwright.chromium.launch()
    elif browser_type == 'firefox':
        return self.playwright.firefox.launch()
    elif browser_type == 'webkit':
        return self.playwright.webkit.launch()
```

**Benefits:**
- Flexible browser selection
- Easy to extend
- Runtime configuration

### 4. Strategy Pattern

**Purpose:** Multiple data source strategies

**Implementation:**
```python
class DataReader:
    @staticmethod
    def read_yaml(file_path):
        # YAML strategy
        
    @staticmethod
    def read_json(file_path):
        # JSON strategy
```

**Benefits:**
- Interchangeable data sources
- Easy to add new strategies
- Consistent interface

### 5. Decorator Pattern

**Purpose:** Add functionality without modifying code

**Implementation:**
```python
@allure_step("Login to application")
def login(self, email, password):
    # Automatically logged as Allure step
```

**Benefits:**
- Automatic logging
- Screenshot on failure
- Clean code

---

## 📂 Directory Structure

```
playwright-bdd-framework/
├── config/                 # Layer 1: Configuration
│   ├── config.py          # Singleton config
│   ├── environments/      # Environment configs
│   └── test_data/         # Test data files
│
├── utils/                  # Layer 1: Utilities
│   ├── browser_manager.py # Factory pattern
│   ├── logger.py          # Logging
│   ├── screenshot_helper.py
│   ├── data_reader.py     # Strategy pattern
│   └── report_helper.py   # Decorator pattern
│
├── pages/                  # Layer 2: Page Objects
│   ├── base_page.py       # Base POM
│   ├── login_page.py
│   ├── home_page.py
│   └── registration_page.py
│
├── step_definitions/       # Layer 3: Test Logic
│   ├── conftest.py
│   ├── login_steps.py
│   ├── registration_steps.py
│   └── common_steps.py
│
├── fixtures/               # Layer 3: Fixtures
│   └── browser_fixtures.py
│
├── features/               # Layer 4: Scenarios
│   ├── login.feature
│   ├── registration.feature
│   └── product_search.feature
│
├── reports/                # Generated reports
├── tests/                  # Additional tests
├── docs/                   # Documentation
├── conftest.py            # Root configuration
├── pytest.ini             # Pytest settings
└── requirements.txt       # Dependencies
```

---

## 🔄 Data Flow

```
1. Test Execution
   pytest → conftest.py → pytest.ini

2. Browser Setup
   conftest.py → browser_fixtures.py → BrowserManager

3. Test Scenario
   feature file → step definitions → page objects

4. Page Interaction
   page object → BasePage → Playwright API

5. Reporting
   test result → pytest hooks → Allure/HTML reports
```

---

## 🔌 Component Interaction

```
┌──────────────┐
│ Feature File │
└──────┬───────┘
       │
       ↓
┌──────────────────┐
│ Step Definitions │
└──────┬───────────┘
       │
       ↓
┌──────────────┐      ┌─────────────┐
│ Page Objects │ ←──→ │ Test Data   │
└──────┬───────┘      └─────────────┘
       │
       ↓
┌──────────────┐      ┌─────────────┐
│  BasePage    │ ←──→ │ Logger      │
└──────┬───────┘      └─────────────┘
       │
       ↓
┌──────────────┐      ┌─────────────┐
│  Playwright  │ ←──→ │ Screenshots │
└──────────────┘      └─────────────┘
```

---

## 🎯 Key Principles

### 1. Separation of Concerns
- Each layer has specific responsibility
- No cross-layer dependencies
- Clear interfaces between layers

### 2. DRY (Don't Repeat Yourself)
- Reusable BasePage methods
- Common step definitions
- Shared fixtures

### 3. Single Responsibility
- Each class has one purpose
- Page objects represent pages
- Utilities provide specific functions

### 4. Open/Closed Principle
- Open for extension
- Closed for modification
- Easy to add new pages/tests

### 5. Dependency Injection
- Fixtures inject dependencies
- Loose coupling
- Easy testing

---

## 📊 Configuration Management

```
Environment Variables (.env)
         ↓
    Config Class (Singleton)
         ↓
   ┌─────┴─────┐
   ↓           ↓
YAML Configs  Test Data
   ↓           ↓
Tests      Page Objects
```

---

## 🧪 Test Execution Flow

```
1. pytest starts
   ↓
2. Load pytest.ini configuration
   ↓
3. Execute conftest.py hooks
   ↓
4. Create browser fixtures
   ↓
5. Load feature files
   ↓
6. Execute step definitions
   ↓
7. Page objects interact with browser
   ↓
8. Capture results and screenshots
   ↓
9. Generate reports
```

---

## 🔒 Error Handling

```
Try-Except in BasePage
         ↓
    Log Error
         ↓
  Capture Screenshot
         ↓
  Attach to Report
         ↓
   Raise Exception
```

---

## 📈 Scalability

The architecture supports:

- **Horizontal Scaling:** Add more page objects, features
- **Vertical Scaling:** Enhance existing components
- **Parallel Execution:** Multiple test workers
- **Multi-Environment:** Different configurations

---

## 🔧 Extensibility Points

1. **New Page Objects:** Inherit from BasePage
2. **New Utilities:** Add to utils/ directory
3. **New Data Sources:** Implement in DataReader
4. **New Browsers:** Add to BrowserManager factory
5. **New Reports:** Add to ReportHelper

---

## 📚 Related Documentation

- [Usage Guide](usage.md)
- [API Reference](api/base-page.md)
- [Best Practices](best-practices.md)
