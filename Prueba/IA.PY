import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import os
import uuid

# Rutas de ficheros (ajusta si lo deseas)
RUTA_ACTIVAS = "incidencias_activas.json"
RUTA_GESTIONADAS = "incidencias_gestionadas.json"
RUTA_LOG = "Incidencias.txt"  # opcional, tu log plano

def cargar_json(ruta):
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def guardar_json(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

def registrar_fecha_hora():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Cargar datos al inicio
incidencias_activas = cargar_json(RUTA_ACTIVAS)
incidencias_gestionadas = cargar_json(RUTA_GESTIONADAS)

def id_corto(id_full):
    return id_full[:8]

def refrescar_listbox():
    listbox_incidentes.delete(0, tk.END)
    for inc in incidencias_activas:
        display = f"{id_corto(inc['id'])} - {inc.get('localizacion','')} - {inc.get('fecha_creada','')}"
        listbox_incidentes.insert(tk.END, display)

def obtener_campos():
    # Si current_id está vacío, se generará al guardar
    return {
        "id": current_id.get() or str(uuid.uuid4()),
        "aviso": entry_aviso.get(),
        "comunicante": entry_comunicante.get(),
        "localizacion": entry_localizacion.get(),
        "codigo": entry_codigo_incidencia.get(),
        "descripcion": entry_descripcion.get("1.0", tk.END).strip(),
        "gestiones": entry_gestiones.get("1.0", tk.END).strip(),
        "equipo": entry_equipo.get(),
        "fecha_registro": date_tag.cget("text"),
        # fecha_creada: si ya existe la mantenemos; si es nueva, la asignamos al guardar
        "fecha_creada": fecha_creada_var.get() or registrar_fecha_hora()
    }

def cargar_en_formulario(inc):
    current_id.set(inc["id"])
    fecha_creada_var.set(inc.get("fecha_creada", registrar_fecha_hora()))
    entry_aviso.delete(0, tk.END); entry_aviso.insert(0, inc.get("aviso",""))
    entry_comunicante.delete(0, tk.END); entry_comunicante.insert(0, inc.get("comunicante",""))
    entry_localizacion.delete(0, tk.END); entry_localizacion.insert(0, inc.get("localizacion",""))
    entry_codigo_incidencia.delete(0, tk.END); entry_codigo_incidencia.insert(0, inc.get("codigo",""))
    entry_descripcion.delete("1.0", tk.END); entry_descripcion.insert("1.0", inc.get("descripcion",""))
    entry_gestiones.delete("1.0", tk.END); entry_gestiones.insert("1.0", inc.get("gestiones",""))
    entry_equipo.delete(0, tk.END); entry_equipo.insert(0, inc.get("equipo",""))
    date_tag.config(text=inc.get("fecha_registro", registrar_fecha_hora()))

def on_select_listbox(event):
    sel = listbox_incidentes.curselection()
    if not sel:
        return
    idx = sel[0]
    inc = incidencias_activas[idx]
    cargar_en_formulario(inc)

def guardar_datos():
    inc = obtener_campos()
    # Si la incidencia es nueva (id no estaba en activas), asignar fecha_creada ahora
    existe = False
    for i, item in enumerate(incidencias_activas):
        if item["id"] == inc["id"]:
            # Mantener la fecha_creada existente si la hubiera
            inc["fecha_creada"] = item.get("fecha_creada", inc["fecha_creada"])
            incidencias_activas[i] = inc
            existe = True
            break
    if not existe:
        # nueva incidencia: fecha_creada ya viene en inc["fecha_creada"]
        incidencias_activas.append(inc)

    # Guardar JSONs
    guardar_json(RUTA_ACTIVAS, incidencias_activas)

    # Escribir en log plano (opcional)
    with open(RUTA_LOG, "a", encoding="utf-8") as archivo:
        archivo.write(f"Aviso: {inc['aviso']}\n")
        archivo.write(f"Comunicante: {inc['comunicante']}\n")
        archivo.write(f"Localización: {inc['localizacion']}\n")
        archivo.write(f"Código de incidencia: {inc['codigo']}\n")
        archivo.write(f"Descripción: {inc['descripcion']}\n")
        archivo.write(f"Gestiones: {inc['gestiones']}\n")
        archivo.write(f"Equipo: {inc['equipo']}\n")
        archivo.write(f"Fecha creada: {inc['fecha_creada']}\n")
        archivo.write(f"Fecha y hora de registro: {inc['fecha_registro']}\n")
        archivo.write(f"Fecha guardado: {registrar_fecha_hora()}\n")
        archivo.write("________________________________\n")

    refrescar_listbox()
    messagebox.showinfo("Guardado", "Incidencia guardada en activas y en el log.")

def marcar_gestionada():
    sel = listbox_incidentes.curselection()
    if not sel:
        messagebox.showwarning("Atención", "Selecciona una incidencia para marcar como gestionada.")
        return
    idx = sel[0]
    inc = incidencias_activas.pop(idx)
    inc["fecha_gestionada"] = registrar_fecha_hora()
    incidencias_gestionadas.append(inc)
    guardar_json(RUTA_ACTIVAS, incidencias_activas)
    guardar_json(RUTA_GESTIONADAS, incidencias_gestionadas)
    refrescar_listbox()
    limpiar_campos()
    messagebox.showinfo("Gestionada", "Incidencia marcada como gestionada y movida a gestionadas.")

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
    date_tag.config(text=registrar_fecha_hora())
    listbox_incidentes.selection_clear(0, tk.END)

# Interfaz
root = tk.Tk()
root.geometry("1000x700")
root.title("CRM Incidencias")

# Variables
current_id = tk.StringVar()
fecha_creada_var = tk.StringVar()

# Layout: izquierda Listbox, derecha formulario
frame_left = tk.Frame(root, width=320)
frame_left.grid(row=0, column=0, rowspan=10, sticky="ns", padx=10, pady=10)
frame_right = tk.Frame(root)
frame_right.grid(row=0, column=1, padx=10, pady=10, sticky="n")

tk.Label(frame_left, text="Incidencias en curso", font=("Calibri Light", 14)).pack(pady=5)
listbox_incidentes = tk.Listbox(frame_left, width=50, height=30)
listbox_incidentes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
listbox_incidentes.bind("<<ListboxSelect>>", on_select_listbox)
scroll = tk.Scrollbar(frame_left, command=listbox_incidentes.yview)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
listbox_incidentes.config(yscrollcommand=scroll.set)

# Formulario (derecha)
tk.Label(frame_right, text="Aviso", font=("Calibri Light", 12)).grid(row=0, column=0, sticky="w")
entry_aviso = tk.Entry(frame_right, font=("Calibri Light", 12), width=50)
entry_aviso.grid(row=0, column=1, pady=5)

tk.Label(frame_right, text="Comunicante", font=("Calibri Light", 12)).grid(row=1, column=0, sticky="w")
entry_comunicante = tk.Entry(frame_right, font=("Calibri Light", 12), width=50)
entry_comunicante.grid(row=1, column=1, pady=5)

tk.Label(frame_right, text="Localización", font=("Calibri Light", 12)).grid(row=2, column=0, sticky="w")
entry_localizacion = tk.Entry(frame_right, font=("Calibri Light", 12), width=50)
entry_localizacion.grid(row=2, column=1, pady=5)

tk.Label(frame_right, text="Código de incidencia", font=("Calibri Light", 12)).grid(row=3, column=0, sticky="w")
entry_codigo_incidencia = tk.Entry(frame_right, font=("Calibri Light", 12), width=50)
entry_codigo_incidencia.grid(row=3, column=1, pady=5)

tk.Label(frame_right, text="Descripción", font=("Calibri Light", 12)).grid(row=4, column=0, sticky="nw")
entry_descripcion = tk.Text(frame_right, font=("Calibri Light", 12), width=60, height=6)
entry_descripcion.grid(row=4, column=1, pady=5)

tk.Label(frame_right, text="Gestiones", font=("Calibri Light", 12)).grid(row=5, column=0, sticky="nw")
entry_gestiones = tk.Text(frame_right, font=("Calibri Light", 12), width=60, height=6)
entry_gestiones.grid(row=5, column=1, pady=5)

tk.Label(frame_right, text="Equipo", font=("Calibri Light", 12)).grid(row=6, column=0, sticky="w")
entry_equipo = tk.Entry(frame_right, font=("Calibri Light", 12), width=50)
entry_equipo.grid(row=6, column=1, pady=5)

tk.Label(frame_right, text="Fecha creada", font=("Calibri Light", 10)).grid(row=7, column=0, sticky="w")
label_fecha_creada = tk.Label(frame_right, textvariable=fecha_creada_var, font=("Calibri Light", 10))
label_fecha_creada.grid(row=7, column=1, sticky="w")

date_tag = tk.Label(frame_right, text=registrar_fecha_hora(), font=("Calibri Light", 10))
date_tag.grid(row=8, column=1, sticky="w", pady=5)

# Botones
btn_guardar = tk.Button(frame_right, text="Guardar", bg="#2C69C4", fg="white", command=guardar_datos, width=14)
btn_guardar.grid(row=9, column=1, sticky="w", pady=10)

btn_gestionada = tk.Button(frame_right, text="Gestionada", bg="#27AE60", fg="white", command=marcar_gestionada, width=20)
btn_gestionada.grid(row=9, column=1, sticky="e", pady=10)

btn_nueva = tk.Button(frame_right, text="Nueva", bg="#C0392B", fg="white", command=limpiar_campos, width=14)
btn_nueva.grid(row=9, column=0, pady=10)

# Inicializar listbox
refrescar_listbox()
root.mainloop()
