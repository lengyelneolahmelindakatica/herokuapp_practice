import sys
import os
from page.home_page import HomePage
# Project root hozzáadása a Python path-hoz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestSmoke(object):
    def setup_method(self):
        self.homepage = HomePage()
        self.homepage.get()

    def teardown_method(self):
        self.homepage.quit()

    def test_smoke(self):
        assert self.homepage.link_ab().is_displayed()
        assert self.homepage.link_add_remove_elements().is_displayed()
        assert self.homepage.link_basic_auth().is_displayed()
        assert self.homepage.link_broken_images().is_displayed()
        assert self.homepage.link_challenging_dom().is_displayed()
        assert self.homepage.link_checkboxes().is_displayed()
        assert self.homepage.link_context_menu().is_displayed()
        assert self.homepage.link_digest_auth().is_displayed()
        assert self.homepage.link_disappearing_elements().is_displayed()
        assert self.homepage.link_drag_and_drop().is_displayed()


