from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_webdriver(show_browser = False) -> webdriver.Chrome:
    chrome_options = Options()
    if not show_browser:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options = chrome_options)
    return driver
