print('\033[91mCalculadora de impuestos de Nueva york\033[0m')
while True:
    try:
        money = float(input('Inserte cantidad de dinero en dólares: '))
    except ValueError:
            print('Debe ser un numero')
            continue
    tax = 0.08875
    if money <= 1:
        print('Su cantidad está libre de impuestos en Nueva York.')
        objetivo = str(input('Inserte otra cantidad en dólares o pulse "Y" para salir del programa: ').upper())
    else:
        resultado = str(money * tax + money)
        resultado2 = str(money*tax)
        print('El coste total es de: ' + resultado + ' $')
        print('El impuesto es de: ' + resultado2 + ' $')
        objetivo = str(input('Inserte otra cantidad en dólares o pulse "Y" para salir del programa: '))
        if objetivo.upper() != "Y": continue
        else:
            break       
