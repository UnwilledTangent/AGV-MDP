# server
# message receiver

import socket

fireBaseSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
fireBaseSocket.bind((socket.gethostname(), 13000))
fireBaseSocket.listen(5)
print("fireBaseSocket listening")
UR5, address = fireBaseSocket.accept()
print("Got connection from ", address)

while True:
    # accept connections from outside
    data = UR5.recv(1024)
    print("Data received is " + data)
    if not data:
        break

UR5.close()
