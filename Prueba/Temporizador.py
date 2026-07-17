import tkinter as tk
from PIL import Image, ImageTk
import time
import subprocess

# --- Función para reproducir audio ---
def play_audio():
    ruta_vlc = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
    ruta_audio = r"D:\Users\jjosh\OneDrive\Escritorio\Coding\Proyectos Python\Prueba\Medios\Audio\genius.mp3"
    subprocess.Popen([ruta_vlc, "--qt-start-minimized", ruta_audio])

# --- Ventana principal ---
root = tk.Tk()
root.title("Temporizador con interfaz")

# --- Cargar imagen de fondo ---
imagen = Image.open(r"D:\ruta\de\tu\imagen.jpg")
imagen = imagen.resize((600, 400))
fondo = ImageTk.PhotoImage(imagen)

canvas = tk.Canvas(root, width=600, height=400)
canvas.pack()
canvas.create_image(0, 0, anchor="nw", image=fondo)

# --- Texto del temporizador ---
texto_tiempo = canvas.create_text(
    300, 200,
    text="00:00",
    fill="white",
    font=("Arial", 48, "bold")
)

# --- Función de cuenta atrás ---
def cuenta_atras(segundos):
    if segundos >= 0:
        mins = segundos // 60
        secs = segundos % 60
        canvas.itemconfig(texto_tiempo, text=f"{mins:02d}:{secs:02d}")
        root.after(1000, cuenta_atras, segundos - 1)
    else:
        play_audio()

# --- Pedir minutos ---
minutos = int(input("¿Cuántos minutos? "))
segundos_totales = minutos * 60

# --- Iniciar cuenta atrás ---
cuenta_atras(segundos_totales)

root.mainloop()
