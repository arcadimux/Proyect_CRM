magic_numbers = [11, 5, 2, 7, 4]
magic_numbers.reverse()
ciudades = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao" ]
ciudades = ciudades.copy()
ciudades.sort()
ciudades.extend(magic_numbers)
ciudades.insert(2, "Alabama")
ciudades.remove("Sevilla")
print(ciudades.index("Valencia"))
print(ciudades.count("Valencia"))
print(ciudades)

    