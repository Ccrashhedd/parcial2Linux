import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import tempfile
import datetime
import os
import json
from modelo_restaurante import MenuItem, PedidoRestaurante, Menu
from dialogo_impresion import DialogoImpresion
from dialogo_login import DialogoLogin
from conexionDB import db_manager
class InterfazRestaurante:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("POS RESTAURANT Premium")
        self.ventana.geometry("1400x800")
        
        # Colores
        self.COLORES = {
            'fondo_principal': '#1a1a1a',
            'fondo_card': '#2d2d2d',
            'texto_principal': '#ffffff',
            'texto_secundario': '#b0b0b0',
            'acento_dorado': '#d4af37',
            'verde_success': '#2ecc71',
            'rojo_danger': '#e74c3c',
        }
        
        self.ventana.configure(bg=self.COLORES['fondo_principal'])
        
        # Datos
        self.menu = Menu()
        self.pedido = PedidoRestaurante()
        
        # Variables
        self.descuento_var = tk.StringVar(value="0")
        self.metodo_pago_var = tk.StringVar(value="Efectivo")
        
        # Mostrar login primero usando módulo separado
        DialogoLogin(self.ventana, self.COLORES, self._login_exitoso)
    
    def _login_exitoso(self):
        """Callback cuando el login es exitoso"""
        # Limpiar todos los widgets de la ventana
        for widget in self.ventana.winfo_children():
            widget.destroy()
        
        # Mostrar interfaz principal
        self.ventana.geometry("1400x800")
        self.ventana.title("POS RESTAURANT Premium")
        self._crear_notebook()
        

    
    def _crear_notebook(self):
        """Crear interfaz con pestañas"""
        # Personalizar estilo de notebook y controles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.COLORES['fondo_principal'])
        style.configure('TNotebook.Tab', padding=[20, 10])
        
        # Configurar Combobox moderno
        style.configure('TCombobox', 
                       fieldbackground=self.COLORES['fondo_card'],
                       background=self.COLORES['acento_dorado'],
                       foreground=self.COLORES['texto_principal'],
                       insertcolor=self.COLORES['acento_dorado'],
                       arrowcolor=self.COLORES['acento_dorado'])
        style.map('TCombobox',
                 fieldbackground=[('readonly', self.COLORES['fondo_card'])],
                 foreground=[('readonly', self.COLORES['texto_principal'])])
        
        # Configurar Scrollbar moderno
        style.configure('TScrollbar',
                       background=self.COLORES['fondo_card'],
                       troughcolor=self.COLORES['fondo_principal'],
                       arrowcolor=self.COLORES['acento_dorado'],
                       darkcolor=self.COLORES['fondo_card'],
                       lightcolor=self.COLORES['fondo_card'])
        
        notebook = ttk.Notebook(self.ventana)
        notebook.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Pestaña Menú
        frame_menu = tk.Frame(notebook, bg=self.COLORES['fondo_principal'])
        notebook.add(frame_menu, text="📱 Menú")
        self._crear_tab_menu(frame_menu)
        
        # Pestaña Carrito
        frame_carrito = tk.Frame(notebook, bg=self.COLORES['fondo_principal'])
        notebook.add(frame_carrito, text="🛒 Carrito")
        self._crear_tab_carrito(frame_carrito)
        
        # Pestaña Gestión de Productos
        frame_productos = tk.Frame(notebook, bg=self.COLORES['fondo_principal'])
        notebook.add(frame_productos, text="⚙️ Productos")
        self._crear_tab_productos(frame_productos)
    
    def _crear_tab_menu(self, parent):
        """Pestaña con menú de items"""
        # Panel superior con filtros - diseño mejorado
        header_frame = tk.Frame(parent, bg=self.COLORES['fondo_card'], height=80)
        header_frame.pack(fill=tk.X, padx=15, pady=12)
        header_frame.pack_propagate(False)
        
        # Container interior para alineación
        inner_frame = tk.Frame(header_frame, bg=self.COLORES['fondo_card'])
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Filtro por tipo de comida (desde BD)
        tk.Label(inner_frame, text="�️ Tipo:", 
                bg=self.COLORES['fondo_card'],
                fg=self.COLORES['acento_dorado'], 
                font=('Inter', 11, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        
        self.tipo_comida_var = tk.StringVar(value="Todos")
        tipos_comida = ["Todos"] + self.menu.obtener_tipos_comida()
        
        combo_tipo = ttk.Combobox(inner_frame, textvariable=self.tipo_comida_var, 
                                 values=tipos_comida, state="readonly", width=18,
                                 font=('Inter', 10))
        combo_tipo.pack(side=tk.LEFT, padx=5)
        combo_tipo.bind("<<ComboboxSelected>>", lambda e: self._actualizar_grid_menu())
        
        # Separador
        tk.Frame(inner_frame, bg=self.COLORES['texto_secundario'], width=2).pack(side=tk.LEFT, fill=tk.Y, padx=15)
        
        # Filtro por día de la semana
        tk.Label(inner_frame, text="📅 Día:", 
                bg=self.COLORES['fondo_card'],
                fg=self.COLORES['acento_dorado'], 
                font=('Inter', 11, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        
        self.dia_semana_var = tk.StringVar(value="Todos")
        dias = ["Todos", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        
        combo_dia = ttk.Combobox(inner_frame, textvariable=self.dia_semana_var, 
                                values=dias, state="readonly", width=18,
                                font=('Inter', 10))
        combo_dia.pack(side=tk.LEFT, padx=5)
        combo_dia.bind("<<ComboboxSelected>>", lambda e: self._actualizar_grid_menu())
        
        # Panel principal con grid
        main_frame = tk.Frame(parent, bg=self.COLORES['fondo_principal'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas con scroll
        canvas = tk.Canvas(main_frame, bg=self.COLORES['fondo_principal'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        
        self.menu_frame = tk.Frame(canvas, bg=self.COLORES['fondo_principal'])
        # Cuando el contenido cambie, actualizar scrollregion
        self.menu_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Insertar frame en canvas y mantener referencia al id de ventana
        self.menu_window_id = canvas.create_window((0, 0), window=self.menu_frame, anchor="nw")
        # Guardar referencia al canvas para recalcular columnas dinámicas
        self.menu_canvas = canvas

        # Parámetro de ancho mínimo estimado por tarjeta (incluye paddings)
        # Ajusta este valor si tus cards son más anchas/estrechas
        self.menu_min_card_width = 360

        # Asegurar que el frame interno siempre tenga el mismo ancho que el canvas
        # y re-calcular la grilla cuando el canvas cambie de tamaño
        def _on_canvas_configure(event):
            try:
                canvas.itemconfig(self.menu_window_id, width=event.width)
            except Exception:
                pass
            # Recalcular y re-layout de las tarjetas según el nuevo ancho
            try:
                # Llamamos a la actualización de la grilla (usa el ancho del canvas internamente)
                self._actualizar_grid_menu()
            except Exception:
                pass

        canvas.bind('<Configure>', _on_canvas_configure)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self._actualizar_grid_menu()
    
    def _actualizar_grid_menu(self):
        """Actualizar grid de menú de forma optimizada con secciones profesionales"""
        # Limpiar widgets previos
        for widget in self.menu_frame.winfo_children():
            widget.destroy()
        
        tipo_comida = self.tipo_comida_var.get()
        dia_semana = self.dia_semana_var.get()
        
        # Calcular dinámicamente el número de columnas según el ancho disponible
        try:
            available_width = self.menu_canvas.winfo_width() if hasattr(self, 'menu_canvas') else None
        except Exception:
            available_width = None

        # Ancho mínimo por tarjeta (incluye paddings/margins)
        card_min = getattr(self, 'menu_min_card_width', 360)

        if available_width and available_width > 0:
            max_columns = 6
            columnas = max(1, min(max_columns, int(available_width // card_min)))
        else:
            columnas = 3

        # Asegurar que las columnas se expandan uniformemente
        for i in range(columnas):
            try:
                self.menu_frame.grid_columnconfigure(i, weight=1, uniform='col')
            except Exception:
                pass
        
        current_row = 0
        items_encontrados = 0
        
        # ============ SECCIÓN 1: PROMOCIONES ACTIVAS ============
        excepciones = self.menu.obtener_excepciones_activas()
        
        if excepciones:
            # Título de sección: Promociones
            titulo_promo = tk.Frame(self.menu_frame, bg=self.COLORES['rojo_danger'], height=50)
            titulo_promo.grid(row=current_row, column=0, columnspan=columnas, sticky='ew', pady=(10, 15), padx=10)
            
            tk.Label(titulo_promo, text="🎁 PROMOCIONES ESPECIALES", 
                    font=('Inter', 14, 'bold'), fg='white',
                    bg=self.COLORES['rojo_danger']).pack(expand=True)
            
            current_row += 1
            col = 0
            
            # Obtener productos con descuento
            productos_promocion = self.menu.obtener_productos_con_descuento()
            
            for producto in productos_promocion:
                # Aplicar filtro de tipo si está seleccionado
                if tipo_comida != "Todos":
                    # Obtener el tipo del producto desde la BD
                    info_prod = self.menu.obtener_precio_producto(producto['id_producto'])
                    if info_prod and info_prod.get('tipo') != tipo_comida:
                        continue
                
                self._crear_card_promocion(self.menu_frame, producto, current_row, col)
                items_encontrados += 1
                col += 1
                if col >= columnas:
                    col = 0
                    current_row += 1
            
            # Si hay items en la última fila, avanzar
            if col > 0:
                current_row += 1
        
        # ============ SECCIÓN 2: MENÚ DEL DÍA ============
        # Título de sección: Menú del Día
        titulo_menu = tk.Frame(self.menu_frame, bg=self.COLORES['acento_dorado'], height=50)
        titulo_menu.grid(row=current_row, column=0, columnspan=columnas, sticky='ew', pady=(20, 15), padx=10)
        
        dia_texto = dia_semana if dia_semana != "Todos" else datetime.datetime.now().strftime("%A").capitalize()
        tk.Label(titulo_menu, text=f"🍽️ MENÚ DEL DÍA - {dia_texto}", 
                font=('Inter', 14, 'bold'), fg='black',
                bg=self.COLORES['acento_dorado']).pack(expand=True)
        
        current_row += 1
        col = 0
        
        # Obtener menú del día desde la base de datos
        if dia_semana == "Todos":
            # Usar día actual
            dia_id = datetime.datetime.now().isoweekday()  # 1=Lunes, 7=Domingo
        else:
            dias_map = {"Lunes": 1, "Martes": 2, "Miércoles": 3, "Jueves": 4, 
                       "Viernes": 5, "Sábado": 6, "Domingo": 7}
            dia_id = dias_map.get(dia_semana, 1)
        
        # Obtener productos del menú del día filtrados por tipo
        if tipo_comida == "Todos":
            productos_dia = self.menu.obtener_menu_del_dia(dia_id)
        else:
            productos_dia = self.menu.obtener_menu_del_dia(dia_id, tipo_comida)
        
        # Mostrar productos del menú del día
        if productos_dia:
            for producto in productos_dia:
                self._crear_card_menu_dia(self.menu_frame, producto, current_row, col)
                items_encontrados += 1
                col += 1
                if col >= columnas:
                    col = 0
                    current_row += 1
        

        
        # Si no hay items, mostrar mensaje
        if items_encontrados == 0:
            msg_frame = tk.Frame(self.menu_frame, bg=self.COLORES['fondo_principal'])
            msg_frame.grid(row=0, column=0, columnspan=columnas, pady=50)
            tk.Label(msg_frame, text="❌ Sin productos en esta categoría",
                    font=('Inter', 14), fg=self.COLORES['texto_secundario'],
                    bg=self.COLORES['fondo_principal']).pack()
    
    def _crear_card_promocion(self, parent, producto, row, col):
        """Crear card de producto en promoción con diseño especial"""
        card = tk.Frame(parent, bg='#8B0000', relief=tk.RAISED, bd=3)  # Rojo oscuro
        card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

        # Banner de promoción
        banner = tk.Frame(card, bg=self.COLORES['rojo_danger'], height=35)
        banner.pack(fill=tk.X)
        tk.Label(banner, text=f"🎁 {producto['promocion']}", 
                font=('Inter', 10, 'bold'), fg='white',
                bg=self.COLORES['rojo_danger']).pack(pady=8)

        # Nombre del producto
        tk.Label(card, text=producto['nombre'], font=('Inter', 13, 'bold'),
                fg='white', bg='#8B0000', wraplength=400).pack(pady=(12, 8), padx=20)

        # Tipo de comida
        tk.Label(card, text=f"🍽️ {producto['tipo']}", font=('Inter', 10),
                fg='#FFD700', bg='#8B0000').pack(pady=4)

        # Separador
        tk.Frame(card, bg='#FFD700', height=2).pack(fill=tk.X, pady=10, padx=15)

        # Frame de precios
        precios_frame = tk.Frame(card, bg='#8B0000')
        precios_frame.pack(pady=8, padx=20, fill=tk.X)

        # Precio original tachado
        tk.Label(precios_frame, text=f"${producto['precio_original']:,.0f}", 
                font=('Inter', 11, 'overstrike'), fg='#FFB6C1',
                bg='#8B0000').pack(side=tk.LEFT)

        # Badge de descuento
        descuento_badge = tk.Frame(precios_frame, bg=self.COLORES['rojo_danger'])
        descuento_badge.pack(side=tk.LEFT, padx=10)
        tk.Label(descuento_badge, text=f"-{producto['descuento']:.0f}%", 
                font=('Inter', 10, 'bold'), fg='white',
                bg=self.COLORES['rojo_danger'], padx=8, pady=2).pack()

        # Precio especial
        tk.Label(precios_frame, text=f"${producto['precio_especial']:,.0f}", 
                font=('Inter', 15, 'bold'), fg='#FFD700',
                bg='#8B0000').pack(side=tk.RIGHT)

        # Botón Agregar
        tk.Button(card, text="🛒 Agregar en Promoción", bg='#FFD700',
                 fg='black', font=('Inter', 11, 'bold'), relief='flat', 
                 padx=15, pady=12,
                 command=lambda: self._agregar_producto_promocion(producto)).pack(
                     fill=tk.X, padx=20, pady=(10, 14))

    def _crear_card_menu_dia(self, parent, producto, row, col):
        """Crear card de producto del menú del día"""
        card = tk.Frame(parent, bg=self.COLORES['fondo_card'], relief=tk.RAISED, bd=2)
        card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

        # Nombre
        tk.Label(card, text=producto['nombre'], font=('Inter', 14, 'bold'),
                fg=self.COLORES['texto_principal'],
                bg=self.COLORES['fondo_card'], wraplength=420).pack(pady=(10, 8), padx=20)

        # Tipo de comida con icono
        tipo_iconos = {
            'Desayuno': '☕',
            'Almuerzo': '🍴',
            'Cena': '🌙',
            'Bebidas': '🥤',
            'Postres': '🍰'
        }
        icono = tipo_iconos.get(producto['tipo'], '🍽️')
        tk.Label(card, text=f"{icono} {producto['tipo']}", font=('Inter', 10),
                fg=self.COLORES['acento_dorado'],
                bg=self.COLORES['fondo_card']).pack(pady=4)

        # Descripción si está disponible
        if producto.get('descripcion'):
            desc_text = producto['descripcion'][:150] + "..." if len(producto['descripcion']) > 150 else producto['descripcion']
            tk.Label(card, text=desc_text, font=('Inter', 9),
                    fg=self.COLORES['texto_secundario'],
                    bg=self.COLORES['fondo_card'], wraplength=400, justify=tk.CENTER).pack(pady=6, padx=20)

        # Separador
        tk.Frame(card, bg=self.COLORES['acento_dorado'], height=2).pack(fill=tk.X, pady=8, padx=15)

        # Precio
        precio_frame = tk.Frame(card, bg=self.COLORES['fondo_card'])
        precio_frame.pack(pady=8, padx=15, fill=tk.X)

        tk.Label(precio_frame, text="Precio:", font=('Inter', 10),
                fg=self.COLORES['texto_secundario'],
                bg=self.COLORES['fondo_card']).pack(side=tk.LEFT)

        tk.Label(precio_frame, text=f"${producto['precio']:,.0f}", font=('Inter', 13, 'bold'),
                fg=self.COLORES['acento_dorado'],
                bg=self.COLORES['fondo_card']).pack(side=tk.RIGHT)

        # Botón Agregar
        tk.Button(card, text="➕ Agregar al Carrito", bg=self.COLORES['verde_success'],
                 fg='white', font=('Inter', 11, 'bold'), relief='flat', 
                 padx=15, pady=12,
                 command=lambda: self._agregar_producto_dia(producto)).pack(fill=tk.X, padx=20, pady=(10, 14))

    def _crear_card_menu(self, parent, item, row, col):
        """Crear card de un item del menú - lado a lado"""
        # Dejar que la tarjeta se adapte al tamaño de la columna para evitar espacios
        card = tk.Frame(parent, bg=self.COLORES['fondo_card'], relief=tk.RAISED, bd=2)
        card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

        # Nombre
        tk.Label(card, text=item.nombre, font=('Inter', 14, 'bold'),
                fg=self.COLORES['texto_principal'],
                bg=self.COLORES['fondo_card'], wraplength=420).pack(pady=(10, 10), padx=20)

        # Descripción
        desc_text = item.descripcion[:200] + "..." if len(item.descripcion) > 200 else item.descripcion
        tk.Label(card, text=desc_text, font=('Inter', 11),
                fg=self.COLORES['texto_secundario'],
                bg=self.COLORES['fondo_card'], wraplength=420, justify=tk.CENTER).pack(pady=8, padx=20)

        # Separador
        tk.Frame(card, bg=self.COLORES['acento_dorado'], height=2).pack(fill=tk.X, pady=8, padx=15)

        # Precio
        precio_frame = tk.Frame(card, bg=self.COLORES['fondo_card'])
        precio_frame.pack(pady=8, padx=15, fill=tk.X)

        tk.Label(precio_frame, text="Precio:", font=('Inter', 10),
                fg=self.COLORES['texto_secundario'],
                bg=self.COLORES['fondo_card']).pack(side=tk.LEFT)

        tk.Label(precio_frame, text=f"${item.precio:,.0f}", font=('Inter', 13, 'bold'),
                fg=self.COLORES['acento_dorado'],
                bg=self.COLORES['fondo_card']).pack(side=tk.RIGHT)

        # Botón Agregar
        tk.Button(card, text="➕ Agregar al Carrito", bg=self.COLORES['verde_success'],
                 fg='white', font=('Inter', 11, 'bold'), relief='flat', 
                 padx=15, pady=12,
                 command=lambda: self._agregar_al_carrito(item)).pack(fill=tk.X, padx=20, pady=(10, 14))
    
    def _crear_card_producto_custom(self, parent, producto, row, col):
        """Crear card de un producto personalizado - lado a lado"""
        card = tk.Frame(parent, bg=self.COLORES['fondo_card'], relief=tk.RAISED, bd=2)
        card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

        # Nombre
        tk.Label(card, text=producto['nombre'], font=('Inter', 14, 'bold'),
                fg=self.COLORES['texto_principal'],
                bg=self.COLORES['fondo_card'], wraplength=420).pack(pady=(10, 10), padx=20)

        # Categoría
        categoria = producto.get('categoria', 'General')
        tk.Label(card, text=f"📁 {categoria}", font=('Inter', 11),
                fg=self.COLORES['acento_dorado'],
                bg=self.COLORES['fondo_card']).pack(pady=6, padx=20)

        # Separador visual
        tk.Frame(card, bg=self.COLORES['acento_dorado'], height=2).pack(fill=tk.X, pady=8, padx=15)

        # Precio (destacado)
        precio_frame = tk.Frame(card, bg=self.COLORES['fondo_card'])
        precio_frame.pack(pady=8, padx=20, fill=tk.X)

        tk.Label(precio_frame, text="Precio:", font=('Inter', 10),
                fg=self.COLORES['texto_secundario'],
                bg=self.COLORES['fondo_card']).pack(side=tk.LEFT)

        tk.Label(precio_frame, text=f"${float(producto['precio']):,.0f}", font=('Inter', 13, 'bold'),
                fg=self.COLORES['acento_dorado'],
                bg=self.COLORES['fondo_card']).pack(side=tk.RIGHT)

        # Botón Agregar
        tk.Button(card, text="➕ Agregar al Carrito", bg=self.COLORES['verde_success'],
                 fg='white', font=('Inter', 11, 'bold'), relief='flat', 
                 padx=15, pady=12,
                 command=lambda: self._agregar_producto_custom_al_carrito(producto)).pack(fill=tk.X, padx=18, pady=(10, 14))
    
    def _agregar_producto_promocion(self, producto):
        """Agregar producto en promoción al carrito con precio especial"""
        self.pedido.agregar_item(
            f"{producto['nombre']} 🎁",
            float(producto['precio_especial']), 
            1
        )
        self._actualizar_carrito()
        self._mostrar_notificacion(
            f"✓ {producto['nombre']} agregado\n💰 Ahorro: ${producto['precio_original'] - producto['precio_especial']:,.0f}"
        )

    def _agregar_producto_dia(self, producto):
        """Agregar producto del menú del día al carrito"""
        self.pedido.agregar_item(producto['nombre'], float(producto['precio']), 1)
        self._actualizar_carrito()
        self._mostrar_notificacion(f"✓ {producto['nombre']} agregado")

    def _agregar_al_carrito(self, item):
        """Agregar item al carrito"""
        self.pedido.agregar_item(item.nombre, item.precio, 1)
        self._actualizar_carrito()
        self._mostrar_notificacion(f"✓ {item.nombre} agregado")
    
    def _agregar_producto_custom_al_carrito(self, producto):
        """Agregar producto personalizado al carrito"""
        self.pedido.agregar_item(producto['nombre'], float(producto['precio']), 1)
        self._actualizar_carrito()
        self._mostrar_notificacion(f"✓ {producto['nombre']} agregado")
    
    def _mostrar_notificacion(self, mensaje):
        """Mostrar notificación temporal dentro de la ventana, esquina superior derecha"""
        # Crear frame de notificación dentro de la ventana principal
        notif_frame = tk.Frame(self.ventana, bg=self.COLORES['verde_success'], height=60)
        
        # Contenedor con padding
        container = tk.Frame(notif_frame, bg=self.COLORES['verde_success'])
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        tk.Label(container, text=mensaje, font=('Inter', 11, 'bold'),
                fg='white', bg=self.COLORES['verde_success']).pack(expand=True)
        
        # Posicionar en esquina superior derecha de la ventana
        notif_frame.place(x=self.ventana.winfo_width() - 370, y=10, width=350, height=60)
        
        # Auto-cerrar después de 2 segundos
        self.ventana.after(2000, notif_frame.destroy)
    
    def _crear_tab_carrito(self, parent):
        """Pestaña del carrito con todos los items"""
        # Panel de items
        items_frame = tk.Frame(parent, bg=self.COLORES['fondo_principal'])
        items_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas con scroll
        canvas = tk.Canvas(items_frame, bg=self.COLORES['fondo_principal'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(items_frame, orient="vertical", command=canvas.yview)
        
        self.carrito_frame = tk.Frame(canvas, bg=self.COLORES['fondo_principal'])
        self.carrito_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.carrito_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Panel inferior con totales y acciones
        footer_frame = tk.Frame(parent, bg=self.COLORES['fondo_card'], height=200)
        footer_frame.pack(fill=tk.X, padx=10, pady=10, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        
        # Totales
        totales_frame = tk.Frame(footer_frame, bg=self.COLORES['fondo_card'])
        totales_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # Subtotal
        tk.Label(totales_frame, text="Subtotal:", font=('Inter', 10),
                fg=self.COLORES['texto_secundario'],
                bg=self.COLORES['fondo_card']).pack(side=tk.LEFT)
        self.label_subtotal = tk.Label(totales_frame, text="$0", font=('Inter', 10, 'bold'),
                                       fg=self.COLORES['texto_principal'],
                                       bg=self.COLORES['fondo_card'])
        self.label_subtotal.pack(side=tk.RIGHT, padx=(0, 50))
        
        # ITBMS
        tk.Label(totales_frame, text="ITBMS (19%):", font=('Inter', 10),
                fg=self.COLORES['texto_secundario'],
                bg=self.COLORES['fondo_card']).pack(side=tk.LEFT)
        self.label_itbms = tk.Label(totales_frame, text="$0", font=('Inter', 10, 'bold'),
                                   fg=self.COLORES['texto_principal'],
                                   bg=self.COLORES['fondo_card'])
        self.label_itbms.pack(side=tk.RIGHT, padx=(0, 50))
        
        # Descuento
        desc_frame = tk.Frame(footer_frame, bg=self.COLORES['fondo_card'])
        desc_frame.pack(fill=tk.X, padx=15, pady=5)
        
        tk.Label(desc_frame, text="Descuento:", font=('Inter', 10),
                fg=self.COLORES['texto_secundario'],
                bg=self.COLORES['fondo_card']).pack(side=tk.LEFT)
        
        self.descuento_var = tk.StringVar(value="0")
        entry_desc = tk.Entry(desc_frame, textvariable=self.descuento_var, width=10, font=('Inter', 9))
        entry_desc.pack(side=tk.RIGHT)
        entry_desc.bind("<KeyRelease>", lambda e: self._actualizar_totales())
        
        # Total
        total_frame = tk.Frame(footer_frame, bg=self.COLORES['fondo_card'])
        total_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(total_frame, text="TOTAL:", font=('Inter', 12, 'bold'),
                fg=self.COLORES['acento_dorado'],
                bg=self.COLORES['fondo_card']).pack(side=tk.LEFT)
        self.label_total = tk.Label(total_frame, text="$0", font=('Inter', 12, 'bold'),
                                   fg=self.COLORES['acento_dorado'],
                                   bg=self.COLORES['fondo_card'])
        self.label_total.pack(side=tk.RIGHT)
        
        # Botones
        botones_frame = tk.Frame(footer_frame, bg=self.COLORES['fondo_card'])
        botones_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Button(botones_frame, text="Procesar Pedido", bg=self.COLORES['verde_success'],
                 fg='white', font=('Inter', 10, 'bold'), relief='flat', padx=20, pady=10,
                 command=self._procesar_pedido).pack(side=tk.LEFT, padx=5)
        
        tk.Button(botones_frame, text="Limpiar Carrito", bg=self.COLORES['rojo_danger'],
                 fg='white', font=('Inter', 10, 'bold'), relief='flat', padx=20, pady=10,
                 command=self._limpiar_carrito).pack(side=tk.LEFT, padx=5)
        
        self._actualizar_carrito()
    
    def _actualizar_carrito(self):
        """Actualizar visualización del carrito"""
        for widget in self.carrito_frame.winfo_children():
            widget.destroy()
        
        if not self.pedido.items:
            # Frame centrado para el carrito vacío - usa anchor center
            empty_frame = tk.Frame(self.carrito_frame, bg=self.COLORES['fondo_principal'])
            empty_frame.pack(expand=True, fill=tk.BOTH, anchor=tk.CENTER)
            
            # Contenedor interior para centrado perfecto
            inner_container = tk.Frame(empty_frame, bg=self.COLORES['fondo_principal'])
            inner_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            
            # Título con emoji
            title_label = tk.Label(inner_container, text="🛒",
                    font=('Inter', 48), fg=self.COLORES['acento_dorado'],
                    bg=self.COLORES['fondo_principal'])
            title_label.pack()
            
            # Texto principal
            main_text = tk.Label(inner_container, text="Carrito Vacío",
                    font=('Inter', 18, 'bold'), fg=self.COLORES['acento_dorado'],
                    bg=self.COLORES['fondo_principal'])
            main_text.pack(pady=(10, 5))
            
            # Texto secundario con diseño
            subtitle_frame = tk.Frame(inner_container, bg=self.COLORES['fondo_card'], 
                                     relief=tk.FLAT, bd=1)
            subtitle_frame.pack(pady=(5, 0), padx=20)
            
            subtitle_label = tk.Label(subtitle_frame, text="Agrega items desde el menú",
                    font=('Inter', 11), fg=self.COLORES['texto_secundario'],
                    bg=self.COLORES['fondo_card'], padx=20, pady=10)
            subtitle_label.pack()
            
            self._actualizar_totales()
            return
        
        for idx, item in enumerate(self.pedido.items):
            item_frame = tk.Frame(self.carrito_frame, bg=self.COLORES['fondo_card'], relief=tk.FLAT, bd=1)
            item_frame.pack(fill=tk.X, pady=8, padx=10)
            
            # Info
            info_frame = tk.Frame(item_frame, bg=self.COLORES['fondo_card'])
            info_frame.pack(fill=tk.X, padx=10, pady=10)
            
            tk.Label(info_frame, text=item['nombre'], font=('Inter', 11, 'bold'),
                    fg=self.COLORES['texto_principal'],
                    bg=self.COLORES['fondo_card']).pack(side=tk.LEFT)
            
            tk.Label(info_frame, text=f"${item['precio'] * item['cantidad']:,.0f}", 
                    font=('Inter', 11, 'bold'), fg=self.COLORES['acento_dorado'],
                    bg=self.COLORES['fondo_card']).pack(side=tk.RIGHT)
            
            # Controles
            control_frame = tk.Frame(item_frame, bg=self.COLORES['fondo_card'])
            control_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
            
            tk.Button(control_frame, text="-", width=2, bg=self.COLORES['rojo_danger'],
                     fg='white', relief='flat', command=lambda i=idx: self._decrementar(i)).pack(side=tk.LEFT, padx=2)
            
            tk.Label(control_frame, text=f"x{item['cantidad']}", font=('Inter', 10),
                    fg=self.COLORES['texto_principal'],
                    bg=self.COLORES['fondo_card']).pack(side=tk.LEFT, padx=10)
            
            tk.Button(control_frame, text="+", width=2, bg=self.COLORES['verde_success'],
                     fg='white', relief='flat', command=lambda i=idx: self._incrementar(i)).pack(side=tk.LEFT, padx=2)
            
            tk.Button(control_frame, text="Eliminar", bg='#666666',
                     fg='white', relief='flat', font=('Inter', 8),
                     command=lambda i=idx: self._eliminar_item(i)).pack(side=tk.RIGHT, padx=2)
        
        self._actualizar_totales()
    
    def _incrementar(self, idx):
        """Incrementar cantidad"""
        if 0 <= idx < len(self.pedido.items):
            self.pedido.items[idx]['cantidad'] += 1
            self._actualizar_carrito()
    
    def _decrementar(self, idx):
        """Decrementar cantidad"""
        if 0 <= idx < len(self.pedido.items):
            if self.pedido.items[idx]['cantidad'] > 1:
                self.pedido.items[idx]['cantidad'] -= 1
            else:
                del self.pedido.items[idx]
            self._actualizar_carrito()
    
    def _eliminar_item(self, idx):
        """Eliminar item del carrito"""
        if 0 <= idx < len(self.pedido.items):
            del self.pedido.items[idx]
            self._actualizar_carrito()
    
    def _actualizar_totales(self):
        """Actualizar cálculo de totales"""
        subtotal = self.pedido.calcular_total()
        
        try:
            descuento = float(self.descuento_var.get() or 0)
        except ValueError:
            descuento = 0
            self.descuento_var.set("0")
        
        itbms = subtotal * 0.19
        total = subtotal + itbms - descuento
        
        self.label_subtotal.config(text=f"${subtotal:,.0f}")
        self.label_itbms.config(text=f"${itbms:,.0f}")
        self.label_total.config(text=f"${total:,.0f}")
    
    def _limpiar_carrito(self):
        """Limpiar carrito"""
        if messagebox.askyesno("Confirmar", "¿Limpiar carrito?"):
            self.pedido.items = []
            self._actualizar_carrito()
    
    def _procesar_pedido(self):
        """Procesar pedido"""
        if not self.pedido.items:
            messagebox.showwarning("Carrito Vacío", "Agrega items antes de procesar")
            return
        
        # Ventana de cliente
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Procesar Pedido")
        ventana.geometry("500x400")
        ventana.configure(bg=self.COLORES['fondo_principal'])
        
        # Centrar
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - 250
        y = (ventana.winfo_screenheight() // 2) - 200
        ventana.geometry(f"+{x}+{y}")
        
        # Título
        tk.Label(ventana, text="Información del Cliente", font=('Inter', 14, 'bold'),
                fg=self.COLORES['acento_dorado'],
                bg=self.COLORES['fondo_principal']).pack(pady=20)
        
        # Nombre cliente
        tk.Label(ventana, text="Nombre del Cliente:", font=('Inter', 11),
                fg=self.COLORES['texto_principal'],
                bg=self.COLORES['fondo_principal']).pack(pady=(10, 0), padx=20, anchor=tk.W)
        
        entry_cliente = tk.Entry(ventana, font=('Inter', 11), width=30)
        entry_cliente.pack(pady=10, padx=20)
        
        # Método de pago - con estilo moderno
        tk.Label(ventana, text="Método de Pago:", font=('Inter', 11),
                fg=self.COLORES['texto_principal'],
                bg=self.COLORES['fondo_principal']).pack(pady=(20, 10), padx=20, anchor=tk.W)
        
        metodo_var = tk.StringVar(value="Efectivo")
        metodos = ["Efectivo", "Tarjeta Crédito", "Tarjeta Débito", "Transferencia"]
        
        combo_pago = ttk.Combobox(ventana, textvariable=metodo_var, values=metodos, 
                                 state="readonly", width=30, font=('Inter', 10))
        combo_pago.pack(pady=10, padx=20)
        combo_pago.current(0)
        
        # Botones
        btn_frame = tk.Frame(ventana, bg=self.COLORES['fondo_principal'])
        btn_frame.pack(pady=30)
        
        def finalizar():
            cliente = entry_cliente.get().strip()
            if not cliente:
                messagebox.showwarning("Error", "Ingresa nombre del cliente")
                return
            
            descuento = float(self.descuento_var.get() or 0)
            self._mostrar_factura_final(cliente, metodo_var.get(), descuento)
            ventana.destroy()
        
        tk.Button(btn_frame, text="Generar Factura", bg=self.COLORES['verde_success'],
                 fg='white', font=('Inter', 11, 'bold'), relief='flat', padx=30, pady=10,
                 command=finalizar).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="Cancelar", bg=self.COLORES['rojo_danger'],
                 fg='white', font=('Inter', 11, 'bold'), relief='flat', padx=30, pady=10,
                 command=ventana.destroy).pack(side=tk.LEFT, padx=10)
    
    def _mostrar_factura_final(self, cliente, metodo_pago, descuento):
        """Mostrar factura final"""
        factura = tk.Toplevel(self.ventana)
        factura.title("Factura")
        factura.geometry("700x800")
        factura.configure(bg=self.COLORES['fondo_principal'])
        
        # Centrar
        factura.update_idletasks()
        x = (factura.winfo_screenwidth() // 2) - 350
        y = (factura.winfo_screenheight() // 2) - 400
        factura.geometry(f"+{x}+{y}")
        
        # Canvas con scroll
        canvas = tk.Canvas(factura, bg=self.COLORES['fondo_principal'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(factura, orient="vertical", command=canvas.yview)
        
        content_frame = tk.Frame(canvas, bg=self.COLORES['fondo_principal'])
        content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Contenido de factura
        factura_text = self._generar_contenido_factura(cliente, metodo_pago, descuento)
        
        tk.Label(content_frame, text=factura_text, font=('Courier', 9),
                fg=self.COLORES['texto_principal'],
                bg=self.COLORES['fondo_principal'], justify=tk.LEFT).pack(padx=20, pady=20)
        
        # Botones
        btn_frame = tk.Frame(factura, bg=self.COLORES['fondo_card'])
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def imprimir_linux():
            self._imprimir_factura_linux(cliente, metodo_pago, descuento)
        
        tk.Button(btn_frame, text="🖨️ Imprimir", bg=self.COLORES['verde_success'],
                 fg='white', font=('Inter', 10, 'bold'), relief='flat', padx=15, pady=10,
                 command=imprimir_linux).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="Cerrar", bg=self.COLORES['rojo_danger'],
                 fg='white', font=('Inter', 10, 'bold'), relief='flat', padx=15, pady=10,
                 command=lambda: (factura.destroy(), self._limpiar_carrito())).pack(side=tk.RIGHT, padx=5)
    
    def _generar_contenido_factura(self, cliente, metodo_pago, descuento):
        """Generar contenido de factura"""
        try:
            subtotal = self.pedido.calcular_total()
            itbms = subtotal * 0.19
            total = subtotal + itbms - descuento
            
            fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            
            contenido = f"""
{'='*50}
                    FACTURA
{'='*50}

Fecha: {fecha}
Cliente: {cliente}

{'-'*50}
ITEMS:
{'-'*50}
"""
            for item in self.pedido.items:
                cantidad = item['cantidad']
                precio = item['precio']
                subtotal_item = precio * cantidad
                contenido += f"{item['nombre']:<30} x{cantidad:>2}  ${subtotal_item:>8,.0f}\n"
            
            contenido += f"""
{'-'*50}
Subtotal:          ${subtotal:>10,.0f}
ITBMS (19%):       ${itbms:>10,.0f}
Descuento:         ${descuento:>10,.0f}
{'-'*50}
TOTAL:             ${total:>10,.0f}
{'-'*50}

Método de Pago: {metodo_pago}

{'='*50}
         Gracias por su compra
{'='*50}
"""
            return contenido
        except Exception as e:
            return f"Error al generar factura: {str(e)}"
    
    def _imprimir_factura_linux(self, cliente, metodo_pago, descuento):
        """Abrir diálogo de impresión tipo Windows"""
        try:
            contenido = self._generar_contenido_factura(cliente, metodo_pago, descuento)
            # Usar el módulo separado de diálogo de impresión
            DialogoImpresion(self.ventana, self.COLORES, contenido, cliente)
        except Exception as e:
            messagebox.showerror("❌ Error de Impresión", f"Error: {str(e)}")
    
    def _guardar_factura(self, cliente, metodo_pago, descuento):
        """Guardar factura como texto"""
        archivo = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos", "*.*")]
        )
        
        if archivo:
            contenido = self._generar_contenido_factura(cliente, metodo_pago, descuento)
            with open(archivo, 'w', encoding='utf-8') as f:
                f.write(contenido)
            messagebox.showinfo("Éxito", f"Factura guardada: {archivo}")
    
    def _crear_tab_productos(self, parent):
        """Pestaña para gestionar productos personalizados - MUESTRA TODOS"""
        # Panel superior con botones y título
        toolbar = tk.Frame(parent, bg=self.COLORES['fondo_card'], height=70)
        toolbar.pack(fill=tk.X, padx=10, pady=10)
        toolbar.pack_propagate(False)
        
        # Título de la sección
        tk.Label(toolbar, text="⚙️ Gestión de Productos", 
                font=('Inter', 12, 'bold'),
                fg=self.COLORES['acento_dorado'],
                bg=self.COLORES['fondo_card']).pack(side=tk.LEFT, padx=15, pady=10)
        
        # Botón actualizar
        tk.Button(toolbar, text="🔄 Actualizar", bg=self.COLORES['acento_dorado'],
                 fg='black', font=('Inter', 10, 'bold'), relief='flat', padx=15, pady=10,
                 command=self._actualizar_lista_productos).pack(side=tk.RIGHT, padx=5, pady=10)
        
        tk.Button(toolbar, text="➕ Nuevo Producto", bg=self.COLORES['verde_success'],
                 fg='white', font=('Inter', 10, 'bold'), relief='flat', padx=15, pady=10,
                 command=self._crear_producto_dialog).pack(side=tk.RIGHT, padx=5, pady=10)
        
        # Lista de productos con scroll mejorado
        lista_frame = tk.Frame(parent, bg=self.COLORES['fondo_principal'])
        lista_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas con scroll
        self.productos_canvas = tk.Canvas(lista_frame, bg=self.COLORES['fondo_principal'], 
                                         highlightthickness=0)
        scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", 
                                 command=self.productos_canvas.yview)
        
        self.productos_lista_frame = tk.Frame(self.productos_canvas, 
                                             bg=self.COLORES['fondo_principal'])
        
        # Bind para actualizar el scroll region
        self.productos_lista_frame.bind(
            "<Configure>",
            lambda e: self.productos_canvas.configure(scrollregion=self.productos_canvas.bbox("all"))
        )
        
        # Bind para scroll con rueda del mouse
        self.productos_canvas.bind_all("<MouseWheel>", 
            lambda e: self.productos_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        # Crear ventana del canvas con ancho dinámico
        canvas_window = self.productos_canvas.create_window((0, 0), 
                                                            window=self.productos_lista_frame, 
                                                            anchor="nw")
        
        # Ajustar ancho del frame al ancho del canvas
        def configurar_ancho(event):
            self.productos_canvas.itemconfig(canvas_window, width=event.width)
        
        self.productos_canvas.bind('<Configure>', configurar_ancho)
        self.productos_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.productos_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        print("📋 Inicializando pestaña de productos...")
        self._actualizar_lista_productos()
    
    def _actualizar_lista_productos(self):
        """Actualizar lista de productos desde la base de datos - TODOS los productos"""
        print("=" * 60)
        print("🔄 Actualizando lista de productos...")
        
        for widget in self.productos_lista_frame.winfo_children():
            widget.destroy()
        
        # Obtener todos los productos de la BD
        try:
            productos_bd = self.menu.obtener_todos_productos()
            print(f"✓ Productos obtenidos: {len(productos_bd) if productos_bd else 0}")
        except Exception as e:
            print(f"✗ Error al obtener productos: {e}")
            import traceback
            traceback.print_exc()
            tk.Label(self.productos_lista_frame, 
                    text=f"❌ Error al cargar productos:\n{str(e)}",
                    font=('Inter', 11), fg=self.COLORES['rojo_danger'],
                    bg=self.COLORES['fondo_principal']).pack(pady=40)
            return
        
        if not productos_bd or len(productos_bd) == 0:
            tk.Label(self.productos_lista_frame, 
                    text="⚠️ Sin productos en la base de datos\n\nHaz clic en '+ Nuevo Producto' para agregar",
                    font=('Inter', 11), fg=self.COLORES['texto_secundario'],
                    bg=self.COLORES['fondo_principal'], justify=tk.CENTER).pack(pady=40)
            return
        
        # Mostrar contador de productos
        contador_frame = tk.Frame(self.productos_lista_frame, bg=self.COLORES['fondo_card'])
        contador_frame.pack(fill=tk.X, pady=(0, 10), padx=10)
        
        tk.Label(contador_frame, 
                text=f"📦 Mostrando TODOS los productos: {len(productos_bd)}", 
                font=('Inter', 12, 'bold'),
                fg=self.COLORES['acento_dorado'],
                bg=self.COLORES['fondo_card']).pack(pady=10)
        
        # Mensaje informativo
        tk.Label(self.productos_lista_frame,
                text="⬇️ Desplázate hacia abajo para ver todos los productos ⬇️",
                font=('Inter', 9),
                fg=self.COLORES['texto_secundario'],
                bg=self.COLORES['fondo_principal']).pack(pady=(0, 10))
        
        # Iterar sobre TODOS los productos
        for idx, prod in enumerate(productos_bd, 1):
            prod_frame = tk.Frame(self.productos_lista_frame, bg=self.COLORES['fondo_card'], 
                                 relief=tk.RAISED, bd=2)
            prod_frame.pack(fill=tk.X, pady=5, padx=10)
            
            # Info con número
            info = tk.Frame(prod_frame, bg=self.COLORES['fondo_card'])
            info.pack(fill=tk.X, padx=10, pady=10)
            
            # Número del producto
            tk.Label(info, text=f"{idx}.", font=('Inter', 10, 'bold'),
                    fg=self.COLORES['acento_dorado'],
                    bg=self.COLORES['fondo_card']).pack(side=tk.LEFT, padx=(0, 5))
            
            tk.Label(info, text=prod['nombre'], font=('Inter', 11, 'bold'),
                    fg=self.COLORES['texto_principal'],
                    bg=self.COLORES['fondo_card']).pack(side=tk.LEFT)
            
            tk.Label(info, text=f"${float(prod['precio']):,.0f}", font=('Inter', 11, 'bold'),
                    fg=self.COLORES['acento_dorado'],
                    bg=self.COLORES['fondo_card']).pack(side=tk.RIGHT, padx=(0, 20))
            
            tk.Label(info, text=f"ID: {prod['id_producto']}", font=('Inter', 8),
                    fg=self.COLORES['texto_secundario'],
                    bg=self.COLORES['fondo_card']).pack(side=tk.RIGHT, padx=(0, 20))
            
            # Botones
            btn = tk.Frame(prod_frame, bg=self.COLORES['fondo_card'])
            btn.pack(fill=tk.X, padx=10, pady=(0, 10))
            
            tk.Button(btn, text="Editar", bg=self.COLORES['acento_dorado'],
                     fg='black', relief='flat', font=('Inter', 9), width=10,
                     command=lambda p=prod: self._editar_producto_dialog(p)).pack(side=tk.LEFT, padx=2)
            
            tk.Button(btn, text="Eliminar", bg=self.COLORES['rojo_danger'],
                     fg='white', relief='flat', font=('Inter', 9), width=10,
                     command=lambda p=prod: self._eliminar_producto(p)).pack(side=tk.LEFT, padx=2)
        
        print(f"✓ Se crearon {len(productos_bd)} widgets de productos en la interfaz")
        print("=" * 60)
    
    def _crear_producto_dialog(self):
        """Diálogo para crear nuevo producto"""
        self._mostrar_form_producto(None, None)
    
    def _editar_producto_dialog(self, producto):
        """Diálogo para editar producto"""
        self._mostrar_form_producto(producto, producto['id_producto'])
    
    def _mostrar_form_producto(self, producto=None, id_producto=None):
        """Mostrar formulario completo de producto con todos los detalles"""
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Editar Producto" if producto else "Nuevo Producto")
        ventana.geometry("550x750")
        ventana.configure(bg=self.COLORES['fondo_principal'])
        
        # Centrar ventana
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - 275
        y = (ventana.winfo_screenheight() // 2) - 375
        ventana.geometry(f"+{x}+{y}")
        
        # Título
        titulo_text = "Editar Producto" if producto else "Crear Nuevo Producto"
        tk.Label(ventana, text=titulo_text, font=('Inter', 14, 'bold'),
                fg=self.COLORES['acento_dorado'],
                bg=self.COLORES['fondo_principal']).pack(pady=(15, 10))
        
        if producto:
            tk.Label(ventana, text=f"ID: {producto['id_producto']}", font=('Inter', 9),
                    fg=self.COLORES['texto_secundario'],
                    bg=self.COLORES['fondo_principal']).pack(pady=(0, 10))
        
        # Nombre
        tk.Label(ventana, text="Nombre:", font=('Inter', 11),
                fg=self.COLORES['texto_principal'],
                bg=self.COLORES['fondo_principal']).pack(pady=(10, 5), padx=20, anchor=tk.W)
        entry_nombre = tk.Entry(ventana, font=('Inter', 11), width=30)
        entry_nombre.pack(pady=5, padx=20)
        if producto:
            entry_nombre.insert(0, producto['nombre'])
        
        # Precio
        tk.Label(ventana, text="Precio (COP):", font=('Inter', 11),
                fg=self.COLORES['texto_principal'],
                bg=self.COLORES['fondo_principal']).pack(pady=(15, 5), padx=20, anchor=tk.W)
        entry_precio = tk.Entry(ventana, font=('Inter', 11), width=30)
        entry_precio.pack(pady=5, padx=20)
        if producto:
            entry_precio.insert(0, str(producto['precio']))
        
        # Descripción / Detalles (Text widget multilínea)
        tk.Label(ventana, text="Descripción y Detalles:", font=('Inter', 11, 'bold'),
                fg=self.COLORES['texto_principal'],
                bg=self.COLORES['fondo_principal']).pack(pady=(15, 5), padx=20, anchor=tk.W)
        
        tk.Label(ventana, text="Ingresa detalles del producto (ingredientes, características, etc.)", 
                font=('Inter', 9),
                fg=self.COLORES['texto_secundario'],
                bg=self.COLORES['fondo_principal']).pack(pady=(0, 5), padx=20, anchor=tk.W)
        
        # Frame para el Text widget con scrollbar
        desc_frame = tk.Frame(ventana, bg=self.COLORES['fondo_principal'])
        desc_frame.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)
        
        # Scrollbar para la descripción
        scrollbar_desc = tk.Scrollbar(desc_frame)
        scrollbar_desc.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Text widget para descripción detallada
        text_desc = tk.Text(desc_frame, font=('Inter', 10), width=40, height=6,
                           wrap=tk.WORD, yscrollcommand=scrollbar_desc.set,
                           bg='white', fg='black', insertbackground='black',
                           relief=tk.SOLID, borderwidth=1)
        text_desc.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_desc.config(command=text_desc.yview)
        
        if producto:
            text_desc.insert('1.0', producto.get('descripcion', ''))
        else:
            # Texto de ejemplo placeholder
            text_desc.insert('1.0', 'Ejemplo: Delicioso platillo preparado con ingredientes frescos...')
            text_desc.config(fg='gray')
            
            # Limpiar placeholder al hacer clic
            def limpiar_placeholder(event):
                if text_desc.get('1.0', tk.END).strip().startswith('Ejemplo:'):
                    text_desc.delete('1.0', tk.END)
                    text_desc.config(fg='black')
            
            text_desc.bind('<FocusIn>', limpiar_placeholder)
        
        # Contador de caracteres
        contador_label = tk.Label(ventana, text="0 / 150 caracteres", 
                                 font=('Inter', 8),
                                 fg=self.COLORES['texto_secundario'],
                                 bg=self.COLORES['fondo_principal'])
        contador_label.pack(pady=(2, 5), padx=20, anchor=tk.E)
        
        def actualizar_contador(event=None):
            texto = text_desc.get('1.0', tk.END).strip()
            longitud = len(texto)
            if texto.startswith('Ejemplo:'):
                longitud = 0
            color = self.COLORES['rojo_danger'] if longitud > 150 else self.COLORES['texto_secundario']
            contador_label.config(text=f"{longitud} / 150 caracteres", fg=color)
        
        text_desc.bind('<KeyRelease>', actualizar_contador)
        actualizar_contador()
        
        # Tipo de Comida (desde BD)
        tk.Label(ventana, text="Tipo de Comida:", font=('Inter', 11),
                fg=self.COLORES['texto_principal'],
                bg=self.COLORES['fondo_principal']).pack(pady=(15, 5), padx=20, anchor=tk.W)
        
        tipos_comida = self.menu.obtener_tipos_comida()
        combo_cat = ttk.Combobox(ventana, values=tipos_comida, state="readonly", width=27)
        combo_cat.pack(pady=5, padx=20)
        if producto:
            combo_cat.set(producto.get('tipo', tipos_comida[0] if tipos_comida else 'Desayuno'))
        else:
            combo_cat.current(0) if tipos_comida else None
        
        # Imagen
        tk.Label(ventana, text="Imagen:", font=('Inter', 11),
                fg=self.COLORES['texto_principal'],
                bg=self.COLORES['fondo_principal']).pack(pady=(15, 5), padx=20, anchor=tk.W)
        
        imagen_frame = tk.Frame(ventana, bg=self.COLORES['fondo_principal'])
        imagen_frame.pack(pady=5, padx=20, fill=tk.X)
        
        label_imagen = tk.Label(imagen_frame, text="Sin imagen", font=('Inter', 9),
                               fg=self.COLORES['texto_secundario'],
                               bg=self.COLORES['fondo_principal'])
        label_imagen.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        imagen_actual = [producto['imagen'] if producto else None]
        
        def seleccionar_imagen():
            archivo = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg")])
            if archivo:
                imagen_actual[0] = archivo
                label_imagen.config(text=os.path.basename(archivo))
        
        tk.Button(imagen_frame, text="Seleccionar", bg=self.COLORES['acento_dorado'],
                 fg='black', relief='flat', font=('Inter', 9),
                 command=seleccionar_imagen).pack(side=tk.RIGHT, padx=5)
        
        # Botones
        btn_frame = tk.Frame(ventana, bg=self.COLORES['fondo_principal'])
        btn_frame.pack(pady=30)
        
        def guardar():
            nombre = entry_nombre.get().strip()
            try:
                precio = float(entry_precio.get())
            except ValueError:
                messagebox.showerror("Error", "Precio inválido. Ingresa solo números")
                return
            
            if precio <= 0:
                messagebox.showerror("Error", "El precio debe ser mayor a 0")
                return
            
            tipo = combo_cat.get()
            # Obtener texto del Text widget
            descripcion = text_desc.get('1.0', tk.END).strip()
            
            if not nombre or not tipo:
                messagebox.showerror("Error", "Completa el nombre y tipo de comida")
                return
            
            # Validar que la descripción no sea el texto de ejemplo
            if not descripcion or descripcion.startswith('Ejemplo:'):
                descripcion = f"Delicioso {nombre} - {tipo}"
            
            # Limitar descripción a 150 caracteres (según BD)
            if len(descripcion) > 150:
                descripcion = descripcion[:147] + "..."
            
            imagen = imagen_actual[0] if imagen_actual[0] else "sin_imagen.png"
            
            # Guardar en la base de datos
            try:
                if id_producto is not None:
                    # Actualizar producto existente
                    exito = self.menu.actualizar_producto(id_producto, nombre, precio, descripcion, imagen)
                    if exito:
                        messagebox.showinfo("✓ Éxito", "Producto actualizado en la base de datos")
                    else:
                        messagebox.showerror("✗ Error", "No se pudo actualizar el producto")
                        return
                else:
                    # Crear nuevo producto
                    nuevo_id = self.menu.crear_producto(nombre, precio, tipo, descripcion, imagen)
                    if nuevo_id:
                        messagebox.showinfo("✓ Éxito", f"Producto creado con ID: {nuevo_id}")
                    else:
                        messagebox.showerror("✗ Error", "No se pudo crear el producto")
                        return
                
                # Recargar productos desde la BD
                self.menu._cargar_menu_desde_db()
                self._actualizar_lista_productos()
                ventana.destroy()
                self._actualizar_grid_menu()
                
            except Exception as e:
                messagebox.showerror("✗ Error", f"Error al guardar en BD: {str(e)}")
        
        tk.Button(btn_frame, text="Guardar", bg=self.COLORES['verde_success'],
                 fg='white', font=('Inter', 11, 'bold'), relief='flat', padx=30, pady=10,
                 command=guardar).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="Cancelar", bg=self.COLORES['rojo_danger'],
                 fg='white', font=('Inter', 11, 'bold'), relief='flat', padx=30, pady=10,
                 command=ventana.destroy).pack(side=tk.LEFT, padx=10)
    
    def _eliminar_producto(self, producto):
        """Eliminar producto de la base de datos"""
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{producto['nombre']}'?\n\nEsta acción no se puede deshacer."):
            try:
                exito = self.menu.eliminar_producto(producto['id_producto'])
                if exito:
                    messagebox.showinfo("✓ Éxito", "Producto eliminado de la base de datos")
                    # Recargar productos
                    self.menu._cargar_menu_desde_db()
                    self._actualizar_lista_productos()
                    self._actualizar_grid_menu()
                else:
                    messagebox.showerror("✗ Error", "No se pudo eliminar el producto")
            except Exception as e:
                messagebox.showerror("✗ Error", f"Error al eliminar: {str(e)}")
    
    def _crear_tab_menu_dias(self, parent):
        """Pestaña para gestionar menús por día - con selección múltiple"""
        # Panel superior con controles
        header_frame = tk.Frame(parent, bg=self.COLORES['fondo_card'])
        header_frame.pack(fill=tk.X, padx=15, pady=12)
        
        # Container interior
        inner_frame = tk.Frame(header_frame, bg=self.COLORES['fondo_card'])
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Título
        tk.Label(inner_frame, text="📅 Crear Menú del Día", 
                font=('Inter', 14, 'bold'),
                fg=self.COLORES['acento_dorado'],
                bg=self.COLORES['fondo_card']).pack(pady=(0, 15))
        
        # Fila 1: Selector de día
        dia_frame = tk.Frame(inner_frame, bg=self.COLORES['fondo_card'])
        dia_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(dia_frame, text="📆 Día:", 
                font=('Inter', 11, 'bold'),
                fg=self.COLORES['texto_principal'],
                bg=self.COLORES['fondo_card']).pack(side=tk.LEFT, padx=(0, 10))
        
        self.dia_menu_var = tk.StringVar(value="Lunes")
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        
        combo_dia = ttk.Combobox(dia_frame, textvariable=self.dia_menu_var, 
                                values=dias, state="readonly", width=20,
                                font=('Inter', 11))
        combo_dia.pack(side=tk.LEFT, padx=5)
        combo_dia.bind("<<ComboboxSelected>>", lambda e: self._cargar_menu_dia_actual())
        
        # Botones de acción
        tk.Button(dia_frame, text="📋 Ver Menú Actual", 
                 bg=self.COLORES['acento_dorado'],
                 fg='black', font=('Inter', 9, 'bold'), relief='flat', 
                 padx=12, pady=6,
                 command=self._cargar_menu_dia_actual).pack(side=tk.LEFT, padx=10)
        
        tk.Button(dia_frame, text="🗑️ Limpiar Todo", 
                 bg=self.COLORES['rojo_promocion'],
                 fg='white', font=('Inter', 9, 'bold'), relief='flat', 
                 padx=12, pady=6,
                 command=self._limpiar_menu_temporal).pack(side=tk.LEFT, padx=5)
        
        # Fila 2: Filtro por tipo
        tipo_frame = tk.Frame(inner_frame, bg=self.COLORES['fondo_card'])
        tipo_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(tipo_frame, text="🍽️ Tipo:", 
                font=('Inter', 11, 'bold'),
                fg=self.COLORES['texto_principal'],
                bg=self.COLORES['fondo_card']).pack(side=tk.LEFT, padx=(0, 10))
        
        self.tipo_filtro_var = tk.StringVar(value="Todos")
        tipos = ["Todos"] + self.menu.obtener_tipos_comida()
        
        combo_tipo = ttk.Combobox(tipo_frame, textvariable=self.tipo_filtro_var,
                                 values=tipos, state="readonly", width=20,
                                 font=('Inter', 11))
        combo_tipo.pack(side=tk.LEFT, padx=5)
        combo_tipo.bind("<<ComboboxSelected>>", lambda e: self._filtrar_productos_por_tipo())
        
        # Fila 3: Agregar producto al menú temporal
        agregar_frame = tk.Frame(inner_frame, bg=self.COLORES['fondo_card'])
        agregar_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(agregar_frame, text="➕ Producto:", 
                font=('Inter', 11, 'bold'),
                fg=self.COLORES['texto_principal'],
                bg=self.COLORES['fondo_card']).pack(side=tk.LEFT, padx=(0, 10))
        
        # Combobox de productos disponibles
        self.producto_agregar_var = tk.StringVar()
        self.combo_productos = ttk.Combobox(agregar_frame, 
                                           textvariable=self.producto_agregar_var,
                                           state="readonly", width=35,
                                           font=('Inter', 10))
        self.combo_productos.pack(side=tk.LEFT, padx=5)
        
        tk.Button(agregar_frame, text="➕ Agregar a Lista", 
                 bg=self.COLORES['verde_success'],
                 fg='white', font=('Inter', 10, 'bold'), relief='flat', 
                 padx=15, pady=6,
                 command=self._agregar_a_lista_temporal).pack(side=tk.LEFT, padx=10)
        
        # Botón para guardar todo el menú
        guardar_frame = tk.Frame(inner_frame, bg=self.COLORES['fondo_card'])
        guardar_frame.pack(fill=tk.X, pady=15)
        
        tk.Button(guardar_frame, text="💾 GUARDAR MENÚ COMPLETO", 
                 bg='#2ecc71',
                 fg='white', font=('Inter', 12, 'bold'), relief='flat', 
                 padx=30, pady=12,
                 command=self._guardar_menu_completo).pack()
        
        # Panel dividido: Menú en construcción | Menú actual
        main_panel = tk.Frame(parent, bg=self.COLORES['fondo_principal'])
        main_panel.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Panel izquierdo: Menú en construcción
        left_panel = tk.Frame(main_panel, bg=self.COLORES['fondo_principal'])
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        tk.Label(left_panel, text="🔨 Menú en Construcción", 
                font=('Inter', 12, 'bold'),
                fg=self.COLORES['verde_success'],
                bg=self.COLORES['fondo_principal']).pack(pady=(0, 10))
        
        # Canvas con scroll para menú temporal
        canvas_temp = tk.Canvas(left_panel, bg=self.COLORES['fondo_principal'], highlightthickness=0)
        scrollbar_temp = ttk.Scrollbar(left_panel, orient="vertical", command=canvas_temp.yview)
        
        self.menu_temporal_frame = tk.Frame(canvas_temp, bg=self.COLORES['fondo_principal'])
        self.menu_temporal_frame.bind(
            "<Configure>",
            lambda e: canvas_temp.configure(scrollregion=canvas_temp.bbox("all"))
        )
        
        canvas_temp.create_window((0, 0), window=self.menu_temporal_frame, anchor="nw")
        canvas_temp.configure(yscrollcommand=scrollbar_temp.set)
        
        canvas_temp.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_temp.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Panel derecho: Menú actual en la base de datos
        right_panel = tk.Frame(main_panel, bg=self.COLORES['fondo_principal'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        tk.Label(right_panel, text="📋 Menú Actual (Base de Datos)", 
                font=('Inter', 12, 'bold'),
                fg=self.COLORES['acento_dorado'],
                bg=self.COLORES['fondo_principal']).pack(pady=(0, 10))
        
        # Canvas con scroll para menú actual
        canvas_actual = tk.Canvas(right_panel, bg=self.COLORES['fondo_principal'], highlightthickness=0)
        scrollbar_actual = ttk.Scrollbar(right_panel, orient="vertical", command=canvas_actual.yview)
        
        self.menu_actual_frame = tk.Frame(canvas_actual, bg=self.COLORES['fondo_principal'])
        self.menu_actual_frame.bind(
            "<Configure>",
            lambda e: canvas_actual.configure(scrollregion=canvas_actual.bbox("all"))
        )
        
        canvas_actual.create_window((0, 0), window=self.menu_actual_frame, anchor="nw")
        canvas_actual.configure(yscrollcommand=scrollbar_actual.set)
        
        canvas_actual.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_actual.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Inicializar lista temporal
        self.productos_menu_temporal = []
        
        # Cargar datos iniciales
        self._cargar_menu_dia_simple()
        self._cargar_menu_dia_actual()
    
    def _cargar_menu_dia_simple(self):
        """Carga los productos disponibles"""
        # Guardar todos los productos para filtrado
        self.todos_productos_disponibles = self.menu.obtener_todos_productos()
        
        # Filtrar por tipo seleccionado
        self._filtrar_productos_por_tipo()
    
    def _filtrar_productos_por_tipo(self):
        """Filtra los productos según el tipo seleccionado"""
        tipo_seleccionado = self.tipo_filtro_var.get()
        
        # Filtrar productos
        if tipo_seleccionado == "Todos":
            productos_filtrados = self.todos_productos_disponibles
        else:
            productos_filtrados = []
            for p in self.todos_productos_disponibles:
                tipo_producto = self.menu.obtener_tipo_producto(p['id_producto'])
                if tipo_producto == tipo_seleccionado:
                    productos_filtrados.append(p)
        
        # Crear lista con formato "nombre - $precio"
        productos_lista = [f"{p['nombre']} - ${p['precio']:.2f}" for p in productos_filtrados]
        self.combo_productos['values'] = productos_lista
        
        # Guardar referencia a productos para búsqueda
        self.productos_ref = {f"{p['nombre']} - ${p['precio']:.2f}": p 
                             for p in productos_filtrados}
        
        if productos_lista:
            self.combo_productos.set(productos_lista[0])
        else:
            self.combo_productos.set("")
    
    def _agregar_a_lista_temporal(self):
        """Agrega un producto a la lista temporal (sin guardar aún)"""
        seleccion = self.producto_agregar_var.get()
        
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un producto")
            return
        
        producto = self.productos_ref.get(seleccion)
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado")
            return
        
        # Verificar que no esté ya en la lista temporal
        if any(p['id_producto'] == producto['id_producto'] for p in self.productos_menu_temporal):
            messagebox.showwarning("Advertencia", f"'{producto['nombre']}' ya está en la lista")
            return
        
        # Agregar a la lista temporal
        self.productos_menu_temporal.append(producto)
        
        # Actualizar vista
        self._mostrar_menu_temporal()
    
    def _mostrar_menu_temporal(self):
        """Muestra los productos en la lista temporal"""
        # Limpiar frame
        for widget in self.menu_temporal_frame.winfo_children():
            widget.destroy()
        
        if not self.productos_menu_temporal:
            tk.Label(self.menu_temporal_frame,
                    text="No hay productos agregados\n\nSelecciona productos y haz clic en 'Agregar a Lista'",
                    font=('Inter', 11),
                    fg=self.COLORES['texto_secundario'],
                    bg=self.COLORES['fondo_principal'],
                    justify=tk.CENTER).pack(pady=30)
            return
        
        # Agrupar por tipo
        productos_por_tipo = {}
        for producto in self.productos_menu_temporal:
            tipo = self.menu.obtener_tipo_producto(producto['id_producto'])
            if tipo not in productos_por_tipo:
                productos_por_tipo[tipo] = []
            productos_por_tipo[tipo].append(producto)
        
        # Mostrar por tipo
        for tipo, prods in sorted(productos_por_tipo.items()):
            # Header del tipo
            tipo_frame = tk.Frame(self.menu_temporal_frame, bg='#27ae60')
            tipo_frame.pack(fill=tk.X, pady=(10, 0), padx=10)
            
            tk.Label(tipo_frame, text=f"{tipo} ({len(prods)})",
                    font=('Inter', 11, 'bold'),
                    fg='white',
                    bg='#27ae60').pack(pady=5, padx=10, anchor='w')
            
            # Productos del tipo
            for producto in prods:
                card = tk.Frame(self.menu_temporal_frame,
                              bg=self.COLORES['fondo_card'],
                              relief='solid', borderwidth=1)
                card.pack(fill=tk.X, pady=3, padx=10)
                
                info_frame = tk.Frame(card, bg=self.COLORES['fondo_card'])
                info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=10)
                
                tk.Label(info_frame, text=producto['nombre'],
                        font=('Inter', 11, 'bold'),
                        fg=self.COLORES['texto_principal'],
                        bg=self.COLORES['fondo_card']).pack(anchor='w')
                
                tk.Label(info_frame, text=f"${producto['precio']:.2f}",
                        font=('Inter', 10),
                        fg=self.COLORES['acento_dorado'],
                        bg=self.COLORES['fondo_card']).pack(anchor='w')
                
                btn_frame = tk.Frame(card, bg=self.COLORES['fondo_card'])
                btn_frame.pack(side=tk.RIGHT, padx=10)
                
                tk.Button(btn_frame, text="✖", 
                         bg=self.COLORES['rojo_promocion'],
                         fg='white', font=('Inter', 10, 'bold'), 
                         relief='flat', padx=8, pady=3,
                         command=lambda p=producto: self._quitar_de_lista_temporal(p)).pack()
        
        # Mostrar total
        total_frame = tk.Frame(self.menu_temporal_frame, bg=self.COLORES['acento_dorado'])
        total_frame.pack(fill=tk.X, pady=10, padx=10)
        
        tk.Label(total_frame, text=f"✓ Total: {len(self.productos_menu_temporal)} productos",
                font=('Inter', 11, 'bold'),
                fg='black',
                bg=self.COLORES['acento_dorado']).pack(pady=8)
    
    def _quitar_de_lista_temporal(self, producto):
        """Quita un producto de la lista temporal"""
        self.productos_menu_temporal = [p for p in self.productos_menu_temporal 
                                        if p['id_producto'] != producto['id_producto']]
        self._mostrar_menu_temporal()
    
    def _limpiar_menu_temporal(self):
        """Limpia toda la lista temporal"""
        if self.productos_menu_temporal:
            if messagebox.askyesno("Confirmar", "¿Limpiar todos los productos de la lista?"):
                self.productos_menu_temporal = []
                self._mostrar_menu_temporal()
        else:
            messagebox.showinfo("Información", "La lista ya está vacía")
    
    def _guardar_menu_completo(self):
        """Guarda el menú temporal completo en la base de datos"""
        if not self.productos_menu_temporal:
            messagebox.showwarning("Advertencia", "No hay productos para guardar")
            return
        
        dia = self.dia_menu_var.get()
        dia_id = self._get_dia_id(dia)
        
        # Confirmar acción
        msg = f"¿Guardar {len(self.productos_menu_temporal)} productos en el menú del {dia}?\n\n"
        msg += "Esto REEMPLAZARÁ el menú actual de ese día."
        
        if not messagebox.askyesno("Confirmar Guardado", msg):
            return
        
        # Primero eliminar el menú actual de ese día
        try:
            query_delete = "DELETE FROM MENU_PRODUCTO WHERE idDiaMenu = %s"
            db_manager.ejecutar_query(query_delete, (dia_id,), fetch=False)
            
            # Guardar cada producto
            productos_guardados = 0
            for producto in self.productos_menu_temporal:
                tipo = self.menu.obtener_tipo_producto(producto['id_producto'])
                if tipo:
                    if self.menu.agregar_producto_a_menu_dia(producto['id_producto'], tipo, dia_id):
                        productos_guardados += 1
            
            if productos_guardados == len(self.productos_menu_temporal):
                messagebox.showinfo("Éxito", 
                    f"✓ Menú guardado correctamente\n\n{productos_guardados} productos guardados en {dia}")
                
                # Limpiar lista temporal
                self.productos_menu_temporal = []
                self._mostrar_menu_temporal()
                
                # Actualizar menú actual
                self._cargar_menu_dia_actual()
                
                # Actualizar la vista del menú principal
                self._actualizar_grid_menu()
            else:
                messagebox.showwarning("Advertencia", 
                    f"Solo se guardaron {productos_guardados} de {len(self.productos_menu_temporal)} productos")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el menú: {str(e)}")
    
    def _cargar_menu_dia_actual(self):
        """Carga y muestra el menú actual de la base de datos"""
        # Limpiar frame
        for widget in self.menu_actual_frame.winfo_children():
            widget.destroy()
        
        dia = self.dia_menu_var.get()
        dia_id = self._get_dia_id(dia)
        
        productos = self.menu.obtener_productos_en_menu_dia(dia_id)
        
        if not productos:
            tk.Label(self.menu_actual_frame,
                    text=f"No hay menú guardado\npara {dia}",
                    font=('Inter', 12),
                    fg=self.COLORES['texto_secundario'],
                    bg=self.COLORES['fondo_principal'],
                    justify=tk.CENTER).pack(pady=30)
            return
        
        # Agrupar por tipo
        productos_por_tipo = {}
        for producto in productos:
            tipo = producto['tipo']
            if tipo not in productos_por_tipo:
                productos_por_tipo[tipo] = []
            productos_por_tipo[tipo].append(producto)
        
        # Mostrar por tipo
        for tipo, prods in sorted(productos_por_tipo.items()):
            # Header del tipo
            tipo_frame = tk.Frame(self.menu_actual_frame, bg=self.COLORES['acento_dorado'])
            tipo_frame.pack(fill=tk.X, pady=(10, 0), padx=10)
            
            tk.Label(tipo_frame, text=f"{tipo} ({len(prods)})",
                    font=('Inter', 11, 'bold'),
                    fg='black',
                    bg=self.COLORES['acento_dorado']).pack(pady=5, padx=10, anchor='w')
            
            # Productos del tipo
            for producto in prods:
                card = tk.Frame(self.menu_actual_frame,
                              bg=self.COLORES['fondo_card'],
                              relief='solid', borderwidth=1)
                card.pack(fill=tk.X, pady=3, padx=10)
                
                info_frame = tk.Frame(card, bg=self.COLORES['fondo_card'])
                info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=10)
                
                tk.Label(info_frame, text=producto['nombre'],
                        font=('Inter', 11, 'bold'),
                        fg=self.COLORES['texto_principal'],
                        bg=self.COLORES['fondo_card']).pack(anchor='w')
                
                tk.Label(info_frame, text=f"${producto['precio']:.2f}",
                        font=('Inter', 10),
                        fg=self.COLORES['acento_dorado'],
                        bg=self.COLORES['fondo_card']).pack(anchor='w')
        
        # Mostrar total
        total_frame = tk.Frame(self.menu_actual_frame, bg='#3498db')
        total_frame.pack(fill=tk.X, pady=10, padx=10)
        
        tk.Label(total_frame, text=f"📋 Total: {len(productos)} productos guardados",
                font=('Inter', 11, 'bold'),
                fg='white',
                bg='#3498db').pack(pady=8)
    
    def _get_dia_id(self, dia_nombre):
        """Convertir nombre de día a ID"""
        dias_map = {
            "Lunes": 1, "Martes": 2, "Miércoles": 3, "Jueves": 4,
            "Viernes": 5, "Sábado": 6, "Domingo": 7
        }
        return dias_map.get(dia_nombre, 1)
    
    def ejecutar(self):
        """Ejecutar aplicación"""
        self.ventana.mainloop()


if __name__ == "__main__":
    app = InterfazRestaurante()
    app.ejecutar()
