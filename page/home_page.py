import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from general_page import GeneralPage

class HomePage(GeneralPage):
    def __init__(self):
        self.URL = 'https://the-internet.herokuapp.com/'
        super().__init__(self.URL)

    def link_ab(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/abtest"]')))

    def link_add_remove_elements(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/add_remove_elements/"]')))

    def link_basic_auth(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/basic_auth"]')))

    def link_broken_images(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/broken_images"]')))

    def link_challenging_dom(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/challenging_dom"]')))

    def link_checkboxes(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/checkboxes"]')))

    def link_context_menu(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/context_menu" and text()="Context Menu"]')))

    def link_digest_auth(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/digest_auth" and text()="Digest Authentication"]')))

    def link_disappearing_elements(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/disappearing_elements" and text()="Disappearing Elements"]')))

    def link_drag_and_drop(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/drag_and_drop" and text()="Drag and Drop"]')))

