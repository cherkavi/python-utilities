# pip3 install --break-system-packages undetected-chromedriver
# pip3 install --break-system-packages webdriver_manager
# https://github.com/ultrafunkamsterdam/undetected-chromedriver

## run before
# remote_port=9123
# google_chrome_pid_file="/tmp/chrome-${remote_port}.pid"
# google-chrome --remote-debugging-port=${remote_port} --user-data-dir=/home/projects/wohnung-parsing-profile & echo $! > $google_chrome_pid_file
# # curl http://127.0.0.1:${remote_port}/json # test connection curl

## run after 
# # stop google-chrome gracefully 
# kill "$(cat $google_chrome_pid_file)"
# # if it doesn't exit after a few seconds:
# sleep 2
# kill -9 "$(cat $google_chrome_pid_file)"

## Check your versions
# $CHROME_DRIVER --version   # x-www-browser https://googlechromelabs.github.io/chrome-for-testing/
# chrome://settings/help

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager #
import selenium
import sys
import argparse
import tty, termios
import json 
import os 
import subprocess

SELENIUM_DRIVER_PATH = os.environ.get("CHROME_DRIVER")
DEFAULT_SELENIUM_CACHE_DIR = "/home/projects/temp/selenium"

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
parser.add_argument('--user-data-dir',
                    help='Path to Chrome user-data directory to persist session/profile',
                    required=False)
parser.add_argument('--remote_debugging_port',
                    help='connect to existing Chrome process via address',
                    required=False)
parser.add_argument('--run_bash_script_after_request',
                    help='after request Y/N execute bash script ( switch to another window? )',
                    required=False)

args = parser.parse_args()
REMOTE_DEBUG= f"127.0.0.1:{args.remote_debugging_port}" if args.remote_debugging_port else None

URL:str = args.url
if not URL.startswith("http") and not URL.startswith("https"):
    sys.stderr.write("specify proper url");
    sys.stderr.flush()
    sys.exit(1)
    
OUTPUT_FILE:str = args.output_file
VISUAL_CHECK:bool = args.visual_check
COOKIES_FILE = args.cookies_file
PROFILE_DIR = args.user_data_dir   # new variable

LANGUAGE = "de-DE"
TIMEZONE_ID = "Europe/Berlin"

GEO_LATITUDE = 48.137154
GEO_LONGITUDE = 11.576124
GEO_ACCURACY_M = 50


cdp_commands = {
    "Browser.grantPermissions": {
            "permissions": ["geolocation"], 
            "origin": URL
         }
    }
cdp_commands_after_open = {
    "Emulation.setTimezoneOverride" : {"timezoneId": TIMEZONE_ID},
    "Emulation.setLocaleOverride" : {"locale": LANGUAGE},
    "Emulation.setGeolocationOverride" : {"latitude": GEO_LATITUDE, "longitude": GEO_LONGITUDE, "accuracy": GEO_ACCURACY_M}
    }

options = ['--disable-gpu', f"--lang={LANGUAGE}", "--disable-blink-features=AutomationControlled"]
if not VISUAL_CHECK:
    options.append('--headless')

## open browser 

# If user provided a profile directory, ensure it exists and pass it to Chrome.
if PROFILE_DIR:
    os.makedirs(PROFILE_DIR, exist_ok=True)
#     # chrome_options.add_argument(f"--user-data-dir={PROFILE_DIR}")
#     chrome_options.user_data_dir=PROFILE_DIR   # obsolete

service = None
if SELENIUM_DRIVER_PATH:
    service = Service(SELENIUM_DRIVER_PATH)


def chrome_options_builder():
    """ to avoid RuntimeError: you cannot reuse the ChromeOptions object """
    chrome_options = uc.ChromeOptions()
    for each_argument in options:
        chrome_options.add_argument(each_argument)

    chrome_options.binary_location = "/usr/bin/google-chrome" 

    if REMOTE_DEBUG:
        # print(f"remote debug:{REMOTE_DEBUG}")
        # for testing the connection: http://127.0.0.1:9123/json 
        # chrome_options.add_experimental_option("debuggerAddress", REMOTE_DEBUG)     doesn't work with undetected-chromedriver
        chrome_options.debugger_address=REMOTE_DEBUG    
    return chrome_options

# if REMOTE_DEBUG:
#     # only for Selenium.Grid
#     from selenium import webdriver
#     driver = webdriver.Remote(command_executor=REMOTE_DEBUG, options=chrome_options)
# else:
#     driver = uc.Chrome(service=service, options=chrome_options)

try:
    driver = uc.Chrome(service=service, options=chrome_options_builder(), use_subprocess=False, keep_alive=False, user_data_dir=PROFILE_DIR)
except selenium.common.exceptions.SessionNotCreatedException:
    if SELENIUM_DRIVER_PATH:
        CUSTOM_CACHE_DIR=os.path.dirname(SELENIUM_DRIVER_PATH)
    else:
        CUSTOM_CACHE_DIR = DEFAULT_SELENIUM_CACHE_DIR        
    if not os.path.exists(CUSTOM_CACHE_DIR):
        os.makedirs(CUSTOM_CACHE_DIR)
    os.environ['WDM_CACHE_DIR'] = CUSTOM_CACHE_DIR # print(f"Setting cache directory to: {CUSTOM_CACHE_DIR}")    
    driver_path=ChromeDriverManager().install()
    driver = uc.Chrome(service=ChromeService(driver_path), options=chrome_options_builder(), use_subprocess=False, keep_alive=False, user_data_dir=PROFILE_DIR)

for each_command in cdp_commands:
    # print(f"{each_command} --> {cdp_commands[each_command]}")
    driver.execute_cdp_cmd(each_command, cdp_commands[each_command])

if COOKIES_FILE:
    load_cookies(driver, COOKIES_FILE)

driver.get(URL)

for each_command in cdp_commands_after_open:
    driver.execute_cdp_cmd(each_command, cdp_commands_after_open[each_command])

## check geolocation 
# result = driver.execute_script(
#         "navigator.geolocation.getCurrentPosition(pos => console.log('Location:', pos.coords.latitude, pos.coords.longitude)); return 'Geolocation requested';"
#     )
# print(f"Script Result: {result}")

if VISUAL_CHECK:
    try:
        while True:
            sys.stdout.write("visual check passed ? press Yes/Ok/J  ( otherwise: Escape )")
            sys.stdout.flush()            
            if args.run_bash_script_after_request is not None:                
                subprocess.Popen(
                    ["bash", args.run_bash_script_after_request],
                    stdout=subprocess.DEVNULL,  # Redirect output so it doesn't hang or clutter
                    stderr=subprocess.DEVNULL,
                    preexec_fn=os.setpgrp       # Decouples the process group (Unix only)
                )                
            resp = getch()
            resp_ch=resp.strip().lower()
            if resp_ch in ( 'y', 'o', 'j', 'Y', 'O', 'J' ):
                sys.stdout.write("\n                    yes\n")
                break
            elif resp == '\x1b':
                sys.stdout.write("\n                    NO\n")
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