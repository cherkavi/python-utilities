# compare json 
# pip install json-compare-deep
import json
import os
import sys

from json_compare import compare

JSON_COMPARE_SUPPRESS_OUTPUT: bool = len(os.environ.get("JSON_COMPARE_SUPPRESS_OUTPUT")) > 0
""" any value leads to suppressing output """


def filter_output(text: str) -> None:
    if JSON_COMPARE_SUPPRESS_OUTPUT:
        return
    if text.startswith("a is "):
        return
    if text.startswith("b is "):
        return
    if text.startswith("ignore_list_seq = True"):
        return
    print(f">>> {text}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("two paths are expected for comparing")
        sys.exit(1)
    with open(sys.argv[1], 'r') as file:
        data_1 = json.load(file)
    with open(sys.argv[2], 'r') as file:
        data_2 = json.load(file)
    if compare(data_1, data_2, callback=filter_output):
        print("ok")
        exit(0)
    else:
        print("ko")
        exit(1)
