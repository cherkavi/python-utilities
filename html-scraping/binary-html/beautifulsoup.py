# print html content as a text in console
# from binary html resource
# 
import requests
from bs4 import BeautifulSoup
import sys

def parse_html(address:str):    
    response = requests.get(address)
    binary_content = response.content

    # Parse the binary content using Beautiful Soup
    soup = BeautifulSoup(binary_content, "html.parser")

    # soup.title.text
    # ??? elements = soup.find_all("li", xpath="/html/body/div[1]/div[1]/div/div/div/div/div/div[2]/div[8]/div/div/ul")
        
    print(soup.find("html"))

if __name__=='__main__':
    if len(sys.argv)<2:
        print("provide target html")
        sys.exit(1)
    parse_html(sys.argv[1])
