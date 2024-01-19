```
from selenium.webdriver import Firefox
>>> from selenium.webdriver.firefox.options import Options
>>> opts = Options()
>>> opts.set_headless()
>>> assert opts.headless  # Operating in headless mode
>>> browser = Firefox(options=opts)
>>> browser.get('https://duckduckgo.com')
```

---
exception: Message: Expected browser binary location, but unable to find binary in default location, no 'moz:firefoxOptions.binary' capability provided, and no binary flag set on the command line
> sudo apt install firefox


exception: start error <EasyProcess cmd_param=['Xephyr', '-help'] cmd=['Xephyr', '-help']oserror=[Errno 2] No such file or directory: 'Xephyr' return_code=None stdout="None" stderr="None" timeout_happened=False>
> sudo apt install xvfb xserver-xephyr


exception: Xephyr program closed. command: ['Xephyr', '-br', '-screen', '1024x768x24', '-displayfd', '5', '-resizeable'] stderr: b'\nXephyr cannot open host display. Is DISPLAY set?\n'
>virtual_display.start();os.environ["DISPLAY"] = virtual_display.new_display_var
>virtual_display: Display = Display(False, size=(1024, 768))


exception: No such file or directory: 'Xvfb' 
> sudo apt install xvfb
