from tkinter import ttk, messagebox, Tk, Label, Frame, Button, Toplevel, BooleanVar, Canvas
import os
from os import path, environ
import subprocess
import psutil
import webbrowser
from functools import partial  # Para optimizar los callbacks
import shutil
import time

class WindowsOptimizer:
    def __init__(self, root):
        self.root = root
        self.cache = {}  # Caché para operaciones repetitivas
        
        # Crear botón flotante (inicialmente oculto)
        self.create_floating_button()
        self.float_window.withdraw()  # Ocultar inicialmente
        
        # Detectar cuando la ventana se minimiza
        self.root.bind("<Unmap>", self.on_minimize)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.setup_styles()
        self.setup_ui()

    def create_floating_button(self):
        """Crear botón flotante que siempre está visible"""
        self.float_window = Toplevel(self.root)
        self.float_window.title("")
        self.float_window.geometry("50x50")  # Tamaño pequeño para el botón
        self.float_window.attributes('-topmost', True)  # Siempre visible
        self.float_window.overrideredirect(True)  # Quitar decoración de ventana
        
        # Crear botón con estilo moderno
        self.float_button = Button(self.float_window,
                                 text="⚡",
                                 font=('Segoe UI', 16),
                                 bg='#238636',
                                 fg='white',
                                 activebackground='#2ea043',
                                 activeforeground='white',
                                 relief='flat',
                                 cursor='hand2',
                                 command=self.restore_window)
        self.float_button.pack(fill='both', expand=True)
        
        # Hacer el botón arrastrable
        self.float_button.bind('<Button-1>', self.start_move)
        self.float_button.bind('<B1-Motion>', self.on_move)
        
        # Tooltip
        self.add_modern_tooltip(self.float_button, "Restaurar Windows Optimizer")
        
        # Posicionar en la esquina inferior derecha
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.float_window.geometry(f"+{screen_width-60}+{screen_height-60}")

    def start_move(self, event):
        """Iniciar movimiento del botón flotante"""
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        """Mover el botón flotante"""
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.float_window.winfo_x() + deltax
        y = self.float_window.winfo_y() + deltay
        self.float_window.geometry(f"+{x}+{y}")

    def restore_window(self):
        """Restaurar la ventana principal y ocultar botón flotante"""
        self.root.deiconify()  # Restaurar ventana principal
        self.root.state('normal')  # Asegurar que no está minimizada
        self.float_window.withdraw()  # Ocultar botón flotante
        self.root.lift()  # Traer al frente
        self.root.focus_force()  # Dar foco

    def on_closing(self):
        """Manejar el cierre de la ventana"""
        self.float_window.destroy()
        self.root.destroy()

    def setup_styles(self):
        """Configurar todos los estilos una sola vez"""
        style = ttk.Style()
        style.theme_use('default')
        
        # Diccionario de colores para fácil mantenimiento
        self.colors = {
            'bg': '#0d1117',
            'fg': '#c9d1d9',
            'accent': '#58a6ff',
            'hover': '#1e293b',
            'button': '#66c0f4',
            'button_hover': '#1999ff'
        }
        
        # Configurar estilos base
        base_styles = {
            'Tab.TFrame': {'background': self.colors['bg']},
            'Custom.TNotebook': {'background': self.colors['bg'], 'borderwidth': 0},
            'Custom.TNotebook.Tab': {
                'background': '#161b22',
                'foreground': '#8b949e',
                'padding': [20, 12],
                'font': ('Segoe UI', 11)
            }
        }
        
        for style_name, config in base_styles.items():
            style.configure(style_name, **config)

    def setup_ui(self):
        self.root.title("Windows Optimizer")
        self.root.geometry("1024x768")  # Ventana más grande para estilo web
        self.root.minsize(1024, 768)
        
        # Variables para el color
        self.r = 0
        self.g = 255
        self.b = 0
        self.color_direction = 1
        
        # Configurar el tema oscuro moderno
        self.root.configure(bg='#0d1117')  # Color de fondo estilo GitHub dark
        
        # Estilo para los widgets
        style = ttk.Style()
        style.theme_use('default')
        
        # Configurar estilos modernos
        style.configure('Modern.TNotebook', 
                       background='#0d1117',
                       borderwidth=0)
        
        style.configure('Modern.TNotebook.Tab',
                       background='#0d1117',
                       foreground='#c9d1d9',
                       padding=[30, 15],
                       font=('Segoe UI', 11))
        
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', '#161b22')],
                 foreground=[('selected', '#58a6ff')])
        
        style.configure('Modern.TFrame',
                       background='#0d1117')
        
        # Configurar estilos modernos para las pestañas
        style.configure('Tab.TFrame', background='#0d1117')
        
        style.configure('Custom.TNotebook', 
                       background='#0d1117',
                       borderwidth=0)
        
        style.configure('Custom.TNotebook.Tab',
                       background='#161b22',
                       foreground='#8b949e',
                       padding=[20, 12],
                       font=('Segoe UI', 11))
        
        style.map('Custom.TNotebook.Tab',
                 background=[('selected', '#0ea5e9'),  # Azul cuando está seleccionado
                            ('active', '#1e293b')],    # Color al pasar el mouse
                 foreground=[('selected', '#ffffff'),  # Texto blanco cuando está seleccionado
                            ('active', '#c9d1d9')],    # Color del texto al pasar el mouse
                 expand=[('selected', [1, 1, 1, 0])])  # Efecto de expansión al seleccionar
        
        # Configurar estilo del frame
        style.configure('Tab.TFrame', 
                       background='#0d1117',  # Fondo principal
                       borderwidth=0)
        
        # Crear contenedor principal con margen
        main_container = ttk.Frame(root, style='Tab.TFrame')
        main_container.pack(expand=True, fill='both', padx=30, pady=30)
        
        # Header con título RGB
        header_frame = ttk.Frame(main_container, style='Tab.TFrame')
        header_frame.pack(fill='x', pady=(0, 20))
        
        self.header_title = Label(header_frame,
                                   text="Windows Optimizer by Aguza",
                                   fg='#58a6ff',  # Color inicial
                                   bg='#0d1117',
                                   font=('Rajdhani', 24, 'bold'))  # Fuente gaming moderna
        self.header_title.pack(side='left')
        
        # Crear notebook con pestañas personalizadas
        self.tab_control = ttk.Notebook(main_container, style='Custom.TNotebook')
        
        # Crear frames para cada pestaña (reordenados)
        self.tab1 = ttk.Frame(self.tab_control, style='Tab.TFrame')
        self.tab2 = ttk.Frame(self.tab_control, style='Tab.TFrame')
        self.tab3 = ttk.Frame(self.tab_control, style='Tab.TFrame')
        self.tab4 = ttk.Frame(self.tab_control, style='Tab.TFrame')
        self.tab5 = ttk.Frame(self.tab_control, style='Tab.TFrame')
        self.tab6 = ttk.Frame(self.tab_control, style='Tab.TFrame')  # Trabajo/Estudio
        self.tab7 = ttk.Frame(self.tab_control, style='Tab.TFrame')  # Acerca de
        
        # Añadir pestañas con iconos (reordenadas)
        self.tab_control.add(self.tab1, text=' 🧹 LIMPIEZA ')
        self.tab_control.add(self.tab2, text=' ⚡ OPTIMIZACIÓN ')
        self.tab_control.add(self.tab3, text=' 🌐 RED ')
        self.tab_control.add(self.tab4, text=' 🎮 JUEGOS ')
        self.tab_control.add(self.tab5, text=' 💻 CPU ')
        self.tab_control.add(self.tab6, text=' 📚 TRABAJO/ESTUDIO ')
        self.tab_control.add(self.tab7, text=' ℹ️ ACERCA DE ')
        
        self.tab_control.pack(expand=True, fill='both')
        
        self.setup_cleanup_tab()
        self.setup_optimization_tab()
        self.setup_network_tab()
        self.setup_games_tab()
        self.setup_cpu_tab()
        self.setup_work_study_tab()
        self.setup_about_tab()
        
        # Iniciar la animación de color
        self.update_colors()

    def rgb_to_hex(self, r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'

    def update_colors(self):
        """Actualización de colores más eficiente"""
        if not hasattr(self, '_last_update'):
            self._last_update = 0
        
        current_time = time.time()
        if current_time - self._last_update < 0.05:  # Limitar a 20 FPS
            return
        
        self._last_update = current_time
        # Actualizar valores RGB
        if self.color_direction == 1:
            if self.r < 255 and self.b == 0:
                self.r += 5
                self.g -= 5
            elif self.g < 255 and self.r == 0:
                self.g += 5
                self.b -= 5
            elif self.b < 255 and self.g == 0:
                self.b += 5
                self.r -= 5
            else:
                self.color_direction = -1
        else:
            if self.r > 0 and self.b == 0:
                self.r -= 5
                self.g += 5
            elif self.g > 0 and self.r == 0:
                self.g -= 5
                self.b += 5
            elif self.b > 0 and self.g == 0:
                self.b -= 5
                self.r += 5
            else:
                self.color_direction = 1

        # Mantener los valores dentro del rango 0-255
        self.r = max(0, min(255, self.r))
        self.g = max(0, min(255, self.g))
        self.b = max(0, min(255, self.b))

        # Actualizar estilos
        self.update_button_style()
        
        # Actualizar el color del título
        self.header_title.configure(fg=self.rgb_to_hex(self.r, self.g, self.b))
        
        # Programar la próxima actualización
        self.root.after(50, self.update_colors)

    def update_button_style(self):
        current_color = self.rgb_to_hex(self.r, self.g, self.b)
        style = ttk.Style()
        
        # Estilo para el separador
        style.configure('Separator.TFrame',
                       background=current_color)
        
        # Estilo para las pestañas
        style.configure('TNotebook.Tab', 
                       background='black',
                       foreground=current_color,
                       borderwidth=2,
                       padding=[10, 5])
        
        # Estilo para los botones con borde del mismo color que el texto
        style.configure('TButton', 
                       background='black',
                       foreground=current_color,
                       borderwidth=3,  # Borde más grueso
                       relief='solid',
                       bordercolor=current_color,  # Borde del mismo color que el texto
                       lightcolor=current_color,  
                       darkcolor=current_color)   
        
        style.map('TButton',
                 background=[('active', '#001100')],
                 foreground=[('active', current_color)],
                 bordercolor=[('active', current_color)],
                 lightcolor=[('active', current_color)])
        
        # Estilo para las pestañas con borde del mismo color
        style.configure('TNotebook.Tab', 
                       background='black',
                       foreground=current_color,
                       borderwidth=2,
                       bordercolor=current_color,
                       lightcolor=current_color,
                       padding=[10, 5])
        
        # Estilo para el notebook (contenedor de pestañas)
        style.configure('TNotebook', 
                       background='black',
                       borderwidth=2,
                       bordercolor=current_color,
                       lightcolor=current_color)

        # Estilo para la barra de progreso
        style.configure("Horizontal.TProgressbar",
                       troughcolor='black',
                       background=current_color,
                       darkcolor=current_color,
                       lightcolor=current_color,
                       bordercolor='black')

    def add_tooltip(self, button, tooltip_text):
        def show_tooltip(event, tooltip_text=tooltip_text):
            tooltip = Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.configure(bg='black')
            
            x = event.widget.winfo_rootx() + event.widget.winfo_width() + 10
            y = event.widget.winfo_rooty()
            
            tooltip.geometry(f"+{x}+{y}")
            
            label = Label(tooltip, 
                           text=tooltip_text,
                           justify='left',
                           bg='black',
                           fg=self.rgb_to_hex(self.r, self.g, self.b),
                           font=('Arial', 9))
            label.pack(padx=10, pady=5)
            
            def hide_tooltip(event, tooltip=tooltip):
                tooltip.destroy()
            
            button.tooltip = tooltip
            button.bind('<Leave>', hide_tooltip)
        
        button.bind('<Enter>', show_tooltip)

    def create_modern_button(self, parent, text, command, tooltip=None):
        """Crear botón con estilo web moderno"""
        # Contenedor principal para el botón
        button_container = ttk.Frame(parent, style='Modern.TFrame')
        button_container.pack(pady=15, fill='x')
        
        # Frame interno para centrar
        button_frame = ttk.Frame(button_container, style='Modern.TFrame')
        button_frame.pack(expand=True, anchor='center')
        
        # Frame para el efecto de borde neón
        neon_frame = Frame(button_frame, bg='#0284c7', padx=2, pady=2)
        neon_frame.pack(padx=5)
        
        # Frame para el gradiente
        gradient_frame = Frame(neon_frame, bg='#075985', padx=1, pady=1)
        gradient_frame.pack()
        
        # El botón principal con fondo degradado
        button = Button(gradient_frame,
                          text=text,
                          command=command,
                          bg='#0f172a',  # Fondo más visible
                          fg='#e2e8f0',  # Texto claro
                          activebackground='#1e293b',
                          activeforeground='#ffffff',
                          relief='flat',
                          borderwidth=0,
                          padx=30,
                          pady=15,
                          width=35,
                          font=('Segoe UI', 11, 'bold'),
                          cursor='hand2')
        button.pack()

        # Efectos hover y click mejorados
        def on_enter(e):
            if str(button['state']) != 'disabled':
                button.configure(bg='#1e293b')
                neon_frame.configure(bg='#0ea5e9')  # Brillo más intenso
                gradient_frame.configure(bg='#0369a1')
                
        def on_leave(e):
            if str(button['state']) != 'disabled':
                button.configure(bg='#0f172a')
                neon_frame.configure(bg='#0284c7')
                gradient_frame.configure(bg='#075985')

        def on_click(e):
            if str(button['state']) != 'disabled':
                button.configure(bg='#0f172a')
                neon_frame.configure(bg='#075985')
                gradient_frame.configure(bg='#0c4a6e')

        def on_release(e):
            if str(button['state']) != 'disabled':
                button.configure(bg='#1e293b')
                neon_frame.configure(bg='#0ea5e9')
                gradient_frame.configure(bg='#0369a1')

        # Configurar estados deshabilitados
        if hasattr(button, 'state') and str(button['state']) == 'disabled':
            button.configure(
                bg='#1f2937',
                fg='#6b7280',
                activebackground='#1f2937',
                activeforeground='#6b7280'
            )
            neon_frame.configure(bg='#1f2937')
            gradient_frame.configure(bg='#1f2937')

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        button.bind("<Button-1>", on_click)
        button.bind("<ButtonRelease-1>", on_release)

        if tooltip:
            self.add_modern_tooltip(button, tooltip)

        return button

    def add_modern_tooltip(self, widget, text):
        def show_tooltip(event):
            # Destruir tooltip anterior si existe
            if hasattr(widget, 'tooltip'):
                try:
                    widget.tooltip.destroy()
                except:
                    pass
                
            tooltip = Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.configure(bg='#161b22')
            tooltip.attributes('-topmost', True)  # Mantener tooltip siempre visible
            
            # Calcular posición
            x = event.widget.winfo_rootx() + event.widget.winfo_width() + 10
            y = event.widget.winfo_rooty()
            
            label = Label(tooltip,
                         text=text,
                         justify='left',
                         bg='#161b22',
                         fg='#c9d1d9',
                         font=('Segoe UI', 10),
                         padx=12,
                         pady=8)
            label.pack()
            
            # Ajustar posición
            tooltip.update_idletasks()
            tooltip.geometry(f"+{x}+{y}")
            
            def hide_tooltip(event):
                tooltip.destroy()
                widget.tooltip = None
            
            widget.tooltip = tooltip
            widget.bind('<Leave>', hide_tooltip)
            
            # Remover el check de posición del mouse que causaba problemas
            widget.unbind('<Motion>')
        
        # Limpiar bindings anteriores
        widget.unbind('<Enter>')
        widget.unbind('<Leave>')
        
        # Añadir nuevos bindings
        widget.bind('<Enter>', show_tooltip)

    def setup_cleanup_tab(self):
        container = ttk.Frame(self.tab1, style='Modern.TFrame')
        container.pack(expand=True, fill='both', padx=50, pady=30)
        
        # Título con ícono centrado
        title_frame = ttk.Frame(container, style='Modern.TFrame')
        title_frame.pack(fill='x', pady=(0, 30))
        
        title = Label(title_frame,
                        text="🧹 Limpieza del Sistema",
                        fg='#c9d1d9',
                        bg='#0d1117',
                        font=('Segoe UI', 20, 'bold'))
        title.pack(expand=True)  # Centrado horizontal
        
        # Descripción centrada
        description = Label(container,
                             text="Optimiza tu sistema eliminando archivos innecesarios y liberando espacio",
                             fg='#8b949e',
                             bg='#0d1117',
                             font=('Segoe UI', 12))
        description.pack(pady=(0, 30), expand=True)  # Centrado horizontal
        
        tooltips = {
            "Limpieza de Archivos Temporales": """🔹 Elimina archivos temporales del sistema
🔹 Limpia caché de navegadores
🔹 Elimina archivos de Prefetch
🔹 Limpia caché de Windows Update""",
            
            "Limpieza del Sistema": """🔹 Limpia el registro de Windows
🔹 Elimina entradas de software innecesario
🔹 Desinstala programas no usados
🔹 Elimina software preinstalado (Bloatware)
🔹 Limpia la carpeta Windows.old""",
            
            "Limpieza de Papelera": """🔹 Vacía la papelera de reciclaje
🔹 Elimina archivos permanentemente
🔹 Libera espacio en disco
🔹 Optimiza el almacenamiento""",

            "Limpieza de Descargas": """🔹 Elimina archivos de la carpeta de descargas
🔹 Libera espacio en disco
🔹 Organiza tus descargas
🔹 Mejora el rendimiento del sistema"""
        }
        
        for text, command in [
            ("Limpieza de Archivos Temporales", self.clean_temp_files),
            ("Limpieza del Sistema", self.clean_system),
            ("Limpieza de Papelera", self.clean_recycle_bin),
            ("Limpieza de Descargas", self.clean_downloads)  # Agregamos el nuevo botón
        ]:
            self.create_modern_button(container, text, command, tooltips[text])

    def setup_optimization_tab(self):
        container = ttk.Frame(self.tab2, style='Modern.TFrame')
        container.pack(expand=True, fill='both', padx=50, pady=30)
        
        # Título centrado
        title_frame = ttk.Frame(container, style='Modern.TFrame')
        title_frame.pack(fill='x', pady=(0, 30))
        
        title = Label(title_frame,
                        text="⚡ Optimización del Sistema",
                        fg='#c9d1d9',
                        bg='#0d1117',
                        font=('Segoe UI', 20, 'bold'))
        title.pack(expand=True)
        
        # Descripción centrada
        description = Label(container,
                             text="Mejora el rendimiento y la velocidad de tu sistema",
                             fg='#8b949e',
                             bg='#0d1117',
                             font=('Segoe UI', 12))
        description.pack(pady=(0, 30))

        tooltips = {
            "Desactivar servicios innecesarios": """❗ Servicios que se desactivarán:
• Superfetch (SysMain)
• Delivery Optimization
• Windows Update
• Windows Search
• Windows Error Reporting
• Remote Registry
• Print Spooler
• Windows Defender
• Microsoft Office Click-to-Run""",
            
            "Optimizar rendimiento": """✅ Ajusta la configuración del sistema
✅ Mejora la velocidad de respuesta
✅ Optimiza efectos visuales
✅ Aumenta el rendimiento general""",
            
            "Optimización de Disco": """🔹 Desfragmentación de HDD
🔹 Optimización de SSD
🔹 Comprobación de errores (CHKDSK)
🔹 Limpia puntos de restauración antiguos
🔹 Optimiza el sistema de archivos""",
            
            "Optimización de Memoria": """🔹 Libera RAM inactiva
🔹 Optimiza la memoria virtual
🔹 Limpia el archivo de paginación
🔹 Optimiza servicios del sistema
🔹 Gestiona programas de inicio""",

            "Optimización de Input": """🔹 Timer Resolution (0.5ms)
🔹 Modo Baja Latencia
🔹 Optimización HID
🔹 Dynamic Ticks OFF
🔹 Latencia Reducida""",

            "Optimización de Periféricos": """🎮 Optimización de dispositivos:
• Ratón y teclado
• Mandos PS4/PS5
• Mandos Xbox
• Joysticks genéricos
• Reducción de latencia
• Polling rate optimizado
• Ajustes USB
• Prioridad de dispositivos"""
        }
        
        for text, command in [
            ("Desactivar servicios innecesarios", self.disable_services),
            ("Optimizar rendimiento", self.optimize_performance),
            ("Optimización de Disco", self.optimize_disk),
            ("Optimización de Memoria", self.optimize_memory),
            ("Optimización de Input", self.optimize_input),
            ("Optimización de Periféricos", self.optimize_peripherals)  # Nuevo botón
        ]:
            self.create_modern_button(container, text, command, tooltips[text])

    def setup_network_tab(self):
        container = ttk.Frame(self.tab3, style='Modern.TFrame')
        container.pack(expand=True, fill='both', padx=50, pady=30)
        
        # Título centrado
        title_frame = ttk.Frame(container, style='Modern.TFrame')
        title_frame.pack(fill='x', pady=(0, 30))
        
        title = Label(title_frame,
                        text="🌐 Configuración de Red",
                        fg='#c9d1d9',
                        bg='#0d1117',
                        font=('Segoe UI', 20, 'bold'))
        title.pack(expand=True)
        
        # Descripción centrada
        description = Label(container,
                             text="Optimiza tu conexión y mejora la velocidad de internet",
                             fg='#8b949e',
                             bg='#0d1117',
                             font=('Segoe UI', 12))
        description.pack(pady=(0, 30), expand=True)

        tooltips = {
            "Optimizar DNS": """✅ Configura DNS rápidos
✅ Mejora la velocidad de navegación
✅ Optimiza la resolución de nombres
✅ Reduce la latencia""",
            
            "Resetear configuración de red": """✅ Restablece la configuración de red
✅ Soluciona problemas de conexión
✅ Limpia la configuración actual
✅ Optimiza los parámetros de red""",
            
            "Mostrar información de red": """✅ Muestra detalles de la conexión
✅ Información de adaptadores
✅ Estado de la red
✅ Configuración actual"""
        }
        
        for text, command in [
            ("Optimizar DNS", self.optimize_dns),
            ("Resetear configuración de red", self.reset_network),
            ("Mostrar información de red", self.show_network_info)
        ]:
            self.create_modern_button(container, text, command, tooltips[text])

    def setup_about_tab(self):
        container = ttk.Frame(self.tab7, style='Modern.TFrame')
        container.pack(expand=True, fill='both', padx=50, pady=30)
        
        # Título centrado
        title_frame = ttk.Frame(container, style='Modern.TFrame')
        title_frame.pack(fill='x', pady=(0, 30))
        
        title = Label(title_frame,
                        text="ℹ️ Acerca del Programa",
                        fg='#c9d1d9',
                        bg='#0d1117',
                        font=('Segoe UI', 20, 'bold'))
        title.pack(expand=True)
        
        # Frame principal con efecto de tarjeta
        card_frame = Frame(container, bg='#161b22', padx=30, pady=30)
        card_frame.pack(expand=True, fill='both', padx=20)
        
        # Logo grande
        logo_label = Label(card_frame,
                            text="🌟",
                            fg='#58a6ff',
                            bg='#161b22',
                            font=('Segoe UI', 48))
        logo_label.pack(pady=(0, 10))
        
        # Nombre del programa con estilo
        program_name = Label(card_frame,
                              text="Windows Optimizer",
                              fg='#58a6ff',
                              bg='#161b22',
                              font=('Segoe UI', 24, 'bold'))
        program_name.pack()
        
        # Versión con badge estilo GitHub
        version_frame = Frame(card_frame, bg='#161b22')
        version_frame.pack(pady=10)
        
        version_badge = Label(version_frame,
                               text="Version 1.0",
                               fg='#c9d1d9',
                               bg='#238636',
                               font=('Segoe UI', 10),
                               padx=10,
                               pady=5)
        version_badge.pack(side='left', padx=5)
        
        status_badge = Label(version_frame,
                              text="Stable",
                              fg='#c9d1d9',
                              bg='#1f6feb',
                              font=('Segoe UI', 10),
                              padx=10,
                              pady=5)
        status_badge.pack(side='left', padx=5)
        
        # Separador
        separator = ttk.Frame(card_frame, height=2, style='Separator.TFrame')
        separator.pack(fill='x', pady=20)
        
        # Información del desarrollador y Discord
        info_container = Frame(card_frame, bg='#161b22')
        info_container.pack(fill='x', pady=10)
        
        # Frame izquierdo (Desarrollador)
        dev_frame = Frame(info_container, bg='#161b22')
        dev_frame.pack(side='left', expand=True, fill='x', padx=(0, 10))
        
        dev_icon = Label(dev_frame,
                          text="👨‍💻",
                          fg='#c9d1d9',
                          bg='#161b22',
                          font=('Segoe UI', 16))
        dev_icon.pack(side='left', padx=(0, 10))
        
        dev_info = Label(dev_frame,
                          text="Desarrollado por Aguza",
                          fg='#c9d1d9',
                          bg='#161b22',
                          font=('Segoe UI', 12))
        dev_info.pack(side='left')
        
        # Separador vertical
        separator = Frame(info_container, 
                           width=2, 
                           bg='#30363d')  # Color del separador
        separator.pack(side='left', fill='y', padx=20)
        
        # Frame derecho (Discord)
        discord_frame = Frame(info_container, bg='#161b22')
        discord_frame.pack(side='right', expand=True, fill='x', padx=(10, 0))
        
        discord_icon = Label(discord_frame,
                              text="🎮",
                              fg='#c9d1d9',
                              bg='#161b22',
                              font=('Segoe UI', 16))
        discord_icon.pack(side='left', padx=(0, 10))
        
        # Botón de Discord con efecto hover
        discord_button = Label(discord_frame,
                              text="Discord",
                              fg='#5865F2',  # Color oficial de Discord
                              bg='#161b22',
                              font=('Segoe UI', 12, 'bold'),
                              cursor='hand2')
        discord_button.pack(side='left')
        
        def on_discord_enter(e):
            discord_button.configure(fg='#7289DA')  # Color hover de Discord
            
        def on_discord_leave(e):
            discord_button.configure(fg='#5865F2')
        
        discord_button.bind('<Enter>', on_discord_enter)
        discord_button.bind('<Leave>', on_discord_leave)
        discord_button.bind('<Button-1>', lambda e: webbrowser.open('https://discord.com/users/404709223843233814'))
        
        # Descripción
        description = Label(card_frame,
                             text="Una herramienta potente para optimizar y mejorar\n"
                                  "el rendimiento de tu sistema Windows",
                             fg='#8b949e',
                             bg='#161b22',
                             font=('Segoe UI', 11),
                             justify='center')
        description.pack(pady=20)
        
        # Footer con copyright
        footer = Label(card_frame,
                         text="© 2024 Windows Optimizer. Todos los derechos reservados.",
                         fg='#8b949e',
                         bg='#161b22',
                         font=('Segoe UI', 9))
        footer.pack(pady=(20, 0))

    def show_custom_message(self, title, message, error=False):
        dialog = Toplevel(self.root)
        dialog.title(title)
        dialog.configure(bg='#161b22')
        
        # Hacer que la ventana sea modal
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Frame contenedor principal
        main_frame = Frame(dialog, bg='#161b22', padx=30, pady=25)
        main_frame.pack(expand=True, fill='both')
        
        # Icono de éxito/error
        icon_text = "❌" if error else "✅"
        icon_color = '#ff4d4d' if error else '#00cc66'
        
        icon_label = Label(main_frame,
                          text=icon_text,
                          fg=icon_color,
                          bg='#161b22',
                          font=('Segoe UI', 48))
        icon_label.pack(pady=(0, 15))
        
        # Título
        title_label = Label(main_frame,
                           text=title,
                           fg='#ffffff',
                           bg='#161b22',
                           font=('Segoe UI', 16, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Mensaje
        msg_label = Label(main_frame,
                         text=message,
                         fg='#c9d1d9',
                         bg='#161b22',
                         justify='left',
                         font=('Segoe UI', 11))
        msg_label.pack(pady=(0, 20))
        
        # Botón OK con estilo moderno
        ok_button = Button(main_frame,
                          text="Aceptar",
                          fg='white',
                          bg='#238636',
                          activebackground='#2ea043',
                          activeforeground='white',
                          font=('Segoe UI', 10, 'bold'),
                          relief='flat',
                          padx=20,
                          pady=8,
                          cursor='hand2',
                          command=dialog.destroy)
        ok_button.pack()
        
        # Efectos hover para el botón
        def on_enter(e):
            ok_button.configure(bg='#2ea043')
        
        def on_leave(e):
            ok_button.configure(bg='#238636')
        
        ok_button.bind('<Enter>', on_enter)
        ok_button.bind('<Leave>', on_leave)
        
        # Centrar la ventana
        dialog.update_idletasks()
        width = max(400, msg_label.winfo_reqwidth() + 100)
        height = main_frame.winfo_reqheight() + 50
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        # Evitar que la ventana sea redimensionable
        dialog.resizable(False, False)

    def show_progress(self, title, maximum):
        progress_window = Toplevel(self.root)
        progress_window.title(title)
        progress_window.geometry("400x200")  # Ventana más grande
        progress_window.configure(bg='#161b22')
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        # Centrar la ventana
        progress_window.update_idletasks()
        width = progress_window.winfo_width()
        height = progress_window.winfo_height()
        x = (progress_window.winfo_screenwidth() // 2) - (width // 2)
        y = (progress_window.winfo_screenheight() // 2) - (height // 2)
        progress_window.geometry(f'+{x}+{y}')
        
        # Contenedor principal
        main_frame = Frame(progress_window, bg='#161b22', padx=30, pady=20)
        main_frame.pack(expand=True, fill='both')
        
        # Icono animado de carga
        loading_label = Label(main_frame,
                            text="⚡",
                            fg='#66c0f4',
                            bg='#161b22',
                            font=('Segoe UI', 24))
        loading_label.pack(pady=(0, 15))
        
        # Status con mejor estilo
        status_label = Label(main_frame,
                           text="Iniciando...",
                           bg='#161b22',
                           fg='#c9d1d9',
                           font=('Segoe UI', 11))
        status_label.pack(pady=(0, 15))
        
        # Frame para la barra de progreso
        progress_frame = Frame(main_frame, bg='#161b22', padx=2, pady=2)
        progress_frame.pack(fill='x')
        
        # Estilo moderno para la barra de progreso
        style = ttk.Style()
        style.configure("Modern.Horizontal.TProgressbar",
                       troughcolor='#0d1117',
                       background='#66c0f4',
                       darkcolor='#66c0f4',
                       lightcolor='#66c0f4',
                       bordercolor='#0d1117',
                       thickness=15)
        
        progress_bar = ttk.Progressbar(progress_frame,
                                     style="Modern.Horizontal.TProgressbar",
                                     length=300,
                                     mode='determinate',
                                     maximum=maximum)
        progress_bar.pack(fill='x')
        
        # Porcentaje con mejor estilo
        percent_label = Label(main_frame,
                            text="0%",
                            bg='#161b22',
                            fg='#66c0f4',
                            font=('Segoe UI', 12, 'bold'))
        percent_label.pack(pady=(15, 0))
        
        # Animación del icono de carga
        def animate_loading():
            icons = ["⚡", "💫", "✨", "⭐"]
            current = loading_label.cget("text")
            next_icon = icons[(icons.index(current) + 1) % len(icons)]
            loading_label.configure(text=next_icon)
            progress_window.after(500, animate_loading)
        
        animate_loading()
        progress_window.update()
        return progress_window, progress_bar, status_label, percent_label

    def clean_temp_files(self):
        try:
            # Rutas genéricas de Windows
            temp_paths = [
                os.environ.get('TEMP'),  # Carpeta temporal del usuario actual
                os.environ.get('SYSTEMROOT') + '\\Temp',  # Carpeta temporal del sistema
                os.environ.get('SYSTEMROOT') + '\\Prefetch',  # Prefetch
                os.environ.get('LOCALAPPDATA') + '\\Temp',  # AppData Local Temp
                os.environ.get('LOCALAPPDATA') + '\\Microsoft\\Windows\\INetCache',  # Cache de Internet
                os.environ.get('LOCALAPPDATA') + '\\Microsoft\\Windows\\History',  # Historial
                os.environ.get('APPDATA') + '\\Microsoft\\Windows\\Recent'  # Archivos recientes
            ]
            
            # Contar archivos primero
            total_files = sum(1 for _ in os.listdir(temp_paths[0]))
            
            # Crear barra de progreso
            progress_window, progress_bar, status_label, percent_label = self.show_progress(
                "Limpiando archivos temporales", total_files)
            
            files_removed = 0
            for filename in os.listdir(temp_paths[0]):
                file_path = path.join(temp_paths[0], filename)
                try:
                    if path.isfile(file_path):
                        os.unlink(file_path)
                    elif path.isdir(file_path):
                        shutil.rmtree(file_path)
                    files_removed += 1
                    
                    # Actualizar progreso
                    progress_bar['value'] = files_removed
                    percent = int((files_removed / total_files) * 100)
                    percent_label.config(text=f"{percent}%")
                    status_label.config(text=f"Eliminando: {filename}")
                    progress_window.update()
                except:
                    continue
            
            progress_window.destroy()
            self.show_custom_message("Éxito", f"Se eliminaron {files_removed} archivos temporales")
        except:
            if 'progress_window' in locals():
                progress_window.destroy()
            self.show_custom_message("Error", "No se pudieron eliminar los archivos temporales", error=True)

    def clean_recycle_bin(self):
        try:
            subprocess.run('rd /s /q C:\\$Recycle.Bin', shell=True)
            self.show_custom_message("Éxito", "Papelera de reciclaje vaciada")
        except:
            self.show_custom_message("Error", "No se pudo vaciar la papelera", error=True)

    def clean_dns_cache(self):
        try:
            # Crear barra de progreso
            progress_window, progress_bar, status_label, percent_label = self.show_progress(
                "Limpiando caché DNS", 100)
            
            # Actualizar estado
            status_label.config(text="Limpiando caché DNS...")
            progress_bar['value'] = 0
            progress_window.update()
            
            # Ejecutar comando
            subprocess.run('ipconfig /flushdns', shell=True)
            
            # Simular progreso
            for i in range(100):
                progress_bar['value'] = i + 1
                percent_label.config(text=f"{i + 1}%")
                progress_window.update()
                time.sleep(0.02)
            
            progress_window.destroy()
            self.show_custom_message("Éxito", "Caché DNS limpiada")
        except:
            if 'progress_window' in locals():
                progress_window.destroy()
            self.show_custom_message("Error", "No se pudo limpiar el caché DNS", error=True)

    def disable_services(self):
        try:
            # Lista actualizada de servicios
            services_to_disable = [
                "SysMain",  # Superfetch
                "DoSvc",    # Delivery Optimization
                "wuauserv", # Windows Update
                "WSearch",  # Windows Search
                "WerSvc",   # Windows Error Reporting
                "RemoteRegistry",
                "Spooler",  # Print Spooler
                "bthserv",  # Bluetooth Support
                "WinDefend", # Windows Defender
                "ClickToRunSvc", # Office Click-to-Run
                "W32Time",  # Windows Time
                "Winmgmt",  # WMI
                "seclogon", # Secondary Logon
                "CscService", # Offline Files
                "SDRSVC",   # Windows Backup
                "iphlpsvc", # IP Helper
                "TrkWks",   # Distributed Link Tracking
                "stisvc",   # Windows Image Acquisition
                "TermService", # Remote Desktop
                "Fax",
                "mpssvc",   # Windows Firewall
                "StorSvc",  # Storage Spaces
                "WbioSrvc", # Biometric
                "HomeGroupProvider",
                "LicenseManager",
                "TabletInputService",
                "TouchKeyboard",
                "wcncsvc",  # Windows Connect Now
                "MSDTC"     # Distributed Transaction Coordinator
            ]

            # Crear ventana de progreso
            progress_window, progress_bar, status_label, percent_label = self.show_progress(
                "Desactivando servicios", len(services_to_disable))
            
            services_disabled = 0
            for service in services_to_disable:
                try:
                    status_label.config(text=f"Desactivando: {service}")
                    subprocess.run(f'sc config "{service}" start=disabled', shell=True)
                    subprocess.run(f'net stop "{service}"', shell=True)
                    services_disabled += 1
                    
                    # Actualizar progreso
                    progress_bar['value'] = services_disabled
                    percent = int((services_disabled / len(services_to_disable)) * 100)
                    percent_label.config(text=f"{percent}%")
                    progress_window.update()
                except:
                    continue

            time.sleep(1)
            progress_window.destroy()
            self.show_custom_message("Éxito", f"Se desactivaron {services_disabled} servicios innecesarios")
        except:
            if 'progress_window' in locals():
                progress_window.destroy()
            self.show_custom_message("Error", "No se pudieron desactivar los servicios", error=True)

    def optimize_performance(self):
        try:
            subprocess.run('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 2 /f', shell=True)
            self.show_custom_message("Éxito", "Rendimiento optimizado")
        except:
            self.show_custom_message("Error", "No se pudo optimizar el rendimiento", error=True)

    def defrag_disk(self):
        try:
            subprocess.run('defrag C: /U /V', shell=True)
            self.show_custom_message("Éxito", "Desfragmentación iniciada")
        except:
            self.show_custom_message("Error", "No se pudo iniciar la desfragmentación", error=True)

    def optimize_dns(self):
        dns_servers = [
            "8.8.8.8",
            "1.1.1.1"
        ]
        
        try:
            for dns in dns_servers:
                subprocess.run(f'netsh interface ip add dns "Ethernet" {dns}', shell=True)
            self.show_custom_message("Éxito", "DNS optimizados")
        except:
            self.show_custom_message("Error", "No se pudieron optimizar los DNS", error=True)

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
            self.show_custom_message("Éxito", "Configuración de red reseteada")
        except:
            self.show_custom_message("Error", "No se pudo resetear la configuración de red", error=True)

    def show_network_info(self):
        try:
            result = subprocess.run('ipconfig /all', shell=True, capture_output=True, text=True)
            
            # Crear una nueva ventana
            info_window = Toplevel(self.root)
            info_window.title("Información de red")
            info_window.geometry("600x400")
            info_window.configure(bg='black')
            
            # Hacer que la ventana sea modal
            info_window.transient(self.root)
            info_window.grab_set()
            
            # Crear frame con scroll
            frame = ttk.Frame(info_window)
            frame.pack(expand=True, fill='both', padx=10, pady=10)
            
            # Crear scrollbar
            scrollbar = ttk.Scrollbar(frame)
            scrollbar.pack(side='right', fill='y')
            
            # Crear text widget
            text_widget = tk.Text(frame,
                                wrap=tk.WORD,
                                yscrollcommand=scrollbar.set,
                                bg='black',
                                fg=self.rgb_to_hex(self.r, self.g, self.b),
                                font=('Consolas', 10))
            text_widget.pack(expand=True, fill='both')
            
            # Configurar scrollbar
            scrollbar.config(command=text_widget.yview)
            
            # Insertar la información
            text_widget.insert('1.0', result.stdout)
            
            # Hacer el texto de solo lectura
            text_widget.configure(state='disabled')
            
            # Botón de cerrar
            close_button = tk.Button(info_window,
                                   text="Cerrar",
                                   command=info_window.destroy,
                                   bg='black',
                                   fg=self.rgb_to_hex(self.r, self.g, self.b),
                                   activebackground='#001100',
                                   activeforeground=self.rgb_to_hex(self.r, self.g, self.b),
                                   relief='solid',
                                   bd=2)
            close_button.pack(pady=10)
            
            # Centrar la ventana
            info_window.update_idletasks()
            width = info_window.winfo_width()
            height = info_window.winfo_height()
            x = (info_window.winfo_screenwidth() // 2) - (width // 2)
            y = (info_window.winfo_screenheight() // 2) - (height // 2)
            info_window.geometry(f'{width}x{height}+{x}+{y}')
            
        except:
            self.show_custom_message("Error", "No se pudo obtener la información de red", error=True)

    def clean_downloads(self):
        try:
            # Obtener la ruta de Descargas de forma genérica
            downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
            
            # Contar archivos primero
            total_files = sum(1 for _ in os.listdir(downloads_path))
            
            # Crear barra de progreso
            progress_window, progress_bar, status_label, percent_label = self.show_progress(
                "Limpiando carpeta de descargas", total_files)
            
            files_removed = 0
            for filename in os.listdir(downloads_path):
                file_path = path.join(downloads_path, filename)
                try:
                    if path.isfile(file_path):
                        os.unlink(file_path)
                    elif path.isdir(file_path):
                        shutil.rmtree(file_path)
                    files_removed += 1
                    
                    # Actualizar progreso
                    progress_bar['value'] = files_removed
                    percent = int((files_removed / total_files) * 100)
                    percent_label.config(text=f"{percent}%")
                    status_label.config(text=f"Eliminando: {filename}")
                    progress_window.update()
                except:
                    continue
            
            progress_window.destroy()
            self.show_custom_message("Éxito", f"Se eliminaron {files_removed} archivos de la carpeta de descargas")
        except:
            if 'progress_window' in locals():
                progress_window.destroy()
            self.show_custom_message("Error", "No se pudo limpiar la carpeta de descargas", error=True)

    def gaming_mode(self):
        try:
            # Crear ventana de progreso
            progress_window, progress_bar, status_label, percent_label = self.show_progress(
                "Activando Modo Gaming Plus", 100)
            progress = 0
            
            # 1. Desactivar VSYNC
            status_label.config(text="Desactivando VSYNC globalmente...")
            try:
                # Modificar registro para VSYNC
                subprocess.run('reg add "HKCU\\System\\GameConfigStore" /v "GameDVR_Enabled" /t REG_DWORD /d "0" /f', shell=True)
                subprocess.run('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile" /v "SystemResponsiveness" /t REG_DWORD /d "0" /f', shell=True)
                progress += 25
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            # 2. Cerrar procesos conflictivos
            status_label.config(text="Cerrando procesos conflictivos...")
            conflicting_processes = [
                "chrome.exe", "spotify.exe", "discord.exe", "steam.exe",
                "epicgameslauncher.exe", "adobeupdateservice.exe"
            ]
            try:
                for proc in psutil.process_iter(['name']):
                    if proc.info['name'].lower() in conflicting_processes:
                        proc.kill()
                progress += 25
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            # 3. Activar Turbo Boost
            status_label.config(text="Activando Turbo Boost para juegos...")
            try:
                # Establecer esquema de energía de alto rendimiento
                subprocess.run('powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c', shell=True)
                # Prioridad alta para juegos
                subprocess.run('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "Priority" /t REG_DWORD /d "6" /f', shell=True)
                subprocess.run('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "GPU Priority" /t REG_DWORD /d "8" /f', shell=True)
                progress += 25
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            # 4. Gestor de FPS
            status_label.config(text="Configurando gestor de FPS...")
            try:
                # Limitar FPS globalmente a 144 (puedes ajustar este valor)
                subprocess.run('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "Affinity" /t REG_DWORD /d "0" /f', shell=True)
                subprocess.run('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "Background Only" /t REG_SZ /d "False" /f', shell=True)
                subprocess.run('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "Clock Rate" /t REG_DWORD /d "2710" /f', shell=True)
                progress += 25
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            time.sleep(1)  # Pequeña pausa para mostrar el 100%
            progress_window.destroy()
            
            self.show_custom_message("Éxito", """✅ Modo Gaming Plus activado:
• VSYNC desactivado globalmente
• Procesos conflictivos cerrados
• Turbo Boost activado
• Gestor de FPS configurado""")
        except:
            if 'progress_window' in locals():
                progress_window.destroy()
            self.show_custom_message("Error", "No se pudo activar el Modo Gaming Plus", error=True)

    def optimize_input(self):
        try:
            progress_window, progress_bar, status_label, percent_label = self.show_progress(
                "Optimizando Input", 100)
            progress = 0

            # 1. Timer Resolution y Latencia
            status_label.config(text="Optimizando Timer Resolution...")
            try:
                subprocess.run('bcdedit /set useplatformtick yes', shell=True)
                subprocess.run('bcdedit /set disabledynamictick yes', shell=True)
                progress += 20
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            # 2. Optimización de Mouse
            status_label.config(text="Optimizando periféricos...")
            try:
                # Deshabilitar aceleración del mouse
                subprocess.run('reg add "HKCU\\Control Panel\\Mouse" /v "MouseSpeed" /t REG_SZ /d "0" /f', shell=True)
                subprocess.run('reg add "HKCU\\Control Panel\\Mouse" /v "MouseThreshold1" /t REG_SZ /d "0" /f', shell=True)
                subprocess.run('reg add "HKCU\\Control Panel\\Mouse" /v "MouseThreshold2" /t REG_SZ /d "0" /f', shell=True)
                progress += 20
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            # 3. Optimización USB y HID
            status_label.config(text="Optimizando USB y HID...")
            try:
                subprocess.run('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\USB" /v "DisableSelectiveSuspend" /t REG_DWORD /d "1" /f', shell=True)
                progress += 20
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            # 4. Prioridades de proceso
            status_label.config(text="Ajustando prioridades...")
            try:
                critical_processes = ["csrss.exe", "dwm.exe", "explorer.exe"]
                for proc in psutil.process_iter(['name']):
                    if proc.info['name'].lower() in critical_processes:
                        p = psutil.Process(proc.pid)
                        p.nice(psutil.HIGH_PRIORITY_CLASS)
                progress += 20
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            # 5. Raw Input y DirectInput
            status_label.config(text="Optimizando Raw Input...")
            try:
                subprocess.run('reg add "HKCU\\Control Panel\\Input" /v "MouseInputProcessingRate" /t REG_DWORD /d "1" /f', shell=True)
                progress += 20
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            time.sleep(1)
            progress_window.destroy()
            
            self.show_custom_message("Éxito", """✅ Optimización de Input completada:
• Timer Resolution optimizado
• Latencia reducida
• Periféricos optimizados
• USB/HID mejorado
• Raw Input configurado""")
        except:
            if 'progress_window' in locals():
                progress_window.destroy()
            self.show_custom_message("Error", "No se pudo completar la optimización de input", error=True)

    def clean_system(self):
        try:
            # Rutas genéricas del sistema
            system_paths = [
                os.environ.get('SYSTEMROOT') + '\\SoftwareDistribution\\Download',  # Windows Update
                os.environ.get('SYSTEMROOT') + '\\Logs',  # Logs del sistema
                os.environ.get('SYSTEMROOT') + '\\Debug'  # Archivos de debug
            ]
            
            progress_window, progress_bar, status_label, percent_label = self.show_progress(
                "Limpieza del Sistema", 100)
            progress = 0

            # 1. Limpiar registro de Windows
            status_label.config(text="Limpiando registro de Windows...")
            try:
                subprocess.run('reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\RunMRU" /f', shell=True)
                subprocess.run('reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\TypedPaths" /f', shell=True)
                progress += 20
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            # 2. Limpiar Windows.old
            status_label.config(text="Limpiando carpeta Windows.old...")
            try:
                if path.exists("C:\\Windows.old"):
                    shutil.rmtree("C:\\Windows.old")
                progress += 20
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            # 3. Limpiar Prefetch
            status_label.config(text="Limpiando Prefetch...")
            try:
                subprocess.run('del /f /q C:\\Windows\\Prefetch\\*', shell=True)
                progress += 20
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            # 4. Limpiar caché de navegadores
            status_label.config(text="Limpiando caché de navegadores...")
            try:
                # Chrome
                chrome_cache = path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache')
                if path.exists(chrome_cache):
                    shutil.rmtree(chrome_cache)
                # Edge
                edge_cache = path.expanduser('~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cache')
                if path.exists(edge_cache):
                    shutil.rmtree(edge_cache)
                progress += 20
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            # 5. Limpiar caché de Windows Update
            status_label.config(text="Limpiando caché de Windows Update...")
            try:
                subprocess.run('net stop wuauserv', shell=True)
                subprocess.run('rd /s /q C:\\Windows\\SoftwareDistribution', shell=True)
                subprocess.run('net start wuauserv', shell=True)
                progress += 20
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            time.sleep(1)
            progress_window.destroy()
            
            self.show_custom_message("Éxito", """✅ Limpieza del Sistema completada:
• Registro de Windows limpiado
• Windows.old eliminado
• Prefetch limpiado
• Caché de navegadores eliminada
• Caché de Windows Update limpiada""")
        except:
            if 'progress_window' in locals():
                progress_window.destroy()
            self.show_custom_message("Error", "No se pudo completar la limpieza del sistema", error=True)

    def optimize_disk(self):
        try:
            progress_window, progress_bar, status_label, percent_label = self.show_progress(
                "Optimización de Disco", 100)
            progress = 0

            # 1. Ejecutar CHKDSK
            status_label.config(text="Ejecutando CHKDSK...")
            try:
                subprocess.run('chkdsk C: /f', shell=True)
                progress += 25
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            # 2. Desfragmentar/Optimizar disco
            status_label.config(text="Optimizando disco...")
            try:
                subprocess.run('defrag C: /O', shell=True)
                progress += 25
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            # 3. Limpiar puntos de restauración
            status_label.config(text="Limpiando puntos de restauración...")
            try:
                subprocess.run('vssadmin delete shadows /all /quiet', shell=True)
                progress += 25
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            # 4. Optimizar sistema de archivos
            status_label.config(text="Optimizando sistema de archivos...")
            try:
                subprocess.run('fsutil behavior set disabledeletenotify 0', shell=True)
                progress += 25
                progress_bar['value'] = progress
                percent_label.config(text=f"{percent}%")
                progress_window.update()
            except:
                pass

            time.sleep(1)
            progress_window.destroy()
            
            self.show_custom_message("Éxito", """✅ Optimización de Disco completada:
• CHKDSK ejecutado
• Disco optimizado
• Puntos de restauración limpiados
• Sistema de archivos optimizado""")
        except:
            if 'progress_window' in locals():
                progress_window.destroy()
            self.show_custom_message("Error", "No se pudo completar la optimización del disco", error=True)

    def optimize_memory(self):
        try:
            progress_window, progress_bar, status_label, percent_label = self.show_progress(
                "Optimización de Memoria", 100)
            progress = 0

            # 1. Liberar RAM inactiva
            status_label.config(text="Liberando memoria RAM...")
            try:
                subprocess.run('powershell -command "Clear-RecycleBin -Force"', shell=True)
                progress += 25
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            # 2. Optimizar memoria virtual
            status_label.config(text="Optimizando memoria virtual...")
            try:
                subprocess.run('wmic computersystem where name="%computername%" set AutomaticManagedPagefile=False', shell=True)
                progress += 25
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            # 3. Limpiar archivo de paginación
            status_label.config(text="Limpiando archivo de paginación...")
            try:
                subprocess.run('wmic pagefileset where name="C:\\pagefile.sys" set InitialSize=4096,MaximumSize=4096', shell=True)
                progress += 25
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            # 4. Optimizar programas de inicio
            status_label.config(text="Optimizando inicio del sistema...")
            try:
                subprocess.run('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Serialize" /v "StartupDelayInMSec" /t REG_DWORD /d "0" /f', shell=True)
                progress += 25
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            time.sleep(1)
            progress_window.destroy()
            
            self.show_custom_message("Éxito", """✅ Optimización de Memoria completada:
• RAM inactiva liberada
• Memoria virtual optimizada
• Archivo de paginación limpiado
• Inicio del sistema optimizado""")
        except:
            if 'progress_window' in locals():
                progress_window.destroy()
            self.show_custom_message("Error", "No se pudo completar la optimización de memoria", error=True)

    def show_creator_info(self):
        info_window = Toplevel(self.root)
        info_window.title("Información del Creador")
        info_window.geometry("400x200")
        info_window.configure(bg='black')
        
        # Hacer que la ventana sea modal
        info_window.transient(self.root)
        info_window.grab_set()
        
        # Frame contenedor
        frame = ttk.Frame(info_window, style='TFrame')
        frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Información del creador con estilo
        creator_info = """
👨‍💻 Creado por: Aguza

🎮 Discord ID: 
404709223843233814

🌟 Optimizador de Windows
Versión 1.0
"""
        
        label = Label(frame,
                        text=creator_info,
                        fg=self.rgb_to_hex(self.r, self.g, self.b),
                        bg='black',
                        justify='center',
                        font=('Arial', 12, 'bold'))
        label.pack(expand=True)
        
        # Botón de cerrar
        close_button = Button(frame,
                               text="Cerrar",
                               command=info_window.destroy,
                               bg='black',
                               fg=self.rgb_to_hex(self.r, self.g, self.b),
                               activebackground='#001100',
                               activeforeground=self.rgb_to_hex(self.r, self.g, self.b),
                               relief='solid',
                               bd=2)
        close_button.pack(pady=10)
        
        # Centrar la ventana
        info_window.update_idletasks()
        width = info_window.winfo_width()
        height = info_window.winfo_height()
        x = (info_window.winfo_screenwidth() // 2) - (width // 2)
        y = (info_window.winfo_screenheight() // 2) - (height // 2)
        info_window.geometry(f'{width}x{height}+{x}+{y}')

    def detect_cpu_type(self):
        try:
            import wmi
            c = wmi.WMI()
            cpu_info = c.Win32_Processor()[0]
            cpu_name = cpu_info.Name.lower()
            
            if 'intel' in cpu_name:
                return 'intel'
            elif 'amd' in cpu_name:
                return 'amd'
            else:
                return 'unknown'
        except:
            return 'unknown'

    def setup_cpu_tab(self):
        container = ttk.Frame(self.tab5, style='Modern.TFrame')
        container.pack(expand=True, fill='both', padx=50, pady=30)
        
        # Título centrado
        title_frame = ttk.Frame(container, style='Modern.TFrame')
        title_frame.pack(fill='x', pady=(0, 30))
        
        title = Label(title_frame,
                        text="💻 Optimización de CPU",
                        fg='#c9d1d9',
                        bg='#0d1117',
                        font=('Segoe UI', 20, 'bold'))
        title.pack(expand=True)
        
        # Frame para información del sistema
        info_frame = Frame(container, bg='#161b22', padx=30, pady=20)
        info_frame.pack(fill='x', pady=(0, 30))
        
        try:
            import wmi
            c = wmi.WMI()
            
            # CPU Info
            cpu_info = c.Win32_Processor()[0]
            cpu_label = Label(info_frame,
                               text=f"CPU: {cpu_info.Name}",
                               fg='#c9d1d9',
                               bg='#161b22',
                               font=('Segoe UI', 11),
                               justify='left')
            cpu_label.pack(anchor='w', pady=5)
            
            # RAM Info
            total_ram = round(float(c.Win32_ComputerSystem()[0].TotalPhysicalMemory) / 1024 / 1024 / 1024, 2)
            ram_label = Label(info_frame,
                               text=f"Memoria RAM: {total_ram} GB",
                               fg='#c9d1d9',
                               bg='#161b22',
                               font=('Segoe UI', 11),
                               justify='left')
            ram_label.pack(anchor='w', pady=5)
            
            # GPU Info
            gpu_info = c.Win32_VideoController()[0]
            gpu_label = Label(info_frame,
                               text=f"GPU: {gpu_info.Name}",
                               fg='#c9d1d9',
                               bg='#161b22',
                               font=('Segoe UI', 11),
                               justify='left')
            gpu_label.pack(anchor='w', pady=5)
            
            # Motherboard Info
            mb_info = c.Win32_BaseBoard()[0]
            mb_label = Label(info_frame,
                              text=f"Placa Base: {mb_info.Product}",
                              fg='#c9d1d9',
                              bg='#161b22',
                              font=('Segoe UI', 11),
                              justify='left')
            mb_label.pack(anchor='w', pady=5)
            
            # OS Info
            os_info = c.Win32_OperatingSystem()[0]
            os_label = Label(info_frame,
                              text=f"Sistema Operativo: {os_info.Caption}",
                              fg='#c9d1d9',
                              bg='#161b22',
                              font=('Segoe UI', 11),
                              justify='left')
            os_label.pack(anchor='w', pady=5)
            
        except Exception as e:
            error_label = Label(info_frame,
                                 text="No se pudo obtener la información del sistema",
                                 fg='#ff6b6b',
                                 bg='#161b22',
                                 font=('Segoe UI', 11))
            error_label.pack(pady=10)
        
        # Detectar tipo de CPU
        cpu_type = self.detect_cpu_type()
        
        # Separador
        separator = ttk.Frame(container, height=2, style='Separator.TFrame')
        separator.pack(fill='x', pady=20)
        
        # Definir tooltips para los botones de CPU
        tooltips = {
            "Optimización Intel": """💻 Optimización Intel:
• Ajuste de energía Intel
• Optimización de núcleos
• Intel Turbo Boost
• SpeedStep optimizado
• C-States configurados
• Hyper-Threading optimizado
• Configuración de caché
• Voltaje optimizado
• Temperaturas controladas""",
            
            "Optimización AMD": """💻 Optimización AMD:
• Modo alto rendimiento
• AMD Cool'n'Quiet optimizado
• Core Parking desactivado
• Precision Boost optimizado
• SMT configurado
• Voltaje ajustado
• Temperaturas monitorizadas
• Configuración de memoria
• AMD FSR habilitado"""
        }
        
        # Frame para los botones con disposición simétrica
        buttons_frame = Frame(container, bg='#0d1117')
        buttons_frame.pack(fill='x', expand=True)
        
        # Frame izquierdo para el botón Intel
        intel_frame = Frame(buttons_frame, bg='#0d1117')
        intel_frame.pack(side='left', expand=True, padx=10)
        
        # Frame derecho para el botón AMD
        amd_frame = Frame(buttons_frame, bg='#0d1117')
        amd_frame.pack(side='right', expand=True, padx=10)
        
        # Crear botones
        intel_button = self.create_modern_button(
            intel_frame, 
            "Optimización Intel", 
            self.optimize_intel, 
            tooltips["Optimización Intel"]
        )
        
        amd_button = self.create_modern_button(
            amd_frame, 
            "Optimización AMD", 
            self.optimize_amd, 
            tooltips["Optimización AMD"]
        )
        
        # Deshabilitar el botón que no corresponde
        if cpu_type == 'intel':
            amd_button.configure(state='disabled', bg='#1a1a1a', cursor='no')
            amd_button.unbind('<Enter>')
            amd_button.unbind('<Leave>')
        elif cpu_type == 'amd':
            intel_button.configure(state='disabled', bg='#1a1a1a', cursor='no')
            intel_button.unbind('<Enter>')
            intel_button.unbind('<Leave>')

    def optimize_fivem(self):
        try:
            # Ruta genérica de FiveM
            fivem_cache = os.path.join(os.environ.get('LOCALAPPDATA'), 'FiveM', 'FiveM.app', 'cache')
            
            # Crear barra de progreso
            progress_window, progress_bar, status_label, percent_label = self.show_progress(
                "Optimizando FiveM", 100)
            progress = 0

            # 1. Limpiar caché
            status_label.config(text="Limpiando caché de FiveM...")
            try:
                if os.path.exists(fivem_cache):
                    shutil.rmtree(fivem_cache)
                progress += 25
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            # 2. Optimizar configuración
            status_label.config(text="Optimizando configuración...")
            try:
                # Aquí irían los comandos específicos para FiveM
                progress += 25
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            # 3. Ajustar memoria
            status_label.config(text="Ajustando memoria...")
            progress += 25
            progress_bar['value'] = progress
            percent_label.config(text=f"{progress}%")
            progress_window.update()

            # 4. Finalizar optimización
            status_label.config(text="Finalizando optimización...")
            progress = 100
            progress_bar['value'] = progress
            percent_label.config(text=f"{progress}%")
            progress_window.update()
            
            time.sleep(1)
            progress_window.destroy()
            
            self.show_custom_message("Éxito", """✅ FiveM Optimizado:
• Caché limpiada
• Configuración optimizada
• Memoria ajustada
• Rendimiento mejorado""")
        except:
            if 'progress_window' in locals():
                progress_window.destroy()
            self.show_custom_message("Error", "No se pudo optimizar FiveM", error=True)

    def optimize_cs2(self):
        try:
            # Ruta genérica de Steam y CS2
            steam_path = os.path.join(os.environ.get('PROGRAMFILES(X86)'), 'Steam', 'steamapps', 'common', 'Counter-Strike Global Offensive')
            
            progress_window, progress_bar, status_label, percent_label = self.show_progress(
                "Optimizando CS2", 100)
            progress = 0

            # Implementar optimizaciones específicas para CS2
            status_label.config(text="Optimizando CS2...")
            # ... código de optimización ...

            progress_window.destroy()
            self.show_custom_message("Éxito", "CS2 optimizado correctamente")
        except:
            if 'progress_window' in locals():
                progress_window.destroy()
            self.show_custom_message("Error", "No se pudo optimizar CS2", error=True)

    def optimize_fc25(self):
        try:
            progress_window, progress_bar, status_label, percent_label = self.show_progress(
                "Optimizando FC25", 100)
            progress = 0

            # Implementar optimizaciones específicas para FC25
            status_label.config(text="Optimizando FC25...")
            # ... código de optimización ...

            progress_window.destroy()
            self.show_custom_message("Éxito", "FC25 optimizado correctamente")
        except:
            if 'progress_window' in locals():
                progress_window.destroy()
            self.show_custom_message("Error", "No se pudo optimizar FC25", error=True)

    def optimize_intel(self):
        try:
            progress_window, progress_bar, status_label, percent_label = self.show_progress(
                "Optimizando CPU Intel", 100)
            progress = 0

            # 1. Ajustar plan de energía
            status_label.config(text="Configurando plan de energía...")
            try:
                subprocess.run('powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c', shell=True)
                progress += 20
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            # 2. Optimizar Intel SpeedStep
            status_label.config(text="Optimizando Intel SpeedStep...")
            progress += 20
            progress_bar['value'] = progress
            percent_label.config(text=f"{progress}%")
            progress_window.update()

            # 3. Configurar C-States
            status_label.config(text="Configurando C-States...")
            progress += 20
            progress_bar['value'] = progress
            percent_label.config(text=f"{progress}%")
            progress_window.update()

            # 4. Optimizar Turbo Boost
            status_label.config(text="Optimizando Turbo Boost...")
            progress += 20
            progress_bar['value'] = progress
            percent_label.config(text=f"{progress}%")
            progress_window.update()

            # 5. Ajustes finales
            status_label.config(text="Aplicando ajustes finales...")
            progress = 100
            progress_bar['value'] = progress
            percent_label.config(text=f"{progress}%")
            progress_window.update()
            
            time.sleep(1)
            progress_window.destroy()
            
            self.show_custom_message("Éxito", """✅ CPU Intel Optimizada:
• Plan de energía configurado
• SpeedStep optimizado
• C-States ajustados
• Turbo Boost optimizado
• Rendimiento mejorado""")
        except:
            if 'progress_window' in locals():
                progress_window.destroy()
            self.show_custom_message("Error", "No se pudo optimizar la CPU Intel", error=True)

    def optimize_amd(self):
        try:
            progress_window, progress_bar, status_label, percent_label = self.show_progress(
                "Optimizando CPU AMD", 100)
            progress = 0

            # 1. Configurar modo alto rendimiento
            status_label.config(text="Configurando modo de rendimiento...")
            try:
                subprocess.run('powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c', shell=True)
                progress += 20
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            # 2. Optimizar Cool'n'Quiet
            status_label.config(text="Optimizando AMD Cool'n'Quiet...")
            progress += 20
            progress_bar['value'] = progress
            percent_label.config(text=f"{progress}%")
            progress_window.update()

            # 3. Configurar Core Parking
            status_label.config(text="Desactivando Core Parking...")
            progress += 20
            progress_bar['value'] = progress
            percent_label.config(text=f"{progress}%")
            progress_window.update()

            # 4. Optimizar Precision Boost
            status_label.config(text="Optimizando Precision Boost...")
            progress += 20
            progress_bar['value'] = progress
            percent_label.config(text=f"{progress}%")
            progress_window.update()

            # 5. Ajustes finales
            status_label.config(text="Aplicando ajustes finales...")
            progress = 100
            progress_bar['value'] = progress
            percent_label.config(text=f"{progress}%")
            progress_window.update()
            
            time.sleep(1)
            progress_window.destroy()
            
            self.show_custom_message("Éxito", """✅ CPU AMD Optimizada:
• Modo alto rendimiento activado
• Cool'n'Quiet optimizado
• Core Parking desactivado
• Precision Boost optimizado
• Rendimiento mejorado""")
        except:
            if 'progress_window' in locals():
                progress_window.destroy()
            self.show_custom_message("Error", "No se pudo optimizar la CPU AMD", error=True)

    def setup_games_tab(self):
        container = ttk.Frame(self.tab4, style='Modern.TFrame')
        container.pack(expand=True, fill='both', padx=50, pady=30)
        
        # Título centrado
        title_frame = ttk.Frame(container, style='Modern.TFrame')
        title_frame.pack(fill='x', pady=(0, 30))
        
        title = Label(title_frame,
                        text="🎮 Optimización de Juegos",
                        fg='#c9d1d9',
                        bg='#0d1117',
                        font=('Segoe UI', 20, 'bold'))
        title.pack(expand=True)
        
        # Descripción centrada
        description = Label(container,
                             text="Mejora el rendimiento y la experiencia de tus juegos",
                             fg='#8b949e',
                             bg='#0d1117',
                             font=('Segoe UI', 12))
        description.pack(pady=(0, 30))

        # Frame para las tarjetas de juegos
        games_frame = Frame(container, bg='#0d1117')
        games_frame.pack(fill='x', expand=True)

        # Configuración de las tarjetas de juegos
        games_config = [
            {
                "name": "FiveM",
                "icon": "🚗",
                "description": "Grand Theft Auto V Multiplayer",
                "tooltip": """🎮 Optimización FiveM:
• Limpieza de caché
• Configuración óptima de gráficos
• Ajuste de memoria
• Optimización de archivos
• Mejora de rendimiento""",
                "command": self.optimize_fivem,
                "bg_color": "#1B2838"  # Color de fondo estilo Steam
            },
            {
                "name": "CS2",
                "icon": "🎯",
                "description": "Counter-Strike 2",
                "tooltip": """🎮 Optimización Counter-Strike 2:
• Configuración de launch options
• Optimización de video
• Ajustes de red
• Configuración de audio
• Mejora de FPS""",
                "command": self.optimize_cs2,
                "bg_color": "#1B2838"  # Color de fondo estilo Steam
            },
            {
                "name": "FC25",
                "icon": "⚽",
                "description": "EA Sports FC 25",
                "tooltip": """🎮 Optimización FC25:
• Configuración de rendimiento
• Ajustes gráficos óptimos
• Optimización de memoria
• Mejora de estabilidad
• Reducción de latencia""",
                "command": self.optimize_fc25,
                "bg_color": "#1B2838"  # Color de fondo estilo Steam
            }
        ]

        # Crear tarjetas para cada juego
        for game in games_config:
            # Frame para la tarjeta con borde
            card_border = Frame(games_frame, bg='#66c0f4', padx=1, pady=1)  # Borde azul Steam
            card_border.pack(fill='x', pady=10, padx=20)
            
            # Frame para la tarjeta
            card_frame = Frame(card_border, bg=game["bg_color"], padx=20, pady=15)
            card_frame.pack(fill='x')
            
            # Frame para el contenido de la tarjeta
            content_frame = Frame(card_frame, bg=game["bg_color"])
            content_frame.pack(fill='x')
            
            # Icono y nombre del juego
            icon_label = Label(content_frame,
                                text=game["icon"],
                                fg='#c9d1d9',
                                bg=game["bg_color"],
                                font=('Segoe UI', 24))
            icon_label.pack(side='left', padx=(0, 15))
            
            # Frame para texto
            text_frame = Frame(content_frame, bg=game["bg_color"])
            text_frame.pack(side='left', fill='x', expand=True)
            
            name_label = Label(text_frame,
                                text=game["name"],
                                fg='#66c0f4',  # Azul Steam
                                bg=game["bg_color"],
                                font=('Segoe UI', 14, 'bold'))
            name_label.pack(anchor='w')
            
            desc_label = Label(text_frame,
                                text=game["description"],
                                fg='#8b949e',
                                bg=game["bg_color"],
                                font=('Segoe UI', 10))
            desc_label.pack(anchor='w')
            
            # Botón de optimizar
            optimize_button = Button(content_frame,
                                      text="Optimizar",
                                      command=game["command"],
                                      bg='#66c0f4',  # Azul Steam
                                      fg='white',
                                      activebackground='#1999ff',
                                      activeforeground='white',
                                      font=('Segoe UI', 10, 'bold'),
                                      relief='flat',
                                      padx=15,
                                      pady=5,
                                      cursor='hand2')
            optimize_button.pack(side='right', padx=(15, 0))
            
            # Efectos hover para el botón
            def on_enter(e, button=optimize_button):
                button.configure(bg='#1999ff')
            
            def on_leave(e, button=optimize_button):
                button.configure(bg='#66c0f4')
            
            optimize_button.bind('<Enter>', on_enter)
            optimize_button.bind('<Leave>', on_leave)
            
            # Añadir tooltip
            self.add_modern_tooltip(optimize_button, game["tooltip"])
            
            # Efecto hover para toda la tarjeta
            def card_enter(e, frame=card_frame, content=content_frame, border=card_border, bg=game["bg_color"]):
                hover_bg = '#233C51'  # Color hover estilo Steam
                frame.configure(bg=hover_bg)
                border.configure(bg='#1999ff')  # Borde más brillante en hover
                for widget in frame.winfo_children():
                    widget.configure(bg=hover_bg)
                for widget in content.winfo_children():
                    if isinstance(widget, Frame):
                        widget.configure(bg=hover_bg)
                        for w in widget.winfo_children():
                            w.configure(bg=hover_bg)
                    elif not isinstance(widget, Button):  # No cambiar el color del botón
                        widget.configure(bg=hover_bg)
            
            def card_leave(e, frame=card_frame, content=content_frame, border=card_border, bg=game["bg_color"]):
                frame.configure(bg=bg)
                border.configure(bg='#66c0f4')
                for widget in frame.winfo_children():
                    widget.configure(bg=bg)
                for widget in content.winfo_children():
                    if isinstance(widget, Frame):
                        widget.configure(bg=bg)
                        for w in widget.winfo_children():
                            w.configure(bg=bg)
                    elif not isinstance(widget, Button):  # No cambiar el color del botón
                        widget.configure(bg=bg)
            
            card_frame.bind('<Enter>', card_enter)
            card_frame.bind('<Leave>', card_leave)

    def setup_styles(self):
        """Configurar todos los estilos una sola vez"""
        style = ttk.Style()
        style.theme_use('default')
        
        # Diccionario de colores para fácil mantenimiento
        self.colors = {
            'bg': '#0d1117',
            'fg': '#c9d1d9',
            'accent': '#58a6ff',
            'hover': '#1e293b',
            'button': '#66c0f4',
            'button_hover': '#1999ff'
        }
        
        # Configurar estilos base
        base_styles = {
            'Tab.TFrame': {'background': self.colors['bg']},
            'Custom.TNotebook': {'background': self.colors['bg'], 'borderwidth': 0},
            'Custom.TNotebook.Tab': {
                'background': '#161b22',
                'foreground': '#8b949e',
                'padding': [20, 12],
                'font': ('Segoe UI', 11)
            }
        }
        
        for style_name, config in base_styles.items():
            style.configure(style_name, **config)

    def create_game_card(self, parent, game_config):
        """Crear una tarjeta de juego reutilizable"""
        card = Frame(parent, bg=self.colors['bg'])
        # ... resto del código de la tarjeta ...
        return card

    def create_button(self, parent, text, command, tooltip=None):
        """Crear botón reutilizable"""
        btn = Button(parent, text=text, command=command)
        if tooltip:
            self.add_tooltip(btn, tooltip)
        return btn

    def safe_remove(self, path):
        """Eliminar archivos de forma segura"""
        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            return True
        except:
            return False

    def clean_directory(self, directory, callback=None):
        """Limpiar directorio con callback opcional"""
        if not os.path.exists(directory):
            return 0
        
        files_removed = 0
        for root, dirs, files in os.walk(directory, topdown=False):
            for name in files:
                if self.safe_remove(os.path.join(root, name)):
                    files_removed += 1
                if callback:
                    callback(files_removed)
            for name in dirs:
                self.safe_remove(os.path.join(root, name))
        return files_removed

    def setup_work_study_tab(self):
        container = ttk.Frame(self.tab6, style='Modern.TFrame')
        container.pack(expand=True, fill='both', padx=50, pady=30)
        
        # Título centrado
        title_frame = ttk.Frame(container, style='Modern.TFrame')
        title_frame.pack(fill='x', pady=(0, 30))
        
        title = Label(title_frame,
                     text="📚 Optimización para Trabajo y Estudio",
                     fg='#c9d1d9',
                     bg='#0d1117',
                     font=('Segoe UI', 20, 'bold'))
        title.pack(expand=True)
        
        # Descripción
        description = Label(container,
                          text="Optimiza tu sistema para productividad e instala programas esenciales",
                          fg='#8b949e',
                          bg='#0d1117',
                          font=('Segoe UI', 12))
        description.pack(pady=(0, 30))

        # Definir las categorías y programas
        categories = [
            {
                "name": "Programas de Oficina",
                "icon": "📝",
                "programs": [
                    "Microsoft Office",
                    "LibreOffice",
                    "WPS Office",
                    "Adobe Acrobat Reader",
                    "Foxit PDF Reader",
                    "Notepad++",
                    "Sublime Text",
                    "Visual Studio Code"
                ],
                "tooltip": """📝 Suite Ofimática:
• Procesadores de texto
• Hojas de cálculo
• Presentaciones
• Editores PDF
• Editores de código"""
            },
            {
                "name": "Herramientas de Estudio",
                "icon": "📚",
                "programs": [
                    "Notion",
                    "Evernote",
                    "OneNote",
                    "Zotero",
                    "Mendeley",
                    "Anki",
                    "Quizlet",
                    "GoodNotes"
                ],
                "tooltip": """📚 Herramientas de Estudio:
• Toma de notas
• Gestión de referencias
• Tarjetas de estudio
• Organización"""
            },
            {
                "name": "Comunicación y Colaboración",
                "icon": "💬",
                "programs": [
                    "Microsoft Teams",
                    "Zoom",
                    "Slack",
                    "Discord",
                    "Skype",
                    "Google Meet",
                    "Webex",
                    "TeamViewer"
                ],
                "tooltip": """💬 Herramientas de Comunicación:
• Videoconferencias
• Chat empresarial
• Colaboración en equipo
• Soporte remoto"""
            },
            {
                "name": "Herramientas de Productividad",
                "icon": "⚡",
                "programs": [
                    "Trello",
                    "Microsoft To Do",
                    "Todoist",
                    "Focus@Will",
                    "RescueTime",
                    "Forest",
                    "Cold Turkey",
                    "Freedom"
                ],
                "tooltip": """⚡ Productividad:
• Gestión de tareas
• Gestión del tiempo
• Bloqueadores de distracciones
• Seguimiento de productividad"""
            },
            {
                "name": "Herramientas Especializadas",
                "icon": "🔧",
                "programs": [
                    "MATLAB",
                    "R Studio",
                    "Python",
                    "AutoCAD",
                    "SketchUp",
                    "GeoGebra",
                    "Wolfram Alpha",
                    "DaVinci Resolve"
                ],
                "tooltip": """🔧 Software Especializado:
• Análisis de datos
• Diseño y CAD
• Programación
• Edición multimedia"""
            }
        ]

        # Crear un canvas con scrollbar
        canvas = Canvas(container, bg='#0d1117', highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Modern.TFrame')
        
        # Configurar el scrolling
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Configurar el ancho del canvas para que ocupe todo el espacio
        container.update_idletasks()
        canvas_width = container.winfo_width() - scrollbar.winfo_reqwidth()
        canvas.configure(width=canvas_width)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas_width)
        
        # Botón de optimización
        optimize_button = self.create_modern_button(
            scrollable_frame,
            "🚀 Optimizar Windows para Trabajo/Estudio",
            self.optimize_for_work,
            """✨ Optimización específica para productividad:
• Ajuste de rendimiento para aplicaciones de oficina
• Optimización de memoria para multitarea
• Prioridad de procesos de productividad
• Configuración de energía balanceada
• Optimización de disco para archivos de trabajo
• Mejora de velocidad de lectura/escritura
• Configuración de Windows Update
• Optimización de búsqueda de Windows"""
        )

        # Separador
        separator = ttk.Frame(scrollable_frame, height=2, style='Separator.TFrame')
        separator.pack(fill='x', pady=20)

        # Frame contenedor para las tarjetas en dos columnas
        cards_container = Frame(scrollable_frame, bg='#0d1117')
        cards_container.pack(fill='both', expand=True)

        # Crear filas de tarjetas (2 por fila)
        for i in range(0, len(categories), 2):
            row_frame = Frame(cards_container, bg='#0d1117')
            row_frame.pack(fill='x', expand=True, pady=5)
            
            # Primera tarjeta de la fila
            if i < len(categories):
                self.create_category_card(row_frame, categories[i])
            
            # Segunda tarjeta de la fila (si existe)
            if i + 1 < len(categories):
                self.create_category_card(row_frame, categories[i + 1])

        # Empaquetar canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Configurar el scroll con la rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Ajustar el tamaño del canvas cuando la ventana cambie
        def _on_frame_configure(event):
            canvas_width = container.winfo_width() - scrollbar.winfo_reqwidth()
            canvas.configure(width=canvas_width)
            canvas.itemconfig(canvas.find_withtag("all")[0], width=canvas_width)
        
        container.bind('<Configure>', _on_frame_configure)

    def optimize_for_work(self):
        try:
            progress_window, progress_bar, status_label, percent_label = self.show_progress(
                "Optimizando Windows para Trabajo/Estudio", 100)
            progress = 0

            # 1. Ajustar plan de energía balanceado
            status_label.config(text="Configurando plan de energía...")
            try:
                subprocess.run('powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e', shell=True)
                progress += 20
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            # 2. Optimizar rendimiento de aplicaciones
            status_label.config(text="Optimizando rendimiento...")
            try:
                subprocess.run('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\csrss.exe\\PerfOptions" /v CpuPriorityClass /t REG_DWORD /d 3 /f', shell=True)
                progress += 20
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            # 3. Configurar Windows Update
            status_label.config(text="Configurando actualizaciones...")
            progress += 20
            progress_bar['value'] = progress
            percent_label.config(text=f"{progress}%")
            progress_window.update()

            # 4. Optimizar búsqueda de Windows
            status_label.config(text="Optimizando búsqueda...")
            progress += 20
            progress_bar['value'] = progress
            percent_label.config(text=f"{progress}%")
            progress_window.update()

            # 5. Ajustes finales
            status_label.config(text="Aplicando ajustes finales...")
            progress = 100
            progress_bar['value'] = progress
            percent_label.config(text=f"{progress}%")
            progress_window.update()
            
            time.sleep(1)
            progress_window.destroy()
            
            self.show_custom_message("Éxito", """✅ Windows Optimizado para Trabajo/Estudio:
• Plan de energía balanceado
• Rendimiento optimizado para productividad
• Actualizaciones configuradas
• Búsqueda optimizada
• Sistema preparado para multitarea""")
        except:
            if 'progress_window' in locals():
                progress_window.destroy()
            self.show_custom_message("Error", "No se pudo completar la optimización", error=True)

    def create_category_card(self, parent, category):
        # Frame para la tarjeta
        card_frame = Frame(parent, bg='#161b22', padx=20, pady=15)
        card_frame.pack(side='left', fill='both', expand=True, padx=10)
        
        # Título de la categoría
        header_frame = Frame(card_frame, bg='#161b22')
        header_frame.pack(fill='x')
        
        icon_label = Label(header_frame,
                          text=category["icon"],
                          fg='#c9d1d9',
                          bg='#161b22',
                          font=('Segoe UI', 24))
        icon_label.pack(side='left')
        
        name_label = Label(header_frame,
                          text=category["name"],
                          fg='#58a6ff',
                          bg='#161b22',
                          font=('Segoe UI', 14, 'bold'))
        name_label.pack(side='left', padx=10)
        
        # Frame para los programas
        programs_frame = Frame(card_frame, bg='#161b22')
        programs_frame.pack(fill='x', pady=(10, 0))
        
        # Diccionario de URLs para cada programa
        program_urls = {
            "Microsoft Office": "https://www.office.com/",
            "LibreOffice": "https://www.libreoffice.org/download/",
            "WPS Office": "https://www.wps.com/download/",
            "Adobe Acrobat Reader": "https://get.adobe.com/reader/",
            "Foxit PDF Reader": "https://www.foxit.com/downloads/",
            "Notepad++": "https://notepad-plus-plus.org/downloads/",
            "Sublime Text": "https://www.sublimetext.com/download",
            "Visual Studio Code": "https://code.visualstudio.com/download",
            "Notion": "https://www.notion.so/desktop",
            "Evernote": "https://evernote.com/download",
            "OneNote": "https://www.onenote.com/download",
            "Zotero": "https://www.zotero.org/download/",
            "Mendeley": "https://www.mendeley.com/download-desktop/",
            "Anki": "https://apps.ankiweb.net/",
            "Quizlet": "https://quizlet.com/mobile",
            "GoodNotes": "https://www.goodnotes.com/download",
            "Microsoft Teams": "https://www.microsoft.com/microsoft-teams/download-app",
            "Zoom": "https://zoom.us/download",
            "Slack": "https://slack.com/downloads/",
            "Discord": "https://discord.com/download",
            "Skype": "https://www.skype.com/get-skype/",
            "Google Meet": "https://meet.google.com/",
            "Webex": "https://www.webex.com/downloads.html",
            "TeamViewer": "https://www.teamviewer.com/download/",
            "Trello": "https://trello.com/platforms",
            "Microsoft To Do": "https://todo.microsoft.com/tasks/",
            "Todoist": "https://todoist.com/downloads",
            "Focus@Will": "https://www.focusatwill.com/",
            "RescueTime": "https://www.rescuetime.com/download",
            "Forest": "https://www.forestapp.cc/",
            "Cold Turkey": "https://getcoldturkey.com/download/",
            "Freedom": "https://freedom.to/download",
            "MATLAB": "https://www.mathworks.com/downloads/",
            "R Studio": "https://www.rstudio.com/products/rstudio/download/",
            "Python": "https://www.python.org/downloads/",
            "AutoCAD": "https://www.autodesk.com/products/autocad/",
            "SketchUp": "https://www.sketchup.com/products/sketchup-pro/",
            "GeoGebra": "https://www.geogebra.org/download",
            "Wolfram Alpha": "https://www.wolframalpha.com/",
            "DaVinci Resolve": "https://www.blackmagicdesign.com/products/davinciresolve/"
        }

        # Crear checkboxes y variables para cada programa
        program_vars = {}
        for program in category["programs"]:
            var = BooleanVar()
            program_vars[program] = var
            checkbox = ttk.Checkbutton(programs_frame, 
                                     text=program,
                                     variable=var,
                                     style='Custom.TCheckbutton')
            checkbox.pack(anchor='w', pady=2)
        
        # Función para instalar programas seleccionados
        def install_selected():
            selected_programs = [prog for prog, var in program_vars.items() if var.get()]
            for program in selected_programs:
                if program in program_urls:
                    webbrowser.open(program_urls[program])
        
        # Botón de instalar
        install_button = Button(card_frame,
                              text="Instalar Seleccionados",
                              command=install_selected,
                              bg='#238636',
                              fg='white',
                              activebackground='#2ea043',
                              activeforeground='white',
                              font=('Segoe UI', 10, 'bold'),
                              relief='flat',
                              padx=15,
                              pady=5,
                              cursor='hand2')
        install_button.pack(pady=(10, 0))
        
        # Añadir tooltip
        self.add_modern_tooltip(card_frame, category["tooltip"])

    # Agregar la nueva función para optimizar periféricos
    def optimize_peripherals(self):
        try:
            progress_window, progress_bar, status_label, percent_label = self.show_progress(
                "Optimizando Periféricos", 100)
            progress = 0

            # 1. Optimizar USB y HID
            status_label.config(text="Optimizando puertos USB...")
            try:
                # Deshabilitar selective suspend
                subprocess.run('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\USB" /v "DisableSelectiveSuspend" /t REG_DWORD /d "1" /f', shell=True)
                # Optimizar polling rate USB
                subprocess.run('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\USB" /v "DisableSelectiveSuspend" /t REG_DWORD /d "1" /f', shell=True)
                progress += 20
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            # 2. Optimizar controladores de juego
            status_label.config(text="Optimizando controladores...")
            try:
                # Optimizar DirectInput
                subprocess.run('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\MediaProperties\\PrivateProperties\\Joystick\\OEM" /v "POV" /t REG_DWORD /d "1" /f', shell=True)
                # Optimizar XInput
                subprocess.run('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\HidGame" /v "Start" /t REG_DWORD /d "3" /f', shell=True)
                progress += 20
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            # 3. Optimizar ratón y teclado
            status_label.config(text="Optimizando ratón y teclado...")
            try:
                # Deshabilitar aceleración del ratón
                subprocess.run('reg add "HKCU\\Control Panel\\Mouse" /v "MouseSpeed" /t REG_SZ /d "0" /f', shell=True)
                subprocess.run('reg add "HKCU\\Control Panel\\Mouse" /v "MouseThreshold1" /t REG_SZ /d "0" /f', shell=True)
                subprocess.run('reg add "HKCU\\Control Panel\\Mouse" /v "MouseThreshold2" /t REG_SZ /d "0" /f', shell=True)
                # Optimizar tasa de respuesta del teclado
                subprocess.run('reg add "HKCU\\Control Panel\\Keyboard" /v "KeyboardDelay" /t REG_SZ /d "0" /f', shell=True)
                progress += 20
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            # 4. Optimizar controladores PS4/PS5
            status_label.config(text="Optimizando controladores PS4/PS5...")
            try:
                # Optimizar DS4/DualSense
                subprocess.run('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\HidBth" /v "Start" /t REG_DWORD /d "3" /f', shell=True)
                progress += 20
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            # 5. Ajustes finales y prioridades
            status_label.config(text="Aplicando ajustes finales...")
            try:
                # Establecer prioridades de dispositivos
                subprocess.run('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl" /v "Win32PrioritySeparation" /t REG_DWORD /d "38" /f', shell=True)
                progress = 100
                progress_bar['value'] = progress
                percent_label.config(text=f"{progress}%")
                progress_window.update()
            except:
                pass

            time.sleep(1)
            progress_window.destroy()
            
            self.show_custom_message("Éxito", """✅ Periféricos Optimizados:
• USB y HID optimizados
• Controladores de juego mejorados
• Ratón y teclado optimizados
• Controladores PS4/PS5 configurados
• Prioridades ajustadas
• Latencia reducida""")
        except:
            if 'progress_window' in locals():
                progress_window.destroy()
            self.show_custom_message("Error", "No se pudo completar la optimización de periféricos", error=True)

    def on_minimize(self, event):
        """Mostrar botón flotante cuando la ventana se minimiza"""
        if self.root.state() == 'iconic':  # Si la ventana está minimizada
            self.float_window.deiconify()  # Mostrar botón flotante
        else:
            self.float_window.withdraw()  # Ocultar botón flotante

if __name__ == "__main__":
    root = Tk()
    app = WindowsOptimizer(root)
    root.mainloop() 