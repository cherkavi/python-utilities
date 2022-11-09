# web-socket

## socket client

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/web-socket/socket-client.py) -->
<!-- The below code snippet is automatically added from ../../python/web-socket/socket-client.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## socket server

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/web-socket/socket-server.py) -->
<!-- The below code snippet is automatically added from ../../python/web-socket/socket-server.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## vars

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/web-socket/vars.py) -->
<!-- The below code snippet is automatically added from ../../python/web-socket/vars.py -->
```py
HOST = "127.0.0.1"
PORT = 3003
QUEUE_LEN = 1
```
<!-- MARKDOWN-AUTO-DOCS:END -->


