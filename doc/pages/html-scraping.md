# html-scraping

## lxml

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/html-scraping/lxml/curl-output-html-parser.py) -->
<!-- The below code snippet is automatically added from ../../python/html-scraping/lxml/curl-output-html-parser.py -->
```py
from lxml import html, etree
import sys

"""
read data from stdin, 
interpret it like full html text, 
print xpath from first command-line argument
usage example
```
curl -X GET google.com | python3 curl-output-html-parser.py "/html/head/title"
curl -X GET google.com | python3 curl-output-html-parser.py "/html/body/a/@href"
curl --cookie cookie.txt --silent "http://loveread.books/read_book.php?id=66258&p=100" | iconv --from-code WINDOWS-1251 --to-code UTF-8 | python3 curl-output-html-parser.py "/html/body/table/tr[2]/td/table/tr/td[2]/div[3]"
```
"""

# read all lines from stdin
lines = [each_line for each_line in sys.stdin]
# parse input data as html file
tree = html.fromstring("\n".join(lines))
if len(sys.argv)==0:
    elements = tree.xpath("/html")
else:
    elements = tree.xpath(sys.argv[1])
if len(elements)>0:
    # print( str(etree.tostring(elements[0])) )
    # print("".join([ str(child.text) for child in elements[0].iterdescendants()]))
    # print("".join([str(etree.tostring(child)) for child in elements[0].iterchildren()]))
    
    if hasattr(elements[0], "itertext"):
        print("\n".join([text.strip() for text in elements[0].itertext()]))
    else:
        print(elements[0])
    sys.exit(0)
else:
    sys.exit(1)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## lxml

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/html-scraping/lxml/parse_page.py) -->
<!-- The below code snippet is automatically added from ../../python/html-scraping/lxml/parse_page.py -->
```py
from lxml import html

page = html.parse("http://www.mctrek.de/bekleidung-unisex-herren/wintersport-skibekleidung/jacken/icepeak-kurt-wintersportjacke-herren_4047336")
# list_of_size = page.xpath('//*[@id="wk_addItem"]/option/text()')
# print(list_of_size)

list_of_size = page.xpath('//*[@id="wk_addItem"]')
print(list_of_size[0].value_options)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## lxml

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/html-scraping/lxml/parse_page_broken_html.py) -->
<!-- The below code snippet is automatically added from ../../python/html-scraping/lxml/parse_page_broken_html.py -->
```py
from lxml import html
import requests

page = requests.get("http://spys.one/free-proxy-list/UA/")
tree = html.fromstring(page.content)
# for XPath remove all "<tbody>" elements 
addresses = tree.xpath("/html/body/table[2]/tr[4]/td/table/tr[*]/td[1]/font[2]")
for each_address in addresses:
    print(each_address.text)
    print(each_address.getchildren()[0].text)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## request html

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/html-scraping/request-html/parse-with-js.py) -->
<!-- The below code snippet is automatically added from ../../python/html-scraping/request-html/parse-with-js.py -->
```py
from requests_html import HTMLSession
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## selenium

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/html-scraping/selenium/read-element.py) -->
<!-- The below code snippet is automatically added from ../../python/html-scraping/selenium/read-element.py -->
```py
# pip install selenium
# wget `curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep browser_download_url | grep linux64 | cut -d '"' -f 4`
# export PATH="$PATH:/path/to/geckodriver/folder"
import selenium
from pyvirtualdisplay import Display
from selenium import webdriver

vdisplay = Display(visible=True, size=(1024, 768))  # vdisplay = xvfbwrapper.Xvfb()
vdisplay.start()
options = selenium.webdriver.firefox.options.Options()
options.add_argument('-profile')
options.add_argument('/home/soft/firefox_profiles/xing.profile')
profile = webdriver.FirefoxProfile("/home/soft/firefox_profiles/xing.profile")
driver = webdriver.Firefox(executable_path="/home/soft/selenium_driver/geckodriver",
                           firefox_profile=profile
                           # options=options
                           # firefox_profile=profile,
                           # service_log_path="/home/soft/firefox_profiles/xing.log"
                           )
print(driver.session_id)
print(f"path to current profile: {driver.profile.profile_dir}")
url = 'https://www.xing.com/m/TATDmlc0kr2TQr0gNHRRgH'

driver.get(url)
search_element = driver.find_elements_by_xpath('//*[@id="wk_addItem"]/option')
# pprint(search_element)
# print(dir(search_element))
for each in search_element:
    print(each.get_attribute('innerHTML').strip())
vdisplay.stop()

# driver.delete_all_cookies()
# driver.refresh()
driver.close()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## selenium

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/html-scraping/selenium/xing-read-cookies.py) -->
<!-- The below code snippet is automatically added from ../../python/html-scraping/selenium/xing-read-cookies.py -->
```py
# pip install selenium
# wget `curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep browser_download_url | grep linux64 | cut -d '"' -f 4`
# export PATH="$PATH:/path/to/geckodriver/folder"
import json
from time import sleep
import os
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait


def create_virtual_display() -> Display:
    vdisplay = Display(visible=True, size=(1024, 768))
    vdisplay.start()
    return vdisplay


def create_browser() -> WebDriver:
    return webdriver.Firefox(executable_path="/home/soft/selenium_driver/geckodriver")


if __name__ == "__main__":
    vdisplay = create_virtual_display()
    driver = create_browser()
    waiter: WebDriverWait = WebDriverWait(driver, 30)

    output_file_cookie = os.environ.get("COOKIE_FILE")

    with open(output_file_cookie, "r") as cookie_file:
        cookies: dict = json.load(cookie_file)
    driver.get("https://www.xing.com")
    for each_cookie in cookies:
        driver.delete_cookie(each_cookie["name"])
        driver.add_cookie(each_cookie)

    url = 'https://www.xing.com/m/J9pTX3JeBaLh37FOtDRagG'
    page = driver.get(url)

    sleep(2)

    # waiter.until(expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR, "some_id"),"expected text"))
    # driver.delete_all_cookies()
    # driver.refresh()
    # driver.close()
    vdisplay.stop()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## selenium

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/html-scraping/selenium/xing-save-cookies.py) -->
<!-- The below code snippet is automatically added from ../../python/html-scraping/selenium/xing-save-cookies.py -->
```py
# pip install selenium
# wget `curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep browser_download_url | grep linux64 | cut -d '"' -f 4`
# export PATH="$PATH:/path/to/geckodriver/folder"
import json
from typing import List
import sys
import os
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep


def create_virtual_display() -> Display:
    vdisplay = Display(visible=True, size=(1024, 768))
    vdisplay.start()
    return vdisplay


def create_browser() -> WebDriver:
    return webdriver.Firefox(executable_path="/home/soft/selenium_driver/geckodriver")


if __name__ == "__main__":
    vdisplay = create_virtual_display()
    driver = create_browser()
    waiter: WebDriverWait = WebDriverWait(driver, 30)

    url = 'https://login.xing.com/'
    page = driver.get(url)

    output_file_cookie = os.environ.get("COOKIE_FILE")
    user_login = os.environ.get("USER_NAME")
    user_password = os.environ.get("USER_PASS")

    accept_button: WebElement = driver.find_element_by_id("consent-accept-button")
    if not accept_button:
        print("can't find button Accept")
        sys.exit(1)
    accept_button.click()

    email_field: WebElement = driver.find_element_by_name("username")
    email_field.send_keys(user_login)

    password_field: WebElement = driver.find_element_by_name("password")
    password_field.send_keys(user_password)

    button_login: WebElement = driver.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div/div[2]/section/div/main/div/div/div/div/div/form/div[5]/button/div")
    button_login.click()
    sleep(2)

    with open(output_file_cookie, "w") as output_file:
        cookies = json.dumps(driver.get_cookies())
        print(cookies)
        output_file.write(cookies)

    # waiter.until(expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR, "some_id"),"expected text"))
    # driver.delete_all_cookies()
    # driver.refresh()
    # driver.close()
    vdisplay.stop()
```
<!-- MARKDOWN-AUTO-DOCS:END -->


