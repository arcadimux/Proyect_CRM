import math
import os
os.system('cls')  # En Windows
# Función para imprimir en verde
def verde(texto):
    print(f"\033[92m{texto}\033[0m")

while True:
    print("Bienvenido a la calculadora.\n + = suma\n - = resta\n * = multiplicación\n / = división\n r = raíz cuadrada\n ** = exponente")
# Ciclo para que el usuario pueda realizar la operación en una sola línea.
    operation = input("Inserte la operación que desea realizar (+, -, *, /, r, **): ")
    a = ""
    b = ""
    op = ""
    for caracter in operation:
        if caracter.isdigit() or caracter == ".":
            if op == "":
                a += caracter
            else:
                b += caracter
        else:
            op = caracter
# Una vez que se han separado los números y la operación, se procede a realizar la operación correspondiente.
    if op == "+":
        verde(float(a) + float(b))
    elif op == "-":
        verde(float(a) - float(b))
    elif op == "*":
        verde(float(a) * float(b))
    elif op == "/":
        if b == 0:
            print("Error: División por cero no permitida")
            continue
        verde(float(a) / float(b))
    elif op == "r":
        if a < 0:
            print("Error: No se puede calcular la raíz cuadrada de un número negativo")
            continue
        verde(math.sqrt(float(a)))
    elif op == "**":
        try:
            verde(float(a) ** float(b))
        except OverflowError:
            print("Error: Resultado demasiado grande. Usa números más pequeños para la exponenciación.")
    else:
        print("Operación no válida")
    res = input("¿Desea realizar otra operación? (Pulse Enter/Q): ").upper()
    if res == "":
        os.system('cls')  # Limpia la consola en Windows
        continue
    elif res == "Q":
        break
    else:
        print("Respuesta no válida, tiene que ser una S o una N.")
        
