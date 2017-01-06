from threading import Thread
from queue import Queue
import socket
from base64 import b64encode, b64decode


sock = None
socket_process = None


def socket_reader(s, q):
    while True:
        try:
            raw = s.recv(1024)
        except:
            break

        if len(raw) == 0:
            break

        data = b64encode(raw).decode()
        q.put('? {}'.format(raw))
        q.put('x {}'.format(data))

    q.put('! disconnected')


def message_printer(q):
    while True:
        print(q.get())


q = Queue()

message_process = Thread(target=message_printer, args=(q,))
message_process.start()

while True:
    line = input()

    # connect command
    if line.startswith('c '):
        try:
            _, host, port = line.split()
        except:
            q.put('! invalid args')
            continue

        if sock is not None:
            q.put('! already connected')
            continue

        try:
            sock = socket.create_connection((host, int(port)))
        except:
            print('! could not connect')
            continue

        socket_process = Thread(target=socket_reader, args=(sock, q))
        socket_process.start()
        q.put('! connected to {} {}'.format(host, port))
        continue

    # disconnect command
    if line.startswith('d '):
        if sock is None:
            q.put('! not connected')
            continue

        sock.close()
        sock = None
        continue

    if line.startswith('x '):
        if sock is None:
            q.put('! not connected')
            continue

        try:
            _, data = line.split()
        except:
            q.put('! invalid args')
            continue

        raw = b64decode(data)
        sock.send(raw)
        continue
