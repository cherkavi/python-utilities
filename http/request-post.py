import logging

import requests

_log = logging.getLogger(__name__)

def _check_captcha_via_rest(secret: str, response: str) -> bool:
    fields_to_send = {
        "secret": secret,
        "response": response}
    # response = requests.post("https://www.google.com/recaptcha/api/siteverify", data=fields_to_send, files={os.path.basename(sample): open(sample, "rb")})

    response_raw = requests.post("https://www.google.com/recaptcha/api/siteverify", data=fields_to_send)
    # !!! it will send object as a url encoded string: secret=my_secret&response=99999

    # if you want to send in JSON, requests json, request json
    response_raw = requests.post("https://www.google.com/recaptcha/api/siteverify", data=json.dumps(fields_to_send))

