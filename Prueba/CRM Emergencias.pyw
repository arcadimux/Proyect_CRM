# Avisa , Código de aviso , Localización , Código de incidencia
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import os
import random


# Rutas de ficheros (ajusta si lo deseas)
RUTA_ACTIVAS = r"D:\Users\jjosh\OneDrive\Escritorio\Coding\Proyectos Python\CRM\Data\incidencias_activas.json"
RUTA_GESTIONADAS = r"D:\Users\jjosh\OneDrive\Escritorio\Coding\Proyectos Python\CRM\Data\incidencias_gestionadas.json"
RUTA_LOG = r"D:\Users\jjosh\OneDrive\Escritorio\Coding\Proyectos Python\CRM\Data\Incidencias.txt"  # opcional, tu log plano

#Permite leer archivos JSON y devolver una lista de diccionarios, o una lista vacía si el archivo no existe o está vacío.
def cargar_json(ruta):
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

#Permite guardar una lista de diccionarios en un archivo JSON, sobrescribiendo el contenido anterior.
def guardar_json(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

def generar_id_numerico():
    return str(random.randint(1000000, 9999999))
id_full = generar_id_numerico()
    
incidencias_activas = cargar_json(RUTA_ACTIVAS)
incidencias_gestionadas = cargar_json(RUTA_GESTIONADAS)

def id_corto(id_full):
    return id_full[:8]

def refrescar_listbox():
    listbox_incidentes.delete(0, tk.END)
    for inc in incidencias_activas:
        display = f"{id_corto(inc['id'])} - {inc.get('localizacion','')} - {inc.get('fecha_creada','')}"
        listbox_incidentes.insert(tk.END, display)

def refrescar_listbox_gestionadas():
    listbox_incidentes.delete(0, tk.END)
    for inc in incidencias_gestionadas:
        display = f"{id_corto(inc['id'])} - {inc.get('localizacion','')} - {inc.get('fecha_gestionada','')}"
        listbox_incidentes.insert(tk.END, display)

def refrescar_listbox_equipo():
    listbox_equipo.delete(0, tk.END)

    sel = listbox_incidentes.curselection()
    if not sel:
        return

    idx = sel[0]

    if modo_actual.get() == "activas":
        inc = incidencias_activas[idx]
    else:
        inc = incidencias_gestionadas[idx]

    for eq in inc.get("equipos", []):
        listbox_equipo.insert(tk.END, f"{eq['equipo']} | {eq['inicio']} | {eq['llegada']}")

def guardar_equipo():
    sel_inc = listbox_incidentes.curselection()
    if not sel_inc:
        messagebox.showwarning("Atención", "Selecciona una incidencia antes de añadir o editar un equipo.")
        return

    idx_inc = sel_inc[0]

    # Seleccionar incidencia según modo
    if modo_actual.get() == "activas":
        inc = incidencias_activas[idx_inc]
    else:
        inc = incidencias_gestionadas[idx_inc]

    # Si no existe la lista de equipos, crearla
    if "equipos" not in inc:
        inc["equipos"] = []

    # ¿Estamos editando un equipo?
    sel_eq = listbox_equipo.curselection()

    if sel_eq:
        # EDITAR equipo existente
        idx_eq = sel_eq[0]
        inc["equipos"][idx_eq] = {
            "equipo": entry_equipo.get(),
            "inicio": inicio_equipo.get(),
            "llegada": llegada_equipo.get()
        }
    else:
        # AÑADIR equipo nuevo
        nuevo_equipo = {
            "equipo": entry_equipo.get(),
            "inicio": inicio_equipo.get(),
            "llegada": llegada_equipo.get()
        }
        inc["equipos"].append(nuevo_equipo)

    # Guardar en JSON
    guardar_json(RUTA_ACTIVAS, incidencias_activas)
    guardar_json(RUTA_GESTIONADAS, incidencias_gestionadas)

    # Actualizar lista visual
    refrescar_listbox_equipo()

    # Limpiar campos
    entry_equipo.delete(0, tk.END)
    inicio_equipo.delete(0, tk.END)
    llegada_equipo.delete(0, tk.END)

def cargar_en_formulario(inc):
    current_id.set(inc["id"])
    fecha_creada_var.set(inc.get("fecha_creada", registrar_fecha_hora()))

    entry_aviso.delete(0, tk.END); entry_aviso.insert(0, inc.get("aviso",""))
    entry_comunicante.delete(0, tk.END); entry_comunicante.insert(0, inc.get("comunicante",""))
    entry_localizacion.delete(0, tk.END); entry_localizacion.insert(0, inc.get("localizacion",""))
    entry_codigo_incidencia.delete(0, tk.END); entry_codigo_incidencia.insert(0, inc.get("codigo",""))
    entry_descripcion.delete("1.0", tk.END); entry_descripcion.insert("1.0", inc.get("descripcion",""))
    entry_gestiones.delete("1.0", tk.END); entry_gestiones.insert("1.0", inc.get("gestiones",""))
    date_tag.config(text=inc.get("fecha_registro", registrar_fecha_hora()))

    #Mostrar fecha gestionada si existe
    if "fecha_gestionada" in inc:
        date_tag_gestionada.config(
            text="Gestionada: " + inc["fecha_gestionada"],
            fg="#B93425"
        )
    else:
        date_tag_gestionada.config(text="")
def guardar_datos():
    inc = obtener_campos()
    existe = False
    for i, item in enumerate(incidencias_activas):
        if item["id"] == inc["id"]:
            inc["fecha_creada"] = item.get("fecha_creada", inc["fecha_creada"])
            if "equipos" in item:
                inc["equipos"] = item["equipos"]
            incidencias_activas[i] = inc
            existe = True
            break

    if not existe:
        inc["equipos"] = []
        incidencias_activas.append(inc)

    guardar_json(RUTA_ACTIVAS, incidencias_activas)
    refrescar_listbox()

def editar_equipo():
    # Solo exigimos que haya un equipo seleccionado
    sel_eq = listbox_equipo.curselection()
    if not sel_eq:
        messagebox.showwarning("Atención", "Selecciona un equipo para editar.")
        return

    # La incidencia ya está seleccionada porque la lista de equipos se muestra en base a ella
    sel_inc = listbox_incidentes.curselection()
    if not sel_inc:
        # Por seguridad, pero sin molestar al usuario
        return

    idx_inc = sel_inc[0]
    idx_eq = sel_eq[0]

    # Seleccionar incidencia según modo
    if modo_actual.get() == "activas":
        inc = incidencias_activas[idx_inc]
    else:
        inc = incidencias_gestionadas[idx_inc]

    equipo = inc["equipos"][idx_eq]

    # Cargar datos en los campos para edición
    entry_equipo.delete(0, tk.END)
    entry_equipo.insert(0, equipo["equipo"])

    inicio_equipo.delete(0, tk.END)
    inicio_equipo.insert(0, equipo["inicio"])

    llegada_equipo.delete(0, tk.END)
    llegada_equipo.insert(0, equipo["llegada"])

def obtener_campos():
    # Si current_id está vacío, se generará al guardar
    return {
        "id": current_id.get() or str(generar_id_numerico()),
        "aviso": entry_aviso.get(),
        "comunicante": entry_comunicante.get(),
        "localizacion": entry_localizacion.get(),
        "codigo": entry_codigo_incidencia.get(),
        "descripcion": entry_descripcion.get("1.0", tk.END).strip(),
        "gestiones": entry_gestiones.get("1.0", tk.END).strip(),
        # fecha_creada: si ya existe la mantenemos; si es nueva, la asignamos al guardar
        "fecha_creada": fecha_creada_var.get() or registrar_fecha_hora()
    }
def marcar_gestionada():
    sel = listbox_incidentes.curselection()
    if not sel:
        messagebox.showwarning("Atención", "Selecciona una incidencia para marcar como gestionada.")
        return
    idx = sel[0]
    inc = incidencias_activas.pop(idx)
    inc["fecha_gestionada"] = registrar_fecha_hora_gestionada()
    incidencias_gestionadas.append(inc)
    guardar_json(RUTA_ACTIVAS, incidencias_activas)
    guardar_json(RUTA_GESTIONADAS, incidencias_gestionadas)
    refrescar_listbox()
    refrescar_listbox_equipo()
    limpiar_campos()
    messagebox.showinfo("Gestionada", "Movida a gestionadas.")

def registrar_fecha_hora():
    fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return fecha_hora_actual

def registrar_fecha_hora_gestionada():
    fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return fecha_hora_actual

def limpiar_campos():
    current_id.set("")            # nueva incidencia
    fecha_creada_var.set("")      # se asignará al guardar si queda vacío
    entry_aviso.delete(0, tk.END)
    entry_comunicante.delete(0, tk.END)
    entry_localizacion.delete(0, tk.END)
    entry_codigo_incidencia.delete(0, tk.END)
    entry_descripcion.delete("1.0", tk.END)
    entry_gestiones.delete("1.0", tk.END)
    entry_equipo.delete(0, tk.END)
    inicio_equipo.delete(0, tk.END)
    llegada_equipo.delete(0, tk.END)
    date_tag.config(text=f"{registrar_fecha_hora()}")
    listbox_incidentes.selection_clear(0, tk.END)

def on_select_listbox(event):
    sel = listbox_incidentes.curselection()
    if not sel:
        return
    idx = sel[0]

    if modo_actual.get() == "activas":
        inc = incidencias_activas[idx]
    else:
        inc = incidencias_gestionadas[idx]

    cargar_en_formulario(inc)
    refrescar_listbox_equipo()

def change_lista():
    if modo_actual.get() == "activas":
        modo_actual.set("gestionadas")
        titulo_lista.set("Incidencias gestionadas")
        date_tag_gestionada.config(text="")   # ← limpiar texto al entrar en gestionadas
        date_tag_gestionada.grid(row=0, sticky="w", column=3, padx=10, pady=10)
        refrescar_listbox_gestionadas()
    else:
        modo_actual.set("activas")
        titulo_lista.set("Incidencias en curso")
        date_tag_gestionada.grid_forget()
        refrescar_listbox()
        




root = tk.Tk()
root.geometry("1200x1100")

#Centrar el contenido en la ventana
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)
root.grid_columnconfigure(2, weight=1)

