# Ensure you have the necessary packages installed
# sudo apt install python3-selenium

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import sys

if len(sys.argv) <= 1:
    print("1: provide url as first parameter")
    sys.exit(1)

url: str = sys.argv[1]

# Check if a webdriver path is provided
if len(sys.argv) > 2:
    # /home/soft/selenium_driver/geckodriver
    webdriver_path = sys.argv[2]
else:
    webdriver_path = None

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

# Create a service object if a webdriver path is provided
if webdriver_path is not None:
    service = Service(webdriver_path)
    driver = webdriver.Firefox(service=service, options=options)
else:
    # Rely on PATH for the geckodriver
    driver = webdriver.Firefox(options=options)

driver.get(url)

# Wait for the page to load (optional: use WebDriverWait for dynamic content)
html: str = driver.page_source

print(html)  # Print the HTML source or write to a file

# Close the browser
driver.quit()