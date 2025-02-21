import tkinter as tk
from tkinter import ttk, messagebox
import os
import shutil
import winreg
import subprocess
import tempfile
import psutil

class WindowsOptimizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Optimizador de Windows 10")
        self.root.geometry("600x400")
        
        # Crear pestañas
        self.tab_control = ttk.Notebook(root)
        
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab3 = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.tab1, text='Limpieza')
        self.tab_control.add(self.tab2, text='Optimización')
        self.tab_control.add(self.tab3, text='Red')
        
        self.tab_control.pack(expand=1, fill="both")
        
        self.setup_cleanup_tab()
        self.setup_optimization_tab()
        self.setup_network_tab()

    def setup_cleanup_tab(self):
        # Botones para limpieza
        ttk.Button(self.tab1, text="Limpiar archivos temporales", 
                  command=self.clean_temp_files).pack(pady=10)
        ttk.Button(self.tab1, text="Limpiar papelera de reciclaje", 
                  command=self.clean_recycle_bin).pack(pady=10)
        ttk.Button(self.tab1, text="Limpiar caché DNS", 
                  command=self.clean_dns_cache).pack(pady=10)

    def setup_optimization_tab(self):
        # Botones para optimización
        ttk.Button(self.tab2, text="Desactivar servicios innecesarios", 
                  command=self.disable_services).pack(pady=10)
        ttk.Button(self.tab2, text="Optimizar rendimiento", 
                  command=self.optimize_performance).pack(pady=10)
        ttk.Button(self.tab2, text="Desfragmentar disco", 
                  command=self.defrag_disk).pack(pady=10)

    def setup_network_tab(self):
        # Botones para red
        ttk.Button(self.tab3, text="Optimizar DNS", 
                  command=self.optimize_dns).pack(pady=10)
        ttk.Button(self.tab3, text="Resetear configuración de red", 
                  command=self.reset_network).pack(pady=10)
        ttk.Button(self.tab3, text="Mostrar información de red", 
                  command=self.show_network_info).pack(pady=10)

    def clean_temp_files(self):
        try:
            temp = tempfile.gettempdir()
            files_removed = 0
            for filename in os.listdir(temp):
                file_path = os.path.join(temp, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                    files_removed += 1
                except:
                    continue
            messagebox.showinfo("Éxito", f"Se eliminaron {files_removed} archivos temporales")
        except:
            messagebox.showerror("Error", "No se pudieron eliminar los archivos temporales")

    def clean_recycle_bin(self):
        try:
            subprocess.run('rd /s /q C:\\$Recycle.Bin', shell=True)
            messagebox.showinfo("Éxito", "Papelera de reciclaje vaciada")
        except:
            messagebox.showerror("Error", "No se pudo vaciar la papelera")

    def clean_dns_cache(self):
        try:
            subprocess.run('ipconfig /flushdns', shell=True)
            messagebox.showinfo("Éxito", "Caché DNS limpiada")
        except:
            messagebox.showerror("Error", "No se pudo limpiar el caché DNS")

    def disable_services(self):
        services_to_disable = [
            "DiagTrack",  # Telemetría de Windows
            "dmwappushservice",  # WAP Push Message Routing
            "Remote Registry"  # Registro remoto
        ]
        
        for service in services_to_disable:
            try:
                subprocess.run(f'sc config "{service}" start=disabled', shell=True)
                subprocess.run(f'net stop "{service}"', shell=True)
            except:
                continue
        messagebox.showinfo("Éxito", "Servicios innecesarios desactivados")

    def optimize_performance(self):
        try:
            # Desactivar efectos visuales
            subprocess.run('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 2 /f', shell=True)
            messagebox.showinfo("Éxito", "Rendimiento optimizado")
        except:
            messagebox.showerror("Error", "No se pudo optimizar el rendimiento")

    def defrag_disk(self):
        try:
            subprocess.run('defrag C: /U /V', shell=True)
            messagebox.showinfo("Éxito", "Desfragmentación iniciada")
        except:
            messagebox.showerror("Error", "No se pudo iniciar la desfragmentación")

    def optimize_dns(self):
        dns_servers = [
            "8.8.8.8",  # Google DNS
            "1.1.1.1"   # Cloudflare DNS
        ]
        
        try:
            for dns in dns_servers:
                subprocess.run(f'netsh interface ip add dns "Ethernet" {dns}', shell=True)
            messagebox.showinfo("Éxito", "DNS optimizados")
        except:
            messagebox.showerror("Error", "No se pudieron optimizar los DNS")

    def reset_network(self):
        try:
            commands = [
                'ipconfig /release',
                'ipconfig /renew',
                'ipconfig /flushdns',
                'netsh winsock reset'
            ]
            
            for cmd in commands:
                subprocess.run(cmd, shell=True)
            messagebox.showinfo("Éxito", "Configuración de red reseteada")
        except:
            messagebox.showerror("Error", "No se pudo resetear la configuración de red")

    def show_network_info(self):
        try:
            result = subprocess.run('ipconfig /all', shell=True, capture_output=True, text=True)
            messagebox.showinfo("Información de red", result.stdout)
        except:
            messagebox.showerror("Error", "No se pudo obtener la información de red")

if __name__ == "__main__":
    root = tk.Tk()
    app = WindowsOptimizer(root)
    root.mainloop() 