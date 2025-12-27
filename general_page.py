from selenium.webdriver.support.wait import WebDriverWait
import os
from datetime import datetime
from generate_driver import get_preconfigured_chrome_driver


class GeneralPage(object):
    def __init__(self, url, browser=None):
        self.URL = url
        if browser is None:
            self.browser = get_preconfigured_chrome_driver()
        else:
            self.browser = browser


    # ===== BROWSER MANAGEMENT =====
    def get(self):
        """Navigate to page"""
        self.browser.get(self.URL)

    def refresh_page(self):
        """Refresh current page"""
        self.browser.refresh()

    def go_back(self):
        """Browser back button"""
        self.browser.back()

    def go_forward(self):
        """Browser forward button"""
        self.browser.forward()

    # ===== PAGE INFORMATION =====
    def get_current_url(self):
        """Get current page URL"""
        return self.browser.current_url

    def get_page_title(self):
        """Get page title"""
        return self.browser.title

    # ===== SCROLLING UTILITIES =====
    def scroll_to_top(self):
        """Scroll to top of page"""
        self.browser.execute_script("window.scrollTo(0, 0);")

    def scroll_to_bottom(self):
        """Scroll to bottom of page"""
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_to_element(self, element):
        """Scroll to specific element"""
        self.browser.execute_script("arguments[0].scrollIntoView();", element)

    # ===== DEBUGGING & LOGGING =====
    def screenshot(self, filename=None):
        """Take screenshot"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        os.makedirs("screenshots", exist_ok=True)
        filepath = os.path.join("screenshots", filename)
        self.browser.save_screenshot(filepath)
        return filepath

    def save_logs(self, filename=None):
        """Save browser logs"""
        # TODO: Implement later when needed
        # if filename is None:
        #     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        #     filename = f"logs_{timestamp}.txt"
        #
        # os.makedirs("logs", exist_ok=True)
        # filepath = os.path.join("logs", filename)
        #
        # try:
        #     browser_logs = self.browser.get_log('browser')
        #     with open(filepath, 'w', encoding='utf-8') as f:
        #         f.write(f"=== BROWSER LOGS - {datetime.now()} ===\n")
        #         f.write(f"URL: {self.get_current_url()}\n")
        #         f.write("=" * 50 + "\n\n")
        #
        #         for log in browser_logs:
        #             timestamp = log.get('timestamp', 'Unknown')
        #             level = log.get('level', 'INFO')
        #             message = log.get('message', '')
        #             f.write(f"[{timestamp}] {level}: {message}\n")
        #
        #     return filepath
        # except Exception as e:
        #     print(f"Log saving error: {str(e)}")
        #     return None
        pass

    def capture_evidence(self, test_name="test"):
        """Take screenshot + save logs"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = self.screenshot(f"{test_name}_{timestamp}.png")
        # log_path = self.save_logs(f"{test_name}_{timestamp}.txt")
        return {'screenshot': screenshot_path}  # , 'logs': log_path}

    # ===== CLEANUP =====
    def close(self):
        """Close current tab"""
        self.browser.close()

    def quit(self):
        """Close browser"""
        self.browser.quit()