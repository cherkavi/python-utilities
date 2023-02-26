#!/usr/bin/env python3

## check running pods in current project
## save results to ./reports subfolder
## in case of changes - send report to Microsoft Teams

import json
import os
import signal
import subprocess
import sys
import time
from datetime import datetime
from typing import List, Set

import requests
from requests import Response


def decode_binary_line(b_line):
    return b_line.decode('utf-8')


def run_command(command: str) -> List[str]:
    process: subprocess.Popen = None
    result: List[str] = []
    try:
        process = subprocess.Popen(command.split(" "), stdout=subprocess.PIPE)
        for b_line in process.stdout:
            line: str = decode_binary_line(b_line)
            if "Running" in line and "-job-" not in line:
                splitted_line: List[str] = line.split(" ")
                service_name: str = splitted_line[0]
                service_time: str = splitted_line[len(splitted_line) - 1].rstrip("\\n").rstrip("\n")
                result.append(f"{service_name} {service_time}")
        return sorted(result)
    finally:
        if process:
            process.stdout.close()


COMMAND_LINE = "oc get pods"
DELAY_IN_SEC_BETWEEN_OC_REQUESTS = 10
FOLDER_FOR_REPORTS = sys.argv[1] if len(sys.argv) > 1 else './reports'
TEAMS_TOKEN = os.environ.get("TEAMS_TOKEN")
TEAMS_CHANNEL_ID = os.environ.get("TEAMS_CHANNEL_ID")
TEAMS_TEAM_ID = os.environ.get("TEAMS_TEAM_ID")


def get_current_report_filename() -> str:
    return f"{FOLDER_FOR_REPORTS}/{datetime.now().strftime('%Y-%m-%d-%H_%M_%S')}"


def save_report_to_file(filename: str, data_for_writing: List[str]):
    with open(filename, "w") as output_file:
        for each_line in data_for_writing:
            print(each_line, file=output_file)
        output_file.flush()


def read_file(filename: str) -> List[str]:
    with open(filename, "r") as reportfile:
        result: List[str] = []
        for each_line in reportfile:
            elements: List[str] = each_line.split(" ")
            if len(elements) >= 1:
                result.append(elements[0])
        return result


def has_diff(filename_previous: str, filename_current: str) -> bool:
    if not filename_previous or filename_previous == "":
        return False
    data_previous: Set[str] = set(read_file(filename_previous))
    data_current: Set[str] = set(read_file(filename_current))
    return len(data_current - data_previous) > 0 or len(data_previous - data_current) > 0


def send_teams_message_with_text(message: str):
    response: Response = requests.post(
        f"https://graph.microsoft.com/v1.0/teams/{TEAMS_TEAM_ID}/channels/{TEAMS_CHANNEL_ID}/messages",
        json={"body": {"content": f"{message}"}},
        headers={"Authorization": f"Bearer {TEAMS_TOKEN}", "Content-type": "application/json"})
    return response.content


def send_teams_message(filename_report: str):
    print(f">>> {filename_report}")
    if TEAMS_TOKEN and TEAMS_CHANNEL_ID and TEAMS_TEAM_ID:
        send_teams_message_with_text(filename_report)


def get_current_status(signum, frame):
    print(f"{read_file(file_report_previous)}")


def send_test_teams_message(signum, frame):
    print(f"Send result: {send_teams_message_with_text(file_report_previous)}")


# kill -n 10 <ps id>
signal.signal(signal.SIGUSR1, send_test_teams_message)
# kill -n 12 <ps id>
signal.signal(signal.SIGUSR2, get_current_status)
print(f"Teams: {TEAMS_CHANNEL_ID}")
print("current process id:", os.getpid())

file_report_previous: str = ""
file_report_current: str = ""
if __name__ == '__main__':
    while 1:
        try:
            result: List[str] = run_command(COMMAND_LINE)
            file_report_current: str = get_current_report_filename()
            save_report_to_file(file_report_current, result)
            if has_diff(file_report_previous, file_report_current):
                send_teams_message(file_report_current)
            file_report_previous = file_report_current
        except Exception as ex:
            file_report_previous = ""
            print(f"error during next iteration execution: {ex}", file=sys.stderr)
        time.sleep(DELAY_IN_SEC_BETWEEN_OC_REQUESTS)
