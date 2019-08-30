ANSIBLE_METADATA = {
    'metadata_version': '1.2',
    'status': ['ready'],
    'supported_by': 'cherkavi'
}

DOCUMENTATION = '''
---
module: oc_collaboration
author: cherkavi
short_description: create/delete and waiting for the start of resource ( pod, job, deployment... ) 
description: example of collaboration with OpenShift via REST API
options:
    operation:
      description:
         one of possible operations: create, delete, waiting_for_start
    file:
      description:
         full path to file with description
    timeout:
      description:
         default value is 120 sec, useful for 'waiting_for_start' only 

requirements: 'os status'

the same you can reach out using K8S module: https://docs.ansible.com/ansible/latest/modules/k8s_module.html
'''

EXAMPLES = '''
apiVersion: batch/v1
kind: Job
metadata:
  name: test-job
spec:
  nodeSelector:         
    composer: true
  template:         
    spec:
      containers:
      - name: busybox
        image: busybox
        command: ["echo", "'hello'"]          
      restartPolicy: Never
  backoffLimit: 1
  

- hosts: all 
  gather_facts: False
  tasks:
  - name: create deployment
    openshift-wait-for-start:
      operation: create
      file: /home/projects/test-job.yml
    register: creation_result
      
  - name: print result
    debug:
      msg: "result is {{ creation_result }}"

  - name: waiting for start/fail
    openshift-wait-for-start:
      operation: waiting_for_start
      file: /home/projects/test-job.yml
      timeout: 50
    register: waiting_result
'''

import requests
import yaml
import subprocess
import time
from ansible.module_utils.basic import AnsibleModule
import abc
# import pdb


def clear_binary_line(b_line):
    return b_line.decode('utf-8').rstrip()


def parse_info(path_to_file):
    return_value = []
    with open(path_to_file, 'r') as data_file:
        yaml_data = yaml.load_all(data_file)
        for each_yaml in yaml_data:
            resource_type = each_yaml['kind'].lower()
            resource_name = each_yaml['metadata']['name']
            return_value.append((resource_type, resource_name))
    return return_value


class Checker:
    def __init__(self, resource_name):
        self.name = resource_name
        # need to check again, result is not ready
        self.need_to_check = True
        # result is defined, readiness status ( Running/Completed or Failed )
        self.ready = False

    @staticmethod
    def create(resource_type, resource_name):
        """ factory method """
        if resource_type == "job":
            return JobChecker(resource_name)
        if resource_type == "deployment":
            return DeploymentChecker(resource_name)
        if resource_type == "pod":
            return PodChecker(resource_name)
        return None

    @staticmethod
    def _parse_response(response):
        if not (200 <= response.status_code < 300):
            return None
        return response.json()['status']

    @abc.abstractmethod
    def _check_phase(self, result):
        self._not_ready()

    def _not_ready(self):
        self.need_to_check = False
        self.ready = False

    @abc.abstractmethod
    def _build_url(self, endpoint, namespace):
        return endpoint + namespace

    def check(self, endpoint, namespace, token):
        url = self._build_url(endpoint, namespace)
        with requests.get(url,
                          verify=False,
                          headers={"Authorization": "Bearer {}".format(token), "Accept": "application/json"}) as response:
            result = Checker._parse_response(response)
            if not result:
                self._not_ready()
            else:
                self._check_phase(result)


class PodChecker(Checker):
    def __init__(self, resource_name):
        super().__init__(resource_name)

    def _build_url(self, endpoint, namespace):
        return "{}/api/v1/namespaces/{}/pods/{}".format(endpoint, namespace, self.name)


    def _check_phase(self, status):
        if status["phase"]:
            if status["phase"]=="Failed":
                self.need_to_check = False
                self.ready = False
                return
            if status["phase"]=="Running":
                self.need_to_check = False
                self.ready = False
                for each_condition in status["conditions"]:
                    if each_condition["type"]=="Ready":
                        self.ready = each_condition["status"]=="True"
                return
        self.need_to_check = True
        self.ready = False