tag = tk.Label(root, text="CRM", fg="green", font=("Calibri Light", 24))
tag.grid(pady=20, padx=20, row=0, column=1)

# Variables
current_id = tk.StringVar()
fecha_creada_var = tk.StringVar()
modo_actual = tk.StringVar(value="activas")
titulo_lista = tk.StringVar(value="Incidencias en curso")
# Barra izquierda y derecha, y lista
frame_left = tk.Frame(root)
frame_left.grid(row=0, column=0, rowspan=10, sticky="ns", padx=10, pady=10)
frame_right = tk.Frame(root)
frame_right.grid(row=0, column=1, padx=10, pady=10, sticky="n")

# Subframe superior con título y botón
frame_header = tk.Frame(frame_left)
frame_header.pack(side="top", fill="x", pady=5)

tk.Label(frame_header, textvariable=titulo_lista, font=("Calibri Light", 14)).pack(side="left", padx=5)

boton_arrow = tk.Button(
    frame_header,
    text="⮞",
    font=("Calibri Light", 16),
    command=change_lista,
    bg="#3498DB",
    fg="white"
)
boton_arrow.pack(side="right", padx=5)

# Subframe para la lista
frame_list = tk.Frame(frame_left)
frame_list.pack(side="top", fill="both", expand=True)

