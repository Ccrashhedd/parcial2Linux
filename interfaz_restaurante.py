"""
interfaz_restaurante.py - Interfaz gráfica para POS de restaurante
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from modelo_restaurante import Menu, Pedido, Factura, MenuItem
import subprocess
import os


class InterfazRestaurante:
    """Interfaz gráfica completa para POS de restaurante"""
    
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("POS Restaurante - Parcial2")
        self.ventana.geometry("1200x700")
        self.ventana.minsize(1000, 600)
        
        # Modelo de datos
        self.menu = Menu()
        self.pedido_actual = Pedido()
        
        # Variables de configuración
        self.nombre_negocio = tk.StringVar(value="RESTAURANT PARCIAL 2")
        self.nit_negocio = tk.StringVar(value="123456789")
        
        # Crear interfaz
        self._crear_menu_principal()
        self._crear_widgets()
    
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
    
    def _crear_widgets(self):
        """Crear la interfaz principal"""
        
        # Frame principal con notebook (pestañas)
        self.notebook = ttk.Notebook(self.ventana)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Pestaña 1: Venta
        self.tab_venta = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_venta, text="📦 Venta")
        self._crear_tab_venta()
        
        # Pestaña 2: Administrar Menú
        self.tab_menu = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_menu, text="🍽️ Menú")
        self._crear_tab_menu()
    
    def _crear_tab_venta(self):
        """Crear pestaña de venta (carrito)"""
        
        # Frame superior: Categorías y menú
        frame_superior = ttk.Frame(self.tab_venta)
        frame_superior.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Categorías
        ttk.Label(frame_superior, text="Categorías:").pack()
        self.categoria_var = tk.StringVar()
        categorias = ["Todos"] + self.menu.obtener_categorias()
        combo_categoria = ttk.Combobox(frame_superior, textvariable=self.categoria_var, 
                                       values=categorias, state="readonly")
        combo_categoria.pack(fill=tk.X, pady=5)
        combo_categoria.bind("<<ComboboxSelected>>", lambda e: self._actualizar_items_menu())
        combo_categoria.current(0)
        
        # Listbox de items
        ttk.Label(frame_superior, text="Menú Disponible:").pack()
        scrollbar = ttk.Scrollbar(frame_superior)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox_menu = tk.Listbox(frame_superior, yscrollcommand=scrollbar.set)
        self.listbox_menu.pack(fill=tk.BOTH, expand=True, pady=5)
        scrollbar.config(command=self.listbox_menu.yview)
        
        # Frame para agregar al carrito
        frame_agregar = ttk.Frame(frame_superior)
        frame_agregar.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame_agregar, text="Cantidad:").pack(side=tk.LEFT, padx=2)
        self.spinbox_cantidad = ttk.Spinbox(frame_agregar, from_=1, to=100, width=5)
        self.spinbox_cantidad.set(1)
        self.spinbox_cantidad.pack(side=tk.LEFT, padx=2)
        
        ttk.Button(frame_agregar, text="➕ Agregar al Carrito", 
                  command=self._agregar_al_carrito).pack(side=tk.LEFT, padx=2)
        
        self._actualizar_items_menu()
        
        # Frame derecho: Carrito y resumen
        frame_derecho = ttk.Frame(self.tab_venta)
        frame_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Carrito
        ttk.Label(frame_derecho, text="🛒 Carrito:", font=("Arial", 12, "bold")).pack()
        
        scrollbar_carrito = ttk.Scrollbar(frame_derecho)
        scrollbar_carrito.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox_carrito = tk.Listbox(frame_derecho, yscrollcommand=scrollbar_carrito.set, height=10)
        self.listbox_carrito.pack(fill=tk.BOTH, expand=True, pady=5)
        scrollbar_carrito.config(command=self.listbox_carrito.yview)
        
        # Frame para editar carrito
        frame_editar = ttk.Frame(frame_derecho)
        frame_editar.pack(fill=tk.X, pady=5)
        
        ttk.Button(frame_editar, text="✏️ Editar Cantidad", 
                  command=self._editar_cantidad_carrito).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_editar, text="❌ Eliminar", 
                  command=self._eliminar_del_carrito).pack(side=tk.LEFT, padx=2)
        
        # Resumen
        self.label_resumen = ttk.Label(frame_derecho, text="", font=("Arial", 10))
        self.label_resumen.pack(fill=tk.X, pady=10)
        
        # Frame de cobro
        frame_cobro = ttk.Frame(frame_derecho)
        frame_cobro.pack(fill=tk.X, pady=10)
        
        ttk.Label(frame_cobro, text="Forma de Pago:").pack(side=tk.LEFT, padx=2)
        self.pago_var = tk.StringVar(value="Efectivo")
        combo_pago = ttk.Combobox(frame_cobro, textvariable=self.pago_var,
                                  values=["Efectivo", "Tarjeta Débito", "Tarjeta Crédito", "Transferencia"],
                                  state="readonly")
        combo_pago.pack(side=tk.LEFT, padx=2)
        
        ttk.Button(frame_cobro, text="💰 COBRAR", 
                  command=self._procesar_cobro).pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
        
        ttk.Button(frame_cobro, text="🔄 Limpiar", 
                  command=self.nuevo_pedido).pack(side=tk.LEFT, padx=2)
    
    def _crear_tab_menu(self):
        """Crear pestaña de administración de menú"""
        
        # Frame superior: Tabla de items
        frame_tabla = ttk.Frame(self.tab_menu)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(frame_tabla, text="Items del Menú", font=("Arial", 12, "bold")).pack()
        
        # Treeview
        colunas = ("ID", "Nombre", "Precio", "Categoría", "Descripción")
        self.tree_menu = ttk.Treeview(frame_tabla, columns=colunas, height=12, show="headings")
        
        for col in colunas:
            self.tree_menu.heading(col, text=col)
            self.tree_menu.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree_menu.yview)
        self.tree_menu.configure(yscrollcommand=scrollbar.set)
        self.tree_menu.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self._actualizar_tabla_menu()
        
        # Frame inferior: Botones de gestión
        frame_botones = ttk.Frame(self.tab_menu)
        frame_botones.pack(fill=tk.X, padx=5, pady=10)
        
        ttk.Button(frame_botones, text="➕ Nuevo Item", 
                  command=self._nuevo_item).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="✏️ Editar", 
                  command=self._editar_item).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="❌ Eliminar", 
                  command=self._eliminar_item).pack(side=tk.LEFT, padx=2)
    
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
            messagebox.showwarning("Carrito Vacío", "Agrега items al carrito antes de cobrar")
            return
        
        # Marcar pedido como completado
        self.pedido_actual.estado = "completado"
        
        # Generar factura
        forma_pago = self.pago_var.get()
        factura = Factura(self.pedido_actual, forma_pago)
        
        # Mostrar factura
        ventana_factura = tk.Toplevel(self.ventana)
        ventana_factura.title("Factura de Venta")
        ventana_factura.geometry("600x600")
        
        text_factura = tk.Text(ventana_factura)
        text_factura.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        text_factura.insert("1.0", factura.generar_texto(
            self.nombre_negocio.get(),
            self.nit_negocio.get()
        ))
        text_factura.config(state="disabled")
        
        # Botones de acciones
        frame_botones = ttk.Frame(ventana_factura)
        frame_botones.pack(fill=tk.X, padx=5, pady=5)
        
        def guardar_factura():
            ruta = filedialog.asksaveasfilename(defaultextension=".txt",
                                               filetypes=[("Texto", "*.txt"), ("PDF", "*.pdf")])
            if ruta:
                factura.guardar_factura(ruta)
                messagebox.showinfo("Éxito", f"✅ Factura guardada en:\n{ruta}")
        
        def imprimir_factura():
            self._imprimir_linux(factura)
        
        ttk.Button(frame_botones, text="💾 Guardar", command=guardar_factura).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="🖨️ Imprimir", command=imprimir_factura).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="❌ Cerrar", command=ventana_factura.destroy).pack(side=tk.LEFT, padx=2)
        
        # Nuevo pedido
        self.nuevo_pedido()
    
    def _imprimir_linux(self, factura: Factura):
        """Imprimir factura en impresora Linux"""
        try:
            # Guardar factura en archivo temporal
            archivo_temp = "/tmp/factura_temporal.txt"
            factura.guardar_factura(archivo_temp)
            
            # Usar 'lp' comando de CUPS (sistema de impresión estándar en Linux)
            resultado = subprocess.run(["lp", archivo_temp], capture_output=True)
            
            if resultado.returncode == 0:
                messagebox.showinfo("Éxito", "✅ Factura enviada a la impresora")
            else:
                messagebox.showerror("Error", f"Error al imprimir:\n{resultado.stderr.decode()}")
                
        except FileNotFoundError:
            messagebox.showerror("Error", "❌ El comando 'lp' no está disponible.\nInstala CUPS.")
    
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
