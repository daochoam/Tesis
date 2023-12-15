import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


class Transformation:
    def __init__(self):
        self.transform_matrices = []

    def matrizTranlation(self, x, y, z):
        return np.array([[1, 0, 0, x],
                        [0, 1, 0, y],
                        [0, 0, 1, z],
                        [0, 0, 0, 1]])

    def matrizRotation_X(self, theta):
        return np.array([[1, 0, 0, 0],
                        [0, np.cos(theta), -np.sin(theta), 0],
                        [0, np.sin(theta), np.cos(theta), 0],
                        [0, 0, 0, 1]])

    def matrizRotation_Y(self, theta):
        return np.array([[np.cos(theta), 0, np.sin(theta), 0],
                        [0, 1, 0, 0],
                        [-np.sin(theta), 0, np.cos(theta), 0],
                        [0, 0, 0, 1]])

    def matrizRotation_Z(self, theta):
        return np.array([[np.cos(theta), -np.sin(theta), 0, 0],
                        [np.sin(theta), np.cos(theta), 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])

    def matrizToDH(self, matriz):
        R = matriz[:3, :3]
        t = np.zeros((3, 1))
        # Crear la matriz extendida a 4x4
        homogeneus = np.eye(4)
        homogeneus[:3, :3] = R
        homogeneus[:3, 3] = t.flatten()

        return homogeneus
