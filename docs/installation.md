# Installation Guide

This guide will help you set up the Playwright BDD Test Automation Framework.

## 📋 Prerequisites

Before installing the framework, ensure you have:

- **Python 3.8 or higher**
  ```bash
  python --version
  ```

- **pip** (Python package manager)
  ```bash
  pip --version
  ```

- **Git** (for cloning the repository)
  ```bash
  git --version
  ```

---

## 🔧 Installation Steps

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd playwright-bdd-framework
```

### Step 2: Create Virtual Environment (Recommended)

Creating a virtual environment isolates your project dependencies.

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs all required packages:
- playwright
- pytest and pytest plugins
- allure-pytest
- python-dotenv
- faker
- pyyaml

### Step 4: Install Playwright Browsers

```bash
playwright install
```

This downloads browser binaries for Chromium, Firefox, and WebKit.

**Install specific browser only:**
```bash
playwright install chromium
playwright install firefox
playwright install webkit
```

**Install with system dependencies (Linux):**
```bash
playwright install --with-deps
```

### Step 5: Configure Environment

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` file with your settings:

```env
ENVIRONMENT=dev
BROWSER=chromium
HEADLESS=false
BASE_URL=https://your-app-url.com
TIMEOUT=30000
SLOW_MO=0
VIDEO=on_failure
SCREENSHOT=only-on-failure
LOG_LEVEL=INFO
```

### Step 6: Verify Installation

Run a test to verify everything is working:

```bash
pytest --collect-only
```

This should list all available tests without running them.

---

## 🐳 Docker Installation (Optional)

If you prefer using Docker:

**Create Dockerfile:**
```dockerfile
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["pytest"]
```

**Build and run:**
```bash
docker build -t playwright-bdd .
docker run -it playwright-bdd pytest -m smoke
```

---

## 🔍 Verify Installation

### Check Python packages:
```bash
pip list | grep -E "playwright|pytest|allure"
```

### Check Playwright browsers:
```bash
playwright --version
```

### Run smoke tests:
```bash
pytest -m smoke --collect-only
```

---

## ⚙️ IDE Setup

### VS Code

**Recommended Extensions:**
- Python
- Playwright Test for VSCode
- Gherkin (Cucumber)
- YAML

**Settings (.vscode/settings.json):**
```json
{
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true
}
```

### PyCharm

1. Open project in PyCharm
2. Set Python interpreter to virtual environment
3. Install Gherkin plugin
4. Configure pytest as test runner

---

## 🚨 Troubleshooting

### Issue: `playwright: command not found`

**Solution:** Ensure virtual environment is activated and playwright is installed:
```bash
pip install playwright
playwright install
```

### Issue: Browser download fails

**Solution:** Check internet connection and try:
```bash
playwright install --force
```

### Issue: Import errors

**Solution:** Ensure you're in the project root and virtual environment is activated:
```bash
cd playwright-bdd-framework
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### Issue: Permission denied (Linux/Mac)

**Solution:** Use sudo for system dependencies:
```bash
sudo playwright install-deps
```

---

## 📦 Dependencies Explained

| Package | Version | Purpose |
|---------|---------|---------|
| playwright | 1.40.0 | Browser automation |
| pytest | 7.4.3 | Test framework |
| pytest-bdd | 6.1.1 | BDD support |
| pytest-playwright | 0.4.3 | Playwright-pytest integration |
| pytest-html | 4.1.1 | HTML reports |
| pytest-xdist | 3.5.0 | Parallel execution |
| pytest-rerunfailures | 12.0 | Retry flaky tests |
| allure-pytest | 2.13.2 | Allure reporting |
| python-dotenv | 1.0.0 | Environment variables |
| faker | 20.1.0 | Fake data generation |
| pyyaml | 6.0.1 | YAML file support |

---

## ✅ Next Steps

After successful installation:

1. **[Quick Start Guide](quick-start.md)** - Run your first test
2. **[Configuration Guide](configuration.md)** - Customize settings
3. **[Writing Tests](writing-tests.md)** - Create your own tests

---

## 🔄 Updating the Framework

To update dependencies:

```bash
pip install --upgrade -r requirements.txt
playwright install
```

To update specific package:

```bash
pip install --upgrade playwright
```

---

## 🗑️ Uninstallation

To remove the framework:

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows

# Remove project directory
cd ..
rm -rf playwright-bdd-framework
```
