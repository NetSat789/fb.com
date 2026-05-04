# 🧪 Facebook Login Automation - Playwright + Python (Data-Driven)

A data-driven test automation framework for testing the Facebook login page using **Playwright** and **Python** with the **Page Object Model (POM)** design pattern.

---

## 📁 Project Structure

```
fb-login-automation/
├── config/
│   └── config.json              # Browser & test configuration
├── pages/
│   ├── __init__.py
│   ├── base_page.py             # Base page with common methods
│   └── login_page.py            # Facebook Login Page Object
├── test_data/
│   ├── login_data.json          # Test data (JSON format)
│   └── login_data.csv           # Test data (CSV format)
├── tests/
│   ├── __init__.py
│   ├── test_login.py            # Data-driven login tests
│   └── test_login_page_ui.py    # UI element validation tests
├── utils/
│   ├── __init__.py
│   ├── config_reader.py         # Configuration reader utility
│   └── data_reader.py           # Multi-format data reader
├── screenshots/                 # Auto-captured failure screenshots
├── reports/                     # HTML test reports
├── conftest.py                  # Pytest fixtures & hooks
├── pytest.ini                   # Pytest configuration
└── requirements.txt             # Python dependencies
```

---

## 🚀 Setup & Installation

### 1. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Playwright Browsers
```bash
playwright install
```

---

## ▶️ Running Tests

### Run All Tests
```bash
pytest
```

### Run Only Data-Driven Login Tests
```bash
pytest tests/test_login.py
```

### Run Only UI Validation Tests
```bash
pytest tests/test_login_page_ui.py
```

### Run by Marker
```bash
pytest -m smoke           # Smoke tests only
pytest -m regression      # Regression tests only
pytest -m login           # Login tests only
```

### Run a Specific Test Case
```bash
pytest tests/test_login.py -k "TC_LOGIN_001"
```

### Run in Headed Mode (visible browser)
Set `"headless": false` in `config/config.json` (default).

### Run in Parallel
```bash
pytest -n 3               # Run with 3 parallel workers
```

---

## 📊 Test Data

Test data is stored in `test_data/` in both **JSON** and **CSV** formats:

| Test ID       | Description                         | Type     |
|---------------|-------------------------------------|----------|
| TC_LOGIN_001  | Valid login with correct credentials| positive |
| TC_LOGIN_002  | Invalid login with wrong password   | negative |
| TC_LOGIN_003  | Unregistered email login            | negative |
| TC_LOGIN_004  | Empty email field                   | negative |
| TC_LOGIN_005  | Empty password field                | negative |
| TC_LOGIN_006  | Both fields empty                   | negative |
| TC_LOGIN_007  | Invalid email format                | negative |
| TC_LOGIN_008  | SQL injection attempt               | security |

### Switch Data Source
In `tests/test_login.py`, change the source parameter:
```python
login_data = DataReader.get_login_test_data(source="json")   # or "csv" or "excel"
```

---

## 📸 Reports & Screenshots

- **HTML Report**: Auto-generated at `reports/report.html`
- **Failure Screenshots**: Auto-captured in `screenshots/` directory

---

## ⚙️ Configuration

Edit `config/config.json` to customize:

| Setting                | Description                    | Default    |
|------------------------|--------------------------------|------------|
| `base_url`             | Target application URL         | fb.com     |
| `browser`              | Browser type                   | chromium   |
| `headless`             | Run without UI                 | false      |
| `slow_mo`              | Delay between actions (ms)     | 500        |
| `timeout`              | Default timeout (ms)           | 30000      |
| `screenshot_on_failure`| Auto screenshot on fail        | true       |

---

## 🏗️ Architecture

- **Page Object Model (POM)** - Clean separation of locators and test logic
- **Data-Driven Testing** - Test data externalized to JSON/CSV/Excel
- **Fluent API** - Chainable page methods for readable tests
- **Auto Screenshot** - Captures screenshots on test failures
- **HTML Reports** - Rich test execution reports via pytest-html
