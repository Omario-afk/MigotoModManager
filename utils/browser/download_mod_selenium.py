import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def download_mod(url):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)  # Keep browser open
    
    # Initialize the Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Navigate to the URL
    driver.get(url)
    
    # Wait for the page to load
    wait = WebDriverWait(driver, 10)
    h1_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    title = h1_element.text.strip()
    
    # Get the page source for BeautifulSoup parsing
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # Continue with existing functionality
    mod_id = url.strip("/").split("/")[-1]
    print(f"Mod ID: {mod_id}")
    print(f"Title: {title}")
    
    matches = soup.find_all(string="1417318")
    for match in matches:
        print(match)
    
    # Note: Browser will stay open due to the detach option

if __name__ == "__main__":
    download_mod("https://gamebanana.com/mods/587147")