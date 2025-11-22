```sh
python3 
```

```py
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import sys
import os
import time
from typing import List 

webdriver_path = os.environ.get("GECKO_DRIVER")
MAX_PAGE_SIZE=999

options = Options()
# options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.set_preference("general.useragent.override", "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0")
# Make browser automation less detectable
options.set_preference("dom.webdriver.enabled", False)
options.set_preference('useAutomationExtension', False)

# options.set_preference('--user-data-dir', '/tmp/selenium-browser')
# options.set_preference('--profile-directory', 'Default')


service = Service(webdriver_path)
# https://www.selenium.dev/documentation/
driver = webdriver.Firefox(service=service, options=options)
# driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(5)
```


```py
url='https://www.rewe.de/angebote/nationale-angebote/'
driver.get(url)
```


```py
each_parameter='usercentrics-root,[data-testid="uc-accept-all-button"]'

click_shadow_root_button_before: List[str]=each_parameter.replace("click_shadow_root_button_before=", "").split(",")
## 1. Get the host element
host_element = driver.find_element(By.ID, click_shadow_root_button_before[0])
## 2. Get the shadow_root
shadow_root = driver.execute_script('return arguments[0].shadowRoot', host_element)   # host_element/shadowRoot
# driver.execute_script('return arguments[0].shadowRoot.innerHTML', host_element)
## 3. Find the element within the shadow root and interact with it
##    Shadow DOMs do not support XPath queries. 
button_inside_shadow = shadow_root.find_element(By.CSS_SELECTOR, click_shadow_root_button_before[1])
# driver.execute_script('return arguments[0].click()', button_inside_shadow)
button_inside_shadow.click()

```

