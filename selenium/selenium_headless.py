# Ensure you have the necessary packages installed
# sudo apt install python3-selenium

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import sys
import time
from typing import List 
import os

DEBUG = True if os.environ.get("DEBUG")=='1' else False

if len(sys.argv) <= 1:
    print("1: provide url as first parameter")
    sys.exit(1)

url: str = sys.argv[1]

# 1. Check if a webdriver path is provided
if len(sys.argv) > 2:
    # /home/soft/selenium_driver/geckodriver
    webdriver_path = sys.argv[2]
    if DEBUG:
        print(f"driver path is: {webdriver_path}")
else:
    webdriver_path = None
    if DEBUG:
        print(f"driver path is empty")

# 2. Check if an output file is provided
output_file = None
if len(sys.argv) > 3:
    output_file = sys.argv[3]
    if DEBUG:
        print(f"output file is {output_file}")

MAX_PAGE_SIZE=999

# 3. Check for page_down command
page_down = 0
for each_parameter in sys.argv:
    if each_parameter.startswith("page_down="):
        page_down = int(each_parameter.replace("page_down=", ""))
        if page_down<=0:
            page_down=MAX_PAGE_SIZE
        break

# 4. Check for page_down_sleep command
page_down_sleep=1
for each_parameter in sys.argv:
    if each_parameter.startswith("page_down_sleep="):
        page_down_sleep = int(each_parameter.replace("page_down_sleep=", ""))
        break

# 5. Check for page_end command
page_end = False
for each_parameter in sys.argv:
    if each_parameter == "page_end":
        page_end = True
        break

# 6. Check for page_down command
page_up = 0
for each_parameter in sys.argv:
    if each_parameter.startswith("page_up="):
        page_up = int(each_parameter.replace("page_up=", ""))
        if page_up<=0:
            page_up=MAX_PAGE_SIZE
        break

# 7. Check for page_up_sleep command
page_up_sleep=1
for each_parameter in sys.argv:
    if each_parameter.startswith("page_up_sleep="):
        page_up_sleep = int(each_parameter.replace("page_up_sleep=", ""))
        break

# 8. Check for click_button_before command
click_button_before=None
for each_parameter in sys.argv:
    if each_parameter.startswith("click_button_before="):
        click_button_before=each_parameter.replace("click_button_before=", "")
        break

click_shadow_root_button_before=None
for each_parameter in sys.argv:
    if each_parameter.startswith("click_shadow_root_button_before="):
        click_shadow_root_button_before: List[str]=each_parameter.replace("click_shadow_root_button_before=", "").split(",")
        break

# Configure Firefox options
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.set_preference("general.useragent.override", "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0")
# Make browser automation less detectable
options.set_preference("dom.webdriver.enabled", False)
options.set_preference('useAutomationExtension', False)

# Create a service object if a webdriver path is provided
if webdriver_path is not None:
    service = Service(webdriver_path)
    # https://www.selenium.dev/documentation/
    driver = webdriver.Firefox(service=service, options=options)
else:
    # Rely on PATH for the geckodriver
    driver = webdriver.Firefox(options=options)

# setup driver 
driver.implicitly_wait(5)

# open link 
driver.get(url)

# post load manipulations
if click_button_before is not None:
    # print("click_button_before: " + click_button_before)
    time.sleep(1)

    try:
        button = driver.find_element(By.XPATH, click_button_before)
        # print("element: "+button )
        button.click()
        time.sleep(2)
    except Exception as e:
        print(f"exception: ${e}", file=sys.stderr)
        sys.exit(1)

if click_shadow_root_button_before is not None:
    ## 1. Get the host element
    host_element = driver.find_element(By.ID, click_shadow_root_button_before[0])
    ## 2. Get the shadow_root
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', host_element)   # host_element/shadowRoot
    # driver.execute_script('return arguments[0].shadowRoot.innerHTML', host_element)
    ## 3. Find the element within the shadow root and interact with it
    ##    Shadow DOMs do not support XPath queries. 
    button_inside_shadow = shadow_root.find_element(By.CSS_SELECTOR, click_shadow_root_button_before[1])
    # driver.execute_script('return arguments[0].click()', button_inside_shadow)
    button_inside_shadow.click()


if page_down > 0:
    time.sleep(page_down_sleep)

    body = driver.find_element(By.TAG_NAME, "body")
    scroll_percentage = 0
    for i in range(page_down):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(page_down_sleep)

        if page_down == MAX_PAGE_SIZE:
            scroll_percentage_before=scroll_percentage
            scroll_percentage = int(driver.execute_script(
                "if (document.documentElement.scrollHeight > window.innerHeight) {"
                "  return (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;"
                "} else {"
                "  return 0;"
                "}"
            ))
            # print(scroll_percentage)
            if scroll_percentage == 100:
                break
            if scroll_percentage_before == scroll_percentage:
                break

if page_end:
    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.END)
    time.sleep(page_down_sleep)

if page_up > 0:
    time.sleep(page_up_sleep)

    body = driver.find_element(By.TAG_NAME, "body")
    
    scroll_percentage = 100
    for i in range(page_up):
        body.send_keys(Keys.PAGE_UP)
        time.sleep(page_up_sleep)

        if page_up == MAX_PAGE_SIZE:
            scroll_percentage_before=scroll_percentage
            scroll_percentage = int(driver.execute_script(
                "if (document.documentElement.scrollHeight > window.innerHeight) {"
                "  return (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;"
                "} else {"
                "  return 0;"
                "}"
            ))
            # print(scroll_percentage)
            if int(scroll_percentage) == 0:
                break
            if scroll_percentage_before == scroll_percentage:
                break


# driver.page_source returns the current state of the DOM.
html: str = driver.page_source

if output_file is not None:
    with open(output_file, 'w') as file:
        file.write(html)
else: 
    print(html)

# Close the browser
driver.quit()
