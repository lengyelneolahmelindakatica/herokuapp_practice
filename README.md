# The Internet (Herokuapp) – POM UI Test Suite

End-to-end UI tests for [the-internet.herokuapp.com](https://the-internet.herokuapp.com/) implemented with a **Page Object Model (POM)** architecture.

## ✨ Features
- Page Object Model with clear separation of concerns
- Pytest test runner + fixtures
- Selenium WebDriver setup with configurable browsers
- Useful helpers: waits, screenshots on failure, test data
- GitHub Actions CI workflow (optional snippet below)
- Allure (or HTML) report generation

## 🧰 Tech Stack
- Python 3.11+
- Selenium WebDriver
- Pytest
- (Optional) Allure / pytest-html
- (Optional) Black + Flake8 linters

## 📁 Project Structure
project/
├── tests/
│   ├── conftest.py
│   ├── test_login.py
│   ├── test_dropdown.py
│   └── ...
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   ├── dropdown_page.py
│   └── ...
├── utils/
│   └── helpers.py
├── reports/
├── requirements.txt
├── pytest.ini
└── .github/workflows/
    └── ci.yml
