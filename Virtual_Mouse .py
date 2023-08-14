# py -3.8 -m pip install autopy가 3.8까지밖에 지원 안함

import cv2
import numpy as np
import hand_traking_module as htm
import time
import autopy

################################
wCam,hCam =640,480
frameR = 100
smoothening = 2
################################

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

plocX,plocY = 0,0 #과거 위치
clocX,clocY = 0,0 #현재 위치

pTime = 0
cTime = 0

detector = htm.handDetector(maxHands=1)

wScr,hScr = autopy.screen.size() 

while True:
    try:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList,bbox = detector.findPosition(img)

        if len(lmList)!=0:
            x1,y1 = lmList[8][1:]
            x2,y2 = lmList[12][1:]

            # print(x1,y1,x2,y2)

            fingers = detector.fingersUp()
            # print(fingers)
            # cv2.rectangle(img,(frameR,0),(wCam-frameR,hCam-frameR*2),(255,0,255),2)
            cv2.rectangle(img,(frameR,frameR),(wCam-frameR,hCam-frameR),(255,0,255),2)

            if fingers[1] == 1 and fingers[2] == 0:

                x3 = np.interp(x1,(frameR,wCam-frameR),(0,wScr))
                y3 = np.interp(y1,(frameR,hCam-frameR),(0,hScr))

                colcX = plocX + (x3 - plocX)/smoothening
                colcY = plocY + (x3 - plocY)/smoothening

                autopy.mouse.move(x3,y3)
                cv2.circle(img,(x1,y1),15,(0,0,255),cv2.FILLED)
                plocX,plocY = clocX,clocY

            if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0:

                length,img,infoline=detector.findDistance(8,12,img)
                print(length)
                if length < 53:
                    cv2.circle(img,(infoline[4],infoline[5]),15,(0,255,0),cv2.FILLED)
                    autopy.mouse.click()
                    time.sleep(1)




        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
        cv2.imshow("Image",img)
        cv2.waitKey(1)
        
    except ValueError:continue