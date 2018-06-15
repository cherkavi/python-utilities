import socket
import sys
from contextlib import closing


def check_port(host, port_number):
   with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(1)
        if sock.connect_ex((host, int(port_number))) == 0:
            print("%s : %s  >>open<<" % (host, port_number))
        else:
            print("%s : %s  NOT open" % (host, port_number))


if __name__=='__main__':
    check_port(sys.argv[1], sys.argv[2])