# Open and close a popup in the UR5 GUI via 2 ports
# Helpful resources
import socket
import time

# initialise variables
UR5Controller = "192.168.0.7"    # IP address pf UR5 Controller
DASHBOARD_PORT = 29999  # Port to interface via DashBoard server
GENERAL_PORT = 30002    # Port to interface via URScript API & normal python code

# initialise sockets
dashboardSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
generalSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET stands for address family, using Internet Protocol 4
# SOCK_STREAM indicates the type of socket (in this case, it's TCP), as opposed to SOCK_DGRAM (UDP)

# connect to UR5 Controller via 2 ports
dashboardSocket.connect((UR5Controller, DASHBOARD_PORT))
generalSocket.connect((UR5Controller, GENERAL_PORT))
dataIn = dashboardSocket.recv(256)
print(dataIn)

while True:
    dataOut = raw_input("Enter message to send or type 'exit': ")
    if dataOut == "exit":
        break
    dashboardSocket.send(dataOut + "\n")

# close socket connection
dashboardSocket.close()
generalSocket.close()

print("End of program")
