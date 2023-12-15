from Kinematic import RobotArm
import numpy as np


##  MATRIZ DE DENAVIT- HARTEMBERG MODEL IRB 140  ##
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

# Visualizar el robot
ABB_IRB140.visualize_robot()

print(A06)
