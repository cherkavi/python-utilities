# copy list of proxy from html page: http://spys.one/free-proxy-list/UA/
# select all lines with proxy using mouse, copy them and paste to file: proxy.txt
# cat proxy.txt | awk '{ print $2" "$3 }' | awk '{ if($1 ~ /\./ ){print $1" "$2}  }' | python3 foxyproxy-generator.py

import json
import random
import sys

def get_type(proxy_type:str) -> int:
    prepared_type = proxy_type.upper
    if prepared_type == "HTTP":
        return 1
    if prepared_type == "HTTPS":
        return 2
    if prepared_type == "SOCKET5":
        return 3
    return 1


def get_proxy_description(proxy_address:str, proxy_type:str):
    """
    proxy address like "91.225.5.43:53495"
    proxy type like: "HTTP", "HTTPS", "SOCKET5"
    """
    proxy = {}
    proxy["title"] = proxy_address
    proxy["type"] = get_type(proxy_type) # "type": 1,
    proxy_elements = proxy_address.strip().split(":")
    proxy["address"] = proxy_elements[0]
    proxy["port"] = proxy_elements[1]
    proxy["active"] = True
    color_red = str(hex(random.randint(0, 255)))[2:]
    color_green = str(hex(random.randint(0, 255)))[2:]
    color_blue = str(hex(random.randint(0, 255)))[2:]
    proxy["color"] = "#" + color_red + color_green + color_blue
    proxy["id"] = "17tj6e157" + str(random.randint(1000000000, 9999999999))
    return proxy


if __name__=="__main__":
    """ input lines like 
    195.74.72.129:49383 HTTPS
    91.225.5.43:53495 HTTP
    109.200.132.147:8888 SOCKS5
    """
    input_lines = list()
    for each_input in sys.stdin:
        input_lines.append(each_input.strip().split(" "))
 
    document = {}
    document["mode"] = "disabled"
    document["logging"] = {}
    document["logging"]["active"] = True
    document["logging"]["maxSize"] = 500
    document["proxySettings"] = list(map(lambda x:get_proxy_description(x[0], x[1]), input_lines))
    
    print(json.dumps(document, indent=2))
