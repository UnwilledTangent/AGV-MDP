def main():
  


  def Connect_To_PLB(): #Function to establish socket connection with PLB
    Connected = False
    counter=0
    while not Connected and (counter<5):
      Connected=socket_open("192.168.0.5",6008,"Sick_Socket")
      counter=counter+1
    end
    if counter>=5:
      popup("Connection to PLB failed","Time out",False,True,blocking=True)
      halt
    else:
      textmsg("Connected to PLB")
    end
    
  end	
  
  def SendString(string): #Function to send a string over the socket. INPUT: string to send
    sent=False
    sent=socket_send_string(string, "Sick_Socket")
    sleep(0.1) 
    if not sent:
      popup("Failed to send string message","Message Transmission Failure",False,True,blocking=True) 
    end
  end
  
  def getMsg(expectedNumbers): #Function to get ascii float number responses. INPUT= Int number of expected floats. OUTPUT= list (length expectedNumbers+1) with expected numbers
    receivedNumbers=0
    
    while receivedNumbers==0:
      receivedMsg=socket_read_ascii_float(expectedNumbers,"Sick_Socket")
      receivedNumbers=receivedMsg[0]
    end
    return receivedMsg
  end

  def ReceiveCommand(type): #Function to receive the different types of response messages from PLB. INPUT= Int type number. OUTPUT= list (length depends on type) with received response
    
    if type==1:    #StateMsg
      
      receivedStateMsg=getMsg(3)
      return receivedStateMsg
    end
    if type==2:    #TriggerMsg
      receivedTrigMsg=getMsg(3)
      return receivedTrigMsg
    end
	if type==3: #PartMsg
	  receivedPartMsg=getMsg(22)
	  return receivedPartMsg
	  
    end
    if type==4: #BinMsg
      receivedBinMsg=getMsg(12)
      return receivedBinMsg
    end
	if type==5:    #AlignmentPointMsg
      receivedAlignPtMsg=getMsg(3)
      return receivedAlignPtMsg
    end
    if type==6: #VerifAlignmentMsg
      receivedVerifAlignMsg=getMsg(7)
      return receivedVerifAlignMsg
    end
	if type==7:    #SaveAlignmentMsg
      receivedSaveAlignMsg=getMsg(2)
      return receivedSaveAlignMsg
    end
  end
  
  def SetState(nState,sJobAlias): #Function to change the state of PLB. INPUT= int nState the desired state number, string sJobAlias the PLB job alias
      
    SendString("SetState,")
    if nState==1:
	  SendString("1,")
    elif nState==3:
	  SendString("3,")
    else:
	  popup("Unrecognized state")
    end
    SendString(sJobAlias)
    SendString(";")
    receivedStateMsg=ReceiveCommand(1)
	if receivedStateMsg[1]!=1:
      popup("Expected 	state message,Received Wrong type")
    end
    if receivedStateMsg[2]!=0:
      errorHandler(receivedStateMsg[2])
      halt
    end  
  end

  def Trigger(imageId): #Function to trigger an image with the camera. INPUT= int image ID number
    SendString("Trigger,")
    socket_set_var("imageId",imageId,"Sick_Socket")
    SendString(";")

    receivedTrigMsg=ReceiveCommand(2)
    if receivedTrigMsg[1]!=2:
      popup("Expected Trig message,Received Wrong type")
    end
    if receivedTrigMsg[2]!=0:
      errorHandler(receivedTrigMsg[2])
      halt
    end
  end 
  
  def LocatePart(jobAlias): #Function to ask PLB to locate a part. INPUT= string PLB job Alias. OUTPUT=list with received part result data
    SendString("LocatePart,")
    SendString(jobAlias)
    SendString(";")
    receivedPartMsg=ReceiveCommand(3)
    if receivedPartMsg[1]!=3:
      popup("Expected Part message,Received Wrong type")     
    end
    
	if receivedPartMsg[2]==111 and receivedPartMsg[2]==112 and receivedPartMsg[2]==113 and receivedPartMsg[2]==114:
		receivedPartMsg=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		
	elif receivedPartMsg[2]!=0 and receivedPartMsg[2]!=3 and receivedPartMsg[2]!=111 and receivedPartMsg[2]!=112 and receivedPartMsg[2]!=113 and receivedPartMsg[2]!=114: #if result not OK and not a license error
      errorHandler(receivedPartMsg[1])
       halt
	end
    
    return receivedPartMsg
  end
  
  def LocateBin(jobAlias): #Function to ask PLB to locate a bin. INPUT= string PLB job Alias.
    SendString("LocateBin,")
    SendString(jobAlias)
    SendString(";")
    receivedBinMsg=ReceiveCommand(4)
    if receivedBinMsg[1]!=4:
      popup("Expected Bin message,Received Wrong type")     
    end
    if receivedBinMsg[2]!=0 and receivedBinMsg[2]!=3 :
      errorHandler(receivedBinMsg[2])
       halt
    end
    
  end
    
  
  def AddAlignmentPoint(positionVector): # Function to send an AddAlignmentPoint command to PLB. INPUT=position of the robot as a meter vector (list length 3)
    socket_set_var("posX",positionVector[0]*1000,"Sick_Socket")
    SendString(",")
    socket_set_var("posY",positionVector[1]*1000,"Sick_Socket")
    SendString(",")
    socket_set_var("posZ",positionVector[2]*1000,"Sick_Socket")
    SendString(";")
    receivedAlignPtMsg=ReceiveCommand(5)
    if receivedAlignPtMsg[1]!=5:
      popup("Expected alignment point message,Received Wrong type")
    end
    if receivedAlignPtMsg[2]!=0:
      errorHandler(receivedAlignPtMsg[2])
      halt
    end
  end 
  
  def VerifyAlignment(positionVector): # Function to send an VerifyAlignment command to PLB. INPUT=position of the robot as a meter vector (list length 3)
    socket_set_var("VerifposX",positionVector[0]*1000,"Sick_Socket") 
    SendString(",")
    socket_set_var("VerifposY",positionVector[1]*1000,"Sick_Socket")    
    SendString(",")
    socket_set_var("VerifposZ",positionVector[2]*1000,"Sick_Socket")    
    SendString(";")
    receivedVerifAlignMsg=ReceiveCommand(6)
    if receivedVerifAlignMsg[1]!=6:
      popup("Expected VerifyAlignment message,Received Wrong type")
    end
    if receivedVerifAlignMsg[2]!=0: 
      errorHandler(receivedVerifAlignMsg[2])
    end
       
  end
  
  def SaveAlignment(): # Function to send a SaveAlignment command to PLB.
    SendString("SaveAlignment;")
	receivedSaveAlignMsg=ReceiveCommand(7)
	if receivedSaveAlignMsg[1]!=7:
      popup("Expected SaveAlignment message,Received Wrong type")
    end
    if receivedSaveAlignMsg[2]!=0:
      errorHandler(receivedSaveAlignMsg[2])
      halt
    end
  end
  
  def extractPosVect(): #Function to extract the position vector of the present TCP position
    pose=get_actual_tcp_pose()
	vec=[0,0,0]
	vec[0]=pose[0]
	vec[1]=pose[1]
	vec[2]=pose[2]
    return vec
  end
  
  def PerformAlignment(): #Function to perform a PLB HEA procedure (adapt robot positions to your environment!)
    SetState(3,"Job")
	# !!!!!! ADAPT THE ROBOT POSITIONS TO YOUR ENVIRONMENT !!!!!!!
	
	movep(p[.151568921592, .460281512138, .259561009600, .048331736095, .015079315702, 2.868624716847], a=1.2, v=0.25, r=0.025) #Move with robot to first position	
    Trigger(1) #First Image
    vec1=extractPosVect() #store position vector
    AddAlignmentPoint(vec1) #Add alignment point to PLBs HEA procedure

	#repeat for the rest of the positions
	movep(p[-.139404452817, .523078933418, .252379127371, -.065841045101, .041544435660, -2.860108630683], a=1.2, v=0.25, r=0.025)
    Trigger(2)
    vec2=extractPosVect()
    AddAlignmentPoint(vec2)

    movep(p[-.269123415887, .447587435739, .200033344414, -.094784056126, .085108761107, -2.568228916725], a=1.2, v=0.25, r=0.025)
	Trigger(3)   
    vec3=extractPosVect()
    AddAlignmentPoint(vec3)

	movep(p[-.371060412623, .083659020183, .212930115399, .012872680108, .096038381121, -1.725588836721], a=1.2, v=0.25, r=0.025)
    Trigger(4)   
    vec4=extractPosVect()
    AddAlignmentPoint(vec4)

    movep(p[-.043092213663, .325157262058, .224341494607, .116202156623, -.014207057654, -2.895107632763], a=1.2, v=0.25, r=0.025)   
    Trigger(5) 
	vec5=extractPosVect()
    AddAlignmentPoint(vec5)

	movep(p[.146060260711, .453788023418, .313324213647, -.104643134723, .008540694918, 2.840992049902], a=1.2, v=0.25, r=0.025)
    Trigger(6)   
    vec6=extractPosVect()
    AddAlignmentPoint(vec6)

	movep(p[-.271941966011, .416737861273, .280460201016, .098479152458, .023054504674, -2.558237358906], a=1.2, v=0.25, r=0.025)
    Trigger(7)   
    vec7=extractPosVect()
    AddAlignmentPoint(vec7)

    movep(p[-.135594358561, .507948669203, .331497826682, -.035484642710, .123135758275, -2.872249849368], a=1.2, v=0.25, r=0.025)
    Trigger(10) 
	vec10=extractPosVect()
    AddAlignmentPoint(vec10)
	
    movep(p[-.27491, .23223, .31975, -.054759605657, .155227213554, -2.797011908045], a=0.2, v=0.1, r=0.025)
    Trigger(11) 
	vec11=extractPosVect()
    AddAlignmentPoint(vec11)
	
    movep(p[-.404259302592, .123441595111, .552119471181, -.074626369964, .062714911844, -1.805916959848], a=1.2, v=0.1, r=0.025)
    Trigger(12) 
	vec12=extractPosVect()
    AddAlignmentPoint(vec12)
	
    movep(p[.220035674776, .424398228894, .433847097582, -.002630243902, -.090151219806, 2.690671470860], a=1.2, v=0.15, r=0.025)
    Trigger(13) 
	vec13=extractPosVect()
    AddAlignmentPoint(vec13)
	
    movep(p[-.015911605212, .280990025248, .434455908148, -.078162653949, .063540927489, -2.858458126862], a=1.2, v=0.25, r=0.025)
    Trigger(14) 
	vec14=extractPosVect()
    AddAlignmentPoint(vec14)
	
    movep(p[-.142713515206, .489732795233, .362369980917, -.136137869683, .157228683584, -2.825565463452], a=1.2, v=0.25, r=0.025)
    Trigger(15) 
	vec15=extractPosVect()
    AddAlignmentPoint(vec15)	
	
    SaveAlignment() 
	
	#Verify Alignment with 2 points
    SetState(1,"Job")
    movep(p[-.09175, .4616, .4937, 0.0125, .1783, 2.2116], a=1.2, v=0.25, r=0.025)
	Trigger(1)	
	Verifvec1=extractPosVect()
    VerifyAlignment(Verifvec1) 
	
	movep(p[.13707, .50438, .38195, 0.1233, .0633, 1.7322], a=1.2, v=0.25, r=0.025)
	Trigger(2)	
	Verifvec2=extractPosVect()
    VerifyAlignment(Verifvec2) 
	
  end
  
  def extractFromList(list,startingIndex,Length): #Function extracting a subset list out of a list. INPUT=list to make the extraction from, int starting extraction index,int length of extraction. OUTPUT= Extracted list
    counter=0
    if Length==6:
      extractedList=[-1,-1,-1,-1,-1,-1]
    elif Length==3:
      extractedList=[-1,-1,-1]
    end
    while counter<Length:
      extractedList[counter]=list[startingIndex]
      counter=counter+1
      startingIndex=startingIndex+1
    end
    return extractedList
  end
    
  def convertPose(PoseFromPLB): #Function to convert the frames from a list with millimiters, and RPY angles in degrees data (as returned by PLB) to a pose variable (meters, radians, axis angle notation) as used by the UR robot. INPUT=list (length 6) with frame format from PLB (mm, RPY angles in degrees). OUTPUT=UR robot pose.
    
    rotRPY=[0,0,0]
    rotRPY[0]=d2r(PoseFromPLB[3])  #Rx
    rotRPY[1]=d2r(PoseFromPLB[4])  #Ry
    rotRPY[2]=d2r(PoseFromPLB[5])  #Rz
    rotVec=rpy2rotvec(rotRPY)
    convertedPose=p[PoseFromPLB[0]/1000,PoseFromPLB[1]/1000,PoseFromPLB[2]/1000,rotVec[0],rotVec[1],rotVec[2]]
    return convertedPose
  end

  def calculateFinalPose(partFrame,relativeToolFrame,verticalCorrection): #Function first converting the frames from list to pose variable then pose multiplying them to obtain the final robot pose. INPUT: 3 lists (length 6) containing PF, RF and VC data. OUTPUT= final pose
    partFramePose=convertPose(partFrame)
    relativeToolFramePose=convertPose(relativeToolFrame)
    verticalCorrectionPose=convertPose(verticalCorrection)
    
    finalPose=pose_trans(verticalCorrectionPose,partFramePose)
  
    finalPose=pose_trans(finalPose,relativeToolFramePose)
    return finalPose
  
  end

  def extractPose(partData):  #Function extracting a meaningful pose from the part result data obtained from PLB. INPUT= list PartResult from PLB (length 22). OUTPUT=final pose.
    partFrame=extractFromList(partData,4,6)
    relativeToolFrame=extractFromList(partData,10,6)
    verticalCorrection=extractFromList(partData,16,6)
    finalPose=calculateFinalPose(partFrame,relativeToolFrame,verticalCorrection)
   
    return 
	
	
	
  end
  
  def errorHandler(errorNumber): #Function returning a popup error message according to the error number from PLB. INPUT=int the PLB error number.
    if errorNumber==-1:
      popup("PLB error -1:Unexpected Error")
    elif errorNumber==1:
      popup("PLB error 1:Robot communication error")
	elif errorNumber==2:
      popup("PLB error 2:Sensor Error")
	elif errorNumber==3:
      popup("PLB error 3:License Error")
	elif errorNumber==21:
      popup("PLB error 21:Unknown Job")
	elif errorNumber==22:
      popup("PLB error 22:Invalid Job")
	elif errorNumber==31:
      popup("PLB error 31:Set state failed")
	elif errorNumber==32:
      popup("PLB error 32:PLB Busy")
	elif errorNumber==41:
      popup("PLB error 41:Trigger error")
	elif errorNumber==42:
      popup("PLB error 42:Invalid State for Triggering")
	elif errorNumber==43:
      popup("PLB error 43:Overtriggered")
	elif errorNumber==44:
      popup("PLB error 44:Acquisition Failed")
	elif errorNumber==101:
      popup("PLB error 101:No image")
	elif errorNumber==102:
      popup("PLB error 102:Invalid State")
	elif errorNumber==103:
      popup("PLB error 103:PLB Busy")
	elif errorNumber==111:
      popup("PLB error 111:No part located")
	elif errorNumber==112:
      popup("PLB error 112:Part Overlapped")
	elif errorNumber==113:
      popup("PLB error 113:Gripper collision")
	elif errorNumber==114:
      popup("PLB error 114:Bin empty")
	elif errorNumber==121:
      popup("PLB error 121:Bin not found")
	elif errorNumber==131:
      popup("PLB error 131:Alignment target not found")
	elif errorNumber==132:
      popup("PLB error 132: Failed to add Alignment point")
    elif errorNumber==133:
      popup("PLB error 133: Too few points in Alignment")
    elif errorNumber==134:
      popup("PLB error 134:Alignment calculation failed")
    elif errorNumber==135:
      popup("PLB error 135:Alignment deviation Threshold exceeded")
    elif errorNumber==136:
      popup("PLB error 136:Too much scaling")	 
    elif errorNumber==137:
      popup("PLB error 137:Invalid Z axis direction")
    end	  
  end   
  
  Connect_To_PLB()
  rq_activate()
  PerformAlignment()
  SetState(1,"Nut")
  scancounter=0
  While scancounter<3:
	  Trigger(1)
	  LocateBin("Job")
	  partData1=LocatePart("Nut")
	  pos1=extractPose(partData1)
	  partData2=LocatePart("Conrod")
	  pos2=extractPose(partData2)
	  partData3=LocatePart("TopFrame")
	  pos3=extractPose(partData3)
	  zlist=[pos1[2],pos2[2],pos3[2]]
	  zlist.sort()
	  for x (0,len(zlist):
		if zlist[-1]==0
			scancounter+=1
			break
		
		elif zlist[-1]==pos1[2]:				#Compare data to see if matches
			scancounter=0
			zlist.remove(pos1[2]])			#remove the largest number from list
			pos=pos1							#Substitute the variable pos
			movep(pose_trans(pos,p[0,0,-0.100,0,0,0])) #PRE-PICK POS AT A POSITION 100mm IN NEGATIVE TOOL Z DIRECTION FROM PICK POSITION
			##Open gripper
			rq_open_and_wait()
			movep(pos)
			##Close gripper
			rq_close_and_wait()
			movep(pose_trans(pos,p[0,0,-0.100,0,0,0]))
			##move to home position of UR5
			popup("Moving to Home Position","Note",False,False,blocking=True)
			#waypoint 4
			movel(p[-353.76, -326.16, 555.47, 1.1881, -2.8890, -0.0133], a=1.2, v=0.25, r=0)
			##move to box 1
			popup("Moving to Box 1","Note",False,False,blocking=True)
			#middle_pos
			movej(p[184.03, -213.68, 570.52, 1.1752, -2.9189, -0.0091], a=1.2, v=0.25, r=0)
			#waypoint 24
			movej(p[197.68, -210.87, 617.89, 1.1754, -2.9188, -0.0095], a=1.2, v=0.25, r=0)
			#scanning
			movej(p[296.03, -258.02, 590.58, 1.1551, -2.9177, -0.0457], a=1.2, v=0.25, r=0)
			#waypoint 6
			movej(p[427.85, -199.30, 554.66, 2.8721, -1.2543, -0.035], a=1.2, v=0.25, r=0)
			#lower_into_box
			movel(p[427.84, -199.22, 522.64, 2.8723, -1.2541, -0.0347], a=1.2, v=0.25, r=0)
			##Open gripper of UR5
			rq_open_and_wait()
			##move to home position of UR5
			popup("Moving to Home Position","Note",False,False,blocking=True)
			#waypoint 6
			movel(p[427.85, -199.30, 554.66, 2.8721, -1.2543, -0.035], a=1.2, v=0.25, r=0)
			#middle_pos
			movej(p[184.03, -213.68, 570.52, 1.1752, -2.9189, -0.0091], a=1.2, v=0.25, r=0)
			
		elif zlist[-1]==pos2[2]:
			scancounter=0
			pos=pos2
			zlist.remove(pos2[2])
			movep(pose_trans(pos,p[0,0,-0.100,0,0,0])) #PRE-PICK POS AT A POSITION 100mm IN NEGATIVE TOOL Z DIRECTION FROM PICK POSITION
			##Open gripper
			rq_open_and_wait()
			movep(pos)
			##Close gripper
			rq_close_and_wait()
			movep(pose_trans(pos,p[0,0,-0.100,0,0,0]))
			##move to home position of UR5
			popup("Moving to Home Position","Note",False,False,blocking=True)
			#waypoint 4
			movel(p[-353.76, -326.16, 555.47, 1.1881, -2.8890, -0.0133], a=1.2, v=0.25, r=0)
			##move to box 2
			popup("Moving to Box 2","Note",False,False,blocking=True)
			#middle_pos
			movej(p[184.03, -213.68, 570.52, 1.1752, -2.9189, -0.0091], a=1.2, v=0.25, r=0)
			#waypoint 24
			movej(p[197.68, -210.87, 617.89, 1.1754, -2.9188, -0.0095], a=1.2, v=0.25, r=0)
			#scanning
			movej(p[296.03, -258.02, 590.58, 1.1551, -2.9177, -0.0457], a=1.2, v=0.25, r=0)
			#waypoint 6
			movej(p[427.85, -199.30, 554.66, 2.8721, -1.2543, -0.035], a=1.2, v=0.25, r=0)
			#lower_into_box
			movel(p[427.84, -199.22, 522.64, 2.8723, -1.2541, -0.0347], a=1.2, v=0.25, r=0)
			##Open gripper of UR5
			rq_open_and_wait()
			##move to home position of UR5
			popup("Moving to Home Position","Note",False,False,blocking=True)
			#waypoint 6
			movel(p[427.85, -199.30, 554.66, 2.8721, -1.2543, -0.035], a=1.2, v=0.25, r=0)
			#middle_pos
			movej(p[184.03, -213.68, 570.52, 1.1752, -2.9189, -0.0091], a=1.2, v=0.25, r=0)
			
		elif zlist[-1]==pos3[2]:
			scancounter=0
			pos=pos3 
			zlist.remove(pos3[2])
			movep(pose_trans(pos,p[0,0,-0.100,0,0,0]))
			#PRE-PICK POS AT A POSITION 100mm IN NEGATIVE TOOL Z DIRECTION FROM PICK POSITION
			##Open gripper
			rq_open_and_wait()
			movep(pos)
			##Close gripper
			rq_close_and_wait()
			movep(pose_trans(pos,p[0,0,-0.100,0,0,0]))
			##move to home position of UR5
			popup("Moving to Home Position","Note",False,False,blocking=True)
			#waypoint 4
			movel(p[-353.76, -326.16, 555.47, 1.1881, -2.8890, -0.0133], a=1.2, v=0.25, r=0)
			##move to box 3
			popup("Moving to Box 3","Note",False,False,blocking=True)
			#middle_pos
			movej(p[184.03, -213.68, 570.52, 1.1752, -2.9189, -0.0091], a=1.2, v=0.25, r=0)
			#waypoint 24
			movej(p[197.68, -210.87, 617.89, 1.1754, -2.9188, -0.0095], a=1.2, v=0.25, r=0)
			#scanning
			movej(p[296.03, -258.02, 590.58, 1.1551, -2.9177, -0.0457], a=1.2, v=0.25, r=0)
			#waypoint 6
			movej(p[427.85, -199.30, 554.66, 2.8721, -1.2543, -0.035], a=1.2, v=0.25, r=0)
			#lower_into_box
			movel(p[427.84, -199.22, 522.64, 2.8723, -1.2541, -0.0347], a=1.2, v=0.25, r=0)
			##Open gripper of UR5
			rq_open_and_wait()
			##move to home position of UR5
			popup("Moving to Home Position","Note",False,False,blocking=True)
			#waypoint 6
			movel(p[427.85, -199.30, 554.66, 2.8721, -1.2543, -0.035], a=1.2, v=0.25, r=0)
			#middle_pos
			movej(p[184.03, -213.68, 570.52, 1.1752, -2.9189, -0.0091], a=1.2, v=0.25, r=0)
	end
	main() 