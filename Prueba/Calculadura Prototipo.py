from tokenize import endpats

while True:
    try:
        num_1 = float(input("Introduzca un primer numero: "))
    except ValueError:
        print("\033[91mError: Debe insertar sólo números.\033[0m")
        continue
    op = input("Introduzca operación: ")
    try:
        num_2 = float(input("Introduzca otro numero: "))
    except ValueError:
        print("\033[91mError: Debe insertar sólo números.\033[0m")
        continue
    if op == "+":
        print(num_1 + num_2)
    elif op == "-":
        print(num_1 - num_2)
    elif op == "*":
        print(num_1 * num_2)
    elif op == "/":
        if num_2 == 0:
            print("No se puede dividir entre 0")
            continue
        print(num_1 / num_2)
    elif op == "^":
        print(num_1 ** num_2)
    else:
        print("Operación no válida")
    while True:
        ok = input("Escriba <ok> para continuar: ")
        if ok == "ok":
            break
        else:
            print("\033[91mDebe escribir <ok> para realizar otra operación.\033[0m")

