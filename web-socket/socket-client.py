import vars
import socket
import contextlib


def start_sender():
    with contextlib.closing(socket.socket()) as sock:
        sock.connect((vars.HOST, vars.PORT))
        # convert string to bytes
        sock.send("this is my string".encode("utf-8"))
        data = sock.recv(1024)
        if data:
            print("data after sending: " + str(data))


if __name__ == "__main__":
    start_sender()