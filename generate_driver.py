from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

def get_preconfigured_chrome_driver():
    options = Options()

    # Ha CI-ben futunk (pl. GitHub Actions vagy HEADLESS változó van megadva)
    if os.getenv("CI") == "true" or os.getenv("HEADLESS", "false").lower() == "true":
        options.add_argument("--headless=new")  # új headless mód
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
    else:
        # Lokális futásnál csak amit tényleg szükséges
        options.add_experimental_option("detach", True)  # csak lokálban kell
        options.add_argument("lang=en")

    # NE használj user-data-dir-t!
    browser = webdriver.Chrome(options=options)
    browser.maximize_window()
    return browser