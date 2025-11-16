"""
interfaz_restaurante.py - Interfaz gráfica para POS de restaurante
Diseño moderno, minimalista con botones ovalados
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from modelo_restaurante import Menu, Pedido, Factura, MenuItem, PedidoRestaurante
import subprocess
import os
import tempfile
import tkinter.font as tkFont
import datetime


class InterfazRestaurante:
    """Interfaz gráfica moderna estilo web para POS de restaurante"""
    
    # Paleta de colores inspirada en diseño web moderno
    COLORES = {
        'fondo_principal': '#1a1a1a',     # Negro elegante
        'fondo_card': '#2d2d2d',          # Gris oscuro para cards
        'fondo_secundario': '#3a3a3a',    # Gris medio
        'acento_dorado': '#d4af37',       # Dorado elegante
        'acento_naranja': '#ff6b35',      # Naranja vibrante
        'texto_principal': '#ffffff',      # Blanco
        'texto_secundario': '#b0b0b0',    # Gris claro
        'texto_muted': '#808080',         # Gris medio
        'verde_success': '#00d4aa',       # Verde moderno
        'rojo_danger': '#ff4757',         # Rojo moderno
        'azul_info': '#3742fa',           # Azul moderno
        'borde_sutil': '#404040',         # Bordes sutiles
        'sombra': '#00000040',            # Sombra suave
        'hover_effect': '#404040',        # Efecto hover
        'gris_neutral': '#666666',        # Gris neutral para botones
    }
    
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("🍽️ POS RESTAURANT - Premium")
        self.ventana.geometry("1400x800")
        self.ventana.minsize(1200, 700)
        
        # Configurar fondo oscuro moderno
        self.ventana.configure(bg=self.COLORES['fondo_principal'])
        
        # Configurar estilo moderno
        self._configurar_estilos()
        
        # Modelo de datos
        self.menu = Menu()
        self.pedido = PedidoRestaurante()
        
        # Variables para la interfaz
        self.nombre_negocio = tk.StringVar(value="Premium Restaurant")
        self.nit_negocio = tk.StringVar(value="123456789-1")
        
        # Crear interfaz moderna
        self._crear_interfaz_moderna()
        
        # Variables de configuración
        self.nombre_negocio = tk.StringVar(value="PREMIUM RESTAURANT")
        self.nit_negocio = tk.StringVar(value="123456789")
        
        # Crear interfaz moderna
        self._crear_interfaz_moderna()
    
    def _configurar_estilos(self):
        """Configurar estilos modernos estilo web oscuro"""
        estilo = ttk.Style()
        estilo.theme_use('clam')
        
        # Configurar tema oscuro moderno
        estilo.configure('TFrame', background=self.COLORES['fondo_principal'])
        estilo.configure('TLabel', background=self.COLORES['fondo_principal'], 
                        foreground=self.COLORES['texto_principal'], font=('Inter', 10))
        
        # Headers grandes
        estilo.configure('Header.TLabel', font=('Inter', 24, 'bold'), 
                        foreground=self.COLORES['acento_dorado'],
                        background=self.COLORES['fondo_principal'])
        
        # Subheaders
        estilo.configure('Subheader.TLabel', font=('Inter', 14, 'bold'), 
                        foreground=self.COLORES['texto_principal'],
                        background=self.COLORES['fondo_card'])
        
        # Cards style
        estilo.configure('Card.TFrame', background=self.COLORES['fondo_card'],
                        relief='flat', borderwidth=1)
        
        self.estilo = estilo
    
    def _crear_interfaz_moderna(self):
        """Crear interfaz moderna estilo web con layout tipo dashboard"""
        
        # Crear interfaz moderna simplificada
        # self._crear_header_principal()
        self._crear_contenido_principal()
        # self._crear_footer_moderno()
    
    def _crear_header_principal(self):
        """Crear header moderno estilo website"""
        header = tk.Frame(self.ventana, bg=self.COLORES['fondo_principal'], height=100)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        # Container del header
        header_content = tk.Frame(header, bg=self.COLORES['fondo_principal'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        # Logo/Título lado izquierdo
        logo_frame = tk.Frame(header_content, bg=self.COLORES['fondo_principal'])
        logo_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Logo con estilo moderno
        logo_text = tk.Label(logo_frame, text="🍽️", font=('Apple Color Emoji', 28),
                            bg=self.COLORES['fondo_principal'])
        logo_text.pack(side=tk.LEFT, padx=(0, 15))
        
        # Textos del logo
        logo_container = tk.Frame(logo_frame, bg=self.COLORES['fondo_principal'])
        logo_container.pack(side=tk.LEFT, fill=tk.Y)
        
        titulo_principal = tk.Label(logo_container, text="PREMIUM", 
                                   font=('Inter', 20, 'bold'),
                                   fg=self.COLORES['acento_dorado'], 
                                   bg=self.COLORES['fondo_principal'])
        titulo_principal.pack(anchor=tk.W)
        
        subtitulo = tk.Label(logo_container, text="RESTAURANT", 
                            font=('Inter', 14),
                            fg=self.COLORES['texto_secundario'], 
                            bg=self.COLORES['fondo_principal'])
        subtitulo.pack(anchor=tk.W, pady=(0, 0))
        
        # Navegación lado derecho
        nav_frame = tk.Frame(header_content, bg=self.COLORES['fondo_principal'])
        nav_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Información de estado
        status_container = tk.Frame(nav_frame, bg=self.COLORES['fondo_principal'])
        status_container.pack(side=tk.RIGHT, fill=tk.Y, padx=(20, 0))
        
        fecha_actual = datetime.datetime.now().strftime('%d %b, %Y')
        hora_actual = datetime.datetime.now().strftime('%H:%M')
        
        fecha_label = tk.Label(status_container, text=fecha_actual,
                              font=('Inter', 11), fg=self.COLORES['texto_secundario'],
                              bg=self.COLORES['fondo_principal'])
        fecha_label.pack(anchor=tk.E)
        
        hora_label = tk.Label(status_container, text=hora_actual,
                             font=('Inter', 16, 'bold'), fg=self.COLORES['texto_principal'],
                             bg=self.COLORES['fondo_principal'])
        hora_label.pack(anchor=tk.E)
    
    def _crear_contenido_principal(self):
        """Crear el contenido principal con layout moderno"""
        
        # Container principal
        main_container = tk.Frame(self.ventana, bg=self.COLORES['fondo_principal'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=(0, 20))
        
        # Layout tipo dashboard: 70% izquierda, 30% derecha
        
        # Panel izquierdo - Menú y productos
        left_panel = tk.Frame(main_container, bg=self.COLORES['fondo_principal'])
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        # Panel derecho - Carrito
        right_panel = tk.Frame(main_container, bg=self.COLORES['fondo_principal'], width=400)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        right_panel.pack_propagate(False)
        
        # Crear contenido de paneles
        self._crear_panel_menu(left_panel)
        self._crear_panel_carrito_simple(right_panel)
    
    def _crear_panel_menu(self, parent):
        """Crear panel de menú estilo web moderno"""
        
        # Header del panel
        menu_header = tk.Frame(parent, bg=self.COLORES['fondo_principal'], height=60)
        menu_header.pack(fill=tk.X, pady=(0, 20))
        menu_header.pack_propagate(False)
        
        # Título y filtros
        header_content = tk.Frame(menu_header, bg=self.COLORES['fondo_principal'])
        header_content.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Título del menú
        menu_title = tk.Label(header_content, text="Nuestro Menú", 
                             font=('Inter', 22, 'bold'),
                             fg=self.COLORES['texto_principal'],
                             bg=self.COLORES['fondo_principal'])
        menu_title.pack(side=tk.LEFT, anchor=tk.W)
        
        # Filtro de categorías (lado derecho)
        filter_frame = tk.Frame(header_content, bg=self.COLORES['fondo_principal'])
        filter_frame.pack(side=tk.RIGHT, anchor=tk.E)
        
        tk.Label(filter_frame, text="Categoría:", 
                font=('Inter', 10), fg=self.COLORES['texto_secundario'],
                bg=self.COLORES['fondo_principal']).pack(side=tk.LEFT, padx=(0, 10))
        
        self.categoria_var = tk.StringVar()
        categorias = ["Todos"] + self.menu.obtener_categorias()
        
        # Combo estilo moderno
        combo_categoria = ttk.Combobox(filter_frame, textvariable=self.categoria_var,
                                      values=categorias, state="readonly", width=15,
                                      font=('Inter', 10))
        combo_categoria.pack(side=tk.LEFT)
        combo_categoria.bind("<<ComboboxSelected>>", lambda e: self._actualizar_items_menu())
        combo_categoria.current(0)
        
        # Grid de items del menú
        self._crear_grid_items(parent)
    
    def _crear_grid_items(self, parent):
        """Crear grid de items estilo web con cards"""
        
        # Container con scroll
        canvas = tk.Canvas(parent, bg=self.COLORES['fondo_principal'], 
                          highlightthickness=0, height=400)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.COLORES['fondo_principal'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Items en grid (3 columnas)
        self.grid_frame = scrollable_frame
        self._actualizar_grid_items()
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Guardar referencias
        self.items_canvas = canvas
        self.items_scrollbar = scrollbar
        
    def _actualizar_grid_items(self):
        """Actualizar el grid de items con cards modernas"""
        # Limpiar grid actual
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        
        categoria = self.categoria_var.get() if hasattr(self, 'categoria_var') else "Todos"
        
        if categoria == "Todos":
            items = self.menu.listar_por_categoria()
        else:
            items = self.menu.listar_por_categoria(categoria)
        
        # Crear cards en grid 3x?
        columnas = 3
        for i, item in enumerate(items):
            fila = i // columnas
            col = i % columnas
            
            # Card container
            card = tk.Frame(self.grid_frame, bg=self.COLORES['fondo_card'],
                           relief='flat', bd=1, highlightbackground=self.COLORES['borde_sutil'])
            card.grid(row=fila, column=col, padx=10, pady=10, sticky='ew')
            
            # Configurar peso de columnas
            self.grid_frame.columnconfigure(col, weight=1)
            
            # Contenido de la card
            self._crear_card_item(card, item)
    
    def _crear_card_item(self, parent, item):
        """Crear una card individual de item estilo web"""
        
        # Padding interno
        content = tk.Frame(parent, bg=self.COLORES['fondo_card'])
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Icono/imagen placeholder (emoji food)
        icons = {'Bebidas': '🥤', 'Comidas': '🍽️', 'Postres': '🍰', 'Entradas': '🥗'}
        icon = icons.get(item.categoria, '🍴')
        
        icon_label = tk.Label(content, text=icon, font=('Apple Color Emoji', 32),
                             bg=self.COLORES['fondo_card'])
        icon_label.pack(pady=(0, 10))
        
        # Nombre del item
        nombre_label = tk.Label(content, text=item.nombre,
                               font=('Inter', 12, 'bold'),
                               fg=self.COLORES['texto_principal'],
                               bg=self.COLORES['fondo_card'],
                               wraplength=150)
        nombre_label.pack(pady=(0, 5))
        
        # Descripción (si existe)
        if hasattr(item, 'descripcion') and item.descripcion:
            desc_label = tk.Label(content, text=item.descripcion[:50] + "..." if len(item.descripcion) > 50 else item.descripcion,
                                 font=('Inter', 9),
                                 fg=self.COLORES['texto_muted'],
                                 bg=self.COLORES['fondo_card'],
                                 wraplength=150)
            desc_label.pack(pady=(0, 10))
        
        # Precio destacado
        precio_frame = tk.Frame(content, bg=self.COLORES['fondo_card'])
        precio_frame.pack(fill=tk.X, pady=(0, 15))
        
        precio_label = tk.Label(precio_frame, text=f"${item.precio:,.0f}",
                               font=('Inter', 14, 'bold'),
                               fg=self.COLORES['acento_dorado'],
                               bg=self.COLORES['fondo_card'])
        precio_label.pack()
        
        # Botón de agregar moderno
        btn_agregar = self.crear_boton_ovalado(content, "Agregar al carrito", 
                                               lambda i=item: self._agregar_item_directo(i),
                                               self.COLORES['verde_success'])
        btn_agregar.pack(fill=tk.X)
    
    def crear_boton_ovalado(self, parent, texto, comando, color=None, ancho=15, alto=2):
        """Crear un botón moderno con bordes redondeados y efectos"""
        if color is None:
            color = self.COLORES['acento_dorado']
        
        # Frame contenedor para efecto de sombra
        contenedor = tk.Frame(parent, bg=parent.cget('bg'), highlightthickness=0)
        
        # Botón principal con efecto moderno
        boton = tk.Button(
            contenedor,
            text=texto,
            command=comando,
            bg=color,
            fg='white',
            font=('Inter', 10, 'bold'),
            relief=tk.FLAT,
            padx=25,
            pady=12,
            highlightthickness=0,
            activebackground=self._oscurecer_color(color),
            activeforeground='white',
            cursor='hand2',
            bd=0,
            borderwidth=0,
        )
        
        # Eventos para efectos hover mejorados
        def on_enter(e):
            boton.config(bg=self._oscurecer_color(color))
            
        def on_leave(e):
            boton.config(bg=color)
        
        boton.bind('<Enter>', on_enter)
        boton.bind('<Leave>', on_leave)
        
        boton.pack(fill=tk.BOTH, expand=True)
        
        return contenedor
    
    def _aclarar_color(self, color):
        """Aclarar un color hexadecimal para efecto hover"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        # Aclarar
        rgb = tuple(min(255, int(c * 1.2)) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*rgb)
    
    def _crear_panel_menu_simple(self, parent):
        """Crear panel de menú funcional con categorías"""
        
        # Header del panel con filtros
        header_frame = tk.Frame(parent, bg=self.COLORES['fondo_principal'])
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 0))
        
        # Título
        titulo = tk.Label(header_frame, text="📦 Menú Premium",
                         font=('Inter', 18, 'bold'),
                         fg=self.COLORES['acento_dorado'],
                         bg=self.COLORES['fondo_principal'])
        titulo.pack(side=tk.LEFT)
        
        # Filtro de categoría
        filtro_frame = tk.Frame(header_frame, bg=self.COLORES['fondo_principal'])
        filtro_frame.pack(side=tk.RIGHT)
        
        tk.Label(filtro_frame, text="Categoría:", 
                font=('Inter', 10), fg=self.COLORES['texto_secundario'],
                bg=self.COLORES['fondo_principal']).pack(side=tk.LEFT, padx=(0, 10))
        
        self.categoria_var = tk.StringVar(value="Todas")
        categorias = ["Todas"] + self.menu.obtener_categorias()
        
        combo_categoria = ttk.Combobox(filtro_frame, textvariable=self.categoria_var,
                                      values=categorias, state="readonly", width=20,
                                      font=('Inter', 10))
        combo_categoria.pack(side=tk.LEFT)
        combo_categoria.bind("<<ComboboxSelected>>", self._filtrar_menu)
        
        # Contenedor scrolleable para el menú
        canvas = tk.Canvas(parent, bg=self.COLORES['fondo_principal'], 
                          highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        self.menu_frame = tk.Frame(canvas, bg=self.COLORES['fondo_principal'])
        
        self.menu_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.menu_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=20)
        
        # Referencias para actualizar
        self.menu_canvas = canvas
        self.menu_scrollbar = scrollbar
        
        # Cargar menú inicial
        self._cargar_menu_visual()
        
    def _filtrar_menu(self, event=None):
        """Filtrar menú por categoría seleccionada"""
        self._cargar_menu_visual()
        
    def _cargar_menu_visual(self):
        """Cargar los items del menú visualmente"""
        # Limpiar contenido actual
        for widget in self.menu_frame.winfo_children():
            widget.destroy()
            
        # Obtener categoría seleccionada
        categoria = self.categoria_var.get() if hasattr(self, 'categoria_var') else "Todas"
        
        # Obtener items filtrados
        if categoria == "Todas":
            items = list(self.menu.items.values())
        else:
            items = [item for item in self.menu.items.values() if item.categoria == categoria]
        
        # Crear cards por fila (3 columnas)
        columnas = 3
        for i, item in enumerate(items):
            fila = i // columnas
            col = i % columnas
            
            # Frame para la card
            card_container = tk.Frame(self.menu_frame, bg=self.COLORES['fondo_principal'])
            card_container.grid(row=fila, column=col, padx=8, pady=8, sticky='ew')
            
            # Configurar grid
            self.menu_frame.columnconfigure(col, weight=1, minsize=200)
            
            # Crear la card del item
            self._crear_card_menu_item(card_container, item)
    
    def _crear_card_menu_item(self, parent, item):
        """Crear card individual para un item del menú"""
        
        # Card principal
        card = tk.Frame(parent, bg=self.COLORES['fondo_card'], 
                       relief='flat', bd=1, padx=15, pady=15)
        card.pack(fill=tk.BOTH, expand=True)
        
        # Emoji por categoría
        emojis = {
            'Entradas': '🥗', 'Platos Principales': '�️', 'Ensaladas': '🥙',
            'Bebidas': '🥤', 'Bebidas Alcohólicas': '🍷', 'Postres': '🍰',
            'Acompañamientos': '🍟'
        }
        emoji = emojis.get(item.categoria, '🍴')
        
        # Icono
        icon_label = tk.Label(card, text=emoji, font=('Apple Color Emoji', 24),
                             bg=self.COLORES['fondo_card'])
        icon_label.pack(pady=(0, 8))
        
        # Nombre del plato
        nombre_label = tk.Label(card, text=item.nombre,
                               font=('Inter', 11, 'bold'),
                               fg=self.COLORES['texto_principal'],
                               bg=self.COLORES['fondo_card'],
                               wraplength=180, justify=tk.CENTER)
        nombre_label.pack(pady=(0, 5))
        
        # Descripción
        if item.descripcion:
            desc_text = item.descripcion[:60] + "..." if len(item.descripcion) > 60 else item.descripcion
            desc_label = tk.Label(card, text=desc_text,
                                 font=('Inter', 9),
                                 fg=self.COLORES['texto_muted'],
                                 bg=self.COLORES['fondo_card'],
                                 wraplength=180, justify=tk.CENTER)
            desc_label.pack(pady=(0, 8))
        
        # Precio destacado
        precio_label = tk.Label(card, text=f"${item.precio:,.0f}",
                               font=('Inter', 14, 'bold'),
                               fg=self.COLORES['acento_dorado'],
                               bg=self.COLORES['fondo_card'])
        precio_label.pack(pady=(0, 10))
        
        # Botón agregar
        btn_agregar = self.crear_boton_ovalado(card, "Agregar", 
                                               lambda i=item: self._agregar_al_carrito_real(i),
                                               self.COLORES['verde_success'])
        btn_agregar.pack(fill=tk.X)
        
    def _agregar_al_carrito_real(self, item):
        """Agregar item real al carrito"""
        try:
            self.pedido.agregar_item(item.nombre, item.precio, 1)
            self._actualizar_carrito_real()
            self._mostrar_notificacion_real(f"✅ {item.nombre} agregado al carrito")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar al carrito: {e}")
        
    def _crear_panel_carrito_simple(self, parent):
        """Crear panel de carrito funcional"""
        
        # Card principal del carrito
        card = tk.Frame(parent, bg=self.COLORES['fondo_card'])
        card.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header del carrito
        header = tk.Frame(card, bg=self.COLORES['fondo_card'])
        header.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        titulo = tk.Label(header, text="🛒 Tu Pedido",
                         font=('Inter', 16, 'bold'),
                         fg=self.COLORES['texto_principal'],
                         bg=self.COLORES['fondo_card'])
        titulo.pack(side=tk.LEFT)
        
        # Botón limpiar carrito
        btn_limpiar = tk.Button(header, text="🗑️",
                               font=('Inter', 14), 
                               bg=self.COLORES['rojo_danger'], fg='white',
                               relief='flat', bd=0, width=3,
                               command=self._limpiar_carrito_real)
        btn_limpiar.pack(side=tk.RIGHT)
        
        # Separador
        sep = tk.Frame(card, bg=self.COLORES['borde_sutil'], height=1)
        sep.pack(fill=tk.X, padx=20)
        
        # Lista de items del carrito (scrolleable)
        items_frame = tk.Frame(card, bg=self.COLORES['fondo_card'])
        items_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Canvas para scroll
        canvas_carrito = tk.Canvas(items_frame, bg=self.COLORES['fondo_card'],
                                  highlightthickness=0, height=300)
        scrollbar_carrito = ttk.Scrollbar(items_frame, orient="vertical", 
                                         command=canvas_carrito.yview)
        
        self.carrito_items_frame = tk.Frame(canvas_carrito, bg=self.COLORES['fondo_card'])
        self.carrito_items_frame.bind(
            "<Configure>",
            lambda e: canvas_carrito.configure(scrollregion=canvas_carrito.bbox("all"))
        )
        
        canvas_carrito.create_window((0, 0), window=self.carrito_items_frame, anchor="nw")
        canvas_carrito.configure(yscrollcommand=scrollbar_carrito.set)
        
        canvas_carrito.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_carrito.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Referencias
        self.canvas_carrito = canvas_carrito
        self.scrollbar_carrito = scrollbar_carrito
        
        # Resumen del pedido
        self._crear_resumen_carrito_real(card)
        
        # Mensaje inicial
        self._mostrar_carrito_vacio()
        
    def _crear_resumen_carrito_real(self, parent):
        """Crear sección de resumen real"""
        
        # Separador
        sep = tk.Frame(parent, bg=self.COLORES['borde_sutil'], height=1)
        sep.pack(fill=tk.X, padx=20, pady=(10, 15))
        
        # Frame de totales
        totales_frame = tk.Frame(parent, bg=self.COLORES['fondo_card'])
        totales_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Labels de información
        self.items_count_label = tk.Label(totales_frame, text="Items: 0",
                                         font=('Inter', 10),
                                         fg=self.COLORES['texto_secundario'],
                                         bg=self.COLORES['fondo_card'])
        self.items_count_label.pack(anchor=tk.W)
        
        self.subtotal_label = tk.Label(totales_frame, text="Subtotal: $0",
                                      font=('Inter', 11),
                                      fg=self.COLORES['texto_secundario'],
                                      bg=self.COLORES['fondo_card'])
        self.subtotal_label.pack(anchor=tk.W, pady=(5, 0))
        
        self.total_label = tk.Label(totales_frame, text="TOTAL: $0",
                                   font=('Inter', 16, 'bold'),
                                   fg=self.COLORES['acento_dorado'],
                                   bg=self.COLORES['fondo_card'])
        self.total_label.pack(anchor=tk.W, pady=(8, 0))
        
        # Botones de acción
        botones_frame = tk.Frame(parent, bg=self.COLORES['fondo_card'])
        botones_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Botón de procesar pedido
        self.btn_procesar = self.crear_boton_ovalado(botones_frame, "💳 Procesar Pedido", 
                                                    self._procesar_pedido_real,
                                                    self.COLORES['verde_success'])
        self.btn_procesar.pack(fill=tk.X)
        
    def _mostrar_carrito_vacio(self):
        """Mostrar mensaje de carrito vacío"""
        for widget in self.carrito_items_frame.winfo_children():
            widget.destroy()
            
        mensaje = tk.Label(self.carrito_items_frame, 
                          text="🛒\n\nCarrito vacío\nAgrega items del menú",
                          font=('Inter', 12),
                          fg=self.COLORES['texto_muted'],
                          bg=self.COLORES['fondo_card'],
                          justify=tk.CENTER)
        mensaje.pack(expand=True, pady=50)
        
    def _actualizar_carrito_real(self):
        """Actualizar visualización del carrito"""
        # Limpiar items actuales
        for widget in self.carrito_items_frame.winfo_children():
            widget.destroy()
        
        if not self.pedido.items:
            self._mostrar_carrito_vacio()
            self._actualizar_totales_carrito()
            return
        
        # Mostrar items del carrito
        for i, item in enumerate(self.pedido.items):
            item_frame = tk.Frame(self.carrito_items_frame, bg=self.COLORES['fondo_card'])
            item_frame.pack(fill=tk.X, pady=5, padx=10)
            
            # Info del item
            info_frame = tk.Frame(item_frame, bg=self.COLORES['fondo_card'])
            info_frame.pack(fill=tk.X)
            
            # Nombre del item
            nombre_label = tk.Label(info_frame, text=item['nombre'],
                                   font=('Inter', 10, 'bold'),
                                   fg=self.COLORES['texto_principal'],
                                   bg=self.COLORES['fondo_card'])
            nombre_label.pack(anchor=tk.W)
            
            # Controles de cantidad
            control_frame = tk.Frame(info_frame, bg=self.COLORES['fondo_card'])
            control_frame.pack(fill=tk.X, pady=(3, 0))
            
            # Botón menos
            btn_menos = tk.Button(control_frame, text="−", width=3,
                                 font=('Inter', 10, 'bold'),
                                 bg=self.COLORES['rojo_danger'], fg='white',
                                 relief='flat', bd=0,
                                 command=lambda idx=i: self._decrementar_item_real(idx))
            btn_menos.pack(side=tk.LEFT)
            
            # Cantidad
            qty_label = tk.Label(control_frame, text=f"  {item['cantidad']}  ",
                                font=('Inter', 10, 'bold'),
                                fg=self.COLORES['texto_principal'],
                                bg=self.COLORES['fondo_card'])
            qty_label.pack(side=tk.LEFT)
            
            # Botón más
            btn_mas = tk.Button(control_frame, text="+", width=3,
                               font=('Inter', 10, 'bold'),
                               bg=self.COLORES['verde_success'], fg='white',
                               relief='flat', bd=0,
                               command=lambda idx=i: self._incrementar_item_real(idx))
            btn_mas.pack(side=tk.LEFT)
            
            # Precio total del item
            precio_item = item['precio'] * item['cantidad']
            precio_label = tk.Label(control_frame, text=f"${precio_item:,.0f}",
                                   font=('Inter', 11, 'bold'),
                                   fg=self.COLORES['acento_dorado'],
                                   bg=self.COLORES['fondo_card'])
            precio_label.pack(side=tk.RIGHT)
            
            # Separador entre items
            if i < len(self.pedido.items) - 1:
                sep = tk.Frame(item_frame, bg=self.COLORES['borde_sutil'], height=1)
                sep.pack(fill=tk.X, pady=(5, 0))
        
        # Actualizar totales
        self._actualizar_totales_carrito()
        
    def _actualizar_totales_carrito(self):
        """Actualizar los totales mostrados"""
        total_items = len(self.pedido.items)
        subtotal = self.pedido.calcular_total()
        
        self.items_count_label.config(text=f"Items: {total_items}")
        self.subtotal_label.config(text=f"Subtotal: ${subtotal:,.0f}")
        self.total_label.config(text=f"TOTAL: ${subtotal:,.0f}")
        
    def _incrementar_item_real(self, indice):
        """Incrementar cantidad de un item en el carrito"""
        if 0 <= indice < len(self.pedido.items):
            self.pedido.items[indice]['cantidad'] += 1
            self._actualizar_carrito_real()
    
    def _decrementar_item_real(self, indice):
        """Decrementar cantidad de un item en el carrito"""
        if 0 <= indice < len(self.pedido.items):
            if self.pedido.items[indice]['cantidad'] > 1:
                self.pedido.items[indice]['cantidad'] -= 1
            else:
                # Eliminar item si cantidad es 0
                del self.pedido.items[indice]
            self._actualizar_carrito_real()
    
    def _limpiar_carrito_real(self):
        """Limpiar todo el carrito"""
        self.pedido.items.clear()
        self._actualizar_carrito_real()
        self._mostrar_notificacion_real("🗑️ Carrito limpiado")
    
    def _procesar_pedido_real(self):
        """Procesar el pedido actual - Ventana única"""
        if not self.pedido.items:
            messagebox.showwarning("Carrito Vacío", "Agrega items al carrito antes de procesar el pedido.")
            return
        
        self._mostrar_ventana_checkout_completa()
    
    def _mostrar_ventana_checkout_completa(self):
        """Mostrar ventana única de checkout con todos los datos"""
        self._mostrar_ventana_checkout()
    
    def _agregar_item_directo(self, item):
        """Método temporal para agregar item"""
        pass
    
    def _mostrar_notificacion(self, mensaje):
        """Método temporal para notificaciones"""
        pass
    
    def _mostrar_notificacion_real(self, mensaje):
        """Mostrar notificación toast moderna"""
        # Crear ventana temporal
        toast = tk.Toplevel(self.ventana)
        toast.title("")
        toast.overrideredirect(True)
        toast.attributes('-topmost', True)
        
        # Posición en la esquina superior derecha
        x = self.ventana.winfo_x() + self.ventana.winfo_width() - 300
        y = self.ventana.winfo_y() + 100
        toast.geometry(f"280x60+{x}+{y}")
        
        # Estilo del toast
        color = self.COLORES['verde_success'] if '✅' in mensaje else self.COLORES['azul_info']
        toast.config(bg=color)
        
        label = tk.Label(toast, text=mensaje,
                        font=('Inter', 11, 'bold'),
                        fg='white', bg=color)
        label.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Auto-cerrar después de 2.5 segundos
        toast.after(2500, toast.destroy)
    
    def _mostrar_ventana_checkout(self):
        """Mostrar ventana consolidada de checkout con ITBMS, descuento y método de pago"""
        
        # Crear ventana modal
        checkout = tk.Toplevel(self.ventana)
        checkout.title("Procesar Pago")
        checkout.geometry("700x900")
        checkout.resizable(False, False)
        checkout.configure(bg=self.COLORES['fondo_principal'])
        checkout.grab_set()
        checkout.transient(self.ventana)
        
        # Centrar ventana
        checkout.update_idletasks()
        x = (checkout.winfo_screenwidth() // 2) - (350)
        y = (checkout.winfo_screenheight() // 2) - (450)
        checkout.geometry(f"+{x}+{y}")
        
        # Container principal con scroll
        main_canvas = tk.Canvas(checkout, bg=self.COLORES['fondo_principal'],
                               highlightthickness=0)
        scrollbar = ttk.Scrollbar(checkout, orient="vertical", command=main_canvas.yview)
        scrollable_frame = tk.Frame(main_canvas, bg=self.COLORES['fondo_principal'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Header
        header = tk.Label(scrollable_frame, text="🧾 Procesar Pago",
                         font=('Inter', 22, 'bold'),
                         fg=self.COLORES['acento_dorado'],
                         bg=self.COLORES['fondo_principal'])
        header.pack(pady=20)
        
        # ==================== SECCIÓN 1: INFORMACIÓN DEL CLIENTE ====================
        cliente_frame = tk.LabelFrame(scrollable_frame, text="📝 Información del Cliente",
                                     bg=self.COLORES['fondo_card'],
                                     fg=self.COLORES['acento_dorado'],
                                     font=('Inter', 11, 'bold'),
                                     padx=20, pady=15)
        cliente_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Mesa
        mesa_frame = tk.Frame(cliente_frame, bg=self.COLORES['fondo_card'])
        mesa_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(mesa_frame, text="Mesa:", font=('Inter', 10, 'bold'),
                bg=self.COLORES['fondo_card'], fg=self.COLORES['texto_principal']).pack(side=tk.LEFT, anchor=tk.W, width=15)
        
        mesa_var = tk.StringVar()
        mesa_entry = tk.Entry(mesa_frame, textvariable=mesa_var, font=('Inter', 11),
                             bg='white', width=20)
        mesa_entry.pack(side=tk.LEFT, padx=10)
        mesa_entry.focus()
        
        # Mesero
        mesero_frame = tk.Frame(cliente_frame, bg=self.COLORES['fondo_card'])
        mesero_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(mesero_frame, text="Mesero:", font=('Inter', 10, 'bold'),
                bg=self.COLORES['fondo_card'], fg=self.COLORES['texto_principal']).pack(side=tk.LEFT, anchor=tk.W, width=15)
        
        mesero_var = tk.StringVar(value="Admin")
        mesero_entry = tk.Entry(mesero_frame, textvariable=mesero_var, font=('Inter', 11),
                               bg='white', width=20)
        mesero_entry.pack(side=tk.LEFT, padx=10)
        
        # ==================== SECCIÓN 2: RESUMEN DEL PEDIDO ====================
        resumen_frame = tk.LabelFrame(scrollable_frame, text="🛒 Resumen del Pedido",
                                     bg=self.COLORES['fondo_card'],
                                     fg=self.COLORES['acento_dorado'],
                                     font=('Inter', 11, 'bold'),
                                     padx=15, pady=10)
        resumen_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        
        # Encabezado de items
        header_frame = tk.Frame(resumen_frame, bg=self.COLORES['fondo_card'])
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(header_frame, text="Descripción", font=('Inter', 9, 'bold'),
                fg=self.COLORES['texto_principal'], bg=self.COLORES['fondo_card'],
                anchor=tk.W).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(header_frame, text="Cant.", font=('Inter', 9, 'bold'),
                fg=self.COLORES['texto_principal'], bg=self.COLORES['fondo_card'],
                width=5).pack(side=tk.LEFT, padx=5)
        
        tk.Label(header_frame, text="Precio", font=('Inter', 9, 'bold'),
                fg=self.COLORES['texto_principal'], bg=self.COLORES['fondo_card'],
                width=10).pack(side=tk.LEFT, padx=5)
        
        tk.Label(header_frame, text="Total", font=('Inter', 9, 'bold'),
                fg=self.COLORES['acento_dorado'], bg=self.COLORES['fondo_card'],
                width=10).pack(side=tk.LEFT, padx=5)
        
        # Línea divisora
        tk.Label(resumen_frame, text="─" * 70, font=('Inter', 8),
                fg=self.COLORES['borde_sutil'], bg=self.COLORES['fondo_card']).pack()
        
        # Lista de items
        items_container = tk.Frame(resumen_frame, bg=self.COLORES['fondo_card'])
        items_container.pack(fill=tk.BOTH, expand=True, pady=5)
        
        for item in self.pedido.items:
            item_line = tk.Frame(items_container, bg=self.COLORES['fondo_card'])
            item_line.pack(fill=tk.X, pady=2)
            
            tk.Label(item_line, text=item['nombre'], font=('Inter', 9),
                    fg=self.COLORES['texto_principal'], bg=self.COLORES['fondo_card'],
                    anchor=tk.W, justify=tk.LEFT).pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            tk.Label(item_line, text=str(item['cantidad']), font=('Inter', 9),
                    fg=self.COLORES['texto_principal'], bg=self.COLORES['fondo_card'],
                    width=5).pack(side=tk.LEFT, padx=5)
            
            tk.Label(item_line, text=f"${item['precio']:,.0f}", font=('Inter', 9),
                    fg=self.COLORES['texto_principal'], bg=self.COLORES['fondo_card'],
                    width=10, anchor=tk.E).pack(side=tk.LEFT, padx=5)
            
            subtotal_item = item['precio'] * item['cantidad']
            tk.Label(item_line, text=f"${subtotal_item:,.0f}", font=('Inter', 9, 'bold'),
                    fg=self.COLORES['acento_dorado'], bg=self.COLORES['fondo_card'],
                    width=10, anchor=tk.E).pack(side=tk.LEFT, padx=5)
        
        # ==================== SECCIÓN 3: CÁLCULOS Y TOTALES ====================
        calculos_frame = tk.LabelFrame(scrollable_frame, text="💰 Cálculo de Totales",
                                      bg=self.COLORES['fondo_card'],
                                      fg=self.COLORES['acento_dorado'],
                                      font=('Inter', 11, 'bold'),
                                      padx=20, pady=15)
        calculos_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Subtotal
        subtotal_line = tk.Frame(calculos_frame, bg=self.COLORES['fondo_card'])
        subtotal_line.pack(fill=tk.X, pady=5)
        
        tk.Label(subtotal_line, text="Subtotal:", font=('Inter', 11),
                fg=self.COLORES['texto_principal'], bg=self.COLORES['fondo_card']).pack(side=tk.LEFT)
        
        subtotal = self.pedido.calcular_total()
        lbl_subtotal = tk.Label(subtotal_line, text=f"${subtotal:,.0f}",
                               font=('Inter', 11, 'bold'),
                               fg=self.COLORES['texto_principal'],
                               bg=self.COLORES['fondo_card'])
        lbl_subtotal.pack(side=tk.RIGHT)
        
        # ITBMS (Impuesto 19%)
        itbms_line = tk.Frame(calculos_frame, bg=self.COLORES['fondo_card'])
        itbms_line.pack(fill=tk.X, pady=5)
        
        tk.Label(itbms_line, text="ITBMS (19%):", font=('Inter', 11),
                fg=self.COLORES['texto_principal'], bg=self.COLORES['fondo_card']).pack(side=tk.LEFT)
        
        itbms = subtotal * 0.19
        lbl_itbms = tk.Label(itbms_line, text=f"${itbms:,.0f}",
                            font=('Inter', 11, 'bold'),
                            fg=self.COLORES['texto_principal'],
                            bg=self.COLORES['fondo_card'])
        lbl_itbms.pack(side=tk.RIGHT)
        
        # Descuento
        descuento_line = tk.Frame(calculos_frame, bg=self.COLORES['fondo_card'])
        descuento_line.pack(fill=tk.X, pady=5)
        
        tk.Label(descuento_line, text="Descuento:", font=('Inter', 10),
                fg=self.COLORES['texto_principal'], bg=self.COLORES['fondo_card']).pack(side=tk.LEFT)
        
        descuento_var = tk.StringVar(value="0")
        descuento_entry = tk.Entry(descuento_line, textvariable=descuento_var, font=('Inter', 10),
                                  bg='white', width=12)
        descuento_entry.pack(side=tk.RIGHT, padx=5)
        
        def actualizar_totales(*args):
            try:
                desc = float(descuento_var.get() or 0)
                total_final = subtotal + itbms - desc
                lbl_total.config(text=f"${total_final:,.0f}")
            except ValueError:
                pass
        
        descuento_var.trace_add("write", actualizar_totales)
        
        # Línea divisora
        tk.Label(calculos_frame, text="="*50, font=('Inter', 9),
                fg=self.COLORES['borde_sutil'], bg=self.COLORES['fondo_card']).pack(pady=5)
        
        # Total final
        total_line = tk.Frame(calculos_frame, bg=self.COLORES['fondo_card'])
        total_line.pack(fill=tk.X, pady=10)
        
        tk.Label(total_line, text="TOTAL:", font=('Inter', 13, 'bold'),
                fg=self.COLORES['acento_dorado'], bg=self.COLORES['fondo_card']).pack(side=tk.LEFT)
        
        total_inicial = subtotal + itbms
        lbl_total = tk.Label(total_line, text=f"${total_inicial:,.0f}",
                            font=('Inter', 14, 'bold'),
                            fg=self.COLORES['acento_dorado'],
                            bg=self.COLORES['fondo_card'])
        lbl_total.pack(side=tk.RIGHT)
        
        # ==================== SECCIÓN 4: MÉTODO DE PAGO ====================
        pago_frame = tk.LabelFrame(scrollable_frame, text="💳 Método de Pago",
                                  bg=self.COLORES['fondo_card'],
                                  fg=self.COLORES['acento_dorado'],
                                  font=('Inter', 11, 'bold'),
                                  padx=20, pady=15)
        pago_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        metodo_pago_var = tk.StringVar(value="Efectivo")
        
        metodos = ["Efectivo", "Tarjeta Crédito", "Tarjeta Débito", "Transferencia"]
        for metodo in metodos:
            rb = tk.Radiobutton(pago_frame, text=metodo, variable=metodo_pago_var,
                               value=metodo, font=('Inter', 10),
                               bg=self.COLORES['fondo_card'],
                               fg=self.COLORES['texto_principal'],
                               selectcolor=self.COLORES['acento_dorado'],
                               activebackground=self.COLORES['fondo_card'])
            rb.pack(anchor=tk.W, pady=5)
        
        # ==================== BOTONES DE ACCIÓN ====================
        botones_frame = tk.Frame(scrollable_frame, bg=self.COLORES['fondo_principal'])
        botones_frame.pack(fill=tk.X, padx=20, pady=20)
        
        def confirmar_pago():
            mesa = mesa_var.get().strip()
            mesero = mesero_var.get().strip()
            
            if not mesa:
                messagebox.showerror("Error", "Por favor ingresa el número de mesa")
                mesa_entry.focus()
                return
            
            try:
                desc = float(descuento_var.get() or 0)
            except ValueError:
                messagebox.showerror("Error", "El descuento debe ser un número válido")
                descuento_entry.focus()
                return
            
            # Calcular totales finales
            subtotal_final = subtotal
            itbms_final = subtotal_final * 0.19
            total_final = subtotal_final + itbms_final - desc
            
            # Crear datos de factura
            factura_data = {
                'numero': f"FACT-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                'fecha': datetime.datetime.now().strftime("%Y-%m-%d"),
                'hora': datetime.datetime.now().strftime("%H:%M:%S"),
                'mesa': mesa,
                'mesero': mesero,
                'items': self.pedido.items.copy(),
                'subtotal': subtotal_final,
                'itbms': itbms_final,
                'descuento': desc,
                'total': total_final,
                'metodo_pago': metodo_pago_var.get(),
                'restaurante': self.nombre_negocio.get(),
                'nit': self.nit_negocio.get()
            }
            
            # Guardar en historial
            if not hasattr(self, 'historial_ventas'):
                self.historial_ventas = []
            self.historial_ventas.append(factura_data)
            
            # Cerrar checkout y mostrar invoice
            checkout.destroy()
            self._mostrar_invoice_directo(factura_data)
            
            # Limpiar carrito
            self.pedido.items.clear()
            self._actualizar_carrito_real()
            
            # Notificación
            self._mostrar_notificacion_real(f"✅ Pago procesado - Factura: {factura_data['numero']}")
        
        # Botón cancelar
        btn_cancelar = self.crear_boton_ovalado(botones_frame, "❌ Cancelar",
                                               lambda: checkout.destroy(),
                                               self.COLORES['rojo_danger'])
        btn_cancelar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Botón procesar pago
        btn_pagar = self.crear_boton_ovalado(botones_frame, "💳 Procesar Pago",
                                            confirmar_pago,
                                            self.COLORES['verde_success'])
        btn_pagar.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))
    
    def _finalizar_pedido_real(self, mesa, mesero):
        """Finalizar el pedido y generar factura"""
        try:
            # Generar número de factura único
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            numero_factura = f"FACT-{timestamp}"
            
            # Crear datos de la factura
            factura_data = {
                'numero': numero_factura,
                'fecha': datetime.datetime.now().strftime("%Y-%m-%d"),
                'hora': datetime.datetime.now().strftime("%H:%M:%S"),
                'mesa': mesa,
                'mesero': mesero,
                'items': self.pedido.items.copy(),
                'subtotal': self.pedido.calcular_total(),
                'total': self.pedido.calcular_total(),
                'restaurante': self.nombre_negocio.get(),
                'nit': self.nit_negocio.get()
            }
            
            # Guardar en historial
            if not hasattr(self, 'historial_ventas'):
                self.historial_ventas = []
            self.historial_ventas.append(factura_data)
            
            # Mostrar opciones de impresión
            self._mostrar_opciones_factura(factura_data)
            
            # Limpiar carrito
            self.pedido.items.clear()
            self._actualizar_carrito_real()
            
            # Notificación de éxito
            self._mostrar_notificacion_real(f"✅ Pedido procesado exitosamente - Factura: {numero_factura}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar el pedido:\n{str(e)}")
    
    def _mostrar_opciones_factura(self, factura_data):
        """Mostrar opciones para la factura generada"""
        
        respuesta = messagebox.askyesnocancel(
            "Factura Generada",
            f"Pedido procesado exitosamente\n\n"
            f"📋 Factura: {factura_data['numero']}\n"
            f"🍽️ Mesa: {factura_data['mesa']}\n"
            f"👤 Mesero: {factura_data['mesero']}\n"
            f"💰 Total: ${factura_data['total']:,.0f}\n\n"
            "¿Qué deseas hacer?\n\n"
            "✅ SÍ = Imprimir factura\n"
            "❌ NO = Solo guardar\n"
            "🔍 CANCELAR = Ver vista previa"
        )
        
        if respuesta is True:  # Sí - Imprimir
            self._imprimir_factura_real(factura_data)
        elif respuesta is False:  # No - Solo guardar
            messagebox.showinfo("Guardado", "✅ Factura guardada correctamente en el sistema")
        else:  # Cancelar - Vista previa
            self._vista_previa_factura_real(factura_data)

    def _imprimir_factura_real(self, factura_data):
        """Imprimir la factura usando CUPS en Linux"""
        try:
            # Crear contenido de la factura
            contenido_factura = self._generar_contenido_factura(factura_data)
            
            # Crear archivo temporal
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
                temp_file.write(contenido_factura)
                temp_filename = temp_file.name
            
            # Mostrar diálogo de impresión CUPS
            self._mostrar_dialog_impresion_real(temp_filename, factura_data)
            
        except Exception as e:
            messagebox.showerror("Error de Impresión", 
                               f"No se pudo imprimir la factura:\n{str(e)}")
    
    def _mostrar_dialog_impresion_real(self, archivo, factura_data):
        """Mostrar diálogo de impresión CUPS"""
        
        # Ventana del diálogo
        dialog = tk.Toplevel(self.ventana)
        dialog.title("🖨️ Imprimir Factura")
        dialog.geometry("500x400")
        dialog.configure(bg=self.COLORES['fondo_principal'])
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.transient(self.ventana)
        
        # Centrar ventana
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - 250
        y = (dialog.winfo_screenheight() // 2) - 200
        dialog.geometry(f"+{x}+{y}")
        
        main_frame = tk.Frame(dialog, bg=self.COLORES['fondo_principal'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_label = tk.Label(main_frame, text="🖨️ Configuración de Impresión",
                               font=('Inter', 16, 'bold'),
                               fg=self.COLORES['acento_dorado'],
                               bg=self.COLORES['fondo_principal'])
        header_label.pack(pady=(0, 20))
        
        # Info de la factura
        info_frame = tk.Frame(main_frame, bg=self.COLORES['fondo_card'], padx=15, pady=10)
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(info_frame, text=f"📋 Factura: {factura_data['numero']}",
                font=('Inter', 11, 'bold'), fg=self.COLORES['texto_principal'],
                bg=self.COLORES['fondo_card']).pack(anchor=tk.W)
        
        tk.Label(info_frame, text=f"🍽️ Mesa: {factura_data['mesa']} | 💰 Total: ${factura_data['total']:,.0f}",
                font=('Inter', 10), fg=self.COLORES['texto_secundario'],
                bg=self.COLORES['fondo_card']).pack(anchor=tk.W, pady=(5, 0))
        
        # Obtener impresoras disponibles
        try:
            result = subprocess.run(['lpstat', '-p'], capture_output=True, text=True)
            impresoras = []
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line.startswith('printer '):
                        nombre = line.split()[1]
                        impresoras.append(nombre)
            
            if not impresoras:
                impresoras = ['Impresora por defecto']
        except:
            impresoras = ['Impresora por defecto']
        
        # Selector de impresora
        printer_frame = tk.Frame(main_frame, bg=self.COLORES['fondo_principal'])
        printer_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(printer_frame, text="Impresora:", font=('Inter', 11, 'bold'),
                fg=self.COLORES['texto_principal'], bg=self.COLORES['fondo_principal']).pack(anchor=tk.W)
        
        impresora_var = tk.StringVar(value=impresoras[0] if impresoras else "Sin impresoras")
        combo_impresora = ttk.Combobox(printer_frame, textvariable=impresora_var,
                                      values=impresoras, state="readonly", width=40)
        combo_impresora.pack(fill=tk.X, pady=(5, 0))
        
        # Opciones de impresión
        opciones_frame = tk.LabelFrame(main_frame, text="Opciones", 
                                      bg=self.COLORES['fondo_card'],
                                      fg=self.COLORES['texto_principal'],
                                      font=('Inter', 10, 'bold'))
        opciones_frame.pack(fill=tk.X, pady=(0, 20))
        
        copias_frame = tk.Frame(opciones_frame, bg=self.COLORES['fondo_card'])
        copias_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(copias_frame, text="Copias:", font=('Inter', 10),
                bg=self.COLORES['fondo_card'], fg=self.COLORES['texto_principal']).pack(side=tk.LEFT)
        
        copias_var = tk.IntVar(value=1)
        copias_spinbox = ttk.Spinbox(copias_frame, from_=1, to=10, width=5, 
                                    textvariable=copias_var)
        copias_spinbox.pack(side=tk.RIGHT)
        
        # Botones de acción
        botones_frame = tk.Frame(main_frame, bg=self.COLORES['fondo_principal'])
        botones_frame.pack(fill=tk.X, pady=(20, 0))
        
        def imprimir():
            try:
                impresora = impresora_var.get()
                copias = copias_var.get()
                
                if impresora == "Sin impresoras":
                    messagebox.showwarning("Sin Impresoras", "No hay impresoras disponibles")
                    return
                
                # Comando de impresión CUPS
                cmd = ['lp']
                if impresora != "Impresora por defecto":
                    cmd.extend(['-d', impresora])
                cmd.extend(['-n', str(copias)])
                cmd.extend(['-t', f"Factura_{factura_data['numero']}"])
                cmd.append(archivo)
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    messagebox.showinfo("Éxito", f"✅ Factura enviada a impresión\n\nImpresora: {impresora}\nCopias: {copias}")
                    dialog.destroy()
                    # Limpiar archivo temporal
                    try:
                        os.unlink(archivo)
                    except:
                        pass
                else:
                    messagebox.showerror("Error", f"Error al imprimir:\n{result.stderr}")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error en el sistema de impresión:\n{str(e)}")
        
        def vista_previa():
            dialog.destroy()
            self._vista_previa_factura_real(factura_data)
        
        # Botón Vista Previa
        btn_vista = self.crear_boton_ovalado(botones_frame, "🔍 Vista Previa",
                                            vista_previa,
                                            self.COLORES['azul_info'])
        btn_vista.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Botón Cancelar
        btn_cancelar = self.crear_boton_ovalado(botones_frame, "❌ Cancelar",
                                               lambda: dialog.destroy(),
                                               self.COLORES['rojo_danger'])
        btn_cancelar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        
        # Botón Imprimir
        btn_imprimir = self.crear_boton_ovalado(botones_frame, "🖨️ Imprimir",
                                               imprimir,
                                               self.COLORES['verde_success'])
        btn_imprimir.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
    
    def _mostrar_invoice_directo(self, factura_data):
        """Mostrar la factura final con opción de imprimir"""
        
        # Ventana de factura final
        invoice_window = tk.Toplevel(self.ventana)
        invoice_window.title("📋 Factura Final")
        invoice_window.geometry("650x900")
        invoice_window.configure(bg=self.COLORES['fondo_principal'])
        invoice_window.transient(self.ventana)
        
        # Centrar ventana
        invoice_window.update_idletasks()
        x = (invoice_window.winfo_screenwidth() // 2) - 325
        y = (invoice_window.winfo_screenheight() // 2) - 450
        invoice_window.geometry(f"+{x}+{y}")
        
        main_frame = tk.Frame(invoice_window, bg=self.COLORES['fondo_principal'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_label = tk.Label(main_frame, text="📋 Factura Final",
                               font=('Inter', 18, 'bold'),
                               fg=self.COLORES['acento_dorado'],
                               bg=self.COLORES['fondo_principal'])
        header_label.pack(pady=(0, 20))
        
        # Frame de contenido con scroll
        content_canvas = tk.Canvas(main_frame, bg='white', relief='solid', bd=1,
                                  highlightthickness=0)
        content_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, 
                                         command=content_canvas.yview)
        content_frame = tk.Frame(content_canvas, bg='white')
        
        content_frame.bind(
            "<Configure>",
            lambda e: content_canvas.configure(scrollregion=content_canvas.bbox("all"))
        )
        
        content_canvas.create_window((0, 0), window=content_frame, anchor="nw")
        content_canvas.configure(yscrollcommand=content_scrollbar.set)
        
        content_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=(0, 20))
        content_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 20))
        
        # Generar contenido de factura formateado
        contenido_texto = self._generar_contenido_factura(factura_data)
        
        # Mostrar contenido línea por línea con formato
        for linea in contenido_texto.split('\n'):
            if 'FACTURA' in linea or '=' in linea:
                label = tk.Label(content_frame, text=linea, font=('Courier', 11, 'bold'),
                               fg=self.COLORES['acento_dorado'], bg='white', justify=tk.CENTER)
            elif linea.strip() and ('$' in linea or ':' in linea):
                label = tk.Label(content_frame, text=linea, font=('Courier', 10),
                               fg='black', bg='white', justify=tk.LEFT)
            else:
                label = tk.Label(content_frame, text=linea, font=('Courier', 9),
                               fg='#666666', bg='white', justify=tk.LEFT)
            label.pack(fill=tk.X, padx=15, pady=2)
        
        # Botones de acción
        botones_frame = tk.Frame(main_frame, bg=self.COLORES['fondo_principal'])
        botones_frame.pack(fill=tk.X, pady=(0, 0))
        
        def imprimir_invoice():
            try:
                contenido_factura = self._generar_contenido_factura(factura_data)
                with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
                    temp_file.write(contenido_factura)
                    temp_filename = temp_file.name
                
                self._mostrar_dialog_impresion_real(temp_filename, factura_data)
                self._mostrar_notificacion_real("✅ Factura enviada a la impresora")
                
            except Exception as e:
                messagebox.showerror("Error de Impresión", 
                                   f"No se pudo imprimir la factura:\n{str(e)}")
        
        # Botón cerrar
        btn_cerrar = self.crear_boton_ovalado(botones_frame, "❌ Cerrar",
                                             lambda: invoice_window.destroy(),
                                             self.COLORES['gris_neutral'])
        btn_cerrar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Botón imprimir
        btn_imprimir = self.crear_boton_ovalado(botones_frame, "🖨️ Imprimir Factura",
                                               imprimir_invoice,
                                               self.COLORES['verde_success'])
        btn_imprimir.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))
    
    def _vista_previa_factura_real(self, factura_data):
        """Mostrar vista previa de la factura"""
        
        # Ventana de vista previa
        preview = tk.Toplevel(self.ventana)
        preview.title("🔍 Vista Previa - Factura")
        preview.geometry("600x800")
        preview.configure(bg=self.COLORES['fondo_principal'])
        preview.transient(self.ventana)
        
        # Centrar ventana
        preview.update_idletasks()
        x = (preview.winfo_screenwidth() // 2) - 300
        y = (preview.winfo_screenheight() // 2) - 400
        preview.geometry(f"+{x}+{y}")
        
        main_frame = tk.Frame(preview, bg=self.COLORES['fondo_principal'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_label = tk.Label(main_frame, text="🔍 Vista Previa de Factura",
                               font=('Inter', 16, 'bold'),
                               fg=self.COLORES['acento_dorado'],
                               bg=self.COLORES['fondo_principal'])
        header_label.pack(pady=(0, 20))
        
        # Contenido de la factura
        factura_frame = tk.Frame(main_frame, bg='white', relief='solid', bd=1)
        factura_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Text widget con scrollbar
        text_frame = tk.Frame(factura_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=('Courier', 10),
                             bg='white', fg='black', relief='flat')
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        # Insertar contenido
        contenido = self._generar_contenido_factura(factura_data)
        text_widget.insert(tk.END, contenido)
        text_widget.configure(state='disabled')
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones
        botones_frame = tk.Frame(main_frame, bg=self.COLORES['fondo_principal'])
        botones_frame.pack(fill=tk.X)
        
        def copiar_al_portapapeles():
            preview.clipboard_clear()
            preview.clipboard_append(contenido)
            self._mostrar_notificacion_real("📋 Factura copiada al portapapeles")
        
        def guardar_archivo():
            try:
                filename = filedialog.asksaveasfilename(
                    title="Guardar Factura",
                    defaultextension=".txt",
                    filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
                    initialname=f"Factura_{factura_data['numero']}.txt"
                )
                if filename:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(contenido)
                    self._mostrar_notificacion_real(f"💾 Factura guardada: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar archivo:\n{str(e)}")
        
        def imprimir():
            preview.destroy()
            self._imprimir_factura_real(factura_data)
        
        # Botón Copiar
        btn_copiar = self.crear_boton_ovalado(botones_frame, "📋 Copiar",
                                             copiar_al_portapapeles,
                                             self.COLORES['azul_info'])
        btn_copiar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Botón Guardar
        btn_guardar = self.crear_boton_ovalado(botones_frame, "💾 Guardar",
                                              guardar_archivo,
                                              self.COLORES['acento_naranja'])
        btn_guardar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        
        # Botón Imprimir
        btn_imprimir = self.crear_boton_ovalado(botones_frame, "🖨️ Imprimir",
                                               imprimir,
                                               self.COLORES['verde_success'])
        btn_imprimir.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
    
    def _generar_contenido_factura(self, factura_data):
        """Generar el contenido formateado de la factura"""
        
        # Calcular ancho total
        ancho = 50
        separador = "=" * ancho
        
        # Obtener datos de factura con valores por defecto
        itbms = factura_data.get('itbms', 0)
        descuento = factura_data.get('descuento', 0)
        metodo_pago = factura_data.get('metodo_pago', 'No especificado')
        
        contenido = f"""
{separador}
        🍽️  {factura_data['restaurante']}  🍽️
{separador}
NIT: {factura_data['nit']}
Fecha: {factura_data['fecha']}        Hora: {factura_data['hora']}
Factura: {factura_data['numero']}
Mesa: {factura_data['mesa']}          Mesero: {factura_data['mesero']}
{separador}
                   DETALLE DEL PEDIDO
{separador}
CANT  DESCRIPCIÓN                    PRECIO    TOTAL
{"-" * ancho}"""
        
        # Agregar items
        for item in factura_data['items']:
            nombre = item['nombre'][:25] + "..." if len(item['nombre']) > 25 else item['nombre']
            cant = str(item['cantidad']).rjust(2)
            precio = f"${item['precio']:,.0f}".rjust(8)
            total = f"${item['precio'] * item['cantidad']:,.0f}".rjust(9)
            
            contenido += f"\n {cant}   {nombre:<25} {precio} {total}"
        
        # Totales con ITBMS y descuento
        contenido += f"""
{"-" * ancho}
                            SUBTOTAL: ${factura_data['subtotal']:>10,.0f}"""
        
        if itbms > 0:
            contenido += f"\n                            ITBMS 19%: ${itbms:>10,.0f}"
        
        if descuento > 0:
            contenido += f"\n                           DESCUENTO: -${descuento:>9,.0f}"
        
        contenido += f"""
                               TOTAL: ${factura_data['total']:>10,.0f}
{separador}
MÉTODO DE PAGO: {metodo_pago}
{separador}
           ¡Gracias por su preferencia!
         www.premiumrestaurant.com
{separador}
Software POS Premium v1.0 - Linux Edition
{separador}
"""
        
        return contenido

    def _oscurecer_color(self, color):
        """Oscurecer un color hex para efecto hover"""
        if color.startswith('#'):
            try:
                # Convertir hex a RGB
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:7], 16)
                
                # Oscurecer 20%
                r = max(0, int(r * 0.8))
                g = max(0, int(g * 0.8))
                b = max(0, int(b * 0.8))
                
                return f"#{r:02x}{g:02x}{b:02x}"
            except:
                return color
        return color
        """Oscurecer un color hexadecimal"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        # Oscurecer
        rgb = tuple(max(0, int(c * 0.8)) for c in rgb)
        return '#{:02x}{:02x}{:02x}'.format(*rgb)
    
    def _crear_menu_principal(self):
        """Crear menú superior"""
        menubar = tk.Menu(self.ventana)
        self.ventana.config(menu=menubar)
        
        # Menú Archivo
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Nuevo Pedido", command=self.nuevo_pedido)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.ventana.quit)
        
        # Menú Configuración
        menu_config = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Configuración", menu=menu_config)
        menu_config.add_command(label="Datos del Negocio", command=self._config_negocio)
        
        # Menú Ayuda
        menu_ayuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Acerca de", command=self._acerca_de)
    
    def _crear_tab_venta(self):
        """Crear pestaña de venta (carrito) con diseño moderno"""
        
        # Crear dos frames principales: izquierda (menú) y derecha (carrito)
        frame_container = tk.Frame(self.tab_venta, bg=self.COLORES['fondo'])
        frame_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # PANEL IZQUIERDO: MENÚ
        frame_menu = tk.Frame(frame_container, bg=self.COLORES['fondo'])
        frame_menu.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Título del panel
        titulo_menu = tk.Label(frame_menu, text="📦 Menú Disponible", 
                               bg=self.COLORES['primario'], fg=self.COLORES['texto_claro'],
                               font=('Segoe UI', 12, 'bold'), pady=10)
        titulo_menu.pack(fill=tk.X)
        
        # Categorías
        frame_cat = tk.Frame(frame_menu, bg=self.COLORES['fondo'])
        frame_cat.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(frame_cat, text="Categoría:").pack(side=tk.LEFT, padx=5)
        self.categoria_var = tk.StringVar()
        categorias = ["Todos"] + self.menu.obtener_categorias()
        combo_categoria = ttk.Combobox(frame_cat, textvariable=self.categoria_var, 
                                       values=categorias, state="readonly", width=20)
        combo_categoria.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        combo_categoria.bind("<<ComboboxSelected>>", lambda e: self._actualizar_items_menu())
        combo_categoria.current(0)
        
        # Listbox de items con estilo mejorado
        frame_listbox = tk.Frame(frame_menu, bg=self.COLORES['fondo'])
        frame_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(frame_listbox)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox_menu = tk.Listbox(frame_listbox, yscrollcommand=scrollbar.set,
                                       bg=self.COLORES['texto_claro'], 
                                       fg=self.COLORES['texto'],
                                       font=('Segoe UI', 10),
                                       relief=tk.FLAT,
                                       highlightthickness=0,
                                       selectmode=tk.SINGLE)
        self.listbox_menu.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox_menu.yview)
        
        # Frame para agregar
        frame_agregar = tk.Frame(frame_menu, bg=self.COLORES['fondo'])
        frame_agregar.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(frame_agregar, text="Cantidad:").pack(side=tk.LEFT, padx=5)
        self.spinbox_cantidad = ttk.Spinbox(frame_agregar, from_=1, to=100, width=8)
        self.spinbox_cantidad.set(1)
        self.spinbox_cantidad.pack(side=tk.LEFT, padx=5)
        
        btn_agregar = self.crear_boton_ovalado(frame_agregar, "➕ Agregar", 
                                               self._agregar_al_carrito, 
                                               self.COLORES['éxito'])
        btn_agregar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self._actualizar_items_menu()
        
        # PANEL DERECHO: CARRITO Y RESUMEN
        frame_carrito = tk.Frame(frame_container, bg=self.COLORES['fondo'], 
                                relief=tk.FLAT, bd=1, highlightbackground=self.COLORES['borde'])
        frame_carrito.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # Título del carrito
        titulo_carrito = tk.Label(frame_carrito, text="🛒 Carrito", 
                                  bg=self.COLORES['secundario'], fg=self.COLORES['texto_claro'],
                                  font=('Segoe UI', 12, 'bold'), pady=10)
        titulo_carrito.pack(fill=tk.X)
        
        # Listbox del carrito
        frame_listbox_carrito = tk.Frame(frame_carrito, bg=self.COLORES['fondo'])
        frame_listbox_carrito.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar_carrito = ttk.Scrollbar(frame_listbox_carrito)
        scrollbar_carrito.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox_carrito = tk.Listbox(frame_listbox_carrito, yscrollcommand=scrollbar_carrito.set,
                                          bg=self.COLORES['texto_claro'],
                                          fg=self.COLORES['texto'],
                                          font=('Segoe UI', 9),
                                          relief=tk.FLAT,
                                          highlightthickness=0,
                                          height=12)
        self.listbox_carrito.pack(fill=tk.BOTH, expand=True)
        scrollbar_carrito.config(command=self.listbox_carrito.yview)
        
        # Botones de edición
        frame_editar = tk.Frame(frame_carrito, bg=self.COLORES['fondo'])
        frame_editar.pack(fill=tk.X, padx=10, pady=5)
        
        btn_editar = self.crear_boton_ovalado(frame_editar, "✏️ Editar", 
                                              self._editar_cantidad_carrito,
                                              self.COLORES['acento'])
        btn_editar.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        btn_eliminar = self.crear_boton_ovalado(frame_editar, "❌ Eliminar", 
                                                self._eliminar_del_carrito,
                                                self.COLORES['error'])
        btn_eliminar.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        # Resumen
        frame_resumen = tk.Frame(frame_carrito, bg=self.COLORES['fondo_oscuro'], 
                                relief=tk.FLAT, padx=15, pady=15)
        frame_resumen.pack(fill=tk.X, padx=10, pady=10)
        
        self.label_resumen = tk.Label(frame_resumen, text="Subtotal: $0.00\nIVA: $0.00\nTOTAL: $0.00",
                                      bg=self.COLORES['fondo_oscuro'],
                                      fg=self.COLORES['texto_claro'],
                                      font=('Segoe UI', 11, 'bold'),
                                      justify=tk.RIGHT)
        self.label_resumen.pack(fill=tk.X)
        
        # Forma de pago
        frame_pago = tk.Frame(frame_carrito, bg=self.COLORES['fondo'])
        frame_pago.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(frame_pago, text="Pago:").pack(side=tk.LEFT, padx=5)
        self.pago_var = tk.StringVar(value="Efectivo")
        combo_pago = ttk.Combobox(frame_pago, textvariable=self.pago_var,
                                  values=["Efectivo", "Tarjeta Débito", "Tarjeta Crédito", "Transferencia"],
                                  state="readonly", width=18)
        combo_pago.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Botones de acción principal
        frame_acciones = tk.Frame(frame_carrito, bg=self.COLORES['fondo'])
        frame_acciones.pack(fill=tk.X, padx=10, pady=10)
        
        btn_cobrar = self.crear_boton_ovalado(frame_acciones, "💰 COBRAR", 
                                             self._procesar_cobro,
                                             self.COLORES['primario'])
        btn_cobrar.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        btn_limpiar = self.crear_boton_ovalado(frame_acciones, "🔄 Limpiar", 
                                              self.nuevo_pedido,
                                              self.COLORES['advertencia'])
        btn_limpiar.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
    
    def _crear_tab_menu(self):
        """Crear pestaña de administración de menú con diseño moderno"""
        
        # Frame con título
        frame_header = tk.Frame(self.tab_menu, bg=self.COLORES['primario'])
        frame_header.pack(fill=tk.X)
        
        titulo = tk.Label(frame_header, text="🍽️ Gestión de Menú", 
                         bg=self.COLORES['primario'], fg=self.COLORES['texto_claro'],
                         font=('Segoe UI', 12, 'bold'), pady=10)
        titulo.pack()
        
        # Frame principal
        frame_contenido = tk.Frame(self.tab_menu, bg=self.COLORES['fondo'])
        frame_contenido.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tabla de items con Treeview mejorado
        frame_tabla = tk.Frame(frame_contenido, bg=self.COLORES['fondo'])
        frame_tabla.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview
        colunas = ("ID", "Nombre", "Precio", "Categoría", "Descripción")
        self.tree_menu = ttk.Treeview(frame_tabla, columns=colunas, height=15, show="headings")
        
        for col in colunas:
            self.tree_menu.heading(col, text=col)
            self.tree_menu.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree_menu.yview)
        self.tree_menu.configure(yscrollcommand=scrollbar.set)
        self.tree_menu.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self._actualizar_tabla_menu()
        
        # Frame de botones de gestión
        frame_botones = tk.Frame(frame_contenido, bg=self.COLORES['fondo'])
        frame_botones.pack(fill=tk.X, pady=10)
        
        btn_nuevo = self.crear_boton_ovalado(frame_botones, "➕ Nuevo Item", 
                                            self._nuevo_item, self.COLORES['éxito'])
        btn_nuevo.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        btn_editar = self.crear_boton_ovalado(frame_botones, "✏️ Editar", 
                                             self._editar_item, self.COLORES['acento'])
        btn_editar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        btn_eliminar = self.crear_boton_ovalado(frame_botones, "❌ Eliminar", 
                                               self._eliminar_item, self.COLORES['error'])
        btn_eliminar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    
    def _actualizar_items_menu(self):
        """Actualizar listbox del menú según categoría seleccionada"""
        self.listbox_menu.delete(0, tk.END)
        categoria = self.categoria_var.get()
        
        if categoria == "Todos":
            items = self.menu.listar_por_categoria()
        else:
            items = self.menu.listar_por_categoria(categoria)
        
        for item in items:
            self.listbox_menu.insert(tk.END, f"{item.nombre} - ${item.precio:,.0f}")
    
    def _actualizar_tabla_menu(self):
        """Actualizar tabla de menú"""
        for item in self.tree_menu.get_children():
            self.tree_menu.delete(item)
        
        for item in self.menu.listar_por_categoria():
            self.tree_menu.insert("", "end", values=(item.id, item.nombre, f"${item.precio:,.0f}", 
                                                     item.categoria, item.descripcion))
    
    def _actualizar_carrito(self):
        """Actualizar listbox del carrito y resumen"""
        self.listbox_carrito.delete(0, tk.END)
        
        for linea in self.pedido_actual.lineas:
            texto = f"{linea.menu_item.nombre} x{linea.cantidad} = ${linea.subtotal:,.0f}"
            self.listbox_carrito.insert(tk.END, texto)
        
        # Actualizar resumen
        resumen = f"""
Subtotal: ${self.pedido_actual.subtotal:,.0f}
IVA (19%): ${self.pedido_actual.impuesto:,.0f}
────────────────────
TOTAL: ${self.pedido_actual.total:,.0f}
"""
        self.label_resumen.config(text=resumen)
    
    def _agregar_al_carrito(self):
        """Agregar item seleccionado al carrito"""
        if not self.listbox_menu.curselection():
            messagebox.showwarning("Aviso", "Selecciona un item del menú")
            return
        
        indice = self.listbox_menu.curselection()[0]
        categoria = self.categoria_var.get()
        
        if categoria == "Todos":
            items = self.menu.listar_por_categoria()
        else:
            items = self.menu.listar_por_categoria(categoria)
        
        item_seleccionado = items[indice]
        cantidad = int(self.spinbox_cantidad.get())
        
        self.pedido_actual.agregar_item(item_seleccionado, cantidad)
        self._actualizar_carrito()
        messagebox.showinfo("Éxito", f"✅ {item_seleccionado.nombre} agregado al carrito")
    
    def _editar_cantidad_carrito(self):
        """Editar cantidad de item en el carrito"""
        if not self.listbox_carrito.curselection():
            messagebox.showwarning("Aviso", "Selecciona un item del carrito")
            return
        
        indice = self.listbox_carrito.curselection()[0]
        linea = self.pedido_actual.lineas[indice]
        
        # Ventana de diálogo para editar cantidad
        ventana_editar = tk.Toplevel(self.ventana)
        ventana_editar.title("Editar Cantidad")
        ventana_editar.geometry("300x150")
        
        ttk.Label(ventana_editar, text=f"Item: {linea.menu_item.nombre}").pack(pady=5)
        ttk.Label(ventana_editar, text="Nueva cantidad:").pack()
        
        spinbox = ttk.Spinbox(ventana_editar, from_=1, to=100, width=10)
        spinbox.set(linea.cantidad)
        spinbox.pack(pady=5)
        
        def guardar():
            nueva_cantidad = int(spinbox.get())
            self.pedido_actual.actualizar_cantidad(linea.menu_item.id, nueva_cantidad)
            self._actualizar_carrito()
            ventana_editar.destroy()
        
        ttk.Button(ventana_editar, text="Guardar", command=guardar).pack(pady=10)
    
    def _eliminar_del_carrito(self):
        """Eliminar item del carrito"""
        if not self.listbox_carrito.curselection():
            messagebox.showwarning("Aviso", "Selecciona un item para eliminar")
            return
        
        indice = self.listbox_carrito.curselection()[0]
        item_a_eliminar = self.pedido_actual.lineas[indice].menu_item.id
        
        self.pedido_actual.remover_item(item_a_eliminar)
        self._actualizar_carrito()
    
    def _procesar_cobro(self):
        """Procesar el cobro y generar factura"""
        if not self.pedido_actual.lineas:
            messagebox.showwarning("Carrito Vacío", "Agrega items al carrito antes de cobrar")
            return
        
        # Marcar pedido como completado
        self.pedido_actual.estado = "completado"
        
        # Generar factura
        forma_pago = self.pago_var.get()
        factura = Factura(self.pedido_actual, forma_pago)
        
        # Mostrar factura con diseño moderno
        ventana_factura = tk.Toplevel(self.ventana)
        ventana_factura.title("Factura de Venta")
        ventana_factura.geometry("700x700")
        ventana_factura.configure(bg=self.COLORES['fondo'])
        
        # Header de la factura
        frame_header = tk.Frame(ventana_factura, bg=self.COLORES['primario'])
        frame_header.pack(fill=tk.X)
        
        titulo_factura = tk.Label(frame_header, text="📄 Factura de Venta", 
                                 bg=self.COLORES['primario'], fg=self.COLORES['texto_claro'],
                                 font=('Segoe UI', 13, 'bold'), pady=12)
        titulo_factura.pack()
        
        # Text widget para mostrar factura
        frame_texto = tk.Frame(ventana_factura, bg=self.COLORES['fondo'])
        frame_texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_factura = tk.Text(frame_texto, bg=self.COLORES['texto_claro'],
                              fg=self.COLORES['texto'], font=('Courier', 9),
                              relief=tk.FLAT, highlightthickness=0)
        text_factura.pack(fill=tk.BOTH, expand=True)
        text_factura.insert("1.0", factura.generar_texto(
            self.nombre_negocio.get(),
            self.nit_negocio.get()
        ))
        text_factura.config(state="disabled")
        
        # Frame de botones de acciones
        frame_botones = tk.Frame(ventana_factura, bg=self.COLORES['fondo'])
        frame_botones.pack(fill=tk.X, padx=10, pady=10)
        
        def guardar_factura():
            ruta = filedialog.asksaveasfilename(defaultextension=".txt",
                                               filetypes=[("Texto", "*.txt"), ("PDF", "*.pdf")])
            if ruta:
                factura.guardar_factura(ruta)
                messagebox.showinfo("Éxito", f"✅ Factura guardada en:\n{ruta}")
        
        def imprimir_factura():
            self._mostrar_dialog_impresion(factura)
        
        btn_guardar = self.crear_boton_ovalado(frame_botones, "💾 Guardar", 
                                              guardar_factura, self.COLORES['secundario'])
        btn_guardar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        btn_imprimir = self.crear_boton_ovalado(frame_botones, "🖨️ Imprimir", 
                                               imprimir_factura, self.COLORES['acento'])
        btn_imprimir.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        btn_cerrar = self.crear_boton_ovalado(frame_botones, "❌ Cerrar", 
                                             ventana_factura.destroy, self.COLORES['error'])
        btn_cerrar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Nuevo pedido
        self.nuevo_pedido()
    
    def _imprimir_linux(self, factura: Factura):
        """Imprimir factura en impresora Linux"""
        try:
            # Guardar factura en archivo temporal
            archivo_temp = "/tmp/factura_temporal.txt"
            factura.guardar_factura(archivo_temp)
            
            # Intentar usar 'lp' comando de CUPS
            try:
                resultado = subprocess.run(["lp", archivo_temp], capture_output=True, text=True, timeout=5)
                
                if resultado.returncode == 0:
                    messagebox.showinfo("Éxito", "✅ Factura enviada a la impresora")
                else:
                    error_msg = resultado.stderr.strip()
                    
                    # Si no hay destinatario (impresora), mostrar alternativas
                    if "no such destination" in error_msg.lower() or "no default destination" in error_msg.lower():
                        self._mostrar_opciones_impresion(archivo_temp, factura)
                    else:
                        messagebox.showerror("Error", f"Error al imprimir:\n{error_msg}")
                        
            except FileNotFoundError:
                # Si 'lp' no existe, intentar con 'lpr'
                self._imprimir_con_lpr(archivo_temp, factura)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al imprimir:\n{str(e)}")
    
    def _imprimir_con_lpr(self, archivo_temp: str, factura: Factura):
        """Alternativa: usar lpr en lugar de lp"""
        try:
            resultado = subprocess.run(["lpr", archivo_temp], capture_output=True, text=True, timeout=5)
            
            if resultado.returncode == 0:
                messagebox.showinfo("Éxito", "✅ Factura enviada a la impresora (lpr)")
            else:
                self._mostrar_opciones_impresion(archivo_temp, factura)
                
        except FileNotFoundError:
            self._mostrar_opciones_impresion(archivo_temp, factura)
    
    def _mostrar_dialog_impresion(self, factura: Factura):
        """Mostrar diálogo de impresión con opciones de CUPS de Linux"""
        ventana_impr = tk.Toplevel(self.ventana)
        ventana_impr.title("Opciones de Impresión")
        ventana_impr.geometry("600x650")
        ventana_impr.resizable(False, False)
        ventana_impr.configure(bg=self.COLORES['fondo'])
        
        # Header
        frame_header = tk.Frame(ventana_impr, bg=self.COLORES['acento'])
        frame_header.pack(fill=tk.X)
        
        titulo = tk.Label(frame_header, text="🖨️ Opciones de Impresión (CUPS)", 
                         bg=self.COLORES['acento'], fg=self.COLORES['texto_claro'],
                         font=('Segoe UI', 12, 'bold'), pady=12)
        titulo.pack()
        
        # Crear un canvas con scrollbar para el contenido
        canvas = tk.Canvas(ventana_impr, bg=self.COLORES['fondo'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(ventana_impr, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.COLORES['fondo'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Sección: Seleccionar Impresora
        frame_impresora = tk.Frame(scrollable_frame, bg=self.COLORES['texto_claro'], 
                                   relief=tk.FLAT, bd=1, highlightbackground=self.COLORES['borde'])
        frame_impresora.pack(fill=tk.X, pady=10)
        
        titulo_imp = tk.Label(frame_impresora, text="📤 Seleccionar Impresora", 
                             bg=self.COLORES['primario'], fg=self.COLORES['texto_claro'],
                             font=('Segoe UI', 10, 'bold'), pady=8)
        titulo_imp.pack(fill=tk.X)
        
        # Obtener lista de impresoras disponibles (CUPS)
        impresoras_list = []
        impresora_defecto = None
        try:
            # Obtener impresoras disponibles
            resultado = subprocess.run(["lpstat", "-p", "-d"], capture_output=True, text=True)
            lineas = resultado.stdout.split('\n')
            
            for linea in lineas:
                linea = linea.strip()
                if linea.startswith('printer'):
                    # Formato: printer <nombre> is idle
                    partes = linea.split()
                    if len(partes) >= 2:
                        nombre = partes[1]
                        impresoras_list.append(nombre)
                elif 'system default' in linea.lower():
                    # Formato: system default destination: <nombre>
                    impresora_defecto = linea.split(':')[-1].strip()
                    
        except Exception as e:
            pass
        
        if not impresoras_list:
            impresoras_list = ["Impresora predeterminada (ninguna configurada)"]
        
        # Variable para la impresora seleccionada
        self.impresora_var = tk.StringVar(value=impresora_defecto if impresora_defecto in impresoras_list else impresoras_list[0])
        
        frame_radio_imp = tk.Frame(frame_impresora, bg=self.COLORES['texto_claro'])
        frame_radio_imp.pack(fill=tk.X, padx=10, pady=10)
        
        for impresora in impresoras_list:
            estado = "✓ Predeterminada" if impresora == impresora_defecto else ""
            texto_radio = f"{impresora} {estado}"
            radio = tk.Radiobutton(frame_radio_imp, text=texto_radio, variable=self.impresora_var,
                                   value=impresora, bg=self.COLORES['texto_claro'],
                                   fg=self.COLORES['texto'], font=('Segoe UI', 10),
                                   selectcolor=self.COLORES['primario'])
            radio.pack(anchor=tk.W, pady=4)
        
        # Sección: Tamaño de Página
        frame_tamano = tk.Frame(scrollable_frame, bg=self.COLORES['texto_claro'],
                               relief=tk.FLAT, bd=1, highlightbackground=self.COLORES['borde'])
        frame_tamano.pack(fill=tk.X, pady=10)
        
        titulo_tam = tk.Label(frame_tamano, text="📄 Tamaño de Página", 
                             bg=self.COLORES['secundario'], fg=self.COLORES['texto_claro'],
                             font=('Segoe UI', 10, 'bold'), pady=8)
        titulo_tam.pack(fill=tk.X)
        
        self.tamano_var = tk.StringVar(value="A4")
        # Opciones estándar de CUPS
        tamanos = [
            ("Ticket (80mm x 200mm)", "80x200mm"),
            ("A4 (210x297mm)", "A4"),
            ("Carta (8.5x11 pulgadas)", "Letter"),
            ("Legal (8.5x14 pulgadas)", "Legal"),
            ("A5 (148x210mm)", "A5"),
            ("A6 (105x148mm)", "A6"),
        ]
        
        frame_radio_tam = tk.Frame(frame_tamano, bg=self.COLORES['texto_claro'])
        frame_radio_tam.pack(fill=tk.X, padx=10, pady=10)
        
        for etiqueta, valor in tamanos:
            radio = tk.Radiobutton(frame_radio_tam, text=etiqueta, variable=self.tamano_var,
                                   value=valor, bg=self.COLORES['texto_claro'],
                                   fg=self.COLORES['texto'], font=('Segoe UI', 9),
                                   selectcolor=self.COLORES['secundario'])
            radio.pack(anchor=tk.W, pady=3)
        
        # Sección: Número de Copias
        frame_copias = tk.Frame(scrollable_frame, bg=self.COLORES['texto_claro'],
                               relief=tk.FLAT, bd=1, highlightbackground=self.COLORES['borde'])
        frame_copias.pack(fill=tk.X, pady=10)
        
        titulo_cop = tk.Label(frame_copias, text="📋 Copias", 
                             bg=self.COLORES['primario'], fg=self.COLORES['texto_claro'],
                             font=('Segoe UI', 10, 'bold'), pady=8)
        titulo_cop.pack(fill=tk.X)
        
        frame_spinbox = tk.Frame(frame_copias, bg=self.COLORES['texto_claro'])
        frame_spinbox.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(frame_spinbox, text="Cantidad de copias:", bg=self.COLORES['texto_claro'],
                fg=self.COLORES['texto'], font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=5)
        
        self.copias_var = tk.StringVar(value="1")
        spinbox_copias = ttk.Spinbox(frame_spinbox, from_=1, to=99, textvariable=self.copias_var, 
                                     width=5, font=('Segoe UI', 10))
        spinbox_copias.pack(side=tk.LEFT, padx=5)
        
        # Sección: Opciones Adicionales
        frame_opciones = tk.Frame(scrollable_frame, bg=self.COLORES['texto_claro'],
                                 relief=tk.FLAT, bd=1, highlightbackground=self.COLORES['borde'])
        frame_opciones.pack(fill=tk.X, pady=10)
        
        titulo_opc = tk.Label(frame_opciones, text="⚙️ Opciones Adicionales", 
                             bg=self.COLORES['primario'], fg=self.COLORES['texto_claro'],
                             font=('Segoe UI', 10, 'bold'), pady=8)
        titulo_opc.pack(fill=tk.X)
        
        frame_check = tk.Frame(frame_opciones, bg=self.COLORES['texto_claro'])
        frame_check.pack(fill=tk.X, padx=10, pady=10)
        
        self.orientacion_var = tk.StringVar(value="portrait")
        ck_portrait = tk.Radiobutton(frame_check, text="Retrato (Portrait)", 
                                    variable=self.orientacion_var, value="portrait",
                                    bg=self.COLORES['texto_claro'], fg=self.COLORES['texto'],
                                    font=('Segoe UI', 9))
        ck_portrait.pack(anchor=tk.W, pady=2)
        
        ck_landscape = tk.Radiobutton(frame_check, text="Apaisado (Landscape)", 
                                     variable=self.orientacion_var, value="landscape",
                                     bg=self.COLORES['texto_claro'], fg=self.COLORES['texto'],
                                     font=('Segoe UI', 9))
        ck_landscape.pack(anchor=tk.W, pady=2)
        
        # Botones de acción
        frame_botones = tk.Frame(ventana_impr, bg=self.COLORES['fondo'])
        frame_botones.pack(fill=tk.X, padx=10, pady=10)
        
        def imprimir_ahora():
            try:
                impresora = self.impresora_var.get()
                copias = self.copias_var.get()
                tamano = self.tamano_var.get()
                orientacion = self.orientacion_var.get()
                
                # Crear archivo temporal
                archivo_temp = "/tmp/factura_temporal.txt"
                factura.guardar_factura(archivo_temp)
                
                # Construir comando lp con las opciones
                cmd = ["lp", archivo_temp]
                
                # Agregar impresora si no es la predeterminada
                if "ninguna configurada" not in impresora.lower():
                    cmd.extend(["-d", impresora])
                
                # Agregar copias
                cmd.extend(["-n", copias])
                
                # Agregar tamaño de página
                cmd.extend(["-o", f"media={tamano}"])
                
                # Agregar orientación
                if orientacion == "landscape":
                    cmd.extend(["-o", "landscape"])
                
                # Ejecutar comando de impresión
                resultado = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                
                if resultado.returncode == 0:
                    messagebox.showinfo("✅ Éxito", 
                        f"Factura enviada a imprimir:\n\n"
                        f"📤 Impresora: {impresora}\n"
                        f"📄 Tamaño: {tamano}\n"
                        f"📋 Copias: {copias}\n"
                        f"📐 Orientación: {orientacion}\n\n"
                        f"El trabajo se ha añadido a la cola de impresión.")
                    ventana_impr.destroy()
                else:
                    error_msg = resultado.stderr.strip()
                    messagebox.showerror("❌ Error de Impresión", 
                        f"No se pudo imprimir:\n\n{error_msg}\n\n"
                        f"Verifica que la impresora esté configurada correctamente.")
                        
            except Exception as e:
                messagebox.showerror("❌ Error", f"Error al imprimir:\n{str(e)}")
        
        def cancelar():
            ventana_impr.destroy()
        
        btn_imprimir = self.crear_boton_ovalado(frame_botones, "🖨️ Imprimir", 
                                               imprimir_ahora, self.COLORES['éxito'])
        btn_imprimir.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        btn_previa = self.crear_boton_ovalado(frame_botones, "👁️ Vista Previa", 
                                             lambda: self._vista_previa_factura(factura),
                                             self.COLORES['secundario'])
        btn_previa.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        btn_cancelar = self.crear_boton_ovalado(frame_botones, "❌ Cancelar", 
                                               cancelar, self.COLORES['error'])
        btn_cancelar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    
    def _vista_previa_factura(self, factura: Factura):
        """Mostrar vista previa de la factura con diseño moderno y elegante"""
        ventana_prev = tk.Toplevel(self.ventana)
        ventana_prev.title("Vista Previa - Factura")
        ventana_prev.geometry("800x900")
        ventana_prev.configure(bg=self.COLORES['fondo'])
        ventana_prev.resizable(True, True)
        
        # Header principal con degradado simulado
        frame_header = tk.Frame(ventana_prev, bg=self.COLORES['primario'], height=80)
        frame_header.pack(fill=tk.X)
        frame_header.pack_propagate(False)
        
        # Container del header
        header_container = tk.Frame(frame_header, bg=self.COLORES['primario'])
        header_container.pack(expand=True, fill=tk.BOTH, padx=20, pady=15)
        
        # Título con icono grande
        titulo_frame = tk.Frame(header_container, bg=self.COLORES['primario'])
        titulo_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        icono_grande = tk.Label(titulo_frame, text="📄", font=('Segoe UI Emoji', 28),
                               bg=self.COLORES['primario'], fg=self.COLORES['texto_claro'])
        icono_grande.pack(side=tk.LEFT, padx=(0, 15))
        
        texto_container = tk.Frame(titulo_frame, bg=self.COLORES['primario'])
        texto_container.pack(side=tk.LEFT, fill=tk.Y)
        
        titulo = tk.Label(texto_container, text="Vista Previa de Factura", 
                         bg=self.COLORES['primario'], fg=self.COLORES['texto_claro'],
                         font=('Segoe UI', 16, 'bold'))
        titulo.pack(anchor=tk.W)
        
        subtitulo = tk.Label(texto_container, text="Previsualización antes de imprimir", 
                            bg=self.COLORES['primario'], fg=self.COLORES['texto_claro'],
                            font=('Segoe UI', 10))
        subtitulo.pack(anchor=tk.W, pady=(2, 0))
        
        # Información adicional en header
        info_frame = tk.Frame(header_container, bg=self.COLORES['primario'])
        info_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        fecha_hora = tk.Label(info_frame, text=f"📅 {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", 
                             bg=self.COLORES['primario'], fg=self.COLORES['texto_claro'],
                             font=('Segoe UI', 9))
        fecha_hora.pack(anchor=tk.E)
        
        total_info = tk.Label(info_frame, text=f"💰 Total: ${factura.total:,.0f}", 
                             bg=self.COLORES['primario'], fg=self.COLORES['texto_claro'],
                             font=('Segoe UI', 11, 'bold'))
        total_info.pack(anchor=tk.E, pady=(5, 0))
        
        # Separador decorativo
        separador = tk.Frame(ventana_prev, bg=self.COLORES['acento'], height=3)
        separador.pack(fill=tk.X)
        
        # Toolbar con opciones
        toolbar = tk.Frame(ventana_prev, bg=self.COLORES['fondo'], height=50)
        toolbar.pack(fill=tk.X, padx=10, pady=10)
        toolbar.pack_propagate(False)
        
        # Opciones de zoom y fuente
        opciones_frame = tk.Frame(toolbar, bg=self.COLORES['fondo'])
        opciones_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        tk.Label(opciones_frame, text="🔍 Tamaño:", bg=self.COLORES['fondo'],
                fg=self.COLORES['texto'], font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=5)
        
        self.zoom_var = tk.StringVar(value="Mediano")
        zoom_combo = ttk.Combobox(opciones_frame, textvariable=self.zoom_var,
                                 values=["Pequeño", "Mediano", "Grande"], 
                                 state="readonly", width=10, font=('Segoe UI', 9))
        zoom_combo.pack(side=tk.LEFT, padx=5)
        
        def cambiar_zoom(event=None):
            tamaños = {"Pequeño": 8, "Mediano": 10, "Grande": 12}
            nuevo_tamaño = tamaños[self.zoom_var.get()]
            text_widget.config(font=('Consolas', nuevo_tamaño))
        
        zoom_combo.bind("<<ComboboxSelected>>", cambiar_zoom)
        
        # Información del documento en toolbar
        info_doc = tk.Frame(toolbar, bg=self.COLORES['fondo'])
        info_doc.pack(side=tk.RIGHT, fill=tk.Y)
        
        lineas_info = tk.Label(info_doc, text="📝 Documento generado automáticamente", 
                              bg=self.COLORES['fondo'], fg=self.COLORES['texto'],
                              font=('Segoe UI', 9))
        lineas_info.pack(side=tk.RIGHT, padx=10)
        
        # Frame principal del contenido con sombra simulada
        contenido_container = tk.Frame(ventana_prev, bg=self.COLORES['borde'])
        contenido_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Frame interno (efecto de elevación)
        frame_texto = tk.Frame(contenido_container, bg=self.COLORES['texto_claro'], 
                              relief=tk.FLAT, bd=0)
        frame_texto.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Scrollbars modernos
        scrollbar_v = ttk.Scrollbar(frame_texto, orient="vertical")
        scrollbar_h = ttk.Scrollbar(frame_texto, orient="horizontal")
        
        # Text widget mejorado
        text_widget = tk.Text(frame_texto, 
                             bg=self.COLORES['texto_claro'], 
                             fg=self.COLORES['texto'], 
                             font=('Consolas', 10),  # Fuente monoespaciada más moderna
                             relief=tk.FLAT, 
                             highlightthickness=0,
                             wrap=tk.NONE,  # Sin wrap para scroll horizontal
                             yscrollcommand=scrollbar_v.set,
                             xscrollcommand=scrollbar_h.set,
                             padx=20,
                             pady=20,
                             selectbackground=self.COLORES['primario'],
                             selectforeground=self.COLORES['texto_claro'])
        
        # Configurar scrollbars
        scrollbar_v.config(command=text_widget.yview)
        scrollbar_h.config(command=text_widget.xview)
        
        # Colocar widgets con grid para mejor control
        text_widget.grid(row=0, column=0, sticky="nsew")
        scrollbar_v.grid(row=0, column=1, sticky="ns")
        scrollbar_h.grid(row=1, column=0, sticky="ew")
        
        frame_texto.grid_rowconfigure(0, weight=1)
        frame_texto.grid_columnconfigure(0, weight=1)
        
        # Contenido de la factura con formato mejorado
        contenido_factura = factura.generar_texto(
            self.nombre_negocio.get(),
            self.nit_negocio.get()
        )
        
        # Agregar contenido
        text_widget.insert(tk.END, contenido_factura)
        text_widget.config(state=tk.DISABLED)
        
        # Footer con botones
        footer = tk.Frame(ventana_prev, bg=self.COLORES['fondo_oscuro'], height=80)
        footer.pack(fill=tk.X)
        footer.pack_propagate(False)
        
        # Container de botones
        botones_container = tk.Frame(footer, bg=self.COLORES['fondo_oscuro'])
        botones_container.pack(expand=True, fill=tk.BOTH, padx=20, pady=15)
        
        # Información en footer izquierda
        info_footer = tk.Frame(botones_container, bg=self.COLORES['fondo_oscuro'])
        info_footer.pack(side=tk.LEFT, fill=tk.Y)
        
        estado_label = tk.Label(info_footer, text="✅ Lista para imprimir", 
                               bg=self.COLORES['fondo_oscuro'], fg=self.COLORES['texto_claro'],
                               font=('Segoe UI', 10, 'bold'))
        estado_label.pack(anchor=tk.W)
        
        tip_label = tk.Label(info_footer, text="💡 Tip: Verifica los datos antes de imprimir", 
                            bg=self.COLORES['fondo_oscuro'], fg=self.COLORES['texto_claro'],
                            font=('Segoe UI', 9))
        tip_label.pack(anchor=tk.W, pady=(2, 0))
        
        # Botones en footer derecha
        botones_frame = tk.Frame(botones_container, bg=self.COLORES['fondo_oscuro'])
        botones_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        def guardar_como():
            from tkinter import filedialog
            archivo = filedialog.asksaveasfilename(
                title="Guardar Factura",
                defaultextension=".txt",
                filetypes=[
                    ("Archivo de texto", "*.txt"),
                    ("PDF", "*.pdf"),
                    ("Todos los archivos", "*.*")
                ]
            )
            if archivo:
                factura.guardar_factura(archivo)
                messagebox.showinfo("✅ Guardado", f"Factura guardada como:\n{archivo}")
        
        def copiar_contenido():
            ventana_prev.clipboard_clear()
            ventana_prev.clipboard_append(contenido_factura)
            messagebox.showinfo("📋 Copiado", "Contenido copiado al portapapeles")
        
        def cerrar():
            ventana_prev.destroy()
        
        # Botones con espaciado profesional
        btn_copiar = self.crear_boton_ovalado(botones_frame, "📋 Copiar", 
                                             copiar_contenido, self.COLORES['acento'])
        btn_copiar.pack(side=tk.RIGHT, padx=5)
        
        btn_guardar = self.crear_boton_ovalado(botones_frame, "💾 Guardar", 
                                              guardar_como, self.COLORES['secundario'])
        btn_guardar.pack(side=tk.RIGHT, padx=5)
        
        btn_cerrar = self.crear_boton_ovalado(botones_frame, "❌ Cerrar", 
                                             cerrar, self.COLORES['error'])
        btn_cerrar.pack(side=tk.RIGHT, padx=5)
        
        # Enfocar la ventana
        ventana_prev.focus()
        ventana_prev.grab_set()  # Hace modal la ventana
    
    def _mostrar_opciones_impresion(self, archivo_temp: str, factura: Factura):
        """Mostrar opciones cuando no hay impresora configurada"""
        ventana_opts = tk.Toplevel(self.ventana)
        ventana_opts.title("Opciones de Impresión")
        ventana_opts.geometry("500x300")
        
        ttk.Label(ventana_opts, 
                 text="⚠️ No hay impresora configurada", 
                 font=("Arial", 12, "bold")).pack(pady=10)
        
        ttk.Label(ventana_opts, 
                 text="Elige una opción:").pack(pady=5)
        
        # Opción 1: Ver impresoras disponibles
        def ver_impresoras():
            try:
                resultado = subprocess.run(["lpstat", "-p", "-d"], capture_output=True, text=True)
                impresoras = resultado.stdout if resultado.stdout else "No se encontraron impresoras"
                messagebox.showinfo("Impresoras Disponibles", impresoras)
            except:
                messagebox.showerror("Error", "No se pudo obtener la lista de impresoras")
        
        ttk.Button(ventana_opts, text="🔍 Ver Impresoras Disponibles", 
                  command=ver_impresoras).pack(fill=tk.X, padx=10, pady=5)
        
        # Opción 2: Guardar a archivo
        def guardar_archivo():
            from tkinter import filedialog
            ruta = filedialog.asksaveasfilename(defaultextension=".txt",
                                               filetypes=[("Texto", "*.txt"), ("PDF", "*.pdf")])
            if ruta:
                factura.guardar_factura(ruta)
                messagebox.showinfo("Éxito", f"✅ Factura guardada en:\n{ruta}")
                ventana_opts.destroy()
        
        ttk.Button(ventana_opts, text="💾 Guardar a Archivo", 
                  command=guardar_archivo).pack(fill=tk.X, padx=10, pady=5)
        
        # Opción 3: Configurar impresora por defecto
        def configurar_impresora():
            ventana_conf = tk.Toplevel(ventana_opts)
            ventana_conf.title("Configurar Impresora")
            ventana_conf.geometry("400x200")
            
            ttk.Label(ventana_conf, text="Nombre de la impresora:").pack(pady=5)
            entry_printer = ttk.Entry(ventana_conf, width=30)
            entry_printer.pack(pady=5)
            
            ttk.Label(ventana_conf, text="Ejemplo: Canon, HP-LaserJet, etc.").pack()
            
            def aplicar():
                nombre_printer = entry_printer.get()
                if nombre_printer:
                    try:
                        resultado = subprocess.run(
                            ["lpadmin", "-d", nombre_printer],
                            capture_output=True, text=True, timeout=5
                        )
                        
                        if resultado.returncode == 0:
                            messagebox.showinfo("Éxito", f"✅ Impresora '{nombre_printer}' configurada")
                            ventana_conf.destroy()
                            ventana_opts.destroy()
                        else:
                            messagebox.showerror("Error", f"No se pudo configurar la impresora:\n{resultado.stderr}")
                    except:
                        messagebox.showerror("Error", "Se requieren permisos de administrador (sudo)")
            
            ttk.Button(ventana_conf, text="Aplicar", command=aplicar).pack(pady=10)
            ttk.Label(ventana_conf, text="(Requiere contraseña de sudo)", font=("Arial", 9, "italic")).pack()
        
        ttk.Button(ventana_opts, text="⚙️ Configurar Impresora", 
                  command=configurar_impresora).pack(fill=tk.X, padx=10, pady=5)
        
        # Opción 4: Ver instrucciones
        def ver_ayuda():
            instrucciones = """
CONFIGURAR IMPRESORA EN LINUX

1. Ver impresoras disponibles:
   lpstat -p -d

2. Establecer impresora por defecto:
   sudo lpadmin -d nombre_impresora

3. Reinstalar CUPS:
   sudo apt-get install cups  (Ubuntu/Debian)
   sudo dnf install cups      (Fedora)

4. Iniciar servicio CUPS:
   sudo systemctl start cups
            """
            messagebox.showinfo("Ayuda - Configuración de Impresoras", instrucciones)
        
        ttk.Button(ventana_opts, text="❓ Ver Ayuda", 
                  command=ver_ayuda).pack(fill=tk.X, padx=10, pady=5)
    
    def nuevo_pedido(self):
        """Crear un nuevo pedido"""
        self.pedido_actual = Pedido()
        self._actualizar_carrito()
    
    def _nuevo_item(self):
        """Crear nuevo item en el menú"""
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Nuevo Item")
        ventana.geometry("400x300")
        
        ttk.Label(ventana, text="Nombre:").pack()
        entry_nombre = ttk.Entry(ventana)
        entry_nombre.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(ventana, text="Precio:").pack()
        entry_precio = ttk.Entry(ventana)
        entry_precio.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(ventana, text="Categoría:").pack()
        combo_categoria = ttk.Combobox(ventana, values=self.menu.obtener_categorias())
        combo_categoria.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(ventana, text="Descripción:").pack()
        text_descripcion = tk.Text(ventana, height=4)
        text_descripcion.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
        
        def guardar():
            try:
                nombre = entry_nombre.get()
                precio = float(entry_precio.get())
                categoria = combo_categoria.get() or "General"
                descripcion = text_descripcion.get("1.0", "end").strip()
                
                self.menu.agregar_item(nombre, precio, categoria, descripcion)
                self._actualizar_tabla_menu()
                self._actualizar_items_menu()
                ventana.destroy()
                messagebox.showinfo("Éxito", "✅ Item agregado")
            except ValueError:
                messagebox.showerror("Error", "El precio debe ser un número")
        
        ttk.Button(ventana, text="Guardar", command=guardar).pack(pady=10)
    
    def _editar_item(self):
        """Editar item del menú"""
        if not self.tree_menu.selection():
            messagebox.showwarning("Aviso", "Selecciona un item para editar")
            return
        
        item_id = self.tree_menu.item(self.tree_menu.selection())['values'][0]
        item = self.menu.obtener_item(item_id)
        
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Editar Item")
        ventana.geometry("400x300")
        
        ttk.Label(ventana, text="Nombre:").pack()
        entry_nombre = ttk.Entry(ventana)
        entry_nombre.insert(0, item.nombre)
        entry_nombre.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(ventana, text="Precio:").pack()
        entry_precio = ttk.Entry(ventana)
        entry_precio.insert(0, str(item.precio))
        entry_precio.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(ventana, text="Categoría:").pack()
        combo_categoria = ttk.Combobox(ventana, values=self.menu.obtener_categorias())
        combo_categoria.set(item.categoria)
        combo_categoria.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(ventana, text="Descripción:").pack()
        text_descripcion = tk.Text(ventana, height=4)
        text_descripcion.insert("1.0", item.descripcion)
        text_descripcion.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
        
        def guardar():
            try:
                self.menu.editar_item(item_id, 
                                     nombre=entry_nombre.get(),
                                     precio=float(entry_precio.get()),
                                     categoria=combo_categoria.get(),
                                     descripcion=text_descripcion.get("1.0", "end").strip())
                self._actualizar_tabla_menu()
                self._actualizar_items_menu()
                ventana.destroy()
                messagebox.showinfo("Éxito", "✅ Item actualizado")
            except ValueError:
                messagebox.showerror("Error", "El precio debe ser un número")
        
        ttk.Button(ventana, text="Guardar", command=guardar).pack(pady=10)
    
    def _eliminar_item(self):
        """Eliminar item del menú"""
        if not self.tree_menu.selection():
            messagebox.showwarning("Aviso", "Selecciona un item para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Eliminar este item?"):
            item_id = self.tree_menu.item(self.tree_menu.selection())['values'][0]
            self.menu.eliminar_item(item_id)
            self._actualizar_tabla_menu()
            self._actualizar_items_menu()
    
    def _config_negocio(self):
        """Configurar datos del negocio"""
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Configuración del Negocio")
        ventana.geometry("400x200")
        
        ttk.Label(ventana, text="Nombre del Negocio:").pack()
        entry_nombre = ttk.Entry(ventana)
        entry_nombre.insert(0, self.nombre_negocio.get())
        entry_nombre.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(ventana, text="NIT:").pack()
        entry_nit = ttk.Entry(ventana)
        entry_nit.insert(0, self.nit_negocio.get())
        entry_nit.pack(fill=tk.X, padx=5, pady=5)
        
        def guardar():
            self.nombre_negocio.set(entry_nombre.get())
            self.nit_negocio.set(entry_nit.get())
            ventana.destroy()
            messagebox.showinfo("Éxito", "✅ Configuración guardada")
        
        ttk.Button(ventana, text="Guardar", command=guardar).pack(pady=10)
    
    def _mostrar_ventana_procesamiento(self):
        """Mostrar ventana de procesamiento del pedido"""
        
        # Crear ventana modal
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Procesar Pedido")
        ventana.geometry("500x600")
        ventana.resizable(False, False)
        ventana.configure(bg=self.COLORES['fondo_principal'])
        ventana.grab_set()  # Modal
        ventana.transient(self.ventana)
        
        # Centrar ventana
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - (500 // 2)
        y = (ventana.winfo_screenheight() // 2) - (600 // 2)
        ventana.geometry(f"+{x}+{y}")
        
        # Container principal
        main_container = tk.Frame(ventana, bg=self.COLORES['fondo_principal'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Header
        header = tk.Label(main_container, text="🧾 Confirmar Pedido",
                         font=('Inter', 20, 'bold'),
                         fg=self.COLORES['acento_dorado'],
                         bg=self.COLORES['fondo_principal'])
        header.pack(pady=(0, 20))
        
        # Información del cliente
        cliente_frame = tk.LabelFrame(main_container, text="Información del Cliente",
                                     bg=self.COLORES['fondo_card'],
                                     fg=self.COLORES['texto_principal'],
                                     font=('Inter', 12, 'bold'))
        cliente_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Mesa
        mesa_frame = tk.Frame(cliente_frame, bg=self.COLORES['fondo_card'])
        mesa_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(mesa_frame, text="Mesa:", font=('Inter', 11),
                bg=self.COLORES['fondo_card'], fg=self.COLORES['texto_principal']).pack(side=tk.LEFT)
        
        mesa_var = tk.StringVar()
        mesa_entry = tk.Entry(mesa_frame, textvariable=mesa_var, font=('Inter', 11),
                             bg='white', width=15)
        mesa_entry.pack(side=tk.RIGHT)
        mesa_entry.focus()
        
        # Resumen del pedido
        resumen_frame = tk.LabelFrame(main_container, text="Resumen del Pedido",
                                     bg=self.COLORES['fondo_card'],
                                     fg=self.COLORES['texto_principal'],
                                     font=('Inter', 12, 'bold'))
        resumen_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Lista de items
        items_text = tk.Text(resumen_frame, height=12, width=50,
                            font=('Inter', 10), bg='white',
                            relief='flat', bd=5)
        items_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Llenar resumen
        resumen_contenido = ""
        for item in self.pedido.items:
            resumen_contenido += f"• {item['nombre']}\n"
            resumen_contenido += f"  Cantidad: {item['cantidad']} x ${item['precio']:,.0f}\n"
            resumen_contenido += f"  Subtotal: ${item['precio'] * item['cantidad']:,.0f}\n\n"
        
        resumen_contenido += f"{'='*40}\n"
        resumen_contenido += f"TOTAL: ${self.pedido.calcular_total():,.0f}"
        
        items_text.insert(tk.END, resumen_contenido)
        items_text.config(state=tk.DISABLED)
        
        # Botones de acción
        botones_frame = tk.Frame(main_container, bg=self.COLORES['fondo_principal'])
        botones_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Botón cancelar
        btn_cancelar = self._crear_boton_moderno(botones_frame, "Cancelar",
                                                lambda: ventana.destroy(),
                                                self.COLORES['rojo_danger'])
        btn_cancelar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Botón confirmar
        def confirmar_pedido():
            mesa = mesa_var.get().strip()
            if not mesa:
                messagebox.showerror("Error", "Por favor ingresa el número de mesa")
                return
            
            # Procesar pedido
            self._finalizar_pedido(mesa)
            ventana.destroy()
        
        btn_confirmar = self._crear_boton_moderno(botones_frame, "Confirmar y Generar Factura",
                                                 confirmar_pedido,
                                                 self.COLORES['verde_success'])
        btn_confirmar.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 0))
    
    def _finalizar_pedido(self, mesa):
        """Finalizar el pedido y generar factura"""
        try:
            # Generar número de factura
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            numero_factura = f"FACT-{timestamp}"
            
            # Crear factura
            factura_data = {
                'numero': numero_factura,
                'fecha': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'mesa': mesa,
                'items': self.pedido.items.copy(),
                'total': self.pedido.calcular_total()
            }
            
            # Guardar en historial (simulado)
            if not hasattr(self, 'historial_ventas'):
                self.historial_ventas = []
            self.historial_ventas.append(factura_data)
            
            # Mostrar opciones de impresión
            self._mostrar_opciones_impresion(factura_data)
            
            # Limpiar carrito
            self.pedido.items.clear()
            self._actualizar_carrito()
            
            # Notificación de éxito
            self._mostrar_notificacion(f"✅ Pedido procesado - Factura: {numero_factura}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar el pedido:\n{str(e)}")
    
    def _mostrar_opciones_impresion(self, factura_data):
        """Mostrar opciones para imprimir la factura"""
        
        respuesta = messagebox.askyesnocancel(
            "Imprimir Factura",
            "¿Deseas imprimir la factura?\n\n"
            f"Factura: {factura_data['numero']}\n"
            f"Mesa: {factura_data['mesa']}\n"
            f"Total: ${factura_data['total']:,.0f}\n\n"
            "Sí = Imprimir\n"
            "No = Solo guardar\n"
            "Cancelar = Ver vista previa"
        )
        
        if respuesta is True:  # Sí - Imprimir
            self._imprimir_factura(factura_data)
        elif respuesta is False:  # No - Solo guardar
            messagebox.showinfo("Guardado", "✅ Factura guardada correctamente")
        else:  # Cancelar - Vista previa
            self._vista_previa_factura(factura_data)
    
    def _imprimir_factura(self, factura_data):
        """Imprimir la factura directamente"""
        try:
            # Mostrar diálogo de impresión
            self._mostrar_dialog_impresion(factura_data)
        except Exception as e:
            messagebox.showerror("Error de Impresión", f"No se pudo imprimir:\n{str(e)}")
    
    def _mostrar_reportes(self):
        """Mostrar ventana de reportes"""
        if not hasattr(self, 'historial_ventas') or not self.historial_ventas:
            messagebox.showinfo("Sin Datos", "No hay ventas registradas para mostrar reportes.")
            return
        
        # Crear ventana de reportes
        ventana = tk.Toplevel(self.ventana)
        ventana.title("📊 Reportes de Ventas")
        ventana.geometry("800x600")
        ventana.configure(bg=self.COLORES['fondo_principal'])
        
        # Centrar ventana
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - (400)
        y = (ventana.winfo_screenheight() // 2) - (300)
        ventana.geometry(f"+{x}+{y}")
        
        # Container principal
        main_container = tk.Frame(ventana, bg=self.COLORES['fondo_principal'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header = tk.Label(main_container, text="📊 Reportes de Ventas",
                         font=('Inter', 18, 'bold'),
                         fg=self.COLORES['acento_dorado'],
                         bg=self.COLORES['fondo_principal'])
        header.pack(pady=(0, 20))
        
        # Estadísticas resumidas
        stats_frame = tk.Frame(main_container, bg=self.COLORES['fondo_card'])
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        stats_content = tk.Frame(stats_frame, bg=self.COLORES['fondo_card'])
        stats_content.pack(fill=tk.X, padx=20, pady=15)
        
        total_ventas = len(self.historial_ventas)
        total_ingresos = sum(venta['total'] for venta in self.historial_ventas)
        promedio_venta = total_ingresos / total_ventas if total_ventas > 0 else 0
        
        # Stats en una fila
        tk.Label(stats_content, text=f"Total Ventas: {total_ventas}",
                font=('Inter', 12, 'bold'), fg=self.COLORES['texto_principal'],
                bg=self.COLORES['fondo_card']).pack(side=tk.LEFT, padx=20)
        
        tk.Label(stats_content, text=f"Ingresos: ${total_ingresos:,.0f}",
                font=('Inter', 12, 'bold'), fg=self.COLORES['acento_dorado'],
                bg=self.COLORES['fondo_card']).pack(side=tk.LEFT, padx=20)
        
        tk.Label(stats_content, text=f"Promedio: ${promedio_venta:,.0f}",
                font=('Inter', 12, 'bold'), fg=self.COLORES['verde_success'],
                bg=self.COLORES['fondo_card']).pack(side=tk.LEFT, padx=20)
        
        # Lista de ventas
        lista_frame = tk.Frame(main_container, bg=self.COLORES['fondo_card'])
        lista_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header de la lista
        header_lista = tk.Frame(lista_frame, bg=self.COLORES['fondo_card'])
        header_lista.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        tk.Label(header_lista, text="Historial de Ventas",
                font=('Inter', 14, 'bold'), fg=self.COLORES['texto_principal'],
                bg=self.COLORES['fondo_card']).pack(side=tk.LEFT)
        
        # Scrollable text para las ventas
        text_ventas = tk.Text(lista_frame, height=15, font=('Inter', 10),
                             bg='white', relief='flat')
        scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=text_ventas.yview)
        text_ventas.configure(yscrollcommand=scrollbar.set)
        
        # Llenar con datos de ventas
        for venta in reversed(self.historial_ventas):  # Más recientes primero
            text_ventas.insert(tk.END, f"Factura: {venta['numero']}\n")
            text_ventas.insert(tk.END, f"Fecha: {venta['fecha']}\n")
            text_ventas.insert(tk.END, f"Mesa: {venta['mesa']}\n")
            text_ventas.insert(tk.END, f"Total: ${venta['total']:,.0f}\n")
            text_ventas.insert(tk.END, f"Items: {len(venta['items'])}\n")
            text_ventas.insert(tk.END, "-" * 50 + "\n\n")
        
        text_ventas.config(state=tk.DISABLED)
        text_ventas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(15, 0), pady=(0, 15))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 15), padx=(0, 15))

    def _acerca_de(self):
        """Mostrar información de la aplicación"""
        messagebox.showinfo("Acerca de", 
            "POS Restaurante v1.0\n\n"
            "Sistema de Punto de Venta para Restaurantes\n"
            "Parcial 2 - Sistema Operativo\n\n"
            "Características:\n"
            "✓ Gestión de menú\n"
            "✓ Carrito de compras\n"
            "✓ Generación de facturas\n"
            "✓ Impresión en Linux\n")
    
    def ejecutar(self):
        """Iniciar la aplicación"""
        self.ventana.mainloop()

# Punto de entrada principal
if __name__ == "__main__":
    app = InterfazRestaurante()
    app.ejecutar()
