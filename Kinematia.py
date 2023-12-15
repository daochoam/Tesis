import sympy as sp
import numpy as np

class Kinematic:
    def Mat_Trasl(self,x, y, z):
        """ Transformación homogénea que representa traslación pura"""
        T = np.array([[1,0,0,x],
                    [0,1,0,y],
                    [0,0,1,z],
                    [0,0,0,1]])
        return T
    
    def Mat_Rotx(self,theta):
        """ Transformación homogénea que representa rotación alrededor de x"""
        T = np.array([[1, 0,0,0],
                    [0, np.cos(theta),-np.sin(theta),0],
                    [0, np.sin(theta), np.cos(theta),0],
                    [0, 0, 0, 1]])
        return T
    
    def Mat_Roty(self,theta):
        """ Transformación homogénea que representa rotación alrededor de x"""
        T = np.array([[np.cos(theta),0,np.sin(theta),0],
                    [0, 1, 0, 0],
                    [-np.sin(theta),0 ,np.cos(theta),0],
                    [0, 0, 0, 1]])
        return T
    
    def Mat_Rotz(self,theta):
        """ Transformación homogénea que representa rotación alrededor de z"""
        T = np.array([[np.cos(theta),-np.sin(theta),0,0],
                    [np.sin(theta), np.cos(theta),0,0],
                    [0,0,1,0],
                    [0,0,0,1]])
        return T

