"""
conftest.py - Pytest fixtures és konfigurációk
Ez a fájl automatikusan betöltődik minden test futtatáskor
"""

import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import json
import os
from datetime import datetime


# ===== PYTEST CONFIGURATION =====

def pytest_addoption(parser):
    """
    Pytest command line opciók hozzáadása
    Használat: pytest --browser=chrome --headless
    """
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser choice: chrome, firefox, edge"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="https://the-internet.herokuapp.com",
        help="Base URL for testing"
    )


# ===== WEBDRIVER FIXTURES =====

@pytest.fixture(scope="session")
def browser_config(request):
    """
    Session scope fixture - egyszer fut le az egész teszt session során
    Browser konfigurációs adatok
    """
    return {
        "browser": request.config.getoption("--browser"),
        "headless": request.config.getoption("--headless"),
        "base_url": request.config.getoption("--base-url")
    }


@pytest.fixture(scope="function")
def driver(browser_config):
    """
    Function scope fixture - minden teszt függvényhez új WebDriver
    WebDriver inicializálás és teardown
    """
    browser = browser_config["browser"].lower()
    headless = browser_config["headless"]

    driver = None

    try:
        if browser == "chrome":
            driver = _setup_chrome_driver(headless)
        elif browser == "firefox":
            driver = _setup_firefox_driver(headless)
        else:
            raise ValueError(f"Nem támogatott browser: {browser}")

        # WebDriver konfigurálás
        driver.maximize_window()
        driver.implicitly_wait(10)

        # Allure-hoz browser info csatolása
        allure.attach(
            f"Browser: {browser.title()}\nHeadless: {headless}",
            name="Browser Configuration",
            attachment_type=allure.attachment_type.TEXT
        )

        yield driver  # Itt adja vissza a driver-t a testnek

    finally:
        # Cleanup - driver bezárása
        if driver:
            driver.quit()


def _setup_chrome_driver(headless=False):
    """Chrome WebDriver setup"""
    options = Options()

    if headless:
        options.add_argument("--headless")

    # Chrome optimalizációs beállítások
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # WebDriver Manager automatikus driver letöltés
    service = Service(ChromeDriverManager().install())

    return webdriver.Chrome(service=service, options=options)


def _setup_firefox_driver(headless=False):
    """Firefox WebDriver setup"""
    options = FirefoxOptions()

    if headless:
        options.add_argument("--headless")

    options.add_argument("--width=1920")
    options.add_argument("--height=1080")

    service = FirefoxService(GeckoDriverManager().install())

    return webdriver.Firefox(service=service, options=options)


# ===== PAGE OBJECT FIXTURES =====

@pytest.fixture(scope="function")
def login_page(driver):
    """
    Login Page Object fixture
    Automatikusan megnyitja a login oldalt
    """
    from page.login_page import LoginPage
    page = LoginPage(driver)
    page.open()  # Automatikusan megnyitja az oldalt
    return page


@pytest.fixture(scope="function")
def dropdown_page(driver):
    """Dropdown Page Object fixture"""
    from pages.dropdown_page import DropdownPage
    page = DropdownPage(driver)
    page.open()
    return page


# ===== TEST DATA FIXTURES =====

@pytest.fixture(scope="session")
def test_users():
    """
    Test user adatok betöltése JSON fájlból
    Session scope - egyszer töltődik be
    """
    test_data_path = os.path.join(os.path.dirname(__file__), "test_data", "users.json")

    try:
        with open(test_data_path, 'r', encoding='utf-8') as file:
            users_data = json.load(file)
            return users_data
    except FileNotFoundError:
        # Fallback adatok ha nincs JSON fájl
        return {
            "valid_user": {
                "username": "tomsmith",
                "password": "SuperSecretPassword!"
            },
            "invalid_user": {
                "username": "invalid_user",
                "password": "wrong_password"
            }
        }


@pytest.fixture(scope="function")
def valid_user(test_users):
    """Érvényes felhasználó adatok"""
    return test_users["valid_user"]


@pytest.fixture(scope="function")
def invalid_user(test_users):
    """Érvénytelen felhasználó adatok"""
    return test_users["invalid_user"]


# ===== ALLURE REPORTING FIXTURES =====

@pytest.fixture(autouse=True)
def setup_allure_environment(request, browser_config):
    """
    Automatikusan futó fixture - minden teszthez
    Allure környezeti információk beállítása
    """
    # Test információk Allure-hoz
    allure.dynamic.parameter("Browser", browser_config["browser"])
    allure.dynamic.parameter("Headless", browser_config["headless"])
    allure.dynamic.parameter("Base URL", browser_config["base_url"])

    # Test kezdési idő
    allure.attach(
        str(datetime.now()),
        name="Test Start Time",
        attachment_type=allure.attachment_type.TEXT
    )


# ===== HOOKS - Pytest esemény kezelők =====

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook - minden teszt befejezése után fut
    Screenshot készítése sikertelen tesztek esetén
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Sikertelen teszt esetén screenshot
        driver = None

        # Driver keresése a fixtures között
        if hasattr(item, 'funcargs'):
            driver = item.funcargs.get('driver', None)

        if driver:
            # Screenshot készítése és csatolása
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"screenshot_failure_{item.name}",
                attachment_type=allure.attachment_type.PNG
            )

            # HTML source csatolása debug célból
            allure.attach(
                driver.page_source,
                name=f"html_source_failure_{item.name}",
                attachment_type=allure.attachment_type.HTML
            )

            # Browser log csatolása
            try:
                browser_logs = driver.get_log('browser')
                if browser_logs:
                    log_text = "\n".join([f"{log['level']}: {log['message']}" for log in browser_logs])
                    allure.attach(
                        log_text,
                        name=f"browser_logs_failure_{item.name}",
                        attachment_type=allure.attachment_type.TEXT
                    )
            except Exception:
                pass  # Nem minden browser támogatja a log funkciót


# ===== UTILITY FIXTURES =====

@pytest.fixture(scope="function")
def wait_time():
    """Várakozási idő konfiguráció"""
    return {
        "short": 2,
        "medium": 5,
        "long": 10
    }


@pytest.fixture(scope="session")
def base_url(browser_config):
    """Alap URL fixture"""
    return browser_config["base_url"]