listbox_incidentes = tk.Listbox(frame_list, width=50, height=25)
listbox_incidentes.pack(side="left", fill="both", expand=True)
listbox_incidentes.bind("<<ListboxSelect>>", on_select_listbox)
scroll = tk.Scrollbar(frame_list, command=listbox_incidentes.yview)
scroll.pack(side="right", fill="y")
listbox_incidentes.config(yscrollcommand=scroll.set)

tk.Label(root, text="Aviso", font=("Calibri Light", 12)).grid(row=1, column=1)
entry_aviso = tk.Entry(root, font=("Calibri Light", 12))
entry_aviso.grid(row=1, column=2, sticky="w", padx=10, pady=10)

tk.Label(root, text="Comunicante", font=("Calibri Light", 12)).grid(row=2, column=1)
entry_comunicante = tk.Entry(root, font=("Calibri Light", 12))
entry_comunicante.grid(row=2, column=2, sticky="w", padx=10, pady=10)

tk.Label(root, text="Localización", font=("Calibri Light", 12)).grid(row=3, column=1)
entry_localizacion = tk.Entry(root, font=("Calibri Light", 12))
entry_localizacion.grid(row=3, column=2, sticky="w", padx=10, pady=10)

tk.Label(root, text="Código de incidencia", font=("Calibri Light", 12)).grid(row=4, column=1)
entry_codigo_incidencia = tk.Entry(root, font=("Calibri Light", 12))
entry_codigo_incidencia.grid(row=4, column=2, sticky="w", padx=10, pady=10)


