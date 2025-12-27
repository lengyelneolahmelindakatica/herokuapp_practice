"""
Base Page Class - A POM alapja
Minden page object ebből örököl, közös funkcionalitásokat tartalmaz
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import allure
import time


class BasePage:
    """
    Base page osztály - minden page object ebből örököl
    Tartalmazza a közös WebDriver műveleteket
    """

    def __init__(self, driver, timeout=10):
        """
        Inicializálás
        :param driver: WebDriver instance
        :param timeout: Implicit wait timeout
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    @allure.step("Navigálás URL-re: {url}")
    def navigate_to(self, url):
        """Navigálás megadott URL-re"""
        self.driver.get(url)
        return self

    @allure.step("Elem keresése: {locator}")
    def find_element(self, locator):
        """
        Elem keresése
        :param locator: Tuple (By.ID, "element_id") formátumban
        :return: WebElement
        """
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="element_not_found_screenshot",
                attachment_type=allure.attachment_type.PNG
            )
            raise TimeoutException(f"Element {locator} nem található {self.timeout} másodperc alatt")

    @allure.step("Elemek keresése: {locator}")
    def find_elements(self, locator):
        """Több elem keresése"""
        return self.driver.find_elements(*locator)

    @allure.step("Klikkelés elemre: {locator}")
    def click(self, locator):
        """
        Klikk egy elemre - megvárja hogy klikkelhető legyen
        """
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            return self
        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="click_failed_screenshot",
                attachment_type=allure.attachment_type.PNG
            )
            raise TimeoutException(f"Nem lehet klikkelni az elemre: {locator}")

    @allure.step("Szöveg beírása: '{text}' -> {locator}")
    def type_text(self, locator, text, clear_first=True):
        """
        Szöveg beírása egy input mezőbe
        :param locator: Element locator
        :param text: Beírandó szöveg
        :param clear_first: Törli-e előbb a mező tartalmát
        """
        element = self.find_element(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
        return self

    @allure.step("Szöveg lekérése elemből: {locator}")
    def get_text(self, locator):
        """Element szövegének lekérése"""
        element = self.find_element(locator)
        return element.text

    @allure.step("Attribútum lekérése: {attribute} -> {locator}")
    def get_attribute(self, locator, attribute):
        """Element attribútumának lekérése"""
        element = self.find_element(locator)
        return element.get_attribute(attribute)

    @allure.step("Elem látható-e: {locator}")
    def is_element_visible(self, locator):
        """
        Ellenőrzi, hogy egy elem látható-e
        """
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    @allure.step("Elem jelenléte: {locator}")
    def is_element_present(self, locator):
        """Ellenőrzi, hogy elem jelen van-e a DOM-ban"""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    @allure.step("Várakozás elem eltűnésére: {locator}")
    def wait_for_element_to_disappear(self, locator):
        """Megvárja hogy egy elem eltűnjön"""
        try:
            self.wait.until(EC.invisibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    @allure.step("Dropdown kiválasztás: '{option_text}' -> {locator}")
    def select_dropdown_by_text(self, locator, option_text):
        """Dropdown option kiválasztása szöveg alapján"""
        dropdown_element = self.find_element(locator)
        select = Select(dropdown_element)
        select.select_by_visible_text(option_text)
        return self

    @allure.step("Dropdown kiválasztás index alapján: {index} -> {locator}")
    def select_dropdown_by_index(self, locator, index):
        """Dropdown option kiválasztása index alapján"""
        dropdown_element = self.find_element(locator)
        select = Select(dropdown_element)
        select.select_by_index(index)
        return self

    @allure.step("Screenshot készítése")
    def take_screenshot(self, name="screenshot"):
        """Screenshot készítése és csatolása az Allure riporthoz"""
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )

    @allure.step("Scroll elemhez: {locator}")
    def scroll_to_element(self, locator):
        """Görgetés egy elemhez"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        return self

    @allure.step("Oldal címének lekérése")
    def get_page_title(self):
        """Oldal title-jének lekérése"""
        return self.driver.title

    @allure.step("Aktuális URL lekérése")
    def get_current_url(self):
        """Aktuális URL lekérése"""
        return self.driver.current_url