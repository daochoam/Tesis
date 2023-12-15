import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class RobotArm:
    def __init__(self):
        self.transform_matrices = []

    def dh_matrix(self, theta, alpha, a, d):
        """
        Crea una matriz de transformación homogénea según los parámetros DH.
        """
        return np.array([
            [np.cos(theta), -np.cos(alpha) * np.sin(theta),
             np.sin(alpha) * np.sin(theta), a * np.cos(theta)],
            [np.sin(theta), np.cos(alpha) * np.cos(theta), -
             np.sin(alpha) * np.cos(theta), a * np.sin(theta)],
            [0, np.sin(alpha), np.cos(alpha), d],
            [0, 0, 0, 1]
        ])

    def add_link(self, theta, alpha, a, d):
        # Agrega un eslabón al brazo robótico.
        self.transform_matrices.append(self.dh_matrix(theta, alpha, a, d))

    def calculate_fk(self):
        """
        Calcula la cinemática directa para obtener la matriz A06.
        """
        if not self.transform_matrices:
            raise ValueError("No se han agregado eslabones al brazo robótico.")

        return np.linalg.multi_dot(self.transform_matrices)

    def visualize_robot(self):
        # Visualiza el robot en 3D utilizando matplotlib.

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Inicializar la matriz de transformación
        T = np.eye(4)

        for i, link in enumerate(self.transform_matrices):
            # Multiplicar la matriz de transformación actual por la anterior
            T = np.dot(T, link)
            # Extraer las posiciones de los extremos de los eslabones
            x, y, z = T[:3, 3]

            # Visualizar el eslabón
            ax.plot([0, x], [0, y], [0, z], marker='o',
                    linestyle='-', label=f'Link {i+1}')

        # Configurar la visualización
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Visualización del Robot')

        plt.legend()
        plt.show()
