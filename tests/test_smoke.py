import sys
import os
import allure

from page.home_page import HomePage
# Project root hozzáadása a Python path-hoz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@allure.epic("Homepage Testing")
@allure.feature("Link Verification")
class TestSmoke(object):  # Test prefix kell pytest-hez

    def setup_method(self):
        self.homepage = HomePage()
        self.homepage.get()

    def teardown_method(self):
        self.homepage.quit()

    @allure.story("Smoke Test - All Links Present")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_smoke_all_links_displayed(self):
        """Verify all homepage links are displayed"""

        with allure.step("Verify A/B Testing link"):
            assert self.homepage.link_ab().is_displayed()

        with allure.step("Verify Add/Remove Elements link"):
            assert self.homepage.link_add_remove_elements().is_displayed()

        with allure.step("Verify Basic Auth link"):
            assert self.homepage.link_basic_auth().is_displayed()

        with allure.step("Verify Broken Images link"):
            assert self.homepage.link_broken_images().is_displayed()

        with allure.step("Verify Challenging Dom link"):
            assert self.homepage.link_challenging_dom().is_displayed()

        with allure.step("Verify Checkboxes link"):
            assert self.homepage.link_checkboxes().is_displayed()

        with allure.step("Verify Context Menu link"):
            assert self.homepage.link_context_menu().is_displayed()

        with allure.step("Verify Digest Auth link"):
            assert self.homepage.link_digest_auth().is_displayed()

        with allure.step("Verify Disappearing Elements link"):
            assert self.homepage.link_disappearing_elements().is_displayed()

        with allure.step("Verify Drag and Drop"):
            assert self.homepage.link_drag_and_drop().is_displayed()

