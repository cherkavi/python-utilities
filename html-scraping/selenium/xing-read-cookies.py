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
