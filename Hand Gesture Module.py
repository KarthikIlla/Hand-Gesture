# Imorting All the required Modules Necessary 
# (opencv, mediapipe, numpy)
# You may include math and time for displaying fps with ouput source
#############################################################################################################
import cv2
import mediapipe as mp
import time
#import math
#############################################################################################################



# The main code is for you to make the class handDetector with all the required functions for getting the 
# info from the detected hand
# For each functions input, output and what has to be done is been included, your task is to write the code
# for getting the required output from the input in the respective functions
#############################################################################################################





class handDetector():
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
# Firstly the initialize constuctor is already defined if need be you can make any changes to this constructor
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

#############################################################################################################
# findHands function takes the image source from the calling block and if the input draw = True then draw the
# hands with all the landmarks using mediapip Hands solution (Read the doc for details)
# Also add the results to the class variable results which would then be used for further calculations
    def findHands(self, img, draw=True):
        #Firstly remember to convert the given image in RBG to RGB
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # call hands.process and pass the converted image to it and store in self.results
        self.results = self.hands.process(imgRGB)

        # For Debugging you can print(results.multi_hand_landmarks)
        # Write the code for drawing the landmarks
        if draw:
           if self.results.multi_hand_landmarks:
              for handLms in self.results.multi_hand_landmarks:
                  self.mpDraw.draw_landmarks(img, handLms,self.mpHands.HAND_CONNECTIONS)
        # Finally return the image

        return img
# findPosition function takes the image source, hand we are currently working in the image source
# and if to draw or not from the calling block and if the input draw = True then draw the
# hand positions with all the landmarks using mediapip Hands solution (Read the doc for details)
# also make the x-coordinate, y-coordinate and the the rectangle containing the hand and also the landmark list
# Also add the results to the class variable results which would then be used for further calculations
    def findPosition(self, img, handNo=0, draw=True):

        bbox = []
        h, w, c = img.shape
        x_max = 0
        y_max = 0
        x_min = w
        y_min = h
        self.lmList = []
        #Write the code here
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                cx = int(lm.x * w)
                cy = int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if cx > x_max:
                    x_max = cx
                if cx < x_min:
                    x_min = cx
                if cy > y_max:
                    y_max = cy
                if cy < y_min:
                    y_min = cy
            bbox = [(x_min,y_min),(x_max,y_max)]

            if draw:
                cv2.rectangle(img, (x_min - 10, y_min - 10), (x_max + 10, y_max + 10), (0, 255, 0), 2)







        # Remember: mp gives you landmarks which are normalized to 0.0 and 1.0 which need to be converted into 
        # exact coordinates for use


        # Draw if the draw given is true

        return self.lmList, bbox
# fingersUp function return list of 5 fingers and their respective state
# 0- down and 1- Up
# Make sure to go through the mediapipe docs to get to know landmark 
# number of each finger and a method to know if the finger is up or not 
    def fingersUp(self):
        fingers = []
        rotlmlist = []
        if self.lmList:
           x = self.lmList[9][1]-self.lmList[0][1]
           y = self.lmList[9][2]-self.lmList[0][2]
           cos = y / ((x ** 2 + y ** 2) ** 0.5)
           sin = x / ((x ** 2 + y ** 2) ** 0.5)
           for i in range(21):
              X = self.lmList[i][1] * cos - self.lmList[i][2] * sin
              Y = self.lmList[i][1] * sin + self.lmList[i][2] * cos
              rotlmlist.append([i, X, Y])
           if rotlmlist[17][1] > rotlmlist[4][1]:
               if rotlmlist[4][1] > rotlmlist[3][1]:
                   fingers.append(0)
               else:
                   fingers.append(1)
           if rotlmlist[4][1] > rotlmlist[17][1]:
               if rotlmlist[3][1] > rotlmlist[4][1]:
                   fingers.append(0)
               else:
                   fingers.append(1)
           if rotlmlist[6][2] > rotlmlist[8][2]:
               fingers.append(0)
           else:
               fingers.append(1)
           if rotlmlist[10][2] > rotlmlist[12][2]:
               fingers.append(0)
           else:
               fingers.append(1)
           if rotlmlist[14][2] > rotlmlist[16][2]:
               fingers.append(0)
           else:
               fingers.append(1)
           if rotlmlist[18][2] > rotlmlist[20][2]:
               fingers.append(0)
           else:
               fingers.append(1)

        return fingers

# findDistance function returns the image after drawing distance between 2 points 
# and drawing thar distance and highlighting the points with r radius circle and 
# t thickness line and also return length there
# this function would help us make our click to execute

    def findDistance(self, p1, p2, img, draw=True,r=15, t=3):

        if self.lmList == []:
            length = 0
            return length
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = 0
        # write your code here
        length = ((x1-x2) ** 2 + (y1-y2) ** 2) ** 0.5
        if draw:
             cv2.circle(img, (x1, y1), r, (0, 255, 0), -1)
             cv2.circle(img, (x2, y2), r, (0, 255, 0), -1)
             cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), t)


        return length, img, [x1, y1, x2, y2, cx, cy]
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################





# Now for the main function is to check and debug the class
# You may change it any way you want
# I have added the FPS counter and take the video feed from the PC
# If you donot have a webcam in yout PC you can use DROID CAM Software
# To debug you can also use image of a hand , the code for this I have commented out
# you can decomment it out and comment the video feed code to debug if you feel 
# some functipn is not working as required


#############################################################################################################

def main():
    pTime = 0
    cTime = 0
    # Add the video source here
    # 0-For your first webcam in the PC
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, handNo=0)
        fin = detector.fingersUp()
        #if len(fin) != 0:
        #    print(fin)
        length = detector.findDistance(p1=4, p2=8, img= img, draw=True)
        #if len(lmList) != 0:
        #    print(lmList[0][3])
        print(length[0])
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (0, 0, 0), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
    
    # img = cv2.imread("./File path for image goes here"")
    # img = detector.findHands(img)
    # lmList = detector.findPosition(img)
    # #if len(lmList) != 0:
    # #    print(lmList[3])



    # cv2.imshow("Image", img)
    # cv2.waitKey(0)
        


if __name__ == "__main__":
    main()