import math
import cv2
import yaml
import numpy as np


class CameraCalibration:
    def __init__(self, calibration_file):
        with open(calibration_file, 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)

        self.camera_matrix = np.array(data['Camera_Matrix'])
        self.distortion_coefficients = np.array(
            data['Distortion_Coefficients'])


class PixelConverter:
    def __init__(self, size_sensor=1/2.3, width_resolution=3648, height_resolution=2736, calibration_file=None):
        self.size_sensor = size_sensor
        self.width_resolution = width_resolution
        self.height_resolution = height_resolution

        # Cargar la calibración de la cámara si se proporciona un archivo de calibración
        self.calibration = None
        if calibration_file:
            self.calibration = CameraCalibration(calibration_file)

    def pixelSize(self):
        size_sensor_cm = self.size_sensor * 2.54
        size_pixel = size_sensor_cm / \
            math.sqrt(self.width_resolution**2 + self.height_resolution**2)
        return size_pixel

    def objectWidth(self, object_width_px, camera_distance_cm, focal_length_mm):
        size_pixel_cm = self.pixelSize()

        # Convertir distancia focal de milímetros a centímetros
        focal_length_cm = focal_length_mm / 10

        # Utilizar la calibración si está disponible
        if self.calibration:
            # Corregir distorsiones en las coordenadas de píxeles
            distorted_points = np.array(
                [[object_width_px, 0]], dtype='float32')
            undistorted_points = cv2.undistortPoints(distorted_points, self.calibration.camera_matrix,
                                                     self.calibration.distortion_coefficients)

            # Obtener el ancho del objeto corregido en centímetros
            object_width_cm = (
                undistorted_points[0, 0, 0] * size_pixel_cm * camera_distance_cm) / focal_length_cm
        else:
            # Sin calibración, utiliza la misma fórmula que antes
            object_width_cm = (object_width_px * size_pixel_cm *
                               camera_distance_cm) / focal_length_cm

        return object_width_cm


# Uso de la clase con calibración de cámara
calibration_file = 'Camera/Camera-Calibration/Camera_Parameter.yaml'
converter = PixelConverter(calibration_file=calibration_file)

# Supongamos que la distancia entre la cámara y el objeto es de 60 cm
camera_distance_cm = 120

# Supongamos que la distancia focal es de 2.8 mm
focal_length_mm = 2.8

# Supongamos que el ancho del objeto en píxeles es de 500
ancho_objeto_cm = converter.objectWidth(
    object_width_px=100, camera_distance_cm=camera_distance_cm, focal_length_mm=focal_length_mm)

print("Ancho del objeto estimado:", ancho_objeto_cm, "centímetros")
