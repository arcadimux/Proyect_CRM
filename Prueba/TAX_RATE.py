TAX_RATE = 0.08875

def format_usd(amount):
    return f"${amount:,.2f}"

print("\033[1;94m╔══════════════════════════════════════╗\033[0m")
print("\033[1;94m║  Calculadora de impuestos — Nueva York  ║\033[0m")
print("\033[1;94m╚══════════════════════════════════════╝\033[0m")

while True:
    try:
        entrada = input("\nCantidad en dólares (o 'S' para salir): ").strip()
        if entrada.upper() == "S":
            print("Hasta luego.")
            break
        money = float(entrada.replace(",", "."))
        if money < 0:
            print("\033[91mLa cantidad no puede ser negativa.\033[0m")
            continue
    except ValueError:
        print("\033[91mDebes introducir un número válido.\033[0m")
        continue

    if money <= 1:
        print("\033[92m✔ Esta cantidad está libre de impuestos en Nueva York.\033[0m")
    else:
        tax = money * TAX_RATE
        total = money + tax
        print(f"\n  Precio base : {format_usd(money)}")
        print(f"  Impuesto    : {format_usd(tax)}  (8.875%)")
        print(f"  \033[1mTotal       : {format_usd(total)}\033[0m")