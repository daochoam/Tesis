import socket
import time


class PoseServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bindAndListen()

    def bindAndListen(self):
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"Esperando conexiones en el puerto {self.port}...")

    def acceptConnection(self):
        conn, addr = self.server.accept()
        print(f"Conectado por {addr}")
        return conn

    def sendVariable(self, conn, variable):
        message = ",".join(map(str, variable))
        conn.sendall(message.encode())
        print(f"Enviando variable: {message}")

    def closeConnection(self, conn):
        conn.close()
