# pip3 install --break-system-packages undetected-chromedriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()

# Set language
chrome_options.add_argument("--lang=de-DE")
# Disable automation flags
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Launch browser
driver = uc.Chrome(options=chrome_options)

# Set timezone
driver.execute_cdp_cmd("Emulation.setTimezoneOverride", {"timezoneId": "Europe/Berlin"})
# Set locale
driver.execute_cdp_cmd("Emulation.setLocaleOverride",{"locale": "de-DE"})

# Set geolocation — example: Munich, Germany
driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {"latitude": 48.137154,"longitude": 11.576124,"accuracy": 50})
# Grant geolocation permission automatically
driver.execute_cdp_cmd("Browser.grantPermissions",{"permissions": ["geolocation"],"origin": "https://google.com"})

driver.get("https://www.immowelt.de/classified-search?distributionTypes=Buy,Buy_Auction,Compulsory_Auction&estateTypes=Apartment&locations=AD08DE6440&numberOfRoomsMin=2&priceMax=425000&priceMin=210000&spaceMin=30")


