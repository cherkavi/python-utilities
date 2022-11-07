#!/usr/bin/env python
import subprocess

output = subprocess.check_output(["curl", "--silent", "https://api.ipify.org"])
print(output)
