from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys

# export your words from translate.google.com to Google tables
# open file and leave only column with word and translation
# copy-paste to text file
# give the name of that text file as an argument for current script
# login and select your Desk

ATTEMPTS_COUNT=5


def find_element_by_xpath(driver, xpath):
	for _ in range(1,ATTEMPTS_COUNT):
		try:
			return driver.find_element_by_xpath(xpath)			
		except:
			continue


def send_keys(element, text):
	for _ in range(1,ATTEMPTS_COUNT):
		try:
			return element.send_keys(text)			
		except:
			continue


def click(element):
	for _ in range(1,ATTEMPTS_COUNT):
		try:
			return element.click()
		except:
			continue


if __name__=='__main__':
	driver = webdriver.Firefox()
	driver.get("https://ankiweb.net")
	input("waiting for logging in and selecting Desk")

	front=find_element_by_xpath(driver, '//*[@id="f0"]')
	back=find_element_by_xpath(driver, '//*[@id="f1"]')
	save=find_element_by_xpath(driver, '/html/body/main/p/button')
	if not front or not back or not save:
		print("some of visual elements were not found")
		sys.exit(1)

	with open(sys.argv[1], "r") as file:
		for each_line in file:
			word1, word2 = file.readline().split("\t")
			word1 = word1.strip()
			word2 = word2.strip()
			print(word1, word2)
			if word1 and word2:
				send_keys(front, word1)
				send_keys(back, word2)
				click(save)
			input("---")
	
