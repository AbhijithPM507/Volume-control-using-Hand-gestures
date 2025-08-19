import cv2
import numpy as np
import mediapipe as mp
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import IAudioEndpointVolume,AudioUtilities
import math
import pyautogui

cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

mHands=mp.solutions.hands
hands=mHands.Hands()
mpDraw=mp.solutions.drawing_utils

devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume=cast(interface,POINTER(IAudioEndpointVolume))
volRange=volume.GetVolumeRange()
minVol,maxVol=volRange[0],volRange[1]

prev_state=None

def fingers_up(lmList):
    fingers=[]
    if lmList[4][0] > lmList[3][0]:
        fingers.append(1)
    else:
        fingers.append(0)
        
    tips=[8,12,16,20]
    for tip in tips:
        if lmList[tip][1] < lmList[tip -2][1]:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers
    

while True:
    success,img=cap.read()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imgRGB)
    
    lmList=[]
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id,lms in enumerate(handLms.landmark):
                h,w,c=img.shape
                cx,cy=int(lms.x*w),int(lms.y*h)
                lmList.append((cx,cy))
            mpDraw.draw_landmarks(img,handLms,mHands.HAND_CONNECTIONS)
            
    if len(lmList) >= 9:
        x1,y1=lmList[4]
        x2,y2=lmList[8]
        
        cv2.circle(img,(x1,y1),10,(250,0,0),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(250,0,0),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(250,0,0),3)
        
        length=math.hypot(x2-x1,y2-y1)
        
        vol=np.interp(length,[30,200],[minVol,maxVol])
        volume.SetMasterVolumeLevel(vol,None)
        
        # fingers=fingers_up(lmList)
        # if fingers==[0,0,0,0,0] and prev_state!="paused":
        #     pyautogui.press("playpause")
        #     prev_state="paused"
        # elif fingers==[1,1,1,1,1] and prev_state!="playing":
        #     pyautogui.press("playpause")
        #     prev_state="playing"
        
        
    cv2.imshow('WOW',img)
    if cv2.waitKey(1) and 0xFF==ord('q'):
        break
    
cap.release(
    
)
cv2.destroyAllWindows()
        

