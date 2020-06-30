```bash
# set up environment
export AUTHY_API_KEY=""

# registration 
python3 authy-user-register.py some-email@gmail.com 15035354000 49

export AUTHY_USER_ID="268229999"

# print status
python3 authy-user-status.py
# scan QR code with GoogleAuthenticator
python3 authy-user-qr-show.py
# check provided token 
python3 authy-user-verify.py 860988
```





# collection of links 
https://authy.com/
https://authy.com/blog/understanding-2fa-the-authy-app-and-sms/
https://www.twilio.com/authy
mailto://customers@authy.com

* python-flask application
https://www.twilio.com/docs/authy/quickstart/two-factor-authentication-python-flask
* python client 2FA api
https://github.com/twilio/authy-python/blob/master/authy/api/resources.py 

# QR code generator, 2D Code generator, 2D BarCode generator
https://www.twilio.com/docs/authy/api/users
github.com/skip2/go-qrcode
http://go-qrcode.appspot.com/


# Account
https://www.twilio.com/console/authy/getting-started

https://www.twilio.com/console
https://www.twilio.com/console/authy/applications
ACCOUNT SID: 
ACCOUNT TOKEN: 

## application 
```bash
x-www-browser https://dashboard.authy.com/applications/292858
x-www-browser https://dashboard.authy.com/applications/292858/settings
# QR codes enable
x-www-browser https://www.twilio.com/console/authy/applications/292858
x-www-browser https://www.twilio.com/console/authy/applications/292858/settings
```
