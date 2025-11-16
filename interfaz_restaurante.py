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
        self.productos_personalizados = []
        self.cargar_productos_personalizados()
        
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
        
    def cargar_productos_personalizados(self):
        """Cargar productos personalizados desde archivo"""
        try:
            if os.path.exists("productos_custom.json"):
                with open("productos_custom.json", "r") as f:
                    self.productos_personalizados = json.load(f)
        except:
            self.productos_personalizados = []
    
    def guardar_productos_personalizados(self):
        """Guardar productos personalizados a archivo"""
        with open("productos_custom.json", "w") as f:
            json.dump(self.productos_personalizados, f, indent=2)
    
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
        # Panel superior con categoría - diseño mejorado
        header_frame = tk.Frame(parent, bg=self.COLORES['fondo_card'], height=70)
        header_frame.pack(fill=tk.X, padx=15, pady=12)
        header_frame.pack_propagate(False)
        
        # Container interior para alineación
        inner_frame = tk.Frame(header_frame, bg=self.COLORES['fondo_card'])
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Label con diseño mejorado
        label = tk.Label(inner_frame, text="🎯 Selecciona una Categoría:", 
                        bg=self.COLORES['fondo_card'],
                        fg=self.COLORES['acento_dorado'], 
                        font=('Inter', 12, 'bold'))
        label.pack(side=tk.LEFT, padx=(0, 15))
        
        self.categoria_var = tk.StringVar(value="Todos")
        categorias = ["Todos", "Entradas", "Platos Principales", "Ensaladas", 
                     "Bebidas", "Bebidas Alcohólicas", "Postres", "Acompañamientos"]
        
        combo = ttk.Combobox(inner_frame, textvariable=self.categoria_var, 
                            values=categorias, state="readonly", width=25,
                            font=('Inter', 10))
        combo.pack(side=tk.LEFT, padx=5)
        combo.bind("<<ComboboxSelected>>", lambda e: self._actualizar_grid_menu())
        
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
        """Actualizar grid de menú de forma optimizada"""
        # Limpiar widgets previos
        for widget in self.menu_frame.winfo_children():
            widget.destroy()
        
        categoria = self.categoria_var.get()
        row = 0
        col = 0
        # Calcular dinámicamente el número de columnas según el ancho disponible
        try:
            available_width = self.menu_canvas.winfo_width() if hasattr(self, 'menu_canvas') else None
        except Exception:
            available_width = None

        # Ancho mínimo por tarjeta (incluye paddings/margins). Ajustable si necesitas tarjetas más pequeñas.
        card_min = getattr(self, 'menu_min_card_width', 360)

        if available_width and available_width > 0:
            # Dejar un máximo razonable de columnas para evitar tarjetas demasiado pequeñas
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
        items_encontrados = 0
        
        # Items del menú predefinido - usar lista en lugar de diccionario.values()
        items_menu = list(self.menu.items.values())
        items_personalizados = self.productos_personalizados
        
        # Combinar listas para una sola iteración
        todos_items = []
        for item in items_menu:
            if categoria == "Todos" or item.categoria == categoria:
                todos_items.append(('menu', item))
        
        for prod in items_personalizados:
            if categoria == "Todos" or prod.get('categoria') == categoria:
                todos_items.append(('custom', prod))
        
        # Renderizar items
        if todos_items:
            for tipo, item in todos_items:
                if tipo == 'menu':
                    self._crear_card_menu(self.menu_frame, item, row, col)
                else:
                    self._crear_card_producto_custom(self.menu_frame, item, row, col)
                
                items_encontrados += 1
                col += 1
                if col >= columnas:
                    col = 0
                    row += 1
        else:
            # Mensaje si no hay items
            msg_frame = tk.Frame(self.menu_frame, bg=self.COLORES['fondo_principal'])
            msg_frame.pack(fill=tk.BOTH, expand=True, pady=50)
            tk.Label(msg_frame, text="❌ Sin productos en esta categoría",
                    font=('Inter', 14), fg=self.COLORES['texto_secundario'],
                    bg=self.COLORES['fondo_principal']).pack()
    
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
        """Pestaña para gestionar productos personalizados"""
        # Panel superior con botones
        toolbar = tk.Frame(parent, bg=self.COLORES['fondo_card'], height=60)
        toolbar.pack(fill=tk.X, padx=10, pady=10)
        toolbar.pack_propagate(False)
        
        tk.Button(toolbar, text="➕ Nuevo Producto", bg=self.COLORES['verde_success'],
                 fg='white', font=('Inter', 10, 'bold'), relief='flat', padx=15, pady=10,
                 command=self._crear_producto_dialog).pack(side=tk.LEFT, padx=5, pady=10)
        
        # Lista de productos
        lista_frame = tk.Frame(parent, bg=self.COLORES['fondo_principal'])
        lista_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas con scroll
        canvas = tk.Canvas(lista_frame, bg=self.COLORES['fondo_principal'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=canvas.yview)
        
        self.productos_lista_frame = tk.Frame(canvas, bg=self.COLORES['fondo_principal'])
        self.productos_lista_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.productos_lista_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self._actualizar_lista_productos()
    
    def _actualizar_lista_productos(self):
        """Actualizar lista de productos personalizados"""
        for widget in self.productos_lista_frame.winfo_children():
            widget.destroy()
        
        if not self.productos_personalizados:
            tk.Label(self.productos_lista_frame, text="Sin productos personalizados",
                    font=('Inter', 11), fg=self.COLORES['texto_secundario'],
                    bg=self.COLORES['fondo_principal']).pack(pady=40)
            return
        
        for idx, prod in enumerate(self.productos_personalizados):
            prod_frame = tk.Frame(self.productos_lista_frame, bg=self.COLORES['fondo_card'], relief=tk.FLAT, bd=1)
            prod_frame.pack(fill=tk.X, pady=8, padx=10)
            
            # Info
            info = tk.Frame(prod_frame, bg=self.COLORES['fondo_card'])
            info.pack(fill=tk.X, padx=10, pady=10)
            
            tk.Label(info, text=prod['nombre'], font=('Inter', 11, 'bold'),
                    fg=self.COLORES['texto_principal'],
                    bg=self.COLORES['fondo_card']).pack(side=tk.LEFT)
            
            tk.Label(info, text=f"${float(prod['precio']):,.0f}", font=('Inter', 11, 'bold'),
                    fg=self.COLORES['acento_dorado'],
                    bg=self.COLORES['fondo_card']).pack(side=tk.RIGHT, padx=(0, 20))
            
            tk.Label(info, text=prod['categoria'], font=('Inter', 9),
                    fg=self.COLORES['texto_secundario'],
                    bg=self.COLORES['fondo_card']).pack(side=tk.RIGHT, padx=(0, 20))
            
            # Botones
            btn = tk.Frame(prod_frame, bg=self.COLORES['fondo_card'])
            btn.pack(fill=tk.X, padx=10, pady=(0, 10))
            
            tk.Button(btn, text="Editar", bg=self.COLORES['acento_dorado'],
                     fg='black', relief='flat', font=('Inter', 9), width=10,
                     command=lambda i=idx: self._editar_producto_dialog(i)).pack(side=tk.LEFT, padx=2)
            
            tk.Button(btn, text="Eliminar", bg=self.COLORES['rojo_danger'],
                     fg='white', relief='flat', font=('Inter', 9), width=10,
                     command=lambda i=idx: self._eliminar_producto(i)).pack(side=tk.LEFT, padx=2)
    
    def _crear_producto_dialog(self):
        """Diálogo para crear nuevo producto"""
        self._mostrar_form_producto(None)
    
    def _editar_producto_dialog(self, idx):
        """Diálogo para editar producto"""
        if 0 <= idx < len(self.productos_personalizados):
            self._mostrar_form_producto(self.productos_personalizados[idx], idx)
    
    def _mostrar_form_producto(self, producto=None, idx=None):
        """Mostrar formulario de producto"""
        ventana = tk.Toplevel(self.ventana)
        ventana.title("Producto" if producto else "Nuevo Producto")
        ventana.geometry("500x550")
        ventana.configure(bg=self.COLORES['fondo_principal'])
        
        # Centrar
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - 250
        y = (ventana.winfo_screenheight() // 2) - 275
        ventana.geometry(f"+{x}+{y}")
        
        # Nombre
        tk.Label(ventana, text="Nombre:", font=('Inter', 11),
                fg=self.COLORES['texto_principal'],
                bg=self.COLORES['fondo_principal']).pack(pady=(20, 5), padx=20, anchor=tk.W)
        entry_nombre = tk.Entry(ventana, font=('Inter', 11), width=30)
        entry_nombre.pack(pady=5, padx=20)
        if producto:
            entry_nombre.insert(0, producto['nombre'])
        
        # Precio
        tk.Label(ventana, text="Precio:", font=('Inter', 11),
                fg=self.COLORES['texto_principal'],
                bg=self.COLORES['fondo_principal']).pack(pady=(15, 5), padx=20, anchor=tk.W)
        entry_precio = tk.Entry(ventana, font=('Inter', 11), width=30)
        entry_precio.pack(pady=5, padx=20)
        if producto:
            entry_precio.insert(0, str(producto['precio']))
        
        # Categoría
        tk.Label(ventana, text="Categoría:", font=('Inter', 11),
                fg=self.COLORES['texto_principal'],
                bg=self.COLORES['fondo_principal']).pack(pady=(15, 5), padx=20, anchor=tk.W)
        
        categorias = ["Entradas", "Platos Principales", "Ensaladas", 
                     "Bebidas", "Bebidas Alcohólicas", "Postres", "Acompañamientos"]
        combo_cat = ttk.Combobox(ventana, values=categorias, state="readonly", width=27)
        combo_cat.pack(pady=5, padx=20)
        if producto:
            combo_cat.set(producto.get('categoria', 'Entradas'))
        
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
                messagebox.showerror("Error", "Precio inválido")
                return
            
            categoria = combo_cat.get()
            
            if not nombre or not categoria:
                messagebox.showerror("Error", "Completa todos los campos")
                return
            
            nuevo_prod = {
                'nombre': nombre,
                'precio': precio,
                'categoria': categoria,
                'imagen': imagen_actual[0]
            }
            
            if idx is not None:
                self.productos_personalizados[idx] = nuevo_prod
            else:
                self.productos_personalizados.append(nuevo_prod)
            
            self.guardar_productos_personalizados()
            self._actualizar_lista_productos()
            ventana.destroy()
            self._actualizar_grid_menu()
        
        tk.Button(btn_frame, text="Guardar", bg=self.COLORES['verde_success'],
                 fg='white', font=('Inter', 11, 'bold'), relief='flat', padx=30, pady=10,
                 command=guardar).pack(side=tk.LEFT, padx=10)
        
        tk.Button(btn_frame, text="Cancelar", bg=self.COLORES['rojo_danger'],
                 fg='white', font=('Inter', 11, 'bold'), relief='flat', padx=30, pady=10,
                 command=ventana.destroy).pack(side=tk.LEFT, padx=10)
    
    def _eliminar_producto(self, idx):
        """Eliminar producto personalizado"""
        if messagebox.askyesno("Confirmar", "¿Eliminar este producto?"):
            del self.productos_personalizados[idx]
            self.guardar_productos_personalizados()
            self._actualizar_lista_productos()
            self._actualizar_grid_menu()
    
    def ejecutar(self):
        """Ejecutar aplicación"""
        self.ventana.mainloop()


if __name__ == "__main__":
    app = InterfazRestaurante()
    app.ejecutar()
