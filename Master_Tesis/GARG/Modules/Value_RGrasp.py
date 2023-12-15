from .Gripper_2F import Gripper
from .Grasp_Reg import Auto_RGrasping
from sympy import Polygon, Symbol, Point, RegularPolygon
import cv2
import imutils
import math
import numpy as np
import matplotlib.pyplot as plt
from sympy import *
from imutils import perspective
#from exif import Image

class Mathemat:
    def Slope(P2,P1):
        m,_= np.polyfit([P2[0],P1[0]],[P2[1],P1[1]],1)
        return m

    def OrSide_RECT(Date_Box):
        _, Size_Box,_ = Date_Box

        ###  Points of the Bounding Rectangle 
        P_Box = cv2.boxPoints(Date_Box) if imutils.is_cv2() else cv2.boxPoints(Date_Box)

        ### Identify the longest side of the rectangle. 
        H_Box = max(Size_Box[1],Size_Box[0])
        D_PBox=math.dist(P_Box[3],P_Box[0])

        ### Identify the longest side of the rectangle.
        m = Mathemat.Slope(P_Box[3],P_Box[0])
        Theta = math.degrees(math.atan(m))

        if int(D_PBox) == int(H_Box):
            X_cmax = (P_Box[3][0]+P_Box[2][0])/2
        else:
            X_cmax = (P_Box[3][0]+P_Box[0][0])/2
            m = -1/m

        return H_Box, X_cmax, m
