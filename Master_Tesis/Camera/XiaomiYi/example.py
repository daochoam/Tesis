import cv2
from yi.camera import XiaomiYi

# Inicializa la cámara XiaomiYi
camera = XiaomiYi()
camera.connect()

# Captura una foto
image_data = camera.capture()
camera.disconnect()

# Decodifica los datos de la imagen
image_np = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

# Muestra la imagen en una ventana
cv2.imshow('Captured Image', image_np)
cv2.waitKey(0)
cv2.destroyAllWindows()
