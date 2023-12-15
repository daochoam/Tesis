import time


def calculate_variable():
    variable = [1.0, 2.0, 3.0, 0.0, 0.0, 5.0]

    while True:
        # Simula la lógica de cálculo de la variable
        variable[5] += 1.0  # Cambia el último valor de la lista
        print(f"Variable calculada: {variable}")

        # Escribe el valor de la variable en un archivo
        with open("shared_variable.txt", "w") as file:
            file.write(",".join(map(str, variable)))

        time.sleep(1)


if __name__ == "__main__":
    calculate_variable()
