from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")
driver = webdriver.Chrome(options=chrome_options)
# driver.implicitly_wait(5)