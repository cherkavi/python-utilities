import vars
import socket
import contextlib


def start_listener():
    with contextlib.closing(socket.socket()) as sock:
        sock.bind((vars.HOST, vars.PORT))
        sock.listen(vars.QUEUE_LEN)
        # need to start separate Thread
        while True:
            connection, address = sock.accept()
            print(address)
            data = connection.recv(1024)
            if data:
                print("data from socket:" + str(data))
                connection.send(data[::-1])
            connection.close()


if __name__ == "__main__":
    start_listener()