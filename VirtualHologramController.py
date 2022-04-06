import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8)

class MRectangle():
    def __init__(self, posCenter=[200,200], size=200, color=[255,0,255]):
        self.center = posCenter
        self.size = size
        self.color = color
        self.update_size(posCenter)

    def update(self, newPos):
        if lp < 40:
            self.update_size(newPos)

    def update_size(self, center=None):
        if center == None:
            center = self.center
        else:
            self.center = center
        self.pt1 = center[0]-self.size//2 , center[1]-self.size//2
        self.pt2 = center[0]+self.size//2 , center[1]+self.size//2

    def update_scale(self, scale):
        self.size = int(scale)
        self.update_size()

    def update_color(self, color):
        self.color = color

prvmf = [0,0]
def check_rotation(mf,rect):
    global prvmf
    mfx = int(np.interp(prvmf[0]-mf[0], [-10,10], [0,255]))
    mfy = int(np.interp(prvmf[1]-mf[1], [-10,10], [0,255]))
    rect.update_color([255,mfx,mfy])
    prvmf = mf


rect = MRectangle()


while True:
    sucess, img = cap.read()
    img = cv2.flip(img, 1)
    lnList, img = detector.findHands(img)

    if lnList:        
        cursor = lnList[0]['lmList'][8]
        lp,_ = detector.findDistance(lnList[0]['lmList'][8],lnList[0]['lmList'][12])

        if rect.pt1[0]<cursor[0]<rect.pt2[0] and rect.pt1[1]<cursor[1]<rect.pt2[1]:
            rect.update(cursor)
        elif detector.fingersUp(lnList[0]).count(1) == 5:
            check_rotation(lnList[0]['lmList'][9],rect)
        else:
            ls,_ = detector.findDistance(lnList[0]['lmList'][4],lnList[0]['lmList'][8])
            scale = np.interp(ls, [40,190], [20,400])
            if lp > 70:
                rect.update_scale(scale)

    cv2.rectangle(img, rect.pt1, rect.pt2, rect.color, cv2.FILLED)
    cv2.imshow("image", img)

    k = cv2.waitKey(10)
    if k == 27:  # press ESC to exit
        break



