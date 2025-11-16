#!/usr/bin/env python3
"""
interfaz_restaurante_v2.py - Interfaz mejorada para POS de restaurante
Version simplificada y limpia con enfoque en impresion en Linux
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from modelo_restaurante import Menu, PedidoRestaurante
import subprocess
import os
import tempfile
import datetime


class InterfazRestaurante:
    """Interfaz POS moderna para restaurante con impresion en Linux"""
    
    COLORES = {
        'fondo_principal': '#1a1a1a',
        'fondo_card': '#2d2d2d',
        'acento_dorado': '#d4af37',
        'acento_naranja': '#ff6b35',
        'texto_principal': '#ffffff',
        'texto_secundario': '#b0b0b0',
        'verde_success': '#00d4aa',
        'rojo_danger': '#ff4757',
        'azul_info': '#3742fa',
    }
    
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("POS RESTAURANT Premium")
        self.ventana.geometry("1400x800")
        self.ventana.minsize(1200, 700)
        self.ventana.configure(bg=self.COLORES['fondo_principal'])
        
        # Datos
        self.menu = Menu()
        self.pedido = PedidoRestaurante()
        self.nombre_negocio = tk.StringVar(value="PREMIUM RESTAURANT")
        self.nit_negocio = tk.StringVar(value="123456789")
        
        self._configurar_estilos()
        self._crear_interfaz_principal()
    
    def _configurar_estilos(self):
        """Configurar estilos ttk"""
        estilo = ttk.Style()
        estilo.theme_use('clam')
        self.estilo = estilo
    
    def _crear_interfaz_principal(self):
        """Crear layout principal: izquierda menu, derecha carrito"""
        
        # Panel izquierdo - Menu
        left_panel = tk.Frame(self.ventana, bg=self.COLORES['fondo_principal'])
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Panel derecho - Carrito
        right_panel = tk.Frame(self.ventana, bg=self.COLORES['fondo_principal'], width=400)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=20, pady=20)
        right_panel.pack_propagate(False)
        
        # Crear paneles
        self._crear_panel_menu(left_panel)
        self._crear_panel_carrito(right_panel)
    
    def _crear_panel_menu(self, parent):
        """Panel izquierdo con menu de items"""
        
        # Encabezado
        header = tk.Label(parent, text="Menu Premium",
                         font=('Inter', 18, 'bold'),
                         fg=self.COLORES['acento_dorado'],
                         bg=self.COLORES['fondo_principal'])
        header.pack(pady=(0, 15))
        
        # Filtro de categoria
        filter_frame = tk.Frame(parent, bg=self.COLORES['fondo_principal'])
        filter_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(filter_frame, text="Categoria:",
                font=('Inter', 10),
                fg=self.COLORES['texto_secundario'],
                bg=self.COLORES['fondo_principal']).pack(side=tk.LEFT, padx=(0, 10))
        
        self.categoria_var = tk.StringVar(value="Todos")
        categorias = ["Todos"] + self.menu.obtener_categorias()
        combo = ttk.Combobox(filter_frame, textvariable=self.categoria_var,
                            values=categorias, state="readonly", width=20)
        combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        combo.bind("<<ComboboxSelected>>", lambda e: self._actualizar_items())
        
        # Canvas con items en grid
        self._crear_grid_items(parent)
    
    def _crear_grid_items(self, parent):
        """Crear grid de items como cards"""
        
        canvas = tk.Canvas(parent, bg=self.COLORES['fondo_principal'],
                          highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        self.grid_frame = tk.Frame(canvas, bg=self.COLORES['fondo_principal'])
        
        self.grid_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.grid_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=(0, 20))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self._actualizar_items()
    
    def _actualizar_items(self):
        """Actualizar items del menu"""
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        
        categoria = self.categoria_var.get()
        if categoria == "Todos":
            items = self.menu.listar_por_categoria()
        else:
            items = self.menu.listar_por_categoria(categoria)
        
        # Grid de 3 columnas
        for i, item in enumerate(items):
            fila = i // 3
            col = i % 3
            
            card = tk.Frame(self.grid_frame, bg=self.COLORES['fondo_card'],
                           relief='solid', bd=1)
            card.grid(row=fila, column=col, padx=8, pady=8, sticky='ew')
            self.grid_frame.columnconfigure(col, weight=1)
            
            self._crear_card_item(card, item)
    
    def _crear_card_item(self, parent, item):
        """Crear una card de item"""
        
        content = tk.Frame(parent, bg=self.COLORES['fondo_card'])
        content.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)
        
        # Nombre
        tk.Label(content, text=item.nombre,
                font=('Inter', 11, 'bold'),
                fg=self.COLORES['texto_principal'],
                bg=self.COLORES['fondo_card'],
                wraplength=120).pack(pady=(0, 8))
        
        # Descripcion
        if item.descripcion:
            desc = item.descripcion[:40] + "..." if len(item.descripcion) > 40 else item.descripcion
            tk.Label(content, text=desc,
                    font=('Inter', 8),
                    fg=self.COLORES['texto_secundario'],
                    bg=self.COLORES['fondo_card'],
                    wraplength=120).pack(pady=(0, 8))
        
        # Precio
        tk.Label(content, text=f"${item.precio:,.0f}",
                font=('Inter', 13, 'bold'),
                fg=self.COLORES['acento_dorado'],
                bg=self.COLORES['fondo_card']).pack(pady=(0, 10))
        
        # Boton agregar
        btn = tk.Button(content, text="Agregar",
                       command=lambda: self._agregar_al_carrito(item),
                       bg=self.COLORES['verde_success'],
                       fg='white',
                       font=('Inter', 9, 'bold'),
                       relief='flat',
                       padx=15, pady=8)
        btn.pack(fill=tk.X)
    
    def _agregar_al_carrito(self, item):
        """Agregar item al carrito"""
        self.pedido.agregar_item(item.nombre, item.precio, 1)
        self._actualizar_carrito()
        self._mostrar_notificacion(f"Agregado: {item.nombre}")
    
    def _crear_panel_carrito(self, parent):
        """Panel derecho con carrito y opciones"""
        
        # Titulo
        header = tk.Label(parent, text="Tu Pedido",
                         font=('Inter', 16, 'bold'),
                         fg=self.COLORES['texto_principal'],
                         bg=self.COLORES['fondo_principal'])
        header.pack(pady=(0, 15))
        
        # Card del carrito
        card = tk.Frame(parent, bg=self.COLORES['fondo_card'])
        card.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Items del carrito
        canvas_carrito = tk.Canvas(card, bg=self.COLORES['fondo_card'],
                                  highlightthickness=0, height=300)
        scrollbar = ttk.Scrollbar(card, orient="vertical", command=canvas_carrito.yview)
        
        self.carrito_frame = tk.Frame(canvas_carrito, bg=self.COLORES['fondo_card'])
        self.carrito_frame.bind(
            "<Configure>",
            lambda e: canvas_carrito.configure(scrollregion=canvas_carrito.bbox("all"))
        )
        
        canvas_carrito.create_window((0, 0), window=self.carrito_frame, anchor="nw")
        canvas_carrito.configure(yscrollcommand=scrollbar.set)
        
        canvas_carrito.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 15), pady=15)
        
        # Resumen
        resumen_frame = tk.Frame(card, bg=self.COLORES['fondo_card'])
        resumen_frame.pack(fill=tk.X, padx=15, pady=15)
        
        self.label_total = tk.Label(resumen_frame, text="Total: $0",
                                   font=('Inter', 14, 'bold'),
                                   fg=self.COLORES['acento_dorado'],
                                   bg=self.COLORES['fondo_card'])
        self.label_total.pack(pady=10)
        
        # Botones de accion
        botones_frame = tk.Frame(card, bg=self.COLORES['fondo_card'])
        botones_frame.pack(fill=tk.X, padx=15, pady=15)
        
        btn_procesar = tk.Button(botones_frame, text="Procesar Pedido",
                                bg=self.COLORES['verde_success'],
                                fg='white',
                                font=('Inter', 10, 'bold'),
                                relief='flat',
                                padx=15, pady=10,
                                command=self._procesar_pedido)
        btn_procesar.pack(fill=tk.X, pady=(0, 10))
        
        btn_limpiar = tk.Button(botones_frame, text="Limpiar Carrito",
                               bg=self.COLORES['rojo_danger'],
                               fg='white',
                               font=('Inter', 10, 'bold'),
                               relief='flat',
                               padx=15, pady=10,
                               command=self._limpiar_carrito)
        btn_limpiar.pack(fill=tk.X)
        
        self._mostrar_carrito_vacio()
    
    def _mostrar_carrito_vacio(self):
        """Mostrar carrito vacio"""
        for widget in self.carrito_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.carrito_frame, text="Carrito vacio\nAgrega items del menu",
                font=('Inter', 11),
                fg=self.COLORES['texto_secundario'],
                bg=self.COLORES['fondo_card'],
                justify=tk.CENTER).pack(expand=True, pady=40)
    
    def _actualizar_carrito(self):
        """Actualizar visualizacion del carrito"""
        for widget in self.carrito_frame.winfo_children():
            widget.destroy()
        
        if not self.pedido.items:
            self._mostrar_carrito_vacio()
            self._actualizar_total()
            return
        
        for idx, item in enumerate(self.pedido.items):
            item_frame = tk.Frame(self.carrito_frame, bg=self.COLORES['fondo_card'])
            item_frame.pack(fill=tk.X, pady=5, padx=10)
            
            # Nombre y cantidad
            info = tk.Frame(item_frame, bg=self.COLORES['fondo_card'])
            info.pack(fill=tk.X)
            
            tk.Label(info, text=item['nombre'],
                    font=('Inter', 10, 'bold'),
                    fg=self.COLORES['texto_principal'],
                    bg=self.COLORES['fondo_card']).pack(side=tk.LEFT)
            
            tk.Label(info, text=f"${item['precio'] * item['cantidad']:,.0f}",
                    font=('Inter', 10, 'bold'),
                    fg=self.COLORES['acento_dorado'],
                    bg=self.COLORES['fondo_card']).pack(side=tk.RIGHT)
            
            # Controles de cantidad
            control = tk.Frame(item_frame, bg=self.COLORES['fondo_card'])
            control.pack(fill=tk.X, pady=(3, 0))
            
            btn_menos = tk.Button(control, text="-", width=2,
                                 bg=self.COLORES['rojo_danger'],
                                 fg='white', relief='flat',
                                 command=lambda i=idx: self._decrementar(i))
            btn_menos.pack(side=tk.LEFT)
            
            tk.Label(control, text=f"  x{item['cantidad']}  ",
                    font=('Inter', 9),
                    fg=self.COLORES['texto_principal'],
                    bg=self.COLORES['fondo_card']).pack(side=tk.LEFT)
            
            btn_mas = tk.Button(control, text="+", width=2,
                               bg=self.COLORES['verde_success'],
                               fg='white', relief='flat',
                               command=lambda i=idx: self._incrementar(i))
            btn_mas.pack(side=tk.LEFT)
            
            btn_eliminar = tk.Button(control, text="Eliminar", width=10,
                                    bg='#666666',
                                    fg='white', relief='flat', font=('Inter', 8),
                                    command=lambda i=idx: self._eliminar_item(i))
            btn_eliminar.pack(side=tk.RIGHT)
        
        self._actualizar_total()
    
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
        """Eliminar item"""
        if 0 <= idx < len(self.pedido.items):
            del self.pedido.items[idx]
            self._actualizar_carrito()
    
    def _limpiar_carrito(self):
        """Limpiar carrito"""
        self.pedido.items.clear()
        self._actualizar_carrito()
        self._mostrar_notificacion("Carrito limpiado")
    
    def _actualizar_total(self):
        """Actualizar total"""
        total = self.pedido.calcular_total()
        self.label_total.config(text=f"Total: ${total:,.0f}")
    
    def _procesar_pedido(self):
        """Procesar pedido y mostrar opciones de pago"""
        if not self.pedido.items:
            messagebox.showwarning("Carrito Vacio", "Agrega items antes de procesar")
            return
        
        self._mostrar_ventana_pago()
    
    def _mostrar_ventana_pago(self):
        """Ventana de pago con datos"""
        
        pago = tk.Toplevel(self.ventana)
        pago.title("Procesar Pago")
        pago.geometry("600x600")
        pago.configure(bg=self.COLORES['fondo_principal'])
        
        # Centrar ventana
        pago.update_idletasks()
        x = (pago.winfo_screenwidth() // 2) - 300
        y = (pago.winfo_screenheight() // 2) - 300
        pago.geometry(f"+{x}+{y}")
        
        container = tk.Frame(pago, bg=self.COLORES['fondo_principal'])
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titulo
        tk.Label(container, text="Procesar Pago",
                font=('Inter', 16, 'bold'),
                fg=self.COLORES['acento_dorado'],
                bg=self.COLORES['fondo_principal']).pack(pady=(0, 20))
        
        # Informacion del cliente
        cliente_frame = tk.LabelFrame(container, text="Informacion del Cliente",
                                     bg=self.COLORES['fondo_card'],
                                     fg=self.COLORES['acento_dorado'],
                                     font=('Inter', 10, 'bold'),
                                     padx=15, pady=10)
        cliente_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(cliente_frame, text="Mesa:", bg=self.COLORES['fondo_card'],
                fg=self.COLORES['texto_principal']).pack(anchor=tk.W, pady=5)
        mesa_var = tk.StringVar()
        mesa_entry = tk.Entry(cliente_frame, textvariable=mesa_var)
        mesa_entry.pack(fill=tk.X, pady=(0, 10))
        mesa_entry.focus()
        
        tk.Label(cliente_frame, text="Mesero:", bg=self.COLORES['fondo_card'],
                fg=self.COLORES['texto_principal']).pack(anchor=tk.W, pady=5)
        mesero_var = tk.StringVar(value="Admin")
        mesero_entry = tk.Entry(cliente_frame, textvariable=mesero_var)
        mesero_entry.pack(fill=tk.X)
        
        # Resumen de items
        resumen_frame = tk.LabelFrame(container, text="Resumen del Pedido",
                                     bg=self.COLORES['fondo_card'],
                                     fg=self.COLORES['acento_dorado'],
                                     font=('Inter', 10, 'bold'),
                                     padx=15, pady=10)
        resumen_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        for item in self.pedido.items:
            subtotal = item['precio'] * item['cantidad']
            tk.Label(resumen_frame, 
                    text=f"{item['nombre']} x{item['cantidad']} = ${subtotal:,.0f}",
                    bg=self.COLORES['fondo_card'],
                    fg=self.COLORES['texto_principal']).pack(anchor=tk.W, pady=2)
        
        # Total
        total = self.pedido.calcular_total()
        tk.Label(container, text=f"Total: ${total:,.0f}",
                font=('Inter', 14, 'bold'),
                fg=self.COLORES['acento_dorado'],
                bg=self.COLORES['fondo_principal']).pack(pady=(0, 15))
        
        # Metodo de pago
        pago_frame = tk.LabelFrame(container, text="Metodo de Pago",
                                  bg=self.COLORES['fondo_card'],
                                  fg=self.COLORES['acento_dorado'],
                                  font=('Inter', 10, 'bold'),
                                  padx=15, pady=10)
        pago_frame.pack(fill=tk.X, pady=(0, 20))
        
        metodo_var = tk.StringVar(value="Efectivo")
        for metodo in ["Efectivo", "Tarjeta Credito", "Tarjeta Debito"]:
            tk.Radiobutton(pago_frame, text=metodo, variable=metodo_var, value=metodo,
                          bg=self.COLORES['fondo_card'],
                          fg=self.COLORES['texto_principal'],
                          selectcolor=self.COLORES['acento_dorado'],
                          activebackground=self.COLORES['fondo_card']).pack(anchor=tk.W, pady=3)
        
        # Botones
        botones = tk.Frame(container, bg=self.COLORES['fondo_principal'])
        botones.pack(fill=tk.X)
        
        def confirmar():
            mesa = mesa_var.get().strip()
            mesero = mesero_var.get().strip()
            
            if not mesa:
                messagebox.showerror("Error", "Ingresa el numero de mesa")
                mesa_entry.focus()
                return
            
            # Generar factura
            factura_data = {
                'numero': f"FACT-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                'fecha': datetime.datetime.now().strftime("%Y-%m-%d"),
                'hora': datetime.datetime.now().strftime("%H:%M:%S"),
                'mesa': mesa,
                'mesero': mesero,
                'items': self.pedido.items.copy(),
                'total': total,
                'metodo_pago': metodo_var.get(),
                'restaurante': self.nombre_negocio.get(),
                'nit': self.nit_negocio.get()
            }
            
            pago.destroy()
            self._mostrar_factura_final(factura_data)
            self.pedido.items.clear()
            self._actualizar_carrito()
        
        btn_cancelar = tk.Button(botones, text="Cancelar",
                                bg=self.COLORES['rojo_danger'],
                                fg='white',
                                font=('Inter', 10, 'bold'),
                                relief='flat',
                                padx=15, pady=8,
                                command=pago.destroy)
        btn_cancelar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        btn_confirmar = tk.Button(botones, text="Confirmar Pago",
                                 bg=self.COLORES['verde_success'],
                                 fg='white',
                                 font=('Inter', 10, 'bold'),
                                 relief='flat',
                                 padx=15, pady=8,
                                 command=confirmar)
        btn_confirmar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
    
    def _mostrar_factura_final(self, factura_data):
        """Mostrar factura final con opciones de impresion"""
        
        factura = tk.Toplevel(self.ventana)
        factura.title("Factura Final")
        factura.geometry("650x800")
        factura.configure(bg=self.COLORES['fondo_principal'])
        
        # Centrar
        factura.update_idletasks()
        x = (factura.winfo_screenwidth() // 2) - 325
        y = (factura.winfo_screenheight() // 2) - 400
        factura.geometry(f"+{x}+{y}")
        
        container = tk.Frame(factura, bg=self.COLORES['fondo_principal'])
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Titulo
        tk.Label(container, text="Factura Final",
                font=('Inter', 16, 'bold'),
                fg=self.COLORES['acento_dorado'],
                bg=self.COLORES['fondo_principal']).pack(pady=(0, 20))
        
        # Contenido de factura
        contenido_txt = self._generar_contenido_factura(factura_data)
        
        # Text widget con scroll
        text_frame = tk.Frame(container, bg='white')
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=('Courier', 9),
                             bg='white', fg='black', relief='solid', bd=1)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.insert(tk.END, contenido_txt)
        text_widget.configure(state='disabled')
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones de accion
        botones = tk.Frame(container, bg=self.COLORES['fondo_principal'])
        botones.pack(fill=tk.X)
        
        def vista_previa():
            self._mostrar_vista_previa_factura(factura_data)
        
        def imprimir():
            self._imprimir_factura_linux(factura_data)
        
        def guardar():
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Texto", "*.txt")],
                initialname=f"Factura_{factura_data['numero']}.txt"
            )
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(contenido_txt)
                messagebox.showinfo("Exito", f"Factura guardada en:\n{filename}")
        
        btn_vista = tk.Button(botones, text="Ver Preview",
                             bg=self.COLORES['azul_info'],
                             fg='white',
                             font=('Inter', 10, 'bold'),
                             relief='flat',
                             padx=10, pady=8,
                             command=vista_previa)
        btn_vista.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        btn_guardar = tk.Button(botones, text="Guardar",
                               bg=self.COLORES['acento_naranja'],
                               fg='white',
                               font=('Inter', 10, 'bold'),
                               relief='flat',
                               padx=10, pady=8,
                               command=guardar)
        btn_guardar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        btn_imprimir = tk.Button(botones, text="Imprimir",
                                bg=self.COLORES['verde_success'],
                                fg='white',
                                font=('Inter', 10, 'bold'),
                                relief='flat',
                                padx=10, pady=8,
                                command=imprimir)
        btn_imprimir.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def _mostrar_vista_previa_factura(self, factura_data):
        """Vista previa de factura"""
        preview = tk.Toplevel(self.ventana)
        preview.title("Vista Previa - Factura")
        preview.geometry("600x700")
        preview.configure(bg=self.COLORES['fondo_principal'])
        
        preview.update_idletasks()
        x = (preview.winfo_screenwidth() // 2) - 300
        y = (preview.winfo_screenheight() // 2) - 350
        preview.geometry(f"+{x}+{y}")
        
        container = tk.Frame(preview, bg=self.COLORES['fondo_principal'])
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        tk.Label(container, text="Vista Previa",
                font=('Inter', 14, 'bold'),
                fg=self.COLORES['acento_dorado'],
                bg=self.COLORES['fondo_principal']).pack(pady=(0, 15))
        
        contenido_txt = self._generar_contenido_factura(factura_data)
        
        text_frame = tk.Frame(container, bg='white')
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=('Courier', 9),
                             bg='white', fg='black')
        scrollbar = ttk.Scrollbar(text_frame, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.insert(tk.END, contenido_txt)
        text_widget.configure(state='disabled')
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Boton cerrar
        btn_cerrar = tk.Button(container, text="Cerrar",
                              bg=self.COLORES['rojo_danger'],
                              fg='white',
                              font=('Inter', 10, 'bold'),
                              relief='flat',
                              padx=15, pady=8,
                              command=preview.destroy)
        btn_cerrar.pack(fill=tk.X)
    
    def _imprimir_factura_linux(self, factura_data):
        """Imprimir factura en Linux usando CUPS"""
        
        try:
            # Generar contenido
            contenido = self._generar_contenido_factura(factura_data)
            
            # Crear archivo temporal
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                f.write(contenido)
                temp_file = f.name
            
            # Mostrar dialogo de impresion
            self._mostrar_dialogo_impresion(temp_file, factura_data)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al preparar impresion:\n{str(e)}")
    
    def _mostrar_dialogo_impresion(self, archivo_temp, factura_data):
        """Dialogo de seleccion de impresora CUPS"""
        
        dialogo = tk.Toplevel(self.ventana)
        dialogo.title("Imprimir Factura")
        dialogo.geometry("500x350")
        dialogo.configure(bg=self.COLORES['fondo_principal'])
        
        dialogo.update_idletasks()
        x = (dialogo.winfo_screenwidth() // 2) - 250
        y = (dialogo.winfo_screenheight() // 2) - 175
        dialogo.geometry(f"+{x}+{y}")
        
        container = tk.Frame(dialogo, bg=self.COLORES['fondo_principal'])
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(container, text="Configuracion de Impresion",
                font=('Inter', 14, 'bold'),
                fg=self.COLORES['acento_dorado'],
                bg=self.COLORES['fondo_principal']).pack(pady=(0, 20))
        
        # Obtener impresoras
        impresoras = self._obtener_impresoras_cups()
        
        # Frame de impresora
        printer_frame = tk.Frame(container, bg=self.COLORES['fondo_card'])
        printer_frame.pack(fill=tk.X, pady=(0, 20), padx=10, pady=10)
        
        tk.Label(printer_frame, text="Impresora:",
                bg=self.COLORES['fondo_card'],
                fg=self.COLORES['texto_principal']).pack(anchor=tk.W, pady=(0, 5))
        
        impresora_var = tk.StringVar(value=impresoras[0] if impresoras else "Sin impresoras")
        combo_imp = ttk.Combobox(printer_frame, textvariable=impresora_var,
                                values=impresoras, state="readonly")
        combo_imp.pack(fill=tk.X)
        
        # Opciones
        opciones_frame = tk.LabelFrame(container, text="Opciones",
                                      bg=self.COLORES['fondo_card'],
                                      fg=self.COLORES['texto_principal'],
                                      font=('Inter', 10, 'bold'),
                                      padx=10, pady=10)
        opciones_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(opciones_frame, text="Copias:",
                bg=self.COLORES['fondo_card'],
                fg=self.COLORES['texto_principal']).pack(anchor=tk.W, pady=(0, 5))
        
        copias_var = tk.IntVar(value=1)
        copias_spin = ttk.Spinbox(opciones_frame, from_=1, to=10, textvariable=copias_var, width=10)
        copias_spin.pack(anchor=tk.W)
        
        # Botones
        botones = tk.Frame(container, bg=self.COLORES['fondo_principal'])
        botones.pack(fill=tk.X)
        
        def imprimir_now():
            impresora = impresora_var.get()
            copias = copias_var.get()
            
            if impresora == "Sin impresoras":
                messagebox.showwarning("Sin Impresoras", "No hay impresoras disponibles")
                return
            
            # Comando de impresion
            cmd = ['lp']
            if impresora != "Impresora predeterminada":
                cmd.extend(['-d', impresora])
            cmd.extend(['-n', str(copias)])
            cmd.append(archivo_temp)
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
                
                if result.returncode == 0:
                    messagebox.showinfo("Exito", 
                                      f"Factura enviada a impresion\n\nImpresora: {impresora}\nCopias: {copias}")
                    dialogo.destroy()
                else:
                    messagebox.showerror("Error", f"Error al imprimir:\n{result.stderr}")
                    
            except FileNotFoundError:
                messagebox.showerror("Error", "Comando 'lp' no encontrado\n\nInstala cups: sudo apt install cups")
            except Exception as e:
                messagebox.showerror("Error", f"Error en impresion:\n{str(e)}")
            finally:
                try:
                    os.unlink(archivo_temp)
                except:
                    pass
        
        btn_cancelar = tk.Button(botones, text="Cancelar",
                                bg=self.COLORES['rojo_danger'],
                                fg='white',
                                font=('Inter', 10, 'bold'),
                                relief='flat',
                                padx=15, pady=8,
                                command=dialogo.destroy)
        btn_cancelar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        btn_imprimir = tk.Button(botones, text="Imprimir",
                                bg=self.COLORES['verde_success'],
                                fg='white',
                                font=('Inter', 10, 'bold'),
                                relief='flat',
                                padx=15, pady=8,
                                command=imprimir_now)
        btn_imprimir.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def _obtener_impresoras_cups(self):
        """Obtener lista de impresoras disponibles en CUPS"""
        try:
            result = subprocess.run(['lpstat', '-p'], capture_output=True, text=True, timeout=3)
            
            if result.returncode == 0:
                impresoras = []
                for linea in result.stdout.strip().split('\n'):
                    if linea.startswith('printer '):
                        nombre = linea.split()[1]
                        impresoras.append(nombre)
                
                if impresoras:
                    return impresoras
            
            return ['Impresora predeterminada']
            
        except:
            return ['Impresora predeterminada']
    
    def _generar_contenido_factura(self, factura_data):
        """Generar contenido formateado de factura"""
        
        ancho = 50
        sep = "=" * ancho
        linea = "-" * ancho
        
        # Calcular totales
        subtotal = factura_data['total']
        itbms = subtotal * 0.19
        total_final = subtotal + itbms
        
        contenido = f"""
{sep}
{factura_data['restaurante'].center(ancho)}
{sep}
NIT: {factura_data['nit']}
Fecha: {factura_data['fecha']}  Hora: {factura_data['hora']}
Factura: {factura_data['numero']}
Mesa: {factura_data['mesa']}  Mesero: {factura_data['mesero']}
{sep}
                    DETALLE DEL PEDIDO
{linea}
DESCRIPCION                        CANT   PRECIO
{linea}"""
        
        for item in factura_data['items']:
            nombre = item['nombre'][:32]
            cant = str(item['cantidad']).rjust(2)
            precio = f"${item['precio']:,.0f}".rjust(10)
            subtotal_item = item['precio'] * item['cantidad']
            total_item = f"${subtotal_item:,.0f}".rjust(10)
            
            contenido += f"\n{nombre:<32} {cant} {precio} {total_item}"
        
        contenido += f"""
{linea}
                            SUBTOTAL: ${subtotal:>10,.0f}
                            ITBMS 19%: ${itbms:>9,.0f}
                               TOTAL: ${total_final:>10,.0f}
{sep}
METODO DE PAGO: {factura_data['metodo_pago']}
{sep}
           Gracias por su preferencia!
{sep}

"""
        
        return contenido
    
    def _mostrar_notificacion(self, mensaje):
        """Mostrar notificacion toast"""
        toast = tk.Toplevel(self.ventana)
        toast.title("")
        toast.overrideredirect(True)
        toast.attributes('-topmost', True)
        
        x = self.ventana.winfo_x() + self.ventana.winfo_width() - 300
        y = self.ventana.winfo_y() + 100
        toast.geometry(f"280x50+{x}+{y}")
        toast.configure(bg=self.COLORES['verde_success'])
        
        tk.Label(toast, text=mensaje,
                font=('Inter', 10, 'bold'),
                fg='white',
                bg=self.COLORES['verde_success']).pack(fill=tk.BOTH, expand=True)
        
        toast.after(2500, toast.destroy)
    
    def ejecutar(self):
        """Iniciar la aplicacion"""
        self.ventana.mainloop()
