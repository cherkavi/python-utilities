import telnetlib
import time
import configparser
import re

host = "212.90.56.52"
port = 93
telnet = None


try:
    print("attempt to connect")
    telnet = telnetlib.Telnet(host, port, timeout=4)
    #print("connected:"+str(telnet))
    telnet.read_until(bytes("login:", "utf8"))
    telnet.write(bytes("admin\n\r", "utf8"))
    #print("waiting for password")
    telnet.read_until(bytes("word:", "utf8"))
    #print("enter password:")
    telnet.write(bytes("admin\n\r", "utf8"))
    telnet.read_until(bytes("\n\r: ", "utf8"))
    print("menu information")
    telnet.write(bytes("i", "utf8"))
    telnet.read_until(bytes("\n\r: ", "utf8"))
    telnet.write(bytes("d", "utf8"))
    return_value=[]
    for line in str(telnet.read_until(bytes("\n\r: ", "utf8"))).split("\\n\\r"):
        if line.startswith("DG"):
            return_value.append(re.sub("[^0-9]*", "", line))
    print(return_value)
except Exception as e:
    print("can't connect")
finally:
    if telnet != None:
        try:
            telnet.close()
        except Exception as e:
            pass