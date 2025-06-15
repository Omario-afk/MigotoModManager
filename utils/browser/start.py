from bs4 import BeautifulSoup
from . import Browser
from .login import LoginManager


class ModDownloader:
    def __init__(self):
        self.browser = Browser()
        self.login_manager = LoginManager(self.browser)

    def download_mod(self, url, username=None, password=None):
        # Navigate to the mod page
        self.browser.navigate_to(url)
        
        # Check login status and handle login if needed
        if username and password:
            if not self.login_manager.login(username, password):
                print("Failed to log in")
                return None
        
        # Get page source and parse with BeautifulSoup
        page_source = self.browser.get_page_source()
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Extract mod information
        mod_id = url.strip("/").split("/")[-1]
        h1 = soup.find('h1')
        title = h1.find(string=True, recursive=False).strip() if h1 else "Unknown Title"
        
        print(f"Mod ID: {mod_id}")
        print(f"Title: {title}")
        
        # Continue with any additional parsing needed
        matches = soup.find_all(string="1417318")
        for match in matches:
            print(match)
        
        return {
            'mod_id': mod_id,
            'title': title,
            'soup': soup
        }

    def close(self):
        self.browser.close()
