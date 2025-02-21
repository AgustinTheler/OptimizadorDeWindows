from cryptography.fernet import Fernet
import base64
import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser
import subprocess
import psutil
import shutil
import time
import wmi
import win32com.client
import win32api
import win32con

def resource_path(relative_path):
    """ Obtener la ruta absoluta al recurso """
    try:
        # PyInstaller crea un directorio temporal y almacena la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def decrypt_and_run():
    try:
        # Lee la clave del archivo usando resource_path
        with open(resource_path('key.txt'), 'rb') as file:
            key = file.read()
        
        # Lee el código encriptado usando resource_path
        with open(resource_path('encrypted_code.txt'), 'rb') as file:
            encrypted_data = file.read()
        
        # Crear el objeto Fernet con la clave
        cipher_suite = Fernet(key)
        
        # Desencriptar el código
        decrypted_code = cipher_suite.decrypt(encrypted_data)
        
        # Crear la ventana principal primero
        root = tk.Tk()
        
        # Crear un namespace local para la ejecución con todas las dependencias
        namespace = {
            'tk': tk,
            'ttk': ttk,
            'messagebox': messagebox,
            'os': os,
            'sys': sys,
            'webbrowser': webbrowser,
            'subprocess': subprocess,
            'psutil': psutil,
            'shutil': shutil,
            'time': time,
            'wmi': wmi,
            'win32com': win32com,
            'win32api': win32api,
            'win32con': win32con,
            'Tk': tk.Tk,
            'Label': tk.Label,
            'Frame': tk.Frame,
            'Button': tk.Button,
            'Toplevel': tk.Toplevel,
            'BooleanVar': tk.BooleanVar,
            'Canvas': tk.Canvas,
            'path': os.path,
            'environ': os.environ,
            'root': root  # Agregamos root al namespace
        }
        
        # Ejecutar el código desencriptado con el namespace
        exec(decrypted_code, namespace)
        
        # Crear la instancia de WindowsOptimizer
        app = namespace['WindowsOptimizer'](root)
        
        # Iniciar el loop principal
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo iniciar la aplicación: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    decrypt_and_run() 