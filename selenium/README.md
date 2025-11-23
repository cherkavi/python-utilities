# Selenium 

## download driver
1. [Firefox (GeckoDriver)](https://github.com/mozilla/geckodriver/releases)
2. [ChromeDriver Downloads](https://sites.google.com/chromium.org/driver/downloads)
3. [OperaDriver Releases](https://github.com/operasoftware/operachromiumdriver/releases)
4. [Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

## selenium examples

### [selenium with additional parameters](./selenium_headless.debug.md)

### [selenium stealth](./selenium_headless_stealth.debug.md)

### minimal example
```py
from selenium.webdriver import Firefox
>>> from selenium.webdriver.firefox.options import Options
>>> opts = Options()
>>> opts.set_headless()
>>> assert opts.headless  # Operating in headless mode
>>> driver = Firefox(options=options, executable_path=path_to_geckodriver) 
>>> driver.get('https://duckduckgo.com')
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