class JobChecker(Checker):
    def __init__(self, resource_name):
        super().__init__(resource_name)

    def _build_url(self, endpoint, namespace):
        return "{}/apis/batch/v1/namespaces/{}/jobs/{}".format(endpoint, namespace, self.name)


    def _check_phase(self, status):
        if "succeeded" in status and status["succeeded"] > 0:
            self.need_to_check = False
            self.ready = True
            return
        if "failed" in status and status["failed"] > 0:
            self.need_to_check = False
            self.ready = True
            return

        for each_condition in status["conditions"]:
            if each_condition["type"] == "Complete":
                self.need_to_check = False
                self.ready = True
                return
            if each_condition["type"] == "Failed":
                self.need_to_check = False
                self.ready = False
                return
        self.need_to_check = True
        return


class DeploymentChecker(Checker):
    def __init__(self, resource_name):
        super().__init__(resource_name)

    def _build_url(self, endpoint, namespace):
        return "{}/apis/extensions/v1beta1/namespaces/{}/deployments/{}".format(endpoint, namespace, self.name)

    def _check_phase(self, status):
        for each_condition in status["conditions"]:
            if each_condition["type"] == "Available":
                self.need_to_check = False
                self.ready = True
                return
            if each_condition["type"] == "Failed":
                self.need_to_check = False
                self.ready = False
                return
        self.need_to_check = True
        return


def is_resource_was_started(endpoint, namespace, token, path_to_description, waiting_seconds=120):
    all_documents = parse_info(path_to_description)
    documents = list(filter(lambda entity: entity is not None, map(lambda x: Checker.create(x[0], x[1]), all_documents)))
    # to debug via PDF
    # pdb.set_trace()
    if len(documents) == 0:
        raise ValueError("file should contain at least one of: pod, job, deployment...")
    while any(map(lambda doc: doc.need_to_check, documents)):
        for each_document in documents:
            each_document.check(endpoint, namespace, token)
        waiting_seconds = waiting_seconds - 1
        time.sleep(1)
    return all(map(lambda doc: doc.ready, documents))

def create(path_to_file):
    try:
        return True, clear_binary_line(subprocess.check_output(["oc", "create", "-f", path_to_file]))
    except subprocess.CalledProcessError:
        return False, "possible resource is already exist "


def delete(path_to_file):
    try:
        return True, clear_binary_line(subprocess.check_output(["oc", "delete", "-f", path_to_file]))
    except subprocess.CalledProcessError:
        return False, "not deleted, maybe not exists"


def module_result(module, return_status, return_value):
    message = return_value if return_value else ""
    if return_status:
        module.exit_json(changed=True, msg=message)
    else:
        module.fail_json(changed=False, msg=message)


def main():
    input_fields = {
        "operation": {"required": True, "type": "str"},
        "file": {"required": True, "type": "str"},
        "timeout": {"required": False, "type": "str", "default": "120"}
    }
    module = AnsibleModule(argument_spec=input_fields)
    operation = module.params["operation"]
    file = module.params["file"]
    timeout = int(module.params["timeout"].strip())

    oc_token = clear_binary_line(subprocess.check_output(["oc", "whoami", "-t"]))
    if "Error from server" in oc_token:
        module_result(module, False, "you must be logged in into OpenShift")
        return

    if operation not in ["create", "delete", "waiting_for_start"]:
        module_result(module, False, "'operation' must be one of: create, delete, waiting_for_start ")
        return

    if operation == "create":
        return_status, return_value = create(file)
        module_result(module, return_status, return_value)
        return

    if operation == "delete":
        return_status, return_value = delete(file)
        module_result(return_status, return_value)
        return 

    oc_status = clear_binary_line(subprocess.check_output(["oc", "status"])).split("\n")[0].split(" ")
    oc_endpoint = oc_status[5]
    oc_namespace = oc_status[2]
    try:
        return_status = is_resource_was_started(oc_endpoint, oc_namespace, oc_token, file, waiting_seconds=timeout)
        module_result(module, return_status, "")
        return
    except ValueError as e:
        module_result(module, False, e.args[0])


if __name__ == '__main__':
    main()

