#!/usr/bin/env python
import requests
import socket


def check_positive_get_response(url):
    try:
        response:requests.Response = requests.get(url, timeout=3)
        return 200 <= response.status_code < 300
    except Exception as e:
        return False
    finally:
        if 'response' in locals():
            response.close()


def is_port_open(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    return result == 0


def print_status(name, url, port=0, is_http=True):
    result = check_positive_get_response(url) if is_http else is_port_open(url, port)
    if result:
        print(" %15s  OK" % name)
    else:
        print(" %15s ---ERROR--- " % name)


print_status("activeMQ", "http://localhost:8161")
print_status("ekyc-dii", "http://localhost:9008/__admin/")
print_status("balas", "http://localhost:19006/__admin/")
print_status("elastic-engine", "http://localhost:19004/__admin/")
print_status("cetrel", "http://localhost:19004/__admin/")
print_status("payment-engine", "http://localhost:19001/__admin/")
print_status("risk", "http://localhost:19005/__admin/")
print_status("mindmatics", "http://localhost:19002/__admin/")
print_status("smtp", "127.0.0.1", 6869, False)
print_status("wip", "http://localhost:19000/__admin/")
print_status("brand-server", "http://localhost:9090/status")
