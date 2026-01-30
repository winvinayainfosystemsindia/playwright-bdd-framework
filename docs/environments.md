# Environment Configuration Guide

This document explains the three environment configurations available in the framework.

## 📁 Environment Files

The framework supports three environments, each with its own configuration file:

```
config/environments/
├── dev.yml      # Development environment
├── qa.yml       # QA/Testing environment
└── prod.yml     # Production environment
```

---

## 🔧 Environment Configurations

### 1. Development Environment (`dev.yml`)

**Purpose:** Local development and initial testing

**Configuration:**
```yaml
base_url: https://dev.example.com
timeout: 30000
api_url: https://api-dev.example.com
database:
  host: dev-db.example.com
  port: 5432
  name: test_db_dev
credentials:
  admin_user: admin@dev.example.com
  admin_password: DevPass123!
features:
  new_ui: true
  beta_features: true
```

**Usage:**
```bash
ENVIRONMENT=dev pytest
# or (default)
pytest
```

---

### 2. QA Environment (`qa.yml`)

**Purpose:** Quality assurance and integration testing

**Configuration:**
```yaml
base_url: https://qa.example.com
timeout: 35000
api_url: https://api-qa.example.com
database:
  host: qa-db.example.com
  port: 5432
  name: test_db_qa
credentials:
  admin_user: admin@qa.example.com
  admin_password: QaPass123!
features:
  new_ui: true
  beta_features: true
```

**Usage:**
```bash
ENVIRONMENT=qa pytest
```

---

### 3. Production Environment (`prod.yml`)

**Purpose:** Production validation and smoke testing

**Configuration:**
```yaml
base_url: https://example.com
timeout: 40000
api_url: https://api.example.com
database:
  host: prod-db.example.com
  port: 5432
  name: test_db_prod
credentials:
  admin_user: admin@example.com
  admin_password: ProdPass123!
features:
  new_ui: false
  beta_features: false
```

**Usage:**
```bash
ENVIRONMENT=prod pytest
```

---

## 🚀 Switching Environments

### Method 1: Environment Variable

```bash
# Development
ENVIRONMENT=dev pytest

# QA
ENVIRONMENT=qa pytest

# Production
ENVIRONMENT=prod pytest
```

### Method 2: Update .env File

Edit `.env` file:
```env
ENVIRONMENT=qa
```

Then run:
```bash
pytest
```

---

## 📝 Configuration Properties

Each environment file supports the following properties:

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| `base_url` | string | Application base URL | `https://qa.example.com` |
| `timeout` | integer | Default timeout (ms) | `35000` |
| `api_url` | string | API endpoint URL | `https://api-qa.example.com` |
| `database.host` | string | Database host | `qa-db.example.com` |
| `database.port` | integer | Database port | `5432` |
| `database.name` | string | Database name | `test_db_qa` |
| `credentials.admin_user` | string | Admin username | `admin@qa.example.com` |
| `credentials.admin_password` | string | Admin password | `QaPass123!` |
| `features.new_ui` | boolean | New UI enabled | `true` |
| `features.beta_features` | boolean | Beta features enabled | `true` |

---

## 🔐 Security Best Practices

### 1. Don't Commit Sensitive Data

- Keep passwords in `.env` file (not committed)
- Use environment variables for sensitive data
- Reference secrets from CI/CD secret management

### 2. Use Different Credentials Per Environment

```yaml
# dev.yml
credentials:
  admin_user: admin@dev.example.com
  admin_password: DevPass123!

# qa.yml
credentials:
  admin_user: admin@qa.example.com
  admin_password: QaPass123!

# prod.yml
credentials:
  admin_user: admin@example.com
  admin_password: ${PROD_PASSWORD}  # From environment variable
```

---

## 🎯 Usage Examples

### Run Smoke Tests on QA

```bash
ENVIRONMENT=qa pytest -m smoke
```

### Run All Tests on Dev

```bash
ENVIRONMENT=dev pytest
```

### Run Specific Feature on Prod

```bash
ENVIRONMENT=prod pytest --features features/login.feature
```

### Run in Parallel on QA

```bash
ENVIRONMENT=qa pytest -n auto
```

---

## 🔄 Adding Custom Properties

You can add custom properties to environment files:

```yaml
# qa.yml
base_url: https://qa.example.com
timeout: 35000

# Custom properties
custom:
  payment_gateway: https://payment-qa.example.com
  email_service: https://email-qa.example.com
  max_retries: 3
  enable_logging: true
```

**Access in code:**

```python
from config.config import config

payment_url = config.env_config.get('custom', {}).get('payment_gateway')
max_retries = config.env_config.get('custom', {}).get('max_retries', 1)
```

---

## 📊 Environment Comparison

| Feature | Dev | QA | Prod |
|---------|-----|-----|------|
| **Purpose** | Development | Testing | Validation |
| **Timeout** | 30s | 35s | 40s |
| **New UI** | ✅ | ✅ | ❌ |
| **Beta Features** | ✅ | ✅ | ❌ |
| **Stability** | Low | Medium | High |
| **Test Scope** | All | All | Smoke only |

---

## 🛠️ Troubleshooting

### Issue: Wrong environment being used

**Solution:** Check `.env` file and ensure `ENVIRONMENT` variable is set correctly.

### Issue: Configuration not loading

**Solution:** Verify YAML syntax is correct:
```bash
python -c "import yaml; yaml.safe_load(open('config/environments/qa.yml'))"
```

### Issue: Missing properties

**Solution:** Ensure all required properties are defined in the environment file.

---

## 📚 Related Documentation

- [Configuration Guide](configuration.md)
- [Usage Guide](usage.md)
- [FAQ](faq.md)
