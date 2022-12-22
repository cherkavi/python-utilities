import subprocess
from subprocess import Popen

print("#call method return status of the message ")
print("command result: ", subprocess.call("ls", shell=False))
# for CentOS/RedHat projects need to use
# subprocess.call(["bash","java -jar my_app.jar"], shell=False)

print("#check_call method return status of the message ")
print("command result: ", subprocess.check_call("ls", shell=False))

print("#check_output method return status of the message ")
print("command result: ", subprocess.check_output(["ls", "."]).splitlines())


def clear_binary_line(b_line):
    # convert bytes to string, bytes2string, byte to string
    next_line = b_line.decode('utf-8')
    if next_line[len(next_line)-1] == "\n":
        next_line = next_line[:-1]
    index = next_line.rfind("/")
    if index >= 0:
        next_line = next_line[index+1:]
    return next_line

print("#execute command with linux pipe subprocess with linux pipe")
# No such file or directory: 'ls -la | grep py'
# :Popen[bytes]
ps = subprocess.Popen("ls -la | grep py | grep 2020 | awk '{print $9}'", shell=True, stdout=subprocess.PIPE)
output:str = clear_binary_line(ps.communicate()[0])
print(output)