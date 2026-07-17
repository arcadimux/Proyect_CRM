month_conv = {
    "01": "enero",
    "02": "febrero",
    "03": "marzo",
    "04": "abril",
    "05": "mayo",
    "06": "junio",
    "07": "julio",
    "08": "agosto",
    "09": "septiembre",
    "10": "octubre",
    "11": "noviembre",
    "12": "diciembre",}
user_input = month_conv.get
while True:
    user_input = input("Introduzca un número de mes desde 01 hasta 12: ")
    if user_input in month_conv:
        print (month_conv.get(user_input))
        break
    else:
        print("Debe ingresar un número del 01 hasta el 12")