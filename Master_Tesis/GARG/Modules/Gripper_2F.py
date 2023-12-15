from Camera.Camera_Calibrate.C_Calibration import Calibrate_Camera
from exif import Image
import math
import numpy as np
import matplotlib.pyplot as plt
from sympy import *


class Gripper(Calibrate_Camera):
    def __init__(self):
        self.WF_Gripper = 0.0
        self.O_Gripper = 0.0
        self.Simul = True

    def Width_FGripper(self, W_FGripper, type='px'):
        if type == 'px':
            self.W_FGripper = W_FGripper
        elif type == 'cm':
            Camera_Matrix, Dist_Coeffs = self.Read_CameraP(
                'Camera_Calibrate/Camera_Parameter.yaml')

    def Hight_FGripper(self, HF_Gripper):
        self.HF_Gripper = HF_Gripper

    def Depht_FGripper(self, DF_Gripper):
        self.DF_Gripper = DF_Gripper

    def Open_Gripper(self, Open_Gripper):
        self.Open_Gripper = Open_Gripper

    def Config_Gripper(self, W_Gripper, Open_Gripper):
        self.Simul = False
        self.WF_Gripper = W_Gripper
        self.O_Gripper = Open_Gripper
