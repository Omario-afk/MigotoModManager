from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Browser:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option("detach", True)  # Keep browser open
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def navigate_to(self, url):
        self.driver.get(url)

    def check_login_status(self):
        try:
            login_element = self.driver.find_element(By.CSS_SELECTOR, "a.LoginSignup[href='/members/account/login']")
            return False  # Not logged in
        except:
            return True  # Logged in

    def get_page_source(self):
        return self.driver.page_source

    def close(self):
        self.driver.quit()
