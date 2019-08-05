import subprocess
import sys
import requests


def clear_binary_line(b_line):
    next_line = b_line.decode('utf-8')
    if next_line[len(next_line)-1] == "\n":
        next_line = next_line[:-1]
    return next_line

def main():
    token = clear_binary_line(subprocess.check_output(["oc", "whoami", "-t"]))
    if "Error from server" in token:
        print("you must be logged in into OpenShift", file=sys.stderr)
        return False

    status = clear_binary_line(subprocess.check_output(["oc", "status"])).split("\n")[0].split(" ")
    endpoint = status[5]
    namespace = status[2]
    url = f"{endpoint}/api/v1/namespaces/{namespace}/pods?limit=10&fieldSelector=status.phase%3DRunning"
    response = requests.get(url, verify=False, headers={"Authorization": f"Bearer {token}", "Accept": "application/json"})
    print(response.content)
    print(response.json()['metadata']['selfLink'])

if __name__ == '__main__':
    main()
