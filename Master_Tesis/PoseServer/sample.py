from PoseServer import PoseServer
import time

HOST = '0.0.0.0'
PORT = 8888


def main():
    try:
        server = PoseServer(HOST, PORT)
        while True:
            connection = server.acceptConnection()
            try:
                while True:
                    with open("shared_variable.txt", "r") as file:
                        variable = list(
                            map(float, file.read().strip().split(',')))
                    # Enviar variable a la conexión
                    server.sendVariable(connection, variable)
                    # Esperar un tiempo (simulando un cálculo o cambio en la variable)
                    time.sleep(1)
            except ConnectionResetError:
                print("Client disconnect.")
                break
            finally:
                server.closeConnection(connection)
    except KeyboardInterrupt:
        pass
    finally:
        server.server.close()


if __name__ == "__main__":
    main()
