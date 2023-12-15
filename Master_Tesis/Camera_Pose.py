from Camera import Calibrate_Camera
from Kinematic import Transformation, RobotArm
import numpy as np

Matrix = Transformation()
C_Calibrate = Calibrate_Camera()
ABB_IRB140 = RobotArm()

##  MATRIZ DE DENAVIT- HARTEMBERG MODEL IRB 140  ##
# Agregar eslabones al brazo robótico
# ? theta, alpha, a, d
ABB_IRB140.add_link(np.pi/2, -np.pi/2, 70, 352)
ABB_IRB140.add_link(-np.pi/2, 0, 360, 0)
ABB_IRB140.add_link(np.pi, np.pi/2, 0, 0)
ABB_IRB140.add_link(np.pi, -np.pi/2, 0, 380)
ABB_IRB140.add_link(np.pi/2, np.pi/2, 0, 0)
ABB_IRB140.add_link(-np.pi, np.pi/2, 0, 65)

# Calcular la cinemática directa
A06 = ABB_IRB140.calculate_fk()


Camera_Matrix, Dist_Coeffs = C_Calibrate.Read_CameraP(
    'Camera/Camera_Calibrate/Camera_Parameter.yaml')

cameraMatriz = Matrix.matrizToDH(Camera_Matrix)

cameraToRobot = cameraMatriz * Matrix.matrizTranlation(
    620, 605, 975) * Matrix.matrizRotation_Z(np.pi/2) * Matrix.matrizRotation_X(np.pi)*A06


pose_robot = np.dot(cameraToRobot, [100, 20, 30, 1])
print(pose_robot)
nuevo_punto = pose_robot[:3] / pose_robot[3]
print(nuevo_punto)
