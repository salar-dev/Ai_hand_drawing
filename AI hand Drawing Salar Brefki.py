## SALAR BERFKI

# Facebook - https://www.facebook.com/salar.brefki
# Instagram - https://www.instagram.com/salarbrefki

from pickle import TRUE
import cv2
import mediapipe as mp
import numpy as np
import os

folderPath = 'header'
myList = os.listdir(folderPath)
# print(myList)
overLayList = []

for imgpath in myList:
   image = cv2.imread(f'{folderPath}/{imgpath}')
   overLayList.append(image)
# print(len(overLayList))

header = overLayList[3]
drawColor = (0, 0, 255)

brushThickness = 15
erasserThickness = 60


cap = cv2.VideoCapture(0)

cap.set(3, 1280)
cap.set(4, 720)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
tipIds = [4, 8, 12, 16, 20]

xp, yp = 0, 0

imgCanves = np.zeros((720, 1280, 3), np.uint8)

while True:
   # 1- Import Image
   success, img = cap.read()
   img = cv2.flip(img, 1)

   # 2- Find Hand Landmarks

   imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

   results = hands.process(imgRGB)

   lmList = []

   if results.multi_hand_landmarks:
      for handLms in results.multi_hand_landmarks:
         for id, lm in enumerate(handLms.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])
            # mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            # tip of index and middel fingers
            if len(lmList) == 21:
               x1, y1 = lmList[8][1:]
               x2, y2 = lmList[12][1:]

               # 3- Check which fingers are ap

               fingers = []

               if lmList[tipIds[0]][1] < lmList[tipIds[0] - 2][1]:
                  fingers.append(1)
               else:
                  fingers.append(0)

               for tip in range(1, 5):
                  if lmList[tipIds[tip]][2] < lmList[tipIds[tip] - 2][2]:
                     fingers.append(1)
                  else:
                     fingers.append(0)
               # print(fingers)
            

               # 4- If Selection Mode - Tow finger are up
               if fingers[1] and fingers[2]:
                  xp, yp = 0, 0
                  cv2.rectangle(img, (x1, y1), (x2, y2), drawColor, cv2.FILLED)
                  print('Selection Mode')

                  #Checking for the click
                  if y1 < 147:
                     if 300 < x1 < 450:
                        header = overLayList[3]
                        drawColor = (0, 0, 255)
                     elif 550 < x1 < 750:
                        header = overLayList[1]
                        drawColor = (255, 0, 0)
                     elif 800 < x1 < 950:
                        header = overLayList[2]
                        drawColor = (0, 255, 0)
                     elif 990 < x1 < 1180:
                        header = overLayList[0]
                        drawColor = (0, 0, 0)


               # 5- If Drawing Mode - Index finger is up
               if fingers[1] and fingers[2] == False:
                  cv2.circle(img, (x1, y1) , 15, drawColor, cv2.FILLED)
                  print('Drawing Mode')
                  if xp == 0 and yp == 0:
                     xp , yp = x1, y1

                  if drawColor == (0, 0, 0):
                     cv2.line(img, (xp, yp), (x1, y1), drawColor, erasserThickness)
                     cv2.line(imgCanves, (xp, yp), (x1, y1), drawColor, erasserThickness)
                  else:
                     cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                     cv2.line(imgCanves, (xp, yp), (x1, y1), drawColor, brushThickness)

                  xp, yp = x1, y1

   imgGray = cv2.cvtColor(imgCanves, cv2.COLOR_BGR2GRAY)
   _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
   imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
   img = cv2.bitwise_and(img, imgInv)
   img = cv2.bitwise_or(img, imgCanves)


   img[0:147, 0:1268] = header
   # img = cv2.addWeighted(img, 0.5, imgCanves, 0.5, 0)
   cv2.imshow('Hand Tracker', img)
   if cv2.waitKey(5) & 0xff == 27:
      break

## SALAR BERFKI

# Facebook - https://www.facebook.com/salar.brefki
# Instagram - https://www.instagram.com/salarbrefki