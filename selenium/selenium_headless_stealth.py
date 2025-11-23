# pip3 install --break-system-packages undetected-chromedriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sys
import argparse
import tty, termios
import json  # Add this import at the top
import os  # new import

def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch

def save_cookies(driver, file_path):
    with open(file_path, 'w') as file:
        json.dump(driver.get_cookies(), file)

def load_cookies(driver, file_path):
    try:
        with open(file_path, 'r') as file:
            cookies = json.load(file)
            for cookie in cookies:
                if cookie.get('domain').startswith('.'):
                    cookie['domain'] = cookie['domain'][1:]
                print(f"cookie: {cookie}")
                driver.add_cookie(cookie)
    except FileNotFoundError:
        print("No cookie file found. Starting fresh.")


def str2bool(value):
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value is expected.')

parser = argparse.ArgumentParser(description='common description for program')
parser.add_argument('--url',
                    help='string argument example',
                    required=True)
parser.add_argument('--output_file',
                    help='string argument example',
                    required=False)
parser.add_argument('--visual_check',
                    help="boolean argument example ",
                    required=False, type=str2bool, default="false")
parser.add_argument('--cookies_file',
                    help='Path to the cookies file',
                    required=False)
parser.add_argument('--profile_dir',
                    help='Path to Chrome user-data directory to persist session/profile',
                    required=False)
args = parser.parse_args()
URL:str = args.url
OUTPUT_FILE:str = args.output_file
VISUAL_CHECK:bool = args.visual_check
COOKIES_FILE = args.cookies_file
PROFILE_DIR = args.profile_dir  # new variable

LANGUAGE = "de-DE"
TIMEZONE_ID = "Europe/Berlin"

GEO_LATITUDE = 48.137154
GEO_LONGITUDE = 11.576124
GEO_ACCURACY_M = 50

cdp_commands = {
    "Emulation.setTimezoneOverride" : {"timezoneId": TIMEZONE_ID},
    "Emulation.setLocaleOverride" : {"locale": LANGUAGE},
    "Emulation.setGeolocationOverride" : {"latitude": GEO_LATITUDE, "longitude": GEO_LONGITUDE, "accuracy": GEO_ACCURACY_M},
    "Browser.grantPermissions": {"permissions": ["geolocation"], "origin": URL}
    }

options = ['--disable-gpu', f"--lang={LANGUAGE}", "--disable-blink-features=AutomationControlled"]
if not VISUAL_CHECK:
    options.append('--headless')

## open browser 
chrome_options = Options()
for each_argument in options:
    chrome_options.add_argument(each_argument)

# If user provided a profile directory, ensure it exists and pass it to Chrome.
if PROFILE_DIR:
    os.makedirs(PROFILE_DIR, exist_ok=True)
    chrome_options.add_argument(f"--user-data-dir={PROFILE_DIR}")

driver = uc.Chrome(options=chrome_options)

for each_command in cdp_commands:
    driver.execute_cdp_cmd(each_command, cdp_commands[each_command])

if COOKIES_FILE:
    load_cookies(driver, COOKIES_FILE)

driver.get(URL)

if VISUAL_CHECK:
    try:
        while True:
            sys.stdout.write("Visual check passed — press Yes/Ok/J  ( otherwise: Escape )")
            sys.stdout.flush()            
            resp = getch()
            resp_ch=resp.strip().lower()
            if resp_ch in ( 'y', 'o', 'j', 'Y', 'O', 'J' ):
                break
            elif resp == '\x1b':
                driver.quit()
                exit(1)
    except (KeyboardInterrupt, EOFError):
        # on Ctrl-C / EOF just continue and quit the browser
        driver.quit()
        exit(2)

## open url 
html: str = driver.page_source

if OUTPUT_FILE is not None:
    with open(OUTPUT_FILE, 'w') as file:
        file.write(html)
else:
    print(html)

if COOKIES_FILE:
    save_cookies(driver, COOKIES_FILE)

driver.quit()