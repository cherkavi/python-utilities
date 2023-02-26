#!/usr/bin/env python

import os
import subprocess

OC_USER = os.environ.get("OC_USER")
OC_PASSWORD = os.environ.get("OC_PASSWORD")
OPEN_SHIFT_URL = oc.environ.get("OC_URL")


def clear_binary_line(b_line) -> str:
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


def execute_cmd_command(command_line) -> str:
    print(command_line)
    # text=True is not working with current python version
    return clear_binary_line(subprocess.check_output(command_line, shell=True))

execute_cmd_command(f"oc login -u {OC_USER} -p {OC_PASSWORD} {OPEN_SHIFT_URL}")

projects:[str]=[line.strip() for line in execute_cmd_command("oc get projects -o custom-columns=NAME:.metadata.name").split("\n") if line!="NAME"]    

error_map:[str,[str]]={}
for each_project in projects:
    print(f"project: {each_project}")
    execute_cmd_command(f"oc project {each_project}")
    error_map[each_project]=[]

    try:
        pvc_in_project_accessible:[str]=[line.strip() for line in execute_cmd_command("oc get pvc -o custom-columns=NAME:.metadata.name").split("\n") if line!="NAME"]    
    except subprocess.CalledProcessError:
        error_map[each_project].append("!!! not possible to read pvc from the project !!!")
        continue

    try:
        pvc_in_project_declared:[str]=execute_cmd_command("oc get dc -o jsonpath={.items[*].spec.template.spec.volumes[*].persistentVolumeClaim.claimName}").split(" ")
    except subprocess.CalledProcessError:
        error_map[each_project].append("!!! not possible to read dc from project !!!")
        continue

    for each_declared_pvc in pvc_in_project_declared:
        if each_declared_pvc not in pvc_in_project_accessible:
            error_map[each_project].append(each_declared_pvc)

for each_entry in error_map.items():
    errors=[', '.join(each_entry[1])]
    print(f"{each_entry[0]} : {errors}") 
    print("------------")


