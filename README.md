# Playwright BDD Test Automation Framework

A comprehensive Python-based test automation framework using Playwright and pytest-bdd for behavior-driven development (BDD) testing.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Reporting](#reporting)
- [Writing Tests](#writing-tests)
- [CI/CD Integration](#cicd-integration)
- [Best Practices](#best-practices)
- [Contributing](#contributing)

## 🎯 Overview

This framework provides a robust, scalable solution for end-to-end testing using:

- **Playwright** for browser automation
- **pytest-bdd** for BDD-style test scenarios
- **Page Object Model** for maintainable test code
- **Allure** for comprehensive test reporting
- **Multi-environment** support (dev, staging, prod)
- **Parallel execution** for faster test runs
- **Auto-retry** for flaky tests

## ✨ Features

- ✅ **BDD Support**: Write tests in Gherkin syntax
- ✅ **Multi-Browser**: Support for Chromium, Firefox, and WebKit
- ✅ **Page Object Model**: Clean separation of test logic and page interactions
- ✅ **Smart Waits**: Playwright's auto-waiting capabilities
- ✅ **Screenshot on Failure**: Automatic screenshot capture and attachment to reports
- ✅ **Video Recording**: Record test execution videos
- ✅ **Parallel Execution**: Run tests in parallel with pytest-xdist
- ✅ **Retry Mechanism**: Auto-retry flaky tests
- ✅ **Comprehensive Logging**: Detailed logs with timestamps
- ✅ **Allure Reports**: Beautiful, interactive test reports
- ✅ **Fake Data Generation**: Dynamic test data using Faker
- ✅ **Environment Management**: Easy switching between environments

## 📁 Project Structure

```
playwright-bdd-framework/
├── config/                      # Configuration management
│   ├── config.py               # Main configuration class (Singleton)
│   ├── environments/           # Environment-specific configs
│   │   ├── dev.yml
│   │   ├── staging.yml
│   │   └── prod.yml
│   └── test_data/              # Test data files
│       └── users.yml
├── features/                    # BDD feature files (Gherkin)
│   ├── login.feature
│   ├── registration.feature
│   └── product_search.feature
├── pages/                       # Page Object Model
│   ├── base_page.py            # Base page with common methods
│   ├── login_page.py
│   ├── home_page.py
│   └── registration_page.py
├── step_definitions/            # BDD step implementations
│   ├── conftest.py
│   ├── login_steps.py
│   ├── registration_steps.py
│   └── common_steps.py
├── utils/                       # Utility modules
│   ├── browser_manager.py      # Browser management (Factory pattern)
│   ├── logger.py               # Logging utilities
│   ├── screenshot_helper.py    # Screenshot capture
│   ├── data_reader.py          # YAML/JSON data reader
│   └── report_helper.py        # Allure reporting utilities
├── fixtures/                    # Pytest fixtures
│   └── browser_fixtures.py     # Browser-related fixtures
├── reports/                     # Test reports (auto-generated)
│   ├── screenshots/
│   ├── videos/
│   └── allure-results/
├── tests/                       # Additional test files
├── conftest.py                  # Root pytest configuration
├── pytest.ini                   # Pytest settings
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

## 🔧 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## 📦 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd playwright-bdd-framework
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers

```bash
playwright install
```

### 5. Configure Environment

Copy `.env.example` to `.env` and update values:

```bash
cp .env.example .env
```

Edit `.env` file:

```env
ENVIRONMENT=dev
BROWSER=chromium
HEADLESS=false
BASE_URL=https://example.com
TIMEOUT=30000
SLOW_MO=0
VIDEO=on_failure
SCREENSHOT=only-on-failure
LOG_LEVEL=INFO
```

## ⚙️ Configuration

### Environment Configuration

Edit environment-specific YAML files in `config/environments/`:

- `dev.yml` - Development environment
- `qa.yml` - QA environment
- `prod.yml` - Production environment

### Test Data

Edit `config/test_data/users.yml` to add/modify test users and data.

## 🚀 Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Feature

```bash
pytest --features features/login.feature
```

### Run with Specific Markers

```bash
# Run smoke tests
pytest -m smoke

# Run regression tests
pytest -m regression

# Run login tests
pytest -m login
```

### Run in Parallel

```bash
# Auto-detect CPU cores
pytest -n auto

# Specify number of workers
pytest -n 4
```

### Run with Different Browser

```bash
# Set in .env file or override via environment variable
BROWSER=firefox pytest
BROWSER=webkit pytest
```

### Run in Different Environment

```bash
ENVIRONMENT=staging pytest
ENVIRONMENT=prod pytest
```

### Run in Headless Mode

```bash
HEADLESS=true pytest
```

### Run with Reruns (Flaky Tests)

```bash
# Retry failed tests 3 times with 2 second delay
pytest --reruns 3 --reruns-delay 2
```

### Run Specific Scenario

```bash
pytest -k "Successful login"
```

## 📊 Reporting

### HTML Report

```bash
pytest --html=reports/report.html --self-contained-html
```

View report: Open `reports/report.html` in browser

### Allure Report

```bash
# Generate Allure results
pytest --alluredir=reports/allure-results

# Serve Allure report
allure serve reports/allure-results
```

### View Logs

Logs are automatically generated in `reports/` directory with timestamps:
- `test_execution_YYYYMMDD_HHMMSS.log`

### Screenshots

Failure screenshots are saved in `reports/screenshots/` with format:
- `FAILED_<test_name>_<timestamp>.png`

### Videos

Test videos (if enabled) are saved in `reports/videos/`

## ✍️ Writing Tests

### 1. Create Feature File

Create a new `.feature` file in `features/` directory:

```gherkin
Feature: User Profile
  As a user
  I want to update my profile
  So that my information is current

  @smoke @profile
  Scenario: Update profile successfully
    Given I am logged in
    When I navigate to profile page
    And I update my name to "John Doe"
    And I click save button
    Then I should see success message
```

### 2. Create Page Object

Create a new page class in `pages/` directory:

```python
from pages.base_page import BasePage

class ProfilePage(BasePage):
    # Locators
    NAME_INPUT = "#name"
    SAVE_BUTTON = "button[type='submit']"
    SUCCESS_MESSAGE = ".success"
    
    def update_name(self, name: str):
        self.fill(self.NAME_INPUT, name)
    
    def click_save(self):
        self.click(self.SAVE_BUTTON)
```

### 3. Implement Step Definitions

Create step definitions in `step_definitions/`:

```python
from pytest_bdd import scenarios, given, when, then

scenarios('../features/profile.feature')

@when('I navigate to profile page')
def navigate_to_profile(profile_page):
    profile_page.navigate()

@when(parsers.parse('I update my name to "{name}"'))
def update_name(profile_page, name):
    profile_page.update_name(name)
```

### 4. Add Page Fixture

Add fixture in `conftest.py`:

```python
@pytest.fixture
def profile_page(page: Page) -> ProfilePage:
    return ProfilePage(page)
```

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Test Automation

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install --with-deps
      
      - name: Run tests
        run: |
          pytest --alluredir=allure-results
        env:
          HEADLESS: true
          ENVIRONMENT: staging
      
      - name: Generate Allure Report
        if: always()
        uses: simple-elf/allure-report-action@master
        with:
          allure_results: allure-results
```

### Jenkins Example

```groovy
pipeline {
    agent any
    
    stages {
        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'playwright install'
            }
        }
        
        stage('Test') {
            steps {
                sh 'pytest --alluredir=allure-results'
            }
        }
        
        stage('Report') {
            steps {
                allure includeProperties: false,
                       jdk: '',
                       results: [[path: 'allure-results']]
            }
        }
    }
}
```

## 📝 Best Practices

### 1. Page Objects
- Keep page objects focused on a single page
- Use descriptive locator names
- Implement methods that represent user actions
- Don't include assertions in page objects

### 2. Step Definitions
- Keep steps reusable and atomic
- Use parsers for parameterized steps
- Store shared data in context fixture
- Add proper logging

### 3. Test Data
- Use YAML files for static test data
- Use Faker for dynamic data generation
- Don't hardcode sensitive data
- Use environment-specific configurations

### 4. Locators
- Prefer data-testid attributes
- Use CSS selectors over XPath
- Keep locators maintainable
- Avoid brittle selectors

### 5. Waits
- Rely on Playwright's auto-waiting
- Use explicit waits when necessary
- Set appropriate timeouts
- Don't use hard-coded sleeps

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings to functions and classes
- Keep functions focused and small
- Write meaningful commit messages

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
- Create an issue in the repository
- Check existing documentation
- Review feature files for examples

## 🎓 Additional Resources

- [Playwright Documentation](https://playwright.dev/python/)
- [pytest-bdd Documentation](https://pytest-bdd.readthedocs.io/)
- [Allure Documentation](https://docs.qameta.io/allure/)
- [Gherkin Syntax](https://cucumber.io/docs/gherkin/)

---

**Happy Testing! 🚀**
