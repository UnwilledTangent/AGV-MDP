# Save as server.py
# Message Receiver
# import os
# from socket import *
# host = ""
# port = 13000
# buf = 1024
# addr = (host, port)
# UDPSock = socket(AF_INET, SOCK_DGRAM)
# UDPSock.bind(addr)
# print("Waiting to receive messages...")
# while True:
#     (data, addr) = UDPSock.recvfrom(buf)
#     print("Received message: " + data)
#     if data == "exit":
#         break
# UDPSock.close()
# os._exit(0)

# Save as client.py
# Message Sender
import os
from socket import *
host = "192.168.100.100" # set to IP address of target computer
port = 27015
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
while True:
    data = raw_input("Enter message to send or type 'exit': ")
    UDPSock.sendto(data, addr)
    if data == "exit":
        break
UDPSock.close()
os._exit(0)
