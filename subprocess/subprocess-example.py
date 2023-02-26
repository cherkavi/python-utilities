from io import BufferedReader, BufferedWriter
import subprocess
import os
from subprocess import Popen
from tabnanny import check

from async_timeout import timeout


print("# call method return status of the message ")
print("command result: ", subprocess.call("ls", shell=False))
# for CentOS/RedHat projects need to use
# subprocess.call(["bash","java -jar my_app.jar"], shell=False)

print("# check_call method return status of the message ")
print("command result: ", subprocess.check_call("ls", shell=False))

print("# check_output method return status of the message ")
print("command result: ", subprocess.check_output(["ls", "."]).splitlines())


def clear_binary_line(b_line):
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

print("# print current home folder")
subprocess.Popen('echo $HOME', shell=True)
# throw exception - no home folder without Shell
# subprocess.Popen('echo $HOME', shell=False)

print("# execute command with linux pipe subprocess with linux pipe and obtain array of bytes")
process_bytes = subprocess.Popen("ls -la | grep py | grep 2020 | awk '{print $9}'", shell=True, stdout=subprocess.PIPE)
output:str = clear_binary_line(process_bytes.communicate()[0])
print(output)
process_bytes.terminate()

print("# execute command with linux pipe subprocess with linux pipe and obtain string, throw exception ")
process_string = subprocess.Popen("ls -la | grep py | grep 2020 | awk '{print $9}'", shell=True, stdout=subprocess.PIPE, text=True)
output:str = process_string.communicate()[0]
print(output)
process_string.terminate()

print("pipes between diff calls, pipes with processes")
p1 = subprocess.Popen(['lsb_release','-a'], stdout=subprocess.PIPE)
p2 = subprocess.Popen(['grep', 'Distributor'], stdin=p1.stdout, stdout=subprocess.PIPE)
p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits
output:str = p2.communicate()[0]
print(output)


# not working on linux
# print("# communication inside one process, multi commands execution ")
# p = Popen(['bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
# reader:BufferedReader = p.stdout
# writer:BufferedWriter = p.stdin

# writer.write('echo "hello world"'.encode("utf-8"))
# writer.flush()

# print(reader.read(1))
# print(reader.readline())

# writer.write('echo $?\n'.encode("utf-8"))
# writer.flush()
# if reader.readline().strip() == '0':
#     print("Command succeeded")

# writer.write('echo "bye world"'.encode("utf-8"))
# stdout, stderr = p.communicate()
# print(stdout)
