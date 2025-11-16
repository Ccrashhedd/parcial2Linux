import tkinter as tk
from tkinter import ttk, messagebox


class InterfazPrincipal:
    """Clase principal para la interfaz gráfica de la aplicación"""
    
    def __init__(self, ventana):
        """
        Inicializa la interfaz gráfica
        
        Args:
            ventana: La ventana raíz de tkinter
        """
        self.ventana = ventana
        self.ventana.title("Sistema Operativo - Parcial 2")
        self.ventana.geometry("800x600")
        self.ventana.minsize(600, 400)
        
        # Configurar estilos
        self.estilo = ttk.Style()
        self.estilo.theme_use('clam')
        
        # Crear el contenido principal
        self._crear_widgets()
    
    def _crear_widgets(self):
        """Crea los widgets principales de la interfaz"""
        
        # Frame superior - Encabezado
        frame_encabezado = ttk.Frame(self.ventana)
        frame_encabezado.pack(side=tk.TOP, fill=tk.X, padx=20, pady=20)
        
        label_titulo = ttk.Label(
            frame_encabezado,
            text="Sistema Operativo - Parcial 2",
            font=("Arial", 16, "bold")
        )
        label_titulo.pack()
        
        label_subtitulo = ttk.Label(
            frame_encabezado,
            text="Gestión de Base de Datos con PostgreSQL",
            font=("Arial", 10)
        )
        label_subtitulo.pack()
        
        # Frame central - Contenido principal
        frame_central = ttk.Frame(self.ventana)
        frame_central.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        label_bienvenida = ttk.Label(
            frame_central,
            text="Bienvenido a la aplicación",
            font=("Arial", 12)
        )
        label_bienvenida.pack(pady=10)
        
        # Frame de botones
        frame_botones = ttk.Frame(frame_central)
        frame_botones.pack(pady=20)
        
        btn_conectar = ttk.Button(
            frame_botones,
            text="Conectar Base de Datos",
            command=self._conectar_db
        )
        btn_conectar.pack(side=tk.LEFT, padx=5)
        
        btn_salir = ttk.Button(
            frame_botones,
            text="Salir",
            command=self.ventana.quit
        )
        btn_salir.pack(side=tk.LEFT, padx=5)
        
        # Frame inferior - Barra de estado
        frame_estado = ttk.Frame(self.ventana)
        frame_estado.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)
        
        self.label_estado = ttk.Label(
            frame_estado,
            text="Estado: Desconectado",
            relief=tk.SUNKEN,
            font=("Arial", 9)
        )
        self.label_estado.pack(fill=tk.X)
    
    def _conectar_db(self):
        """Maneja la conexión a la base de datos"""
        messagebox.showinfo(
            "Conexión",
            "Función de conexión a la base de datos\n(Aún no implementada)"
        )
        self.label_estado.config(text="Estado: Intentando conectar...")
    
    def ejecutar(self):
        """Inicia el loop principal de la aplicación"""
        self.ventana.mainloop()
