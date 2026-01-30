# Quick Start Guide

Get up and running with the Playwright BDD framework in 5 minutes!

## 🚀 5-Minute Quick Start

### 1. Install Dependencies (2 minutes)

```bash
# Navigate to project
cd playwright-bdd-framework

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure Environment (1 minute)

```bash
# Copy environment template
cp .env.example .env

# Edit .env (optional - defaults work fine)
# Set your BASE_URL if testing a specific application
```

### 3. Run Your First Test (2 minutes)

```bash
# Run smoke tests
pytest -m smoke

# Or run all tests
pytest

# Run with HTML report
pytest --html=reports/report.html
```

**That's it!** 🎉 You've run your first automated tests.

---

## 📊 View Results

### Console Output
Test results appear in the terminal with pass/fail status.

### HTML Report
Open `reports/report.html` in your browser to see detailed results.

### Allure Report (Optional)
```bash
# Generate Allure report
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

---

## 🎯 Common Commands

### Run Specific Tests

```bash
# Run login tests only
pytest -m login

# Run registration tests only
pytest -m registration

# Run specific feature
pytest step_definitions/login_steps.py
```

### Run in Different Browsers

```bash
# Firefox
BROWSER=firefox pytest -m smoke

# WebKit (Safari)
BROWSER=webkit pytest -m smoke
```

### Run in Headless Mode

```bash
HEADLESS=true pytest -m smoke
```

### Run in Parallel

```bash
# Auto-detect CPU cores
pytest -n auto

# Use 4 workers
pytest -n 4
```

---

## 📝 Your First Custom Test

### 1. Create a Feature File

Create `features/my_test.feature`:

```gherkin
Feature: My First Test
  As a user
  I want to test the application
  
  @smoke
  Scenario: Simple navigation test
    Given I am on the login page
    Then I should see the login form
```

### 2. Create Step Definitions

Create `step_definitions/my_test_steps.py`:

```python
from pytest_bdd import scenarios, given, then

scenarios('../features/my_test.feature')

@given('I am on the login page')
def navigate_to_login(login_page):
    login_page.navigate()

@then('I should see the login form')
def verify_login_form(login_page):
    assert login_page.is_visible(login_page.LOGIN_BUTTON)
```

### 3. Run Your Test

```bash
pytest step_definitions/my_test_steps.py -v
```

---

## 🔧 Quick Configuration

### Change Base URL

Edit `.env`:
```env
BASE_URL=https://your-app.com
```

### Change Browser

Edit `.env`:
```env
BROWSER=firefox  # or chromium, webkit
```

### Enable Video Recording

Edit `.env`:
```env
VIDEO=on  # Records all tests
```

---

## 📚 What's Next?

Now that you've run your first test, explore more:

1. **[Writing Tests](writing-tests.md)** - Learn to write comprehensive tests
2. **[Configuration Guide](configuration.md)** - Customize the framework
3. **[Page Object Model](page-object-model.md)** - Understand POM pattern
4. **[Reporting](reporting.md)** - Advanced reporting options

---

## 🆘 Quick Troubleshooting

### Tests fail with "Browser not found"
```bash
playwright install chromium
```

### Import errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### No tests collected
```bash
# Verify you're in the project root
cd playwright-bdd-framework
pytest --collect-only
```

---

## 💡 Pro Tips

1. **Use markers** to run specific test groups:
   ```bash
   pytest -m "smoke and login"
   ```

2. **Run with verbose output** for more details:
   ```bash
   pytest -v
   ```

3. **Stop on first failure** for quick debugging:
   ```bash
   pytest -x
   ```

4. **Show print statements** during test execution:
   ```bash
   pytest -s
   ```

5. **Combine options** for powerful test execution:
   ```bash
   pytest -m smoke -n auto --html=reports/report.html
   ```

---

## 🎓 Learning Path

**Beginner:**
1. Run existing tests ✅ (You are here!)
2. Understand test structure
3. Modify existing tests

**Intermediate:**
1. Write new feature files
2. Create step definitions
3. Add new page objects

**Advanced:**
1. Customize framework configuration
2. Add new utilities
3. Integrate with CI/CD

---

## ✅ Checklist

- [ ] Installed dependencies
- [ ] Configured `.env` file
- [ ] Ran smoke tests successfully
- [ ] Viewed HTML report
- [ ] Tried different browsers
- [ ] Created a custom test
- [ ] Explored documentation

---

**Congratulations!** 🎉 You're ready to start automating tests with this framework.

For detailed information, see the [full documentation](README.md).
