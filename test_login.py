"""
test_login.py - Login funkcionalitás teljes tesztelése
Komplett példa a POM + Pytest + Allure használatára
"""

import pytest
import allure
from login_page import LoginPage
from pages.secure_area_page import SecureAreaPage


@allure.epic("Authentication")
@allure.feature("User Login")
class TestLoginFunctionality:
    """
    Login funkcionalitás tesztjei
    """

    @allure.story("Successful Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.critical
    @pytest.mark.login
    def test_successful_login_valid_credentials(self, login_page, valid_user):
        """
        Teszt: Sikeres bejelentkezés érvényes adatokkal

        Előfeltételek:
        - Login oldal megnyitva
        - Érvényes felhasználói adatok rendelkezésre állnak

        Lépések:
        1. Felhasználónév megadása
        2. Jelszó megadása
        3. Login gomb megnyomása
        4. Sikeres bejelentkezés ellenőrzése
        """
        with allure.step("Given: Login oldal megnyitva"):
            assert login_page.is_login_form_displayed(), "Login form nem látható"

        with allure.step("When: Bejelentkezés érvényes adatokkal"):
            secure_page = login_page.login(
                username=valid_user["username"],
                password=valid_user["password"]
            )

        with allure.step("Then: Sikeres bejelentkezés ellenőrzése"):
            assert isinstance(secure_page, SecureAreaPage), "Nem SecureAreaPage lett betöltve"
            assert secure_page.is_success_message_displayed(), "Sikeres bejelentkezési üzenet nem jelent meg"
            assert secure_page.is_logout_button_displayed(), "Logout gomb nem látható"

        # Allure attachment - success screenshot
        login_page.take_screenshot("successful_login_result")

        # További ellenőrzések
        with allure.step("Additional verifications"):
            current_url = secure_page.get_current_url()
            assert "/secure" in current_url, f"Helytelen URL: {current_url}"

            page_title = secure_page.get_page_title()
            assert "The Internet" in page_title, f"Helytelen oldal cím: {page_title}"

    @allure.story("Failed Login")
    @allure.severity(allure.severity_level.HIGH)
    @pytest.mark.regression
    @pytest.mark.login
    def test_failed_login_invalid_credentials(self, login_page, invalid_user):
        """
        Teszt: Sikertelen bejelentkezés érvénytelen adatokkal
        """
        with allure.step("Given: Login oldal megnyitva"):
            assert login_page.is_login_form_displayed()

        with allure.step("When: Bejelentkezési kísérlet érvénytelen adatokkal"):
            result_page = login_page.login(
                username=invalid_user["username"],
                password=invalid_user["password"]
            )

        with allure.step("Then: Hibaüzenet megjelenésének ellenőrzése"):
            # A result_page továbbra is LoginPage kell legyen
            assert isinstance(result_page, LoginPage), "Nem LoginPage-en maradtunk"
            assert result_page.is_invalid_credentials_displayed(), "Hibaüzenet nem jelent meg"

            error_message = result_page.get_error_message()
            allure.attach(error_message, name="Error Message", attachment_type=allure.attachment_type.TEXT)

        with allure.step("And: Login form továbbra is látható"):
            assert result_page.is_login_form_displayed(), "Login form eltűnt"

    @allure.story("Empty Fields Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.login
    @pytest.mark.parametrize("username,password,expected_behavior", [
        ("", "", "both_empty"),
        ("tomsmith", "", "password_empty"),
        ("", "SuperSecretPassword!", "username_empty"),
    ])
    def test_empty_fields_validation(self, login_page, username, password, expected_behavior):
        """
        Teszt: Üres mezők validációjának tesztelése

        Paraméterezett teszt - többféle input kombinációval
        """
        with allure.step(f"Testing scenario: {expected_behavior}"):
            allure.dynamic.title(f"Empty fields validation - {expected_behavior}")

        with allure.step("When: Login kísérlet a megadott adatokkal"):
            result_page = login_page.login(username=username, password=password)

        with allure.step("Then: Megfelelő hibaüzenet vagy validáció"):
            # Itt általában a frontend validáció lépne életbe
            # De a the-internet.herokuapp.com nem validál, így ellenőrizzük hogy login page-en maradtunk
            assert isinstance(result_page, LoginPage), f"Nem LoginPage-en maradtunk - scenario: {expected_behavior}"

            if expected_behavior != "both_empty":
                # Ha van valami kitöltve, akkor hibaüzenet várható
                error_message = result_page.get_error_message()
                assert error_message is not None, f"Hibaüzenet hiányzik - scenario: {expected_behavior}"

    @allure.story("Login Form Validation")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.ui
    @pytest.mark.fast
    def test_login_form_elements_presence(self, login_page):
        """
        Teszt: Login form elemeinek jelenléte
        """
        with allure.step("Login form elemek ellenőrzése"):
            assert login_page.is_login_form_displayed(), "Login form nem látható"

        with allure.step("Username field ellenőrzése"):
            assert login_page.is_element_present(login_page.USERNAME_INPUT), "Username mező hiányzik"

        with allure.step("Password field ellenőrzése"):
            assert login_page.is_element_present(login_page.PASSWORD_INPUT), "Password mező hiányzik"

        with allure.step("Login button ellenőrzése"):
            assert login_page.is_element_present(login_page.LOGIN_BUTTON), "Login gomb hiányzik"

        with allure.step("Page heading ellenőrzése"):
            heading_text = login_page.get_text(login_page.PAGE_HEADING)
            assert "Login Page" in heading_text, f"Helytelen heading: {heading_text}"

    @allure.story("Login Page Navigation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_login_page_navigation(self, driver):
        """
        Teszt: Login oldal navigáció és betöltés
        """
        with allure.step("Login page inicializálás"):
            login_page = LoginPage(driver)

        with allure.step("Navigálás login oldalra"):
            login_page.open()

        with allure.step("URL ellenőrzése"):
            current_url = login_page.get_current_url()
            assert "/login" in current_url, f"Helytelen URL: {current_url}"

        with allure.step("Page title ellenőrzése"):
            page_title = login_page.get_page_title()
            assert "The Internet" in page_title, f"Helytelen title: {page_title}"

    @allure.story("Input Field Interaction")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.ui
    @pytest.mark.medium
    def test_input_field_interactions(self, login_page):
        """
        Teszt: Input mezők interakciói
        """
        test_username = "testuser123"
        test_password = "testpass456"

        with allure.step("Username mező kitöltése és ellenőrzése"):
            login_page.enter_username(test_username)
            username_value = login_page.get_attribute(login_page.USERNAME_INPUT, "value")
            assert username_value == test_username, f"Username érték nem egyezik: {username_value}"

        with allure.step("Password mező kitöltése és ellenőrzése"):
            login_page.enter_password(test_password)
            password_value = login_page.get_attribute(login_page.PASSWORD_INPUT, "value")
            assert password_value == test_password, f"Password érték nem egyezik: {password_value}"

        with allure.step("Mezők törlése"):
            login_page.type_text(login_page.USERNAME_INPUT, "", clear_first=True)
            login_page.type_text(login_page.PASSWORD_INPUT, "", clear_first=True)

            assert login_page.is_username_field_empty(), "Username mező nem üres"
            assert login_page.is_password_field_empty(), "Password mező nem üres"


# ===== SIKERTELEN TESZT PÉLDA (DEMO CÉLRA) =====

@allure.epic("Authentication")
@allure.feature("User Login")
@allure.story("Intentional Failure Demo")
class TestIntentionalFailure:
    """
    Szándékosan sikertelen teszt - screenshot demo
    """

    @pytest.mark.skip(reason="Demo teszt - szándékosan sikertelen")
    def test_intentional_failure_for_screenshot_demo(self, login_page):
        """
        Ez a teszt szándékosan sikertelen - demonstrálja az automatikus screenshot készítést
        """
        with allure.step("Szándékos assertion failure"):
            # Ez mindig sikertelen lesz - screenshot készül róla
            assert False, "Ez egy szándékos hiba a screenshot demo céljából"