# Selenium 

## Installation
### download driver
1. [Firefox (GeckoDriver)](https://github.com/mozilla/geckodriver/releases)
2. [ChromeDriver Downloads](https://sites.google.com/chromium.org/driver/downloads)
3. [OperaDriver Releases](https://github.com/operasoftware/operachromiumdriver/releases)
4. [Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

### set env variable 
```sh
echo $GECKO_DRIVER
$GECKO_DRIVER --version
# geckodriver 0.36.0 (a3d508507022 2025-02-24 15:57 +0000)
```

## dry run
```sh
url=https://www.selenium.dev/documentation/                   # destination url for parsing
PATH_TO_GECKO_DRIVER=/home/soft/selenium_driver/chromedriver  # chrome   
PATH_TO_GECKO_DRIVER=/home/soft/selenium_driver/geckodriver   # firefox 
output_file=/tmp/output.txt
python3 ${HOME_PROJECTS_GITHUB}/python-utilities/selenium/selenium_headless.py $url $PATH_TO_GECKO_DRIVER $output_file

cat /tmp/output.txt
```

## selenium examples

### [selenium with additional parameters](./selenium_headless.debug.md)

### [selenium stealth](./selenium_headless_stealth.debug.md)

### minimal example Chrome
```py
# GECKO_DRIVER=/home/soft/selenium_driver/chromedriver python3
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import os
path_to_geckodriver=os.environ["GECKO_DRIVER"]; print(path_to_geckodriver)
service = Service(path_to_geckodriver)
options = Options()
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://duckduckgo.com')
```

### minimal example Firefox
```py
# python3
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import os
path_to_geckodriver=os.environ["GECKO_DRIVER"]; print(path_to_geckodriver)
service = Service(path_to_geckodriver)
options = Options()
options.add_argument('--disable-gpu')
driver = webdriver.Firefox(service=service, options=options)
# DO NOT install Firefox via SNAP !!!
driver.get('https://duckduckgo.com')
```

### minimal example Firefox 
```py
# python3
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import os
path_to_geckodriver=os.environ["GECKO_DRIVER"]; print(path_to_geckodriver)
service = Service(path_to_geckodriver)
options = Options()
options.add_argument('--disable-gpu')
driver = webdriver.Firefox(service=service, options=options)
# DO NOT install Firefox via SNAP !!!
driver.get('https://duckduckgo.com')
```

## exceptions
---
**exception:** Message: Expected browser binary location, but unable to find binary in default location, no 'moz:firefoxOptions.binary' capability provided, and no binary flag set on the command line
> sudo apt install firefox

---
**exception:** start error <EasyProcess cmd_param=['Xephyr', '-help'] cmd=['Xephyr', '-help']oserror=[Errno 2] No such file or directory: 'Xephyr' return_code=None stdout="None" stderr="None" timeout_happened=False>
> sudo apt install xvfb xserver-xephyr

---
**exception:** Xephyr program closed. command: ['Xephyr', '-br', '-screen', '1024x768x24', '-displayfd', '5', '-resizeable'] stderr: b'\nXephyr cannot open host display. Is DISPLAY set?\n'
>virtual_display.start();os.environ["DISPLAY"] = virtual_display.new_display_var
>virtual_display: Display = Display(False, size=(1024, 768))

---
**exception:** No such file or directory: 'Xvfb' 
> sudo apt install xvfb

---
**exception:** selenium.common.exceptions.SessionNotCreatedException: Message: session not created: cannot connect to chrome at 127.0.0.1:34977
> check version of your Chrome and ChromeDriver 
google-chrome --version 
https://googlechromelabs.github.io/chrome-for-testing/#stable

