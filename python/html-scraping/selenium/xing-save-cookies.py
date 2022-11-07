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
