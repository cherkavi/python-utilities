from typing import List
import sys, paramiko
import os, subprocess
from typing import Dict


class AirflowBuilder:
    """
    collection of static methods for building request-body for Airflow REST API 
    """
    @staticmethod
    def auto_labeler(session_id: str, method: str)-> str:
        return '\'{"conf":{"session_id":"'+session_id+'","branch":"'+method+'"}}\''


class SshCommandExecutor:
    def __init__(self, host_name: str, user_name: str, user_pass: str):
        self.host_name = host_name
        self.user_name = user_name
        self.user_pass = user_pass

    def execute_command(self, command:str, print_error:bool = False) -> List[str]:
        """
        execute SSH command against remote host
        """
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.load_system_host_keys()
            ssh.connect(self.host_name, username=self.user_name, password=self.user_pass)
            # dir(ssh)
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
            if print_error:
                print(ssh_stderr.readlines())
            return [each_line.strip("\n") for each_line in ssh_stdout.readlines()]
        finally:
            ssh.close()

    def execute_airflow_dag(self, airflow_url:str, airflow_dag_name: str, airflow_user: str, airflow_pass: str, data_body: str) -> List[str]:
        """
        trig Airflow DAG 
        airflow_url = "https://airflow-stg.dplapps.advantagedp.org"
        data_body = '\'{"conf":{"session_id":"ed573f33-4103-47ba-b9ee-f424ec2f9313","branch":"run_labelers"} }\''
        print(executor.execute_airflow_dag(airflow_url, "auto_labelling", "label_search_depl-s", "passw", data_body))
        """
        url = f"{airflow_url}/api/experimental/dags/{airflow_dag_name}/dag_runs"
        airflow_pass_fixed='"'+airflow_pass+'"'
        command = f"curl --data-binary {data_body} -u {airflow_user}:{airflow_pass_fixed} -X POST {url}"
        print(airflow_user, airflow_pass_fixed, data_body)
        return self.execute_command(command)

    def maprfs_check_subfolder(self, path: str, deep_level: int, folder_name: str) -> List[str]:
        """
        check existence of subfolder by path on deep_level,
        Example:
        "/mapr/dp.prod.munich/ad-vantage/data/store/enriched/auto_labels/single", 5, "6ec6d14d-3e39-4bd2-a7f9-b646f7b96cd9"
        """
        return self.execute_command(f"find {path} -maxdepth {deep_level} -mindepth {deep_level} | grep {folder_name}")

    def maprfs_get_subfolders(self, path: str, deep_level: int) -> List[str]:
        """
        check existence of subfolder by path on deep_level,
        Example:
        "/mapr/dp.prod.munich/ad-vantage/data/store/enriched/auto_labels/single", 5
        """
        return self.execute_command(f"find {path} -maxdepth {deep_level} -mindepth {deep_level}")

    def elastic_records_by_session(self, url:str, index_name: str, session_id: str) -> List[str]:
        command = f'curl --silent -X GET "{url}/{index_name}/_count?q=sessionId:{session_id}" | jq ".count"'
        return self.execute_command(command)


def get_first_record(list_of_string: List[str])->str:
    if len(list_of_string)>0:
        return list_of_string[0]
    else:
        return ""


def get_last_subfolder(full_path: str)->str:
    marker = full_path.rfind("/")
    return full_path[marker+1:] if marker>0 else ""


def parse_login(var_name:str) -> str:
    dirty_value:str = var_name[len("USER_"):]
    last_underscore_position = dirty_value.rfind("_")
    if last_underscore_position>0:
        return dirty_value[:last_underscore_position]+"-"+ (dirty_value[last_underscore_position+1:] if len(dirty_value)>(last_underscore_position+1) else "")
    else:
        return dirty_value


def parse_passw(var_passw: str) -> str:
    return var_passw[1:].strip("\"")


def parse_users_from_env()-> Dict[str, str]:
    return_value: Dict[str, str] = dict()
    for each_value in str(subprocess.check_output("env")).split("\\n"):
        if each_value.startswith("USER_"):
            env_var_first_part = each_value.split("=")[0]
            return_value[parse_login(env_var_first_part)]=parse_passw(each_value[len(env_var_first_part):])
    return return_value


list_of_users = parse_users_from_env()
