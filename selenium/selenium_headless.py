from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Set up headless Chrome (no GUI)
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

# You can specify the path to chromedriver if not in PATH
driver = webdriver.Chrome(options=options)

url = "http://example.com"
driver.get(url)

# Wait for page to load JS (optional: use WebDriverWait for dynamic content)
html = driver.page_source

print(html)  # or write to file

driver.quit()