class Value_RGrasp (Auto_RGrasping,Gripper):
    def __init__(self,Object_Boxes,*args):
        Gripper.__init__(self,*args)
        self.Object_Boxes=Object_Boxes
        self.W_GR=0.0
        self.D_GR=0.0
        self.Method=False
    
    def status(self):
        print("")
    
    def __Object_Address__(self,Size_Box):
        self.Size_Box=Size_Box
        H_Box = max(self.Size_Box[1],self.Size_Box[0])
        W_Box = min(self.Size_Box[1],self.Size_Box[0])
        return H_Box, W_Box

    def __Open_Gripper__(self,Size_Box):
        H_Box, W_Box = self.__Object_Address__(Size_Box)

        if self.W_GR <= 0.0 or self.W_GR > 1.0:
            self.W_GR = 0.1
        
        if self.O_Gripper <= 0.0 or self.O_Gripper<1.1:
            Open_Gripper = W_Box*(1+self.W_GR)
            if 0.0< self.O_Gripper<=1.1: print('The value O_Gripper is <= 1.1, Open Gripper will be '+str(100+self.W_GR*100)+'% Width Object.')
            elif self.O_Gripper <= 0.0 : print('The value O_Gripper is <= 0.0, Open Gripper will be '+str(100+self.W_GR*100)+'% Width Object.')
        elif 1.1 <= self.O_Gripper <= 2.0:
            Open_Gripper = self.O_Gripper*W_Box
            if 1.1<self.O_Gripper<=2.0: print('The value O_Gripper is '+str(self.O_Gripper)+', Open Gripper will be '+str(100+(Open_Gripper-1)*100)+'% Width Object.')
        return Open_Gripper
    
    # Trasform the point or polygon opencv to point-polygon sympy
    def np2Poly(self, Grasp_Value, type_mode="Polygon"):
        self.Grasp_Val = Grasp_Value
        self.P_RGrasp=[]
        for i in range(len(self.Grasp_Val)-1):
            self._Obj=[]
            for j in range(len(self.Grasp_Val[i])-1):
                if type_mode=="Polygon":
                    self._Obj.append(Polygon(*self.Grasp_Val[i][j]))
                elif type_mode=="Point":
                    self._Obj.append(Point(*self.Grasp_Val[i][j]))
            self.P_RGrasp.append(self._Obj)
        return self.P_RGrasp
    
    # Trasform the countour opencv to polygon sympy
    def cnt2Poly(self,cnt): 
        self.cnt=cnt
        cntPoly=[]
        for i in range(len(cnt)-1):
            Points=[]
            for j in range(len(cnt[i])-1):
                Points.append(Point(*cnt[i][j]))
            cntPoly.append(Polygon(*Points))
        return cntPoly
    
    def get_Dcenter(self,c_cnt,C_RGrasp):
        self.C_cnt=c_cnt
        self.C_RGrasp=C_RGrasp
        dist_cent=[]
        for i in range(len(self.C_RGrasp)-1):
            self.C_cnt.distance(self.C_RGrasp[i])
        return dist_cent

    # Get the area intersection between RGrasp and Contours Objects
    def get_Ainter(self,Contour,RGrasp):
        self.RGrasp=RGrasp
        area_params=[]
        for i in range(len(self.RGrasp)-1):
            poly_inter = self.Contour.intersection(self.RGrasp[i])
            area_params.append(poly_inter.area)
        return area_params

    def Val_GR(self, Grasp_Regions):
        """
            ** Grasp_Region: All information of the Objects
            ***** Date_Box = Center_Box, Size_Box, Theta_Box
            ***** Point_Box = Approximate Bounding Rectangle along with the Objects
            ***** Max_Cnt = Curve joining all the continuous points by Objects.
            ***** C_RGrasp = Genters of Grasping Regions by Objects
            ***** R_Grasp = Grasping Regions by Objects
            ***** SubReg = Grasping Sub-Regions by Objects
            ***** And_CntRG = Intersection Contours Objects vs Grasping Regions
        """
        Date_Box, Cnt,C_RGrasp, R_Grasp= Grasp_Regions
        Center_Box, Size_Box, Theta_Box = self.get_Date_Box(Date_Box)

        P_Contour = self.cnt2Poly(Cnt)
        P_RGrasp = self.np2Poly(R_Grasp)
        P_CGrasp = self.np2Poly(C_RGrasp,"Point")

        for i in range(len(P_Contour)-1):
            area_params=self.get_Ainter(P_Contour[i],P_RGrasp[i])

                ## Calculating Euclidean distance
        #D_PBox = np.linalg.norm(P_Box[3] - P_Box[0])
    
    def Cnt_Intersections(D,Object,C_RGrasp,R_Grasp):

        S_Object, Max_Cnt, Date_Box, Point_Box  = Object
        # Create intersecting space
        Space = np.zeros([S_Object[0],S_Object[0]],np.uint8)

        A_CntAnd=[]
        # Create Contour Space
        Center_Box, _, _ = Date_Box[D]
        S_Contour = cv2.drawContours(Space.copy(), Max_Cnt, D, (255, 255, 255), -1)
        for i in range(len(R_Grasp)):
            # Create Grasp Region Space
            S_RGrasp = cv2.drawContours(Space.copy(), [R_Grasp[i].astype("int")], -1, (255, 255, 255), -1)
            
            # Find Area of Intersection between Object Outline and Grasp Region
            Intersecc = cv2.bitwise_and(S_Contour,S_Contour, mask=S_RGrasp)
            # Find the contour of the intersected area
            CntAnd, _ = cv2.findContours(Intersecc,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            # Calculate the Area of ​​intersection
            A_CntAnd.append(cv2.contourArea(CntAnd[0]))
                
            # Calculates the distance between the Object Center and the center of the intersection area
            Dist_Centers=list(abs(math.dist(Center_Box,C_RGrasp[j])) for j in range(len(C_RGrasp)))
        
        # Normalization
        N_DCenters=list(1-(Dist_Centers[j]/max(Dist_Centers)) for j in range(len(Dist_Centers)))
        N_ACntAnd=list(A_CntAnd[j]/max(A_CntAnd) for j in range(len(A_CntAnd)))

        Intersecc=[Dist_Centers,N_DCenters,A_CntAnd,N_ACntAnd]
        print(A_CntAnd,N_ACntAnd)
        print(Dist_Centers,N_DCenters)
        return Intersecc




