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


# example
        entity_object:Dict = {"hello":"work"}
        try:
            response: requests.Response = requests.post(self._build_url(resource_type, resource_type_id, sub_resource_type), json=entity_object)
        except RequestException as ex:
            raise ShopifyException(ex)


# post auth basic
        try:
            response: Response = requests.post(self._build_url(dag_name),
                                               json=self._build_body(product_data_api, dag_name),
                                               auth=(self._user, self._password), headers=AirflowEventGenerator.HEADERS)
        except RequestException as ex:
            raise EventGeneratorException(f"airflow execution exception: {ex.message}")
        if not 200 <= response.status_code < 300:
            raise EventGeneratorException(f"airflow execution exception: {response.text}")

