# Contributing to Playwright BDD Framework

Thank you for your interest in contributing to the Playwright BDD Test Automation Framework! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Feature Requests](#feature-requests)

---

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment tool

### Setup Development Environment

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/playwright-bdd-framework.git
   cd playwright-bdd-framework
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

---

## Development Process

### Branching Strategy

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Urgent production fixes

### Workflow

1. Create a branch from `develop`
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Run tests and quality checks
   ```bash
   pytest
   black .
   flake8 .
   pylint pages/ utils/ config/
   ```

4. Commit your changes
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

5. Push and create Pull Request
   ```bash
   git push origin feature/your-feature-name
   ```

---

## Coding Standards

### Python Style Guide

- Follow **PEP 8** style guide
- Use **Black** for code formatting (line length: 120)
- Use **isort** for import sorting
- Use **type hints** where applicable

### Code Quality

- **Pylint score**: Maintain > 8.0
- **Code coverage**: Maintain > 80%
- **Complexity**: Keep cyclomatic complexity < 10

### Documentation

- Add docstrings to all classes and functions
- Use Google-style docstrings
- Update README.md for significant changes
- Add inline comments for complex logic

### Example

```python
def calculate_total(items: List[Dict], tax_rate: float = 0.1) -> float:
    """
    Calculate total price including tax.
    
    Args:
        items: List of item dictionaries with 'price' key
        tax_rate: Tax rate as decimal (default: 0.1)
        
    Returns:
        Total price including tax
        
    Raises:
        ValueError: If items list is empty
    """
    if not items:
        raise ValueError("Items list cannot be empty")
        
    subtotal = sum(item['price'] for item in items)
    return subtotal * (1 + tax_rate)
```

---

## Testing Guidelines

### Writing Tests

1. **Feature Files**
   - Use descriptive scenario names
   - Follow Given-When-Then format
   - Add appropriate tags (@smoke, @regression)

2. **Step Definitions**
   - Keep steps atomic and reusable
   - Use parsers for parameterization
   - Add proper logging

3. **Page Objects**
   - One page object per page
   - Use descriptive method names
   - Centralize locators as class constants

### Running Tests

```bash
# All tests
pytest

# Specific marker
pytest -m smoke

# With coverage
pytest --cov=pages --cov=utils --cov-report=html

# Code quality
black --check .
flake8 .
pylint pages/ utils/ config/
bandit -r pages/ utils/ config/
```

---

## Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Code coverage maintained/improved
- [ ] Documentation updated
- [ ] Commit messages follow convention
- [ ] Pre-commit hooks pass

### PR Template

Use the provided PR template and fill all sections:
- Description of changes
- Type of change
- Testing performed
- Screenshots (if UI changes)
- Checklist completion

### Review Process

1. Automated checks must pass (CI/CD)
2. At least one approval required
3. No unresolved comments
4. Branch up-to-date with base branch

---

## Commit Message Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements
- `ci`: CI/CD changes

### Examples

```
feat(login): add remember me functionality

Implemented remember me checkbox on login page
with session persistence using local storage.

Closes #123
```

```
fix(screenshot): resolve screenshot capture timing issue

Fixed race condition in screenshot helper that caused
intermittent failures when capturing on test failure.

Fixes #456
```

---

## Reporting Bugs

### Before Reporting

1. Check existing issues
2. Verify bug in latest version
3. Collect reproduction steps

### Bug Report Template

Use the bug report template and include:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Screenshots/logs

---

## Feature Requests

### Proposing Features

1. Check existing feature requests
2. Discuss in issues first
3. Provide clear use case
4. Consider implementation impact

### Feature Request Template

Use the feature request template and include:
- Problem statement
- Proposed solution
- Alternatives considered
- Additional context

---

## Code Review Guidelines

### For Authors

- Keep PRs focused and small
- Provide context in description
- Respond to feedback promptly
- Update PR based on comments

### For Reviewers

- Be constructive and respectful
- Focus on code quality and maintainability
- Test changes locally when needed
- Approve only when satisfied

---

## Questions?

- Open a discussion on GitHub
- Contact maintainers
- Check documentation

Thank you for contributing! 🎉
