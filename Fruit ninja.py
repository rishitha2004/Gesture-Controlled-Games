import cv2
from cvzone.HandTrackingModule import HandDetector
import mouse
import numpy as np
import pyautogui


cap = cv2.VideoCapture(0)
cam_w, cam_h = 640, 480
cap.set(3, cam_w)
cap.set(4, cam_h)
frameR=100
detector = HandDetector(detectionCon=0.65, maxHands=1)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img=detector.findHands(img)
    cv2.rectangle(img, (frameR, frameR), (cam_w-frameR, cam_h-frameR), (255,0,255), 2)
    if hands:
        lmlist=hands[0]['lmList']
        ind_x,ind_y=lmlist[8][0],lmlist[8][1]
        cv2.circle(img, (ind_x, ind_y), 5, (0, 255, 255), 2)
        conv_x = int(np.interp(ind_x, (frameR, cam_w - frameR), (0,1920)))
        conv_y = int(np.interp(ind_y, (frameR, cam_h - frameR), (0, 1080)))
        mouse.move(conv_x, conv_y)
        fingers=detector.fingersUp(hands[0])
        if fingers[4]==1:
            pyautogui.mouseDown()

    cv2.imshow("Feed", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()