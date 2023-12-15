import numpy as np
import cv2
import imutils
import pandas as pd
from imutils import perspective

class Seg_Image:
    def __init__(self):
        self.image=[]
        self.sigma=0.33
        self.name_window=""

    def HSV_Histogram(self,img_hsv,mask=None,type=cv2.THRESH_OTSU):
        H_Hist = cv2.calcHist([img_hsv], [0], mask, [180],[0, 180])
        S_Hist = cv2.calcHist([img_hsv], [1], mask, [256],[0, 255])
        V_Hist = cv2.calcHist([img_hsv], [2], mask, [256],[0, 255])
        
        H_Thresh,_ = cv2.threshold(img_hsv[:,:,0],0,180,type)
        S_Thresh,_ = cv2.threshold(img_hsv[:,:,1],0,255,type)
        V_Thresh,_ = cv2.threshold(img_hsv[:,:,2],0,255,type)

        HSV_Thresh=[H_Thresh,S_Thresh,V_Thresh]
        HSV_Hist=[H_Hist,S_Hist,V_Hist]
        return HSV_Hist,HSV_Thresh

    def Sobel_Canny(self,image, sigma=0.33):    
        self.image = image
        self.sigma=sigma
        dx = cv2.convertScaleAbs(cv2.Scharr(self.image, cv2.CV_32F, 1, 0,3,cv2.BORDER_DEFAULT))
        dy = cv2.convertScaleAbs(cv2.Scharr(self.image, cv2.CV_32F, 0, 1,3,cv2.BORDER_DEFAULT))
        sobel = cv2.addWeighted(dx, 1, dy, 1, 0.0)

        # compute the median of the single channel pixel intensities
        v = np.median(sobel)
        
        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(sobel,lower,upper)   
        # return the edged image
        return edged

    def Max_Contours(self,image):
        self.image = image

        cnts, hyre = cv2.findContours(image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key = cv2.contourArea, reverse = True)

        Max_Cnt=[]
        for i in range(len(cnts)):
            ACnts = cv2.contourArea(cnts[i])
            if ACnts > 3000:
                Max_Cnt.append(cnts[i])
        return Max_Cnt
    
    def Object_Boxes(self,Contours):
        Date_Box=[]
        Point_Box=[]
        for cnt in Contours:
            Date_B = cv2.minAreaRect(cnt)
            Point_B = cv2.BoxPoints(Date_B) if imutils.is_cv2() else cv2.boxPoints(Date_B)
            Point_B = np.array(Point_B, dtype="int")
    
            Date_Box.append(Date_B)
            Point_Box.append(perspective.order_points(Point_B))


        Contour_Boxes = pd.concat([ pd.DataFrame(Date_Box,columns=['Center_Box','Size_Box','Theta_Box']),pd.DataFrame(list(zip(Point_Box,Contours)), columns = ['Points_Box','Contours'])], axis=1)
        return Contour_Boxes
    
    def Morph_Transform(self, image, K=3, Morph_Type=0,Morph_Shape=1, iterations =1):
        self.image=image
        """
            Morph_Type: (0) ERODE, (1) DILATE, (2) OPEN, (3) CLOSE, (4) GRADIENT, (5) TOPHAT, (6) BLACKHAT, (7) HITMISS.
            Moph_Shape: (0) RECT, (1) CROSS, (2) ELLIPSE 
        """
        Kernel = cv2.getStructuringElement(Morph_Shape, ksize=(K,K))
        MorphTrans = cv2.morphologyEx(self.image, Morph_Type, Kernel,iterations)
        return MorphTrans

    def Mask_Created(self,image,_Down=np.array([0,0,0]),_High=np.array([180,255,255]), B_And=False):
        self.image = image
        Mask = cv2.inRange(self.image, _Down.astype(int), _High.astype(int))
        Res_Mask = cv2.bitwise_not(Mask)
        if B_And==True:
            Res_Mask = Mask
            #Res_Mask = cv2.bitwise_and(image, image, mask=Res_Mask)
        return Res_Mask

    def GRAY2HSV(self,image):
        Image_HSV = cv2.cvtColor(cv2.cvtColor(image, cv2.COLOR_GRAY2RGB), cv2.COLOR_RGB2HSV)
        return Image_HSV