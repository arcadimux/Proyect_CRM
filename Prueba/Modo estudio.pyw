import os
import time
import subprocess
import tkinter as tk
from tracemalloc import stop

ruta_vlc = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
ruta_audio = r"D:\Users\jjosh\OneDrive\Escritorio\Coding\Proyectos Python\Prueba\Medios\Audio\genius.mp3"
#Función para reproducir el audio

def play_audio():
    subprocess.Popen([ruta_vlc, "--qt-start-minimized", ruta_audio])

#Título de la ventana
root = tk.Tk()
root.title("Modo estudio")
root.geometry("400x300")
tag = tk.Label(root, text="Modo estudio", fg="purple", font=("Calibri Light", 24))
tag.pack()

#Inserta el tiempo en formato 00:00
entrada = tk.Entry(root, font=("Calibri Light", 14))
entrada.insert(0, "01:00")
entrada.pack(pady=20)

#Temporizador
counter = tk.Label(root, text="", font=("Calibri Light", 14))
counter.pack(pady=20)

def start_timer():
    minutos = entrada.get()
    a = ""
    b = ""
    symbol = ""
    for caracter in minutos:
        if caracter.isdigit():
            if symbol == "":
                a += caracter
            else:
                b += caracter
        else:
            symbol = caracter
    
    if symbol == ":":
        horas_segundos = int(a) * 3600
        minutos_segundos = int(b) * 60
        segundos_totales = horas_segundos + minutos_segundos
        play_audio()
        countdown(segundos_totales)
        
def countdown(i):        
    if i >= 0:
        minutos_restantes = i // 60
        segundos_restantes = i % 60
        counter.config(text=f"{minutos_restantes:02d}:{segundos_restantes:02d}")
        root.after(1000, countdown, i - 1)
    else:
        counter.config(text="¡Tiempo!")
        os.system('taskkill /f /im vlc.exe')

boton_iniciar = tk.Button(root, text="Iniciar", command=start_timer, font=("Calibri Light", 14))
boton_iniciar.pack(pady=20)

boton_detener = tk.Button(root, text="Detener", command=lambda: os.system('taskkill /f /im vlc.exe'), font=("Calibri Light", 14))
boton_detener.pack(pady=10)

root.mainloop()
