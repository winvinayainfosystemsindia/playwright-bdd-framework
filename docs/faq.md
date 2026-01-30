# Frequently Asked Questions (FAQ)

Common questions and answers about the Playwright BDD framework.

## 🔧 Installation & Setup

### Q: Which Python version is required?
**A:** Python 3.8 or higher is required.

### Q: Do I need to install browsers separately?
**A:** No, run `playwright install` to download browser binaries automatically.

### Q: Can I use this framework on Windows/Mac/Linux?
**A:** Yes, the framework is cross-platform compatible.

### Q: How do I update dependencies?
**A:** Run `pip install --upgrade -r requirements.txt` and `playwright install`.

---

## 🚀 Running Tests

### Q: How do I run only smoke tests?
**A:** Use `pytest -m smoke`

### Q: How do I run tests in parallel?
**A:** Use `pytest -n auto` or `pytest -n 4` for 4 workers.

### Q: How do I run tests in headless mode?
**A:** Set `HEADLESS=true pytest` or edit `.env` file.

### Q: How do I run a specific feature file?
**A:** Use `pytest --features features/login.feature`

### Q: Tests are running too slow, how to speed up?
**A:** 
- Run in parallel: `pytest -n auto`
- Run in headless mode: `HEADLESS=true pytest`
- Run only smoke tests: `pytest -m smoke`

---

## 🐛 Debugging

### Q: Where are test logs stored?
**A:** Logs are in `reports/test_execution_YYYYMMDD_HHMMSS.log`

### Q: Where are screenshots saved?
**A:** Screenshots are in `reports/screenshots/`

### Q: How do I see browser during test execution?
**A:** Set `HEADLESS=false` in `.env` file.

### Q: How do I debug a failing test?
**A:**
1. Run with verbose: `pytest -vv -s`
2. Check logs in `reports/`
3. Review screenshots in `reports/screenshots/`
4. Run single test: `pytest -k "test_name"`

### Q: How do I add print statements for debugging?
**A:** Use `logger.info("message")` instead of `print()` for better logging.

---

## 📝 Writing Tests

### Q: How do I create a new test?
**A:** 
1. Create feature file in `features/`
2. Create page object in `pages/`
3. Create step definitions in `step_definitions/`
4. Add page fixture in `conftest.py`

### Q: Can I use regular pytest tests without BDD?
**A:** Yes, create test files in `tests/` directory.

### Q: How do I share data between steps?
**A:** Use the `context` fixture:
```python
@when('I save data')
def save_data(context):
    context['my_data'] = 'value'

@then('I use data')
def use_data(context):
    data = context['my_data']
```

### Q: How do I use test data from YAML files?
**A:**
```python
from config.config import config
user = config.get_test_user('valid')
```

---

## 🌐 Browser & Configuration

### Q: How do I switch browsers?
**A:** Set `BROWSER=firefox` or `BROWSER=webkit` in `.env` file.

### Q: Can I run tests on multiple browsers?
**A:** Yes, run separately:
```bash
BROWSER=chromium pytest
BROWSER=firefox pytest
BROWSER=webkit pytest
```

### Q: How do I change the base URL?
**A:** Edit `BASE_URL` in `.env` file.

### Q: How do I test on different environments?
**A:** Set `ENVIRONMENT=qa` or edit `config/environments/qa.yml`

### Q: How do I increase timeout?
**A:** Edit `TIMEOUT=60000` in `.env` file (value in milliseconds).

---

## 📊 Reporting

### Q: How do I generate HTML reports?
**A:** Run `pytest --html=reports/report.html`

### Q: How do I generate Allure reports?
**A:**
```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

### Q: Where can I find test videos?
**A:** Videos are in `reports/videos/` (if video recording is enabled).

### Q: How do I enable video recording?
**A:** Set `VIDEO=on` in `.env` file.

---

## 🔄 CI/CD

### Q: Can I use this in GitHub Actions?
**A:** Yes, see [CI/CD Integration](ci-cd-integration.md) documentation.

### Q: How do I run tests in Docker?
**A:** Use the Playwright Docker image:
```dockerfile
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy
```

### Q: How do I run tests headless in CI?
**A:** Set `HEADLESS=true` in CI environment variables.

---

## ⚠️ Common Issues

### Q: "Browser not found" error
**A:** Run `playwright install chromium`

### Q: "Module not found" error
**A:** Ensure virtual environment is activated and dependencies installed.

### Q: Tests pass locally but fail in CI
**A:** 
- Ensure headless mode is enabled in CI
- Check timeouts (CI may be slower)
- Verify environment variables are set

### Q: Element not found errors
**A:**
- Increase timeout
- Use proper waits instead of sleeps
- Verify selectors are correct

### Q: Flaky tests
**A:** 
- Use `pytest --reruns 3` to retry
- Add proper waits
- Check for race conditions

---

## 🎯 Best Practices

### Q: Should I use CSS or XPath selectors?
**A:** Prefer CSS selectors. Use data-testid attributes when possible.

### Q: How do I handle dynamic elements?
**A:** Use Playwright's auto-waiting or explicit waits:
```python
self.wait_for_element(selector, 'visible')
```

### Q: Should I use sleep() in tests?
**A:** No, use proper waits instead:
```python
# Bad
time.sleep(5)

# Good
self.wait_for_element(selector, 'visible')
```

### Q: How do I organize page objects?
**A:** One page object per page, inherit from BasePage.

---

## 🔐 Security

### Q: How do I handle sensitive data?
**A:** 
- Use `.env` file (not committed to git)
- Use environment variables
- Never hardcode credentials

### Q: Is it safe to commit .env file?
**A:** No, `.env` is in `.gitignore`. Commit `.env.example` instead.

---

## 📚 Learning

### Q: I'm new to BDD, where do I start?
**A:** 
1. Read [Quick Start Guide](quick-start.md)
2. Review [Test Examples](examples/test-examples.md)
3. Study existing feature files

### Q: I'm new to Playwright, where do I learn?
**A:** 
- [Playwright Documentation](https://playwright.dev/python/)
- Review `BasePage` methods
- Study existing page objects

### Q: Where can I find more examples?
**A:** Check `features/` and `step_definitions/` directories.

---

## 🆘 Getting Help

### Q: Where do I report bugs?
**A:** Create an issue in the repository.

### Q: How do I request new features?
**A:** Create a feature request in the repository.

### Q: Where can I ask questions?
**A:** 
- Check this FAQ
- Review documentation
- Create a discussion in the repository

---

## 📖 Related Documentation

- [Installation Guide](installation.md)
- [Quick Start](quick-start.md)
- [Usage Guide](usage.md)
- [Troubleshooting](troubleshooting.md)
