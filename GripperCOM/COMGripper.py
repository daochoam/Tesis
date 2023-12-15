import serial
from serial.tools import list_ports
import time


def findArduinoPort():
    # Busca automáticamente el puerto al que está conectado el Arduino
    ports = list(list_ports.comports())
    for p in ports:
        print(f"Port: {p.device}, Description: {p.description}")
        return p.device
    return "Arduino not found"


def sendOpeningGripper(value, PORT):
    Arduino = serial.Serial(PORT, 9600)
    Arduino.write(f"{value}\n".encode('utf-8'))


def closeChanel(PORT):
    Arduino = serial.Serial(PORT, 9600)
    Arduino.close()


PORT = findArduinoPort()

try:
    while True:
        value = "setup"
        sendOpeningGripper(value, PORT)
        # Espera un tiempo antes de enviar más datos (opcional)
        time.sleep(1)

except KeyboardInterrupt:
    # Cierra el puerto serie al interrumpir el programa
    closeChanel(PORT)

    print("Comunicación serial cerrada.")
