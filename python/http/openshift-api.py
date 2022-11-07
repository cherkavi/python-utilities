import subprocess
import sys
import requests
import json
import yaml

# suppress printing warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def clear_binary_line(b_line):
    next_line = b_line.decode('utf-8')
    if next_line[len(next_line)-1] == "\n":
        next_line = next_line[:-1]
    return next_line


def get_all_pods(endpoint, namespace, token):
    url = f"{endpoint}/api/v1/namespaces/{namespace}/pods?limit=10&fieldSelector=status.phase%3DRunning"
    response = requests.get(url,
                            verify=False,
                            headers={"Authorization": f"Bearer {token}", "Accept": "application/json"})
    return [each_item['metadata']['name'] for each_item in response.json()['items']]
    # print(response.json()['metadata']['selfLink'])


def create(endpoint, namespace, token, path_to_file):
    url = f"{endpoint}/api/v1/namespaces/{namespace}/pods"
    with open(path_to_file, 'r') as data_file:
        yaml_data = yaml.load(data_file)
    data = json.dumps(yaml_data)
    response = requests.post(url,
                             verify=False,
                             headers={"Authorization": f"Bearer {token}",
                                      "Accept": "application/json",
                                      "Content-Type": "application/json"
                                      },
                             data=data)
    return response.json()


def delete(endpoint, namespace, token, path_to_file):
    with open(path_to_file, 'r') as data_file:
        yaml_data = yaml.load(data_file)
    resource_type = yaml_data['kind'].lower()
    resource_name = yaml_data['metadata']['name']
    url = f"{endpoint}/api/v1/namespaces/{namespace}/{resource_type}s/{resource_name}"
    response = requests.delete(url,
                               verify=False,
                               headers={"Authorization": f"Bearer {token}",
                                        "Accept": "application/json",
                                        "Content-Type": "application/json"
                                        }
                               )
    return response.json


def main():
    token = clear_binary_line(subprocess.check_output(["oc", "whoami", "-t"]))
    if "Error from server" in token:
        print("you must be logged in into OpenShift", file=sys.stderr)
        return False

    status = clear_binary_line(subprocess.check_output(["oc", "status"])).split("\n")[0].split(" ")
    endpoint = status[5]
    namespace = status[2]

    # print(get_all_pods(endpoint, namespace, token))
    print("delete")
    print(delete(endpoint, namespace, token, "/home/projects/current-task/openshift-docker/working-example-pod.yml"))
    print("create")
    print(create(endpoint, namespace, token, "/home/projects/current-task/openshift-docker/working-example-pod.yml"))


if __name__ == '__main__':
    main()
