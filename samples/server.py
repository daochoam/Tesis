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


def main():
    try:
        server = PoseServer('0.0.0.0', 8888)

        while True:
            # Aceptar nueva conexión
            connection = server.acceptConnection()

            try:
                while True:
                    # Leer el valor de la variable desde el archivo
                    with open("shared_variable.txt", "r") as file:
                        variable = list(
                            map(float, file.read().strip().split(',')))

                    # Enviar variable a la conexión
                    server.sendVariable(connection, variable)

                    # Esperar un tiempo (simulando un cálculo o cambio en la variable)
                    time.sleep(1)

            except ConnectionResetError:
                # Maneja la desconexión del cliente
                print("Cliente desconectado.")
                break

            finally:
                # Cerrar la conexión
                server.closeConnection(connection)

    except KeyboardInterrupt:
        pass

    finally:
        server.server.close()


if __name__ == "__main__":
    main()
