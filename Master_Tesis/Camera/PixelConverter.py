import math
import numpy as np
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS


class PixelConverter:
    def __init__(self, size_sensor=1/2.3, width_resolution=3648, height_resolution=2736):
        self.size_sensor = size_sensor
        self.width_resolution = width_resolution
        self.height_resolution = height_resolution

    def pixelSize(self):
        size_sensor_cm = self.size_sensor * 2.54
        size_pixel = size_sensor_cm / \
            math.sqrt(self.width_resolution**2 + self.height_resolution**2)
        return size_pixel

    def objectWidth(self, object_width_px, camera_distance_cm):
        size_pixel_cm = self.pixelSize()
        # Distancia focal en milímetros (considerando el rango)
        focaLength_mm = 2.8 * (1 - 0.05)  # Distancia focal mínima
        # Convertir de milímetros a centímetros
        focaLength_cm = focaLength_mm / 10

        object_width_cm = (object_width_px * size_pixel_cm *
                           camera_distance_cm) / focaLength_cm
        return object_width_cm


def obtener_longitud_focal(imagen_path):
    try:
        imagen = Image.open(imagen_path)
        exif_info = imagen._getexif()

        # ID de la etiqueta EXIF para la longitud focal
        id_longitud_focal = 0x920a

        if exif_info and id_longitud_focal in exif_info:
            longitud_focal = exif_info[id_longitud_focal]
            return longitud_focal
        else:
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None


ruta_imagen = 'Camera/Camera_Calibrate/ChessBoard/2.jpg'

# Obtener la longitud focal
longitud_focal = obtener_longitud_focal(ruta_imagen)

if longitud_focal is not None:
    print(f"Longitud Focal: {longitud_focal} mm")
else:
    print("No se encontró información de longitud focal en la imagen.")


# Uso de la clase
converter = PixelConverter()

# Supongamos que la distancia entre la cámara y el objeto es de 60 cm
camera_distance_cm = 60

ancho_objeto_cm = converter.objectWidth(
    object_width_px=108.78, camera_distance_cm=camera_distance_cm)

print("Ancho del objeto estimado:", ancho_objeto_cm, "centímetros")
