#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cvzone
import cv2
import numpy as np
import mediapipe
from cvzone.FaceMeshModule import FaceMeshDetector
from datetime import datetime, timedelta
cap=cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)
idlist =[22,23,24,26,110,157,158,159,160,161,130,243]
ratioList = []
blinkCounter = 0
counter = 0
color = (255, 0, 255)
t=datetime.now()

while True:
    rat, frame=cap.read()
    frame,faces= detector.findFaceMesh(frame)
    #checking screen time 
    
    current_time = datetime.now()
    dif = current_time - t 
    mins, secs = divmod(dif.total_seconds(), 60)
    min = int(mins)
    sec = int(secs)
    timer = '{:02d}:{:02d}'.format(min, sec)
    cvzone.putTextRect(frame, timer, (390, 100), scale=1.5,
                           colorR=color)
    
    if dif.total_seconds() > 1200:# Here 10 means 10 seconds. Put the required time in seconds, for eg:- 5 mins = 300s
        for sec in range(15):
            cvzone.putTextRect(frame, 'Take a break', (50, 150), scale=1.5,
                           colorR=color)
            
            
        
    
            
        # print('{:%H:%M:%S}'.format(current_time))

    
    if faces:
        face= faces[0]
        for id in idlist:
            cv2.circle(frame,face[id],5,(255,0,255),cv2.FILLED)
        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]
        lenghtVer, _ = detector.findDistance(leftUp, leftDown)
        lenghtHor, _ = detector.findDistance(leftLeft, leftRight)
        cv2.line(frame, leftUp, leftDown, (0, 200, 0), 3)
        cv2.line(frame, leftLeft, leftRight, (0, 200, 0), 3)
        ratio = int((lenghtVer / lenghtHor) * 100)
        ratioList.append(ratio)
        if len(ratioList) > 3:
            ratioList.pop(0)
        ratioAvg = sum(ratioList) / len(ratioList)
        if ratioAvg < 35 and counter == 0:
            blinkCounter += 1
            color = (0,200,0)
            counter = 1
        if counter != 0:
            counter += 1
            if counter > 10:
                counter = 0
                color = (255,0, 255)
        cvzone.putTextRect(frame, f'Blink Count: {blinkCounter}', (50, 200),
                           colorR=color)
        if blinkCounter <12 and dif.total_seconds() > 60:
            cvzone.putTextRect(frame, 'blink your eyes more often', (50, 300), scale=1.5,
                           colorR=color)
            if blinkCounter>12:
                break
            
    
    cv2.imshow('frame',frame)       
    if cv2.waitKey(1) == ord('q'):
        break


# In[ ]:




