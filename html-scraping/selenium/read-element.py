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
