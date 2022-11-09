# selenium

## selenium_utils

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/selenium/selenium_utils.py) -->
<!-- The below code snippet is automatically added from ../../python/selenium/selenium_utils.py -->
```py
import os
from time import sleep
from typing import Optional

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


def parse_bool_value(str_value: str) -> Optional[bool]:
    if str_value.strip().lower() in ["true", "ok", "yes"]:
        return True
    if str_value.strip().lower() in ["false", "ko", "no"]:
        return False
    return None

def create_virtual_display(show_display: bool) -> Display:
    """
    should be created before using #create_browser
    in case of using virtual display
    """
    virtual_display: Display = Display(visible=show_display, size=(1024, 768))
    virtual_display.start()
    os.environ["DISPLAY"] = virtual_display.new_display_var
    return virtual_display


def create_browser(path_to_geckodriver: str) -> WebDriver:
    """
    https://github.com/mozilla/geckodriver/releases
    full path to Gecko driver like "/home/soft/selenium_driver/geckodriver"
    """
    return webdriver.Firefox(executable_path=path_to_geckodriver)


def pass_xing_login(driver: WebDriver, xing_login: str, xing_pass: str) -> bool:
    """
    pass login on XING using driver and login/password
    :Returns:
        * True - login successfull
        * False - can't login
    """
    url = 'https://loginix.com/'
    driver.get(url)
    sleep(3)
    try:
        permission_accept:WebElement = driver.find_element_by_xpath('//*[@id="consent-accept-button"]')
        permission_accept.click()
    except NoSuchElementException:
        # no question about privacy
        pass


    try:
        driver.find_element_by_name("username").send_keys(xing_login)
    except NoSuchElementException:
        print("no element by name: username")
        return False

    try:
        driver.find_element_by_name("password").send_keys(xing_pass)
    except NoSuchElementException:
        print("no element by name: password")
        return False

    try:
        driver.find_element_by_xpath(
            "/html/body/div[1]/div[2]/div/div[2]/section/div/main/div/div/div/div/div/form/div[5]/button/div").click()
    except NoSuchElementException:
        print("no element button login ")
        return False
    sleep(2)

    try:
        driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[2]/section/div/main/div/div/div/div/div[2]/div[2]/button[1]/div/span").click()
        sleep(2)
    except NoSuchElementException:
        # no element 'Try two factor authentication' with button Skip
        pass

    return True
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## test_selenium_utils

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/selenium/test_selenium_utils.py) -->
<!-- The below code snippet is automatically added from ../../python/selenium/test_selenium_utils.py -->
```py
import os
import sys
from os import environ

from pyvirtualdisplay import Display
from selenium.webdriver.firefox.webdriver import WebDriver

from xing_web.selenium_utils import pass_xing_login, create_browser, create_virtual_display, parse_bool_value

if __name__=='__main__':
    try:
        xing_login: str = environ.get("XING_LOGIN")
        if not xing_login:
            print("no variable XING_LOGIN")
            sys.exit(11)

        xing_passw: str = environ.get("XING_PASSW")
        if not xing_passw:
            print("no variable XING_PASSW")
            sys.exit(12)

        driver_path: str = environ.get("GECKO_DRIVER")
        if not driver_path:
            print("no variable GECKO_DRIVER")
            sys.exit(13)

        # given
        if parse_bool_value(environ.get("CREATE_DISPLAY", "True")):
            display: Display = create_virtual_display(parse_bool_value(environ.get("SHOW_BROWSER", "False")))
        else:
            display: Display = None
        driver: WebDriver = create_browser(driver_path)

        # when
        login_result = pass_xing_login(driver, xing_login, xing_passw)
    except Exception as e:
        print(f"exception: {e}")
        sys.exit(1)
    if driver:
        driver.close()
    if display:
        display.stop()
    print("done")
    sys.exit(0)
```
<!-- MARKDOWN-AUTO-DOCS:END -->


