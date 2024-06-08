from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys

# browser automation 
# export your words from translate.google.com to Google tables
# open file and leave only column with word and translation
# copy-paste to text file
# give the name of that text file as an argument for current script
# application will ask for login, select Desk, click button Add


ATTEMPTS_COUNT=5


def find_element_by_xpath(driver, xpath):
    for _ in range(1,ATTEMPTS_COUNT):
        try:
            return driver.find_element(By.XPATH, xpath)
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
	print("-----------------------------------------")
	print("waiting for logging in")
	print("selecting destination Desk")
	input("click button Add and see 'UI for adding'")

	front=find_element_by_xpath(driver, '/html/body/div/main/form/div[1]/div/div')
	back=find_element_by_xpath(driver, '/html/body/div/main/form/div[2]/div/div')
	save=find_element_by_xpath(driver, '/html/body/div/main/form/button')
	if not front:
		print("Front element was not found")
		sys.exit(1)
	if not back:
		print("Back element was not found")
		sys.exit(1)
	if not save:
		print("Add button was not found")
		sys.exit(1)

	with open(sys.argv[1], "r") as file:
		for each_line in file:
			words = each_line.split("\t")
			if len(words) != 2:
				input(f"---skip line: {each_line}")				
				continue
			word1 = words[0]
			word2 = words[1]
			word1 = word1.strip()
			word2 = word2.strip()
			print(word1, word2)
			if word1 and word2:
				send_keys(front, word1)
				send_keys(back, word2)
				click(save)
			input("---")
	
