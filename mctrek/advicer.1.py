from pprint import pprint
from selenium import webdriver
from xvfbwrapper import Xvfb

start_page = "http://www.mctrek.de/shop/sale?hersteller[]=Jack+Wolfskin&suchevon="

# list_of_size = page.xpath('//*[@id="wk_addItem"]/option/text()')
# print(list_of_size)
# list_of_size = 
# print(list_of_size[0].value_options)


def next_page_generator():
    index = 0
    while True:
        yield start_page + str(index*24)
        index = index+1

next_page = next_page_generator()
html_url = next_page.next()
xpath = '/html/body/div[9]/div/div[2]/div[2]/div[6]/div[4]/a/div[1]'


vdisplay = Xvfb()
vdisplay.start()
response = webdriver.Firefox()
response.get(html_url)
search_element = response.find_elements_by_xpath(xpath)
# pprint(search_element)
# print(dir(search_element))
for each in search_element:
	print(each.get_attribute('innerHTML').strip())
vdisplay.stop()