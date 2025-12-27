"""
Login Page Object - the-internet.herokuapp.com login oldal
POM implementáció példa
"""

from selenium.webdriver.common.by import By
import allure
from page.base_page import BasePage


class LoginPage(BasePage):
    """
    Login oldal Page Object
    URL: https://the-internet.herokuapp.com/login
    """

    # ===== LOCATORS (Element azonosítók) =====
    # Minden elem locator-ja egy helyen, könnyen karbantartható

    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    # Flash üzenetek
    FLASH_MESSAGE = (By.ID, "flash")
    SUCCESS_MESSAGE_TEXT = "You logged into a secure area!"
    INVALID_CREDENTIALS_TEXT = "Your username is invalid!"

    # Oldal azonosítók
    LOGIN_FORM = (By.ID, "login")
    PAGE_HEADING = (By.TAG_NAME, "h2")

    def __init__(self, driver):
        """Inicializálás - meghívja a BasePage konstruktorát"""
        super().__init__(driver)
        self.url = "https://the-internet.herokuapp.com/login"

    # ===== PAGE ACTIONS (Oldal műveletek) =====

    @allure.step("Login oldal megnyitása")
    def open(self):
        """Login oldal megnyitása"""
        self.navigate_to(self.url)
        self._verify_page_loaded()
        return self

    @allure.step("Felhasználónév beírása: {username}")
    def enter_username(self, username):
        """
        Felhasználónév beírása
        :param username: A beírandó felhasználónév
        """
        self.type_text(self.USERNAME_INPUT, username)
        return self

    @allure.step("Jelszó beírása")
    def enter_password(self, password):
        """
        Jelszó beírása (nem logoljuk a jelszót biztonsági okokból)
        :param password: A beírandó jelszó
        """
        self.type_text(self.PASSWORD_INPUT, password)
        return self

    @allure.step("Login gombra klikkelés")
    def click_login_button(self):
        """Login gomb megnyomása"""
        self.click(self.LOGIN_BUTTON)
        return self

    @allure.step("Teljes bejelentkezési folyamat: {username}")
    def login(self, username, password):
        """
        Teljes login folyamat egy lépésben
        :param username: Felhasználónév
        :param password: Jelszó
        :return: Következő oldal (SecureAreaPage vagy marad LoginPage)
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

        # Ha sikeres a login, SecureAreaPage-re navigálunk
        if self.is_login_successful():
            from pages.secure_area_page import SecureAreaPage
            return SecureAreaPage(self.driver)

        # Ha sikertelen, maradunk a LoginPage-en
        return self

    # ===== VERIFICATIONS (Ellenőrzések) =====

    @allure.step("Login sikerességének ellenőrzése")
    def is_login_successful(self):
        """
        Ellenőrzi, hogy sikeres volt-e a bejelentkezés
        :return: True ha sikeres, False ha sikertelen
        """
        try:
            flash_text = self.get_text(self.FLASH_MESSAGE)
            return self.SUCCESS_MESSAGE_TEXT in flash_text
        except:
            return False

    @allure.step("Hibaüzenet ellenőrzése")
    def get_error_message(self):
        """
        Hibaüzenet szövegének lekérése
        :return: A hibaüzenet szövege
        """
        try:
            return self.get_text(self.FLASH_MESSAGE)
        except:
            return None

    @allure.step("Érvénytelen bejelentkezési adatok ellenőrzése")
    def is_invalid_credentials_displayed(self):
        """
        Ellenőrzi, hogy megjelent-e az érvénytelen adatok hibaüzenete
        """
        try:
            flash_text = self.get_text(self.FLASH_MESSAGE)
            return self.INVALID_CREDENTIALS_TEXT in flash_text
        except:
            return False

    @allure.step("Login form jelenléte")
    def is_login_form_displayed(self):
        """Ellenőrzi, hogy a login form látható-e"""
        return self.is_element_visible(self.LOGIN_FORM)

    @allure.step("Felhasználónév mező ürességének ellenőrzése")
    def is_username_field_empty(self):
        """Ellenőrzi, hogy a felhasználónév mező üres-e"""
        username_value = self.get_attribute(self.USERNAME_INPUT, "value")
        return username_value == ""

    @allure.step("Jelszó mező ürességének ellenőrzése")
    def is_password_field_empty(self):
        """Ellenőrzi, hogy a jelszó mező üres-e"""
        password_value = self.get_attribute(self.PASSWORD_INPUT, "value")
        return password_value == ""

    # ===== PRIVATE METHODS (Belső metódusok) =====

    @allure.step("Oldal betöltésének ellenőrzése")
    def _verify_page_loaded(self):
        """
        Privát metódus - ellenőrzi hogy az oldal teljesen betöltött-e
        """
        # Várakozás a login form megjelenésére
        assert self.is_element_visible(self.LOGIN_FORM), "Login form nem található!"

        # Oldal címének ellenőrzése
        expected_title = "The Internet"
        actual_title = self.get_page_title()
        assert expected_title in actual_title, f"Helytelen oldal cím: {actual_title}"

        # URL ellenőrzése
        current_url = self.get_current_url()
        assert self.url in current_url, f"Helytelen URL: {current_url}"