import subprocess

print("#call method return status of the message ")
print("command result: ", subprocess.call("ls", shell=False))

print("#check_call method return status of the message ")
print("command result: ", subprocess.check_call("ls", shell=False))

print("#check_output method return status of the message ")
print("command result: ", subprocess.check_output(["ls", ".."]).splitlines())


# for CentOS/RedHat projects need to use
# subprocess.call(["bash","java -jar my_app.jar"], shell=False)