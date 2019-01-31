# Open and close a popup in the UR5 GUI via 2 ports
# Helpful resources
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import socket
import time

# initialise variables for Dashboard
UR5Controller = "192.168.0.7"    # IP address pf UR5 Controller
DASHBOARD_PORT = 29999  # Port to interface via DashBoard server

# initialise socket for Dashboard
dashboardSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to UR5 Controller via Dashboard ports
dashboardSocket.connect((UR5Controller, DASHBOARD_PORT))
data = dashboardSocket.recv(256)
print(data)

# initialise connection to Firebase
cred = credentials.Certificate('C:\\Users\\EEE\\Desktop\\jsonKeyFileFirebase.json')
firebase_admin.initialize_app(cred)
dataBase = firestore.client()
print("Connected to Google Firebase")

# initialise firebase variables
UR5LoadedProgram = dataBase.collection(u'UR5').document(u'loadedProgram')
UR5ProgramState = dataBase.collection(u'UR5').document(u'programState')

# send command to open and close a popup
while 1:
    time.sleep(5)

    # get loaded program of UR5
    dashboardSocket.send("get loaded program" + "\n")
    loadedProgramData = dashboardSocket.recv(256)
    print("Loaded Program is: " + loadedProgramData + "\n")
    time.sleep(0.25)

    # get program state of UR5
    dashboardSocket.send("programState" + "\n")
    programStateData = dashboardSocket.recv(256)
    print("Program State is: " + programStateData + "\n")
    time.sleep(0.25)

    # update loadedProgram document
    UR5LoadedProgram.update({
        u'loadedProgram': unicode(loadedProgramData),
    })

    # update programState document
    UR5ProgramState.update({
        u'programState': unicode(programStateData),
    })


# close socket connection
dashboardSocket.close()

print("End of program")
