import subprocess
import json
from typing import List

def clear_binary_line(b_line:bytes) -> str:
    # convert bytes to string, bytes2string, byte to string
    next_line = b_line.decode('utf-8')
    if len(next_line)==0:
        return ""            
    if next_line[len(next_line)-1] == "\n":
        next_line = next_line[:-1]
    index = next_line.rfind("/")
    if index >= 0:
        next_line = next_line[index+1:]
    return next_line

# subprocess curl, requests emulator, requests clear call
code="bx4pqba"
client_id="dj0yJmTBj"
client_secret="a871c009"
redirect_uri="https://ec2-5.eu-central-1.compute.amazonaws.com"
command=f"curl -X POST https://api.login.yahoo.com/oauth2/get_token --data 'code={code}&grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&response_type=code'"
output:bytes = subprocess.check_output(command.split(" "))
response: dict = json.loads(clear_binary_line(output))

if "error" in response:
    print(response["error"])
    print(response["error_description"])
else:
    print(response["access_token"])
    print(response["refresh_token"])
    print(response["expires_in"])
    print(response["bearer"])
