"""
application for checking html resources for white/black text in the response
input data should be provided in the input file with below lines (rest will be filtered out):
```
ADVERT_URL_BN='https://bn.ua/prodaja-5-dom-k'
ADVERT_WHITE_BN='Купить дом'
ADVERT_BLACK_BN='404'

ADVERT_URL_KRYSHA=https://metry.ua/novoo
ADVERT_WHITE_KRYSHA='Продажа Озеро'
ADVERT_BLACK_KRYSHA=''
```
"""
import sys
from typing import List, Dict, Tuple
import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning

GREEN = "\033[92m"  # Green text
RED = "\033[91m"    # Red text
RESET = "\033[0m"   # Reset to default color

# Suppress only the InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)

def parse_variables(file_path: str) -> Tuple[Dict[str, str], Dict[str, str], Dict[str, str], Dict[str, str]]:
    dict_url:Dict[str] = dict()
    dict_white:Dict[str] = dict()
    dict_black:Dict[str] = dict()
    dict_keepass:Dict[str] = dict()

    with open(file_path) as f:
        for each_line in f.readlines():
            each_line=each_line.strip()
            if each_line.startswith("ADVERT"):
                position_equals:int=each_line.find('=')
                position_underscore:int=each_line.find('_', 8)
                if position_equals<0 or position_underscore<0:
                    continue
                name:str = each_line[position_underscore+1: position_equals]
                if each_line.startswith("ADVERT_WHITE"):
                    dict_white[name]=each_line.strip()[position_equals+1:].strip("'")
                if each_line.startswith("ADVERT_BLACK"):
                    dict_black[name]=each_line.strip()[position_equals+1:].strip("'")
                if each_line.startswith("ADVERT_URL"):
                    dict_url[name]=each_line.strip()[position_equals+1:].strip("'")
                if each_line.startswith("ADVERT_KEEPASS"):
                    dict_keepass[name]=each_line.strip()[position_equals+1:].strip("'")
    return dict_url, dict_white, dict_black, dict_keepass

def fetch_and_check_url(url: str, white: str, black: str) -> bool:
    headers = {
         'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
        ,'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
    }
    
    try:
        # Send the GET request with the headers
        response = requests.get(url, headers=headers, verify=False, allow_redirects=True)        
        # Check if the request was successful
        if 200 <= response.status_code < 300:
            if black != '':
                for each_black in black.split(';'):
                    if each_black in response.text:
                        return False
            if white in response.text:
                return True
            
            # print("no options")
            return False      
        else:
            # print(f"Request failed with status code: {response.status_code}")
            return False
    
    except requests.RequestException as e:
        # print(f"An error occurred: {e}")
        return False


if __name__=='__main__':
    if len(sys.argv)<2:
        print("provide file with 'ADVERT_' prefixes ")
        exit(1)
    # file_path='/Dropbox/Dropbox/house-site/adverts.md'
    file_path=sys.argv[1]

    dict_url, dict_white, dict_black, dict_keepass = parse_variables(file_path)
    keys= dict_url.keys()

    false_results_counter: int = 0
    for name in keys: 
        result = fetch_and_check_url(dict_url[name], dict_white[name], dict_black[name])
        if result:
            print(f"{GREEN}{name} {dict_url[name]}:\n       {result}{RESET}")
        else:
            print(f"{RED}{name} {dict_url[name]}:\n       check advert: {dict_keepass[name]}{RESET}")
            false_results_counter+=1
    if false_results_counter>0:
        print("")
        print("keepass-tech-get-url-clipboard  ")
        print("keepass-tech-get-user-clipboard ")
        print("keepass-tech-get-pass-clipboard ")
