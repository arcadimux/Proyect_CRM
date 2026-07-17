secret_word = "elefante"
prueba = ""
conteo_prueba = 0
conteo_limite = 3
sin_pruebas = False
while prueba != secret_word and not sin_pruebas:
    if conteo_prueba < conteo_limite:
        prueba = input("Introduzca una contraseña: ")
        conteo_prueba += 1
    else: sin_pruebas = True
if sin_pruebas:print("¡Perdiste!")
else: print("¡Tú ganas!")