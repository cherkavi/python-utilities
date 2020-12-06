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

