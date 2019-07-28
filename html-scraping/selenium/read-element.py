# pip install selenium
# wget `curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep browser_download_url | grep linux64 | cut -d '"' -f 4`
# export PATH="$PATH:/path/to/geckodriver/folder"
from selenium import webdriver
from xvfbwrapper import Xvfb
from pyvirtualdisplay import Display
from pprint import pprint


vdisplay = Xvfb()
# vdisplay = Display(visible=0)
vdisplay.start()
response = webdriver.Firefox()
# url = 'http://www.mctrek.de/bekleidung-unisex-herren/wintersport-skibekleidung/jacken/jack-wolfskin-icy-storm-flex-jacke-m_4047919'
url = 'http://www.mctrek.de/bekleidung-unisex-herren/wintersport-skibekleidung/jacken/icepeak-kurt-wintersportjacke-herren_4047336'
response.get(url)
search_element = response.find_elements_by_xpath('//*[@id="wk_addItem"]/option')
# pprint(search_element)
# print(dir(search_element))
for each in search_element:
	print(each.get_attribute('innerHTML').strip())
vdisplay.stop()