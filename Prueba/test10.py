def translate(frase):
    traduccion = ""
    for letter in frase:
        if letter in "AEIOUaeiou":
            traduccion = traduccion + "h"
        else:
            traduccion = traduccion + letter
    return traduccion

print(translate(input("ingrese una frase: ")))