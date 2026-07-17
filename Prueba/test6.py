es_hombre = True
es_alto = True
if es_hombre and es_alto:
    print("¡Eres un hombre alto!")
elif es_hombre and not es_alto:
    print("Eres un hombre bajito")
elif not es_hombre and es_alto:
    print("No eres hombre, pero eres alto")
else:
    print("No eres un hombre, ni eres alto")