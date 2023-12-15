from .Gripper_2F import Gripper
import cv2
import imutils
import math
import numpy as np
import matplotlib.pyplot as plt
from sympy import *
from imutils import perspective
import argparse
import pandas as pd
# from exif import Image


class Auto_RGrasping(Gripper):
    def __init__(self, *args):
        Gripper.__init__(self, *args)
        self.W_GR = 0.0
        self.D_GR = 0.0
        self.O_Gripper = 0.0

    def status(self):
        if self.O_Gripper <= 0.0 or self.O_Gripper < 1.1:
            if 0.0 < self.O_Gripper <= 1.1:
                print('The value O_Gripper is <= 1.1, Open Gripper will be ' +
                      str(100+self.W_GR*100)+'% Width Object.')
            elif self.O_Gripper <= 0.0:
                print('The value O_Gripper is <= 0.0, Open Gripper will be ' +
                      str(100+self.W_GR*100)+'% Width Object.')
        elif 1.1 <= self.O_Gripper <= 2.0:
            if 1.1 < self.O_Gripper <= 2.0:
                print('The value O_Gripper is '+str(self.O_Gripper)+', Open Gripper will be ' +
                      str(100+(self.Open_Gripper-1)*100)+'% Width Object.')

        if self.WF_Gripper <= 0.0:
            print('The Width Finger Gripper is <= 0.0, this will be ' +
                  str(0.05*100)+'% the Height Object.')
        if self.D_GR <= 0.0:
            print('The Value Distance between Grasping Regions is <= 0.0, this will be 50% the Width Finger Gripper.')
        if self.D_GR > 2*self.WF_Gripper:
            print('The Value Distance between Grasping Regions cant be > 2*Width Finger Gripper, this will be 50% the Width Finger Gripper.')
        elif self.D_GR > 1.0 and self.D_GR <= 2*self.WF_Gripper:
            print('The Distance between Grasping Regions will be ' +
                  str((self.D_GR/self.WF_Gripper)*100)+'% Width Finger Gripper.')
        elif self.D_GR > 0.0 and self.D_GR <= 1.0:
            print('The Distance between Grasping Regions will be ' +
                  str(self.D_GR*100)+'% Width Finger Gripper.')

    def __Object_Address__(self, Size_Box):
        self.Size_Box = Size_Box
        H_Box = max(self.Size_Box[1], self.Size_Box[0])
        W_Box = min(self.Size_Box[1], self.Size_Box[0])
        return H_Box, W_Box

    def get_Date_Box(self, Date_Box):
        self.Date_Box = Date_Box
        Center_Box = [self.Date_Box[i][0] for i in range(len(self.Date_Box)-1)]
        Size_Box = [self.Date_Box[i][1] for i in range(len(self.Date_Box)-1)]
        Theta_Box = [self.Date_Box[i][2] for i in range(len(self.Date_Box)-1)]
        return Center_Box, Size_Box, Theta_Box

    def __SideRECT__(self, Date_Box):
        # Points of the Bounding Rectangle
        P_Box = cv2.boxPoints(Date_Box.to_numpy()) if imutils.is_cv2(
        ) else cv2.boxPoints(Date_Box.to_numpy())

        # Identify the longest side of the rectangle.
        H_Box = max(Date_Box.Size_Box[1], Date_Box.Size_Box[0])

        if Date_Box.Theta_Box == 90:
            m = None
        elif Date_Box.Size_Box[1] <= Date_Box.Size_Box[0]:
            m = np.tan(np.radians(Date_Box.Theta_Box))
        elif Date_Box.Size_Box[1] > Date_Box.Size_Box[0]:
            m = -1/(np.tan(np.radians(Date_Box.Theta_Box)))

        return H_Box, m

    def __Open_Gripper__(self, Size_Box):
        __, W_Box = self.__Object_Address__(Size_Box)

        if self.W_GR <= 0.0 or self.W_GR > 1.0:
            self.W_GR = 0.1

        if self.O_Gripper <= 0.0 or self.O_Gripper < 1.1:
            self.Open_Gripper = W_Box*(1+self.W_GR)
        elif 1.1 <= self.O_Gripper <= 2.0:
            self.Open_Gripper = self.O_Gripper*W_Box
        return self.Open_Gripper

    def GRASP_RC(self, Date_Box, WF_Gripper=1, D_GR=10):
        '''
            GRASP REGIONS CENTERS
            Esta función calcula de forma automatica, los centros de las posibles Regiones de 
            Grasping en objetos cilindricos para grippers de 2 Fingers 

            # Date_Box: Info of the Bounding Rectangle (Center,Size,Angle)
            # WF_Gripper: Width Finger of the Gripper
            # D_GR: Distance between Grasping Regions
        '''
        # Create Grasp Regions Centers list
        C_RGrasp = list()

        # Center Bounding Rectangle
        Xc, Yc = Date_Box.Center_Box

        H_Box, m = self.__SideRECT__(Date_Box)

        # Distance between Grasping Regions Centers
        D = (WF_Gripper+D_GR)

        # Ecuation of the line
        n = int(0.5*H_Box/(WF_Gripper+1.25*D_GR))
        C_RGrasp.append(Date_Box.Center_Box)
        if m == None:
            x = np.array([1, 1], dtype=float)*Xc
            y = np.array([1, 1], dtype=float)*Yc
            for i in range(1, n+1):
                if Date_Box.Size_Box[1] < Date_Box.Size_Box[0]:
                    y = np.array([1, 1], dtype=float)*Yc + \
                        np.array([-1, 1], dtype=float)*(D*(i+1))
                elif Date_Box.Size_Box[1] >= Date_Box.Size_Box[0]:
                    x = np.array([1, 1], dtype=float)*Xc + \
                        np.array([-1, 1], dtype=float)*(D*(i+1))
                for j in range(len(x)):
                    C_RGrasp.append([int(x[j]), int(y[j])])
        else:
            X = Symbol('X')
            b = Yc-(m*Xc)
            Y = m*X+b
            # Calc of the distance equation of two points "D^2 = (X-Xc)^2+(Y-Yc)^2"
            for i in range(n):
                x = list(solve(Eq(pow(D*(i+1), 2), pow(X-Xc, 2)+pow(Y-Yc, 2)), X))
                y = list(m.astype(dtype=np.float64) *
                         x[j]+b for j in range(len(x)))
                for j in range(len(x)):
                    C_RGrasp.append([int(x[j]), int(y[j])])

        C_RGrasp = sorted(C_RGrasp, key=lambda p: float(p[0]))

        return C_RGrasp

    def Grasp_Regions(self, Object_Boxes, W_GR=0.0, D_GR=0.0):
        '''
            GRASPING REGIONS 2 FINGERS
            Esta función calcula de forma automatica, posibles Regiones de Grasping en objetos
            cilindricos para grippers de 2 Fingers, partiendo del analisis de la forma de mismos 

            ** Object_Boxes: Info of the Object [Date_Box,Point_Box,Max_Cnt]
            ***** Bounding Rectangle (Center,Size,Angle) + Points Boxes
            ***** Center_Box, Size_Box, Theta_Box = Date_Box
            ***** Point_Box = Approximate Bounding Rectangle along with the Objects
            ***** Max_Cnt = Curve joining all the continuous points by Objects.
            ** WF_Gripper: Width Finger of the Gripper
            ** O_Gripper: Gripper Opening
            ** W_GR: Delta Width Grasping Regions
            ** D_GR: Distance between Grasping Regions
        '''
        self.D_GR = D_GR
        self.W_GR = W_GR

        if self.W_GR <= 0.0 or self.W_GR > 1:
            self.W_GR = 0.1

        Grasp_Regions = list()
        CGrasp_Reg = list()
        Grasp_Reg = list()
        for D in range(len(Object_Boxes)):

            H_Box, W_Box = self.__Object_Address__(Object_Boxes.Size_Box[D])
            Open_Gripper = self.__Open_Gripper__(Object_Boxes.Size_Box[D])

            if Open_Gripper >= (1+W_GR)*W_Box:
                if self.WF_Gripper <= 0.0:
                    self.WF_Gripper = 0.05*H_Box
                if D_GR <= 0.0:
                    Dist_GR = 0.5*self.WF_Gripper
                if D_GR > 2*self.WF_Gripper:
                    Dist_GR = 0.5*self.WF_Gripper
                elif D_GR > 1.0 and D_GR <= 2*self.WF_Gripper:
                    Dist_GR = (D_GR/100)*self.WF_Gripper
                elif D_GR > 0.0 and D_GR <= 1.0:
                    Dist_GR = D_GR*self.WF_Gripper

                C_RGrasp = self.GRASP_RC(
                    Object_Boxes.iloc[D, 0:3], self.WF_Gripper, Dist_GR)

                R_Grasp = []
                for i in range(len(C_RGrasp)):
                    # Grasp Regions Points CalculationH
                    if Object_Boxes.Size_Box[D][0] <= Object_Boxes.Size_Box[D][1]:
                        Rect_Grasp = list((C_RGrasp[i], (int(H_Reg[0]), int(H_Reg[1])), Object_Boxes.Theta_Box[D]) for H_Reg in [
                                          [W_Box, H_Box], [Open_Gripper, self.WF_Gripper]])
                    else:
                        Rect_Grasp = list((C_RGrasp[i], (int(H_Reg[0]), int(
                            H_Reg[1])), Object_Boxes.Theta_Box[D]-90) for H_Reg in [[W_Box, H_Box], [Open_Gripper, self.WF_Gripper]])
                    # Region General de Agarre del Objeto encontrada
                    Box_RGrasp = list(cv2.boxPoints(Rect_Grasp[j]) if imutils.is_cv2(
                    ) else cv2.boxPoints(Rect_Grasp[j]) for j in range(len(Rect_Grasp)))
                    Box_RGrasp = list(
                        np.array(Box_RGrasp[j], dtype="int") for j in range(len(Box_RGrasp)))
                    Box_RGrasp = list(perspective.order_points(
                        Box_RGrasp[j]) for j in range(len(Rect_Grasp)))
                    R_Grasp.append(Box_RGrasp[1])
                CGrasp_Reg.append(C_RGrasp)
                Grasp_Reg.append(R_Grasp)

        Grasp_Regions = pd.concat([Object_Boxes, pd.DataFrame(list(zip(
            CGrasp_Reg, Grasp_Reg)), columns=['Centers_GraspReg', 'Grasp_Regions'])], axis=1)
        return Grasp_Regions
