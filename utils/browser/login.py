from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class LoginManager:
    def __init__(self, browser):
        self.browser = browser
        self.login_url = "https://gamebanana.com/members/account/login"

    def check_and_redirect(self):
        if not self.browser.check_login_status():
            self.browser.navigate_to(self.login_url)
            return True
        return False

    def login(self, username, password):
        if not self.check_and_redirect():
            return True  # Already logged in

        try:
            # Wait for login form to be present
            username_field = self.browser.wait.until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_field = self.browser.driver.find_element(By.NAME, "password")
            
            # Fill in credentials
            username_field.send_keys(username)
            password_field.send_keys(password)
            
            # Find and click login button
            login_button = self.browser.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # Wait for login to complete
            self.browser.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.LoginSignup[href='/members/account/login']"))
            )
            
            return True
        except Exception as e:
            print(f"Login failed: {str(e)}")
            return False
