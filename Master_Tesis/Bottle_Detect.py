from Image_Recognition import Detector
from Camera import Calibrate_Camera
from Imagine_Procc import Imag_Process
from Camera import XiaomiYi, Calibrate_Camera
from GARG import Auto_RGrasping, Value_RGrasp
from sympy import Polygon, Symbol, Point, RegularPolygon
import matplotlib.pyplot as plt
import cv2
import numpy as np
from sympy import *

#!/usr/bin/python3
from time import sleep

camera = XiaomiYi()
# Make connection to the camera.
cap = cv2.VideoCapture('rtsp://192.168.42.1:554/live')

try:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('img.png', gray)
except Exception as e:
    print(f"Error al leer el fotograma: {e}")
finally:
    cap.release()

if not frame.empty():
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('img.png', gray)
else:
    print("Error: La matriz de fotograma está vacía.")


""" # Carga la imagen en color desde el archivo
path = "Database/1.jpg"
# Utiliza cv2.IMREAD_COLOR para cargar la imagen en color
Bottles = cv2.imread(path, cv2.IMREAD_COLOR) """

# Muestra la imagen en color (opcional)


""" Path = "Database/1.jpg"
Bottles = cv2.imread(Path, cv2.COLOR_BGR2RGB) """


# Initializing the objects
Image_Processing = Imag_Process()
Grasping_Reg = Auto_RGrasping()
C_Calibrate = Calibrate_Camera()

Obj_Detector = Detector(model_type="ML2R", score_thresh=0.9)
window_name = 'image'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.imshow(window_name, Bottles)

Camera_Matrix, Dist_Coeffs = C_Calibrate.Read_CameraP(
    'Camera/Camera_Calibrate/Camera_Parameter.yaml')
Bottles = C_Calibrate.Undistor(Bottles, Camera_Matrix, Dist_Coeffs)


predict = Obj_Detector.Predict()
prediction = Obj_Detector.Image_Predict(Bottles, predict)
image_show = Obj_Detector.Image_Segment(Bottles, prediction)


Contornos = Obj_Detector.Detect_Contours(prediction)
Grasp_Boxes = Image_Processing.Object_Boxes(Contornos)

# Draw_Contour = Image_Processing.Visual_Draw(Bottles,Grasp_Boxes)
Draw_Contour = Image_Processing.Visual_Draw(Bottles, Grasp_Boxes)
# Image_Processing.Image_Show(Draw_Contour,'Draw_Contour')
Image_Processing.Image_Show(Draw_Contour, 'Draw_Contour')

Grasping_Reg = Auto_RGrasping()
Grasp_Regions = Grasping_Reg.Grasp_Regions(Grasp_Boxes)
print(Grasp_Regions)

B_Rect = Image_Processing.Visual_GARG(Bottles, Grasp_Regions, [1, 3])
Image_Processing.Image_Show(B_Rect, 'Grasping Regions')

cv2.waitKey(0)
