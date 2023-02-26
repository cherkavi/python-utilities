import os
import subprocess

OC_USER: str = os.environ.get("OC_USER")
OC_PASSWORD: str = os.environ.get("OC_PASS")
OPEN_SHIFT_URL: str = os.environ.get("OPEN_SHIFT_URL")

print(f"{OC_USER}")
print(f"{OC_PASSWORD}")
print(f"{OPEN_SHIFT_URL}")

def execute_cmd_command(command_line: str) -> str:
    print(f"command: {command_line}")
    return subprocess.check_output(command_line, shell=True, text=True)

print(execute_cmd_command(f"oc login -u {OC_USER} -p {OC_PASSWORD} {OPEN_SHIFT_URL}"))
print(execute_cmd_command(f"oc whoami"))