# Descripción
tk.Label(root, text="Descripción", font=("Calibri Light", 12)).grid(row=5, column=1)
entry_descripcion = tk.Text(root, font=("Calibri Light", 12), width=40, height=5)
entry_descripcion.grid(row=5, column=2, sticky="w", padx=10, pady=10)
# Gestiones
tk.Label(root, text="Gestiones", font=("Calibri Light", 12)).grid(row=6, column=1)
entry_gestiones = tk.Text(root, font=("Calibri Light", 12), width=40, height=5)
entry_gestiones.grid(row=6, column=2, sticky="w", padx=10, pady=10)


# Equipo , aviso , llegada
frame_equipo = tk.Frame(root)
frame_equipo.grid(row=8, column=1, columnspan=3, sticky="w", pady=10)

tk.Label(frame_equipo, text="Equipo", font=("Calibri Light", 12)).grid(row=0, column=0, padx=5)
entry_equipo = tk.Entry(frame_equipo, font=("Calibri Light", 12), width=10)
entry_equipo.grid(row=0, column=1, padx=5)

tk.Label(frame_equipo, text="Inicio", font=("Calibri Light", 12)).grid(row=0, column=2, padx=5)
inicio_equipo = tk.Entry(frame_equipo, font=("Calibri Light", 12), width=10)
inicio_equipo.grid(row=0, column=3, padx=5)

tk.Label(frame_equipo, text="Llegada", font=("Calibri Light", 12)).grid(row=0, column=4, padx=5)
llegada_equipo = tk.Entry(frame_equipo, font=("Calibri Light", 12), width=10)
llegada_equipo.grid(row=0, column=5, padx=5)

botton_guardar_equipo = tk.Button(
    frame_equipo,
    text="✓",
    font=("Calibri Light", 16),
    command=guardar_equipo,
    bg="#3498DB",
    fg="white"
)
botton_guardar_equipo.grid(row=0, column=6, padx=5)

botton_nuevo_equipo = tk.Button(
    frame_equipo,
    text="✎",
    font=("Calibri Light", 16),
    command=editar_equipo,
    bg="#77DB34",
    fg="white"
)
botton_nuevo_equipo.grid(row=0, column=7, padx=5)

# Subframe para Equipo debajo del formulario
frame_bottom = tk.Frame(root)
frame_bottom.grid(row=10, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
frame_bottom.grid_rowconfigure(0, weight=1)
frame_bottom.grid_columnconfigure(0, weight=1)

frame_equipo_list = tk.Frame(frame_bottom)
frame_equipo_list.pack(side="top", fill="both", expand=True)

listbox_equipo = tk.Listbox(frame_equipo_list, width=30, height=10)
listbox_equipo.pack(side="left", fill="both", expand=True)
scroll_equipo = tk.Scrollbar(frame_equipo_list, command=listbox_equipo.yview)
scroll_equipo.pack(side="right", fill="y")
listbox_equipo.config(yscrollcommand=scroll_equipo.set)



#Fecha y hora de creación
date_tag = tk.Label(root, text=f"{registrar_fecha_hora()}", font=("Calibri Light", 12))
date_tag.grid(row=0, sticky="w", column=2, padx=10, pady=10)
#Fecha y hora gestionada
date_tag_gestionada = tk.Label(root, text="Gestionada: " + f"{registrar_fecha_hora_gestionada()}", fg="#B93425", font=("Calibri Light", 12))

#Botones
frame_botones = tk.Frame(root)
frame_botones.grid(row=9, column=0, columnspan=3, sticky="n", pady=10)
botton_guardar = tk.Button(frame_botones, text="Guardar", bg="#2C69C4", fg="white", command=guardar_datos, font=("Calibri Light", 14))
botton_guardar.pack(side="left", padx=25)

botton_nueva = tk.Button(frame_botones, text="Nueva", bg="#C0392B", fg="white", command=limpiar_campos, font=("Calibri Light", 14))
botton_nueva.pack(side="left", padx=25)

botton_gestionada = tk.Button(frame_botones, text="Gestionada", bg="#27AE60", command=marcar_gestionada, fg="white", font=("Calibri Light", 14))
botton_gestionada.pack(side="left", padx=25)

refrescar_listbox()
refrescar_listbox_equipo()

root.mainloop()