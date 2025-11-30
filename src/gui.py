#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Interfaz gráfica moderna para el Gestor de Productos."""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from datetime import datetime
import urllib.request
from urllib.error import URLError
import tempfile

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database_psql import BaseDatos
from src.impresora import Impresora
from config import APP_CONFIG

CARPETA_IMAGENES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "imagenes")


class GestorProductos:
    """Ventana principal del gestor."""

    def __init__(self, root: tk.Tk):
        self.root = root
        # Importar la configuración de BD desde config.py
        from config import DB_CONFIG
        self.db = BaseDatos(**DB_CONFIG)
        self._imagenes_cache = {}
        self.producto_seleccionado = None
        self.producto_items = {}
        self.productos_seleccionados = set()
        self._configurar_ventana()
        self._construir_interfaz()
        self.cargar_productos()

    def _configurar_ventana(self):
        self.color_primario = "#1976D2"
        self.color_fondo = "#1E1E1E"
        self.color_panel = "#2A2A2A"
        self.color_texto = "#FFFFFF"

        self.root.title(APP_CONFIG.get("title", "Gestor de Productos"))
        self.root.geometry(
            f"{APP_CONFIG.get('window_width', 1800)}x{APP_CONFIG.get('window_height', 1000)}"
        )
        self.root.minsize(1400, 800)
        self.root.configure(bg=self.color_fondo)
        
        # Manejador para cierre limpio de la ventana
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _construir_interfaz(self):
        main_frame = tk.Frame(self.root, bg=self.color_fondo)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self._crear_barra_superior(main_frame)
        self._crear_area_busqueda(main_frame)
        self._crear_tabla(main_frame)
        self._crear_barra_inferior(main_frame)

    def _crear_barra_superior(self, parent):
        header = tk.Frame(parent, bg=self.color_primario, height=70)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)

        titulo = tk.Label(
            header,
            text="📦 GESTOR DE PRODUCTOS",
            font=("Segoe UI", 20, "bold"),
            bg=self.color_primario,
            fg="white",
        )
        titulo.pack(side=tk.LEFT, padx=20)

        version = tk.Label(
            header,
            text=f"v{APP_CONFIG.get('version', '1.0')}",
            font=("Segoe UI", 10),
            bg=self.color_primario,
            fg="white",
        )
        version.pack(side=tk.LEFT)

        botones = [
            ("✨ NUEVO", self.abrir_nuevo_producto, "#4CAF50"),
            ("✏️ EDITAR", self.abrir_editar_producto, "#2196F3"),
            ("🗑️ ELIMINAR", self.eliminar_producto, "#F44336"),
            ("🖨️ IMPRIMIR", self.abrir_vista_previa, "#FF9800"),
            ("🔄 ACTUALIZAR", self.cargar_productos, "#00BCD4"),
        ]

        for texto, comando, color in botones:
            btn = tk.Button(
                header,
                text=texto,
                command=comando,
                font=("Segoe UI", 10, "bold"),
                bg=color,
                fg="white",
                borderwidth=0,
                padx=14,
                pady=8,
                cursor="hand2",
            )
            btn.pack(side=tk.LEFT, padx=5)

    def _crear_area_busqueda(self, parent):
        frame = tk.Frame(parent, bg=self.color_panel, height=50)
        frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        frame.pack_propagate(False)

        tk.Label(
            frame,
            text="Buscar:",
            font=("Segoe UI", 10, "bold"),
            bg=self.color_panel,
            fg="white",
        ).pack(side=tk.LEFT, padx=(15, 5))

        self.entry_busqueda = tk.Entry(
            frame,
            font=("Segoe UI", 10),
            bg="#3A3A3A",
            fg="white",
            insertbackground="#81D4FA",
            width=35,
        )
        self.entry_busqueda.pack(side=tk.LEFT, padx=5)
        self.entry_busqueda.bind("<KeyRelease>", self.buscar_productos)

        tk.Button(
            frame,
            text="Limpiar",
            command=self.limpiar_busqueda,
            bg="#9C27B0",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
            padx=12,
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=5)

    def _crear_tabla(self, parent):
        container = tk.Frame(parent, bg=self.color_panel)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Canvas con scrollbar para las filas
        canvas_frame = tk.Frame(container, bg=self.color_panel)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg=self.color_panel, highlightthickness=0, bd=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.color_panel)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self._on_frame_configure(e)
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Permitir scroll con mousewheel SOLO en el canvas
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Button-4>", self._on_mousewheel)
        self.canvas.bind("<Button-5>", self._on_mousewheel)

        # Bind para ajustar ancho cuando se redimensiona el canvas
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self.producto_items = {}
        self.tree = None  # Para compatibilidad
    
    def _on_closing(self):
        """Maneja el cierre limpio de la aplicación"""
        try:
            # Cerrar conexión a la base de datos
            if hasattr(self, 'db') and self.db:
                self.db.desconectar()
                print("✓ Base de datos desconectada correctamente")
        except Exception as e:
            print(f"Advertencia al cerrar BD: {e}")
        finally:
            # Destruir la ventana y salir
            self.root.destroy()
            print("✓ Aplicación cerrada")
    
    def _on_frame_configure(self, event):
        """Actualiza la región de scroll cuando el frame cambia"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _on_canvas_configure(self, event):
        """Ajusta el ancho del scrollable_frame al ancho del canvas"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _crear_barra_inferior(self, parent):
        footer = tk.Frame(parent, bg=self.color_fondo, height=40)
        footer.pack(fill=tk.X)
        footer.pack_propagate(False)

        tk.Label(
            footer,
            text="© 2025 - Gestor de Productos",
            font=("Segoe UI", 9),
            bg=self.color_fondo,
            fg="#999999",
        ).pack(side=tk.LEFT, padx=15)

    # Eventos y lógica de negocio

    def _cargar_imagen_tabla(self, nombre_imagen: str):
        """Carga imagen pequeña (80x80) para la tabla"""
        if not nombre_imagen:
            return None

        cache_key = f"tabla_{nombre_imagen}"
        if cache_key in self._imagenes_cache:
            return self._imagenes_cache[cache_key]

        # Construir la ruta de la imagen
        ruta = os.path.join(CARPETA_IMAGENES, nombre_imagen)

        if not os.path.exists(ruta) or not HAS_PIL:
            return None

        try:
            imagen = Image.open(ruta)
            imagen.thumbnail((80, 80), Image.Resampling.LANCZOS)
            foto = ImageTk.PhotoImage(imagen)
            self._imagenes_cache[cache_key] = foto
            return foto
        except Exception as e:
            print(f"Error cargando imagen {nombre_imagen}: {e}")
            return None

    def _cargar_imagen_item(self, nombre_imagen: str):
        if not nombre_imagen:
            return None

        if nombre_imagen in self._imagenes_cache:
            return self._imagenes_cache[nombre_imagen]

        # Construir la ruta de la imagen
        ruta = os.path.join(CARPETA_IMAGENES, nombre_imagen)

        if not os.path.exists(ruta) or not HAS_PIL:
            return None

        try:
            imagen = Image.open(ruta)
            imagen.thumbnail((150, 150), Image.Resampling.LANCZOS)
            foto = ImageTk.PhotoImage(imagen)
            self._imagenes_cache[nombre_imagen] = foto
            return foto
        except Exception as e:
            print(f"Error cargando imagen {nombre_imagen}: {e}")
            return None

    def cargar_productos(self):
        productos = self.db.obtener_todos_productos()
        
        # Limpiar filas anteriores
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.producto_items = {}
        
        for producto in productos:
            self._crear_fila_producto(producto)
    
    def _crear_fila_producto(self, producto):
        """Crea una fila de producto con imagen real"""
        # Frame para la fila (horizontal: imagen + datos)
        fila = tk.Frame(self.scrollable_frame, bg="#2E2E2E", relief=tk.RAISED, bd=1)
        fila.pack(fill=tk.X, pady=5, padx=0)

        # Frame para imagen (100x100)
        img_frame = tk.Frame(fila, bg="#1A1A1A", width=120, height=100)
        img_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=8, pady=8)
        img_frame.pack_propagate(False)

        # Cargar y mostrar imagen
        foto = self._cargar_imagen_tabla(producto.get("imagen_path"))
        if foto:
            label_img = tk.Label(img_frame, image=foto, bg="#1A1A1A", bd=0)
            label_img.image = foto
            label_img.pack(fill=tk.BOTH, expand=True)
        else:
            tk.Label(img_frame, text="📷", font=("Arial", 40), bg="#1A1A1A", fg="#555555").pack(fill=tk.BOTH, expand=True)

        # Frame para datos (vertical: nombre, descripción, precio, etc)
        datos = tk.Frame(fila, bg="#2E2E2E")
        datos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=8)

        # Nombre (grande)
        nombre_frame = tk.Frame(datos, bg="#2E2E2E")
        nombre_frame.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(nombre_frame, text=f"#{producto['id']}", font=("Segoe UI", 9, "bold"), bg="#2E2E2E", fg="#1976D2").pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(nombre_frame, text=producto["nombre"], font=("Segoe UI", 13, "bold"), bg="#2E2E2E", fg="white").pack(side=tk.LEFT)
        tk.Label(nombre_frame, text=f"${producto['precio']:.2f}", font=("Segoe UI", 12, "bold"), bg="#2E2E2E", fg="#4CAF50").pack(side=tk.RIGHT, padx=10)

        # Descripción
        desc = producto["descripcion"][:80] + "..." if len(producto["descripcion"]) > 80 else producto["descripcion"]
        tk.Label(datos, text=desc, font=("Segoe UI", 9), bg="#2E2E2E", fg="#AAAAAA", wraplength=600, justify=tk.LEFT).pack(fill=tk.X, pady=2)

        # Bindings para seleccionar y editar
        for widget in [fila, img_frame, datos, nombre_frame]:
            widget.bind("<Button-1>", lambda e, pid=producto["id"]: self._seleccionar_producto(pid, e))
            widget.bind("<Double-1>", lambda e, pid=producto["id"]: self._editar_producto_id(pid))
        
        self.producto_items[producto["id"]] = fila
    
    def _seleccionar_producto(self, producto_id, event=None):
        """Selecciona un producto (Ctrl+Click para múltiple)"""
        # Si es Ctrl+Click, agregar/quitar de la selección
        if event and event.state & 0x4:  # 0x4 es Ctrl
            if producto_id in self.productos_seleccionados:
                self.productos_seleccionados.remove(producto_id)
            else:
                self.productos_seleccionados.add(producto_id)
        else:
            # Click normal: seleccionar solo este
            self.productos_seleccionados = {producto_id}
        
        # Actualizar colores
        for pid, frame in self.producto_items.items():
            if pid in self.productos_seleccionados:
                frame.config(bg=self.color_primario, relief=tk.SUNKEN)
                for child in frame.winfo_children():
                    self._cambiar_bg_recursivo(child, self.color_primario)
            else:
                frame.config(bg="#2E2E2E", relief=tk.RAISED)
                for child in frame.winfo_children():
                    self._cambiar_bg_recursivo(child, "#2E2E2E")
        
        self.producto_seleccionado = producto_id
    
    def _cambiar_bg_recursivo(self, widget, color):
        """Cambia background recursivamente"""
        try:
            if widget.winfo_class() == "Frame":
                widget.config(bg=color)
                for child in widget.winfo_children():
                    self._cambiar_bg_recursivo(child, color)
            elif widget.winfo_class() == "Label" and not widget.cget("image"):
                widget.config(bg=color)
        except:
            pass
    
    def _on_mousewheel(self, event):
        """Maneja el scroll del mouse"""
        if event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
    
    def _editar_producto_id(self, producto_id):
        """Muestra vista individual del producto al hacer doble click"""
        producto = self.db.obtener_producto(producto_id)
        if producto:
            VentanaProductoIndividual(self.root, self.db, producto)

    def buscar_productos(self, event=None):
        termino = self.entry_busqueda.get().strip()
        
        # Limpiar filas
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.producto_items = {}
        
        productos = self.db.buscar_productos(termino) if termino else self.db.obtener_todos_productos()
        for producto in productos:
            self._crear_fila_producto(producto)

    def limpiar_busqueda(self):
        self.entry_busqueda.delete(0, tk.END)
        self.cargar_productos()

    def _obtener_producto_seleccionado(self):
        if not hasattr(self, 'producto_seleccionado') or not self.producto_seleccionado:
            messagebox.showwarning("Atención", "Selecciona un producto primero")
            return None
        return self.db.obtener_producto(self.producto_seleccionado)

    def abrir_nuevo_producto(self):
        VentanaProducto(self.root, self.db, self.cargar_productos, modo="crear")

    def abrir_editar_producto(self):
        producto = self._obtener_producto_seleccionado()
        if producto:
            VentanaProducto(self.root, self.db, self.cargar_productos, modo="editar", producto=producto)

    def eliminar_producto(self):
        producto = self._obtener_producto_seleccionado()
        if not producto:
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar '{producto['nombre']}'?"):
            return
        try:
            self.db.eliminar_producto(producto["id"])
            messagebox.showinfo("Éxito", "Producto eliminado correctamente")
            self.cargar_productos()
        except Exception as error:
            messagebox.showerror("Error", str(error))

    def abrir_vista_previa(self):
        if not self.productos_seleccionados:
            messagebox.showwarning("Atención", "Selecciona productos para imprimir\n(Ctrl+Click para múltiples)")
            return

        productos = []
        for pid in self.productos_seleccionados:
            producto = self.db.obtener_producto(pid)
            if producto:
                productos.append(producto)
        
        if productos:
            VentanaVistaPrevia(self.root, productos)


class VentanaProducto:
    """Ventana para crear o editar productos."""

    def __init__(self, parent, db, callback, modo="crear", producto=None):
        self.db = db
        self.callback = callback
        self.modo = modo
        self.producto = producto
        self.nueva_imagen = None
        self.imagen_guardada = producto.get("imagen_path") if producto else None

        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Nuevo Producto" if modo == "crear" else f"Editar - {producto['nombre']}")
        self.ventana.geometry("600x700")
        self.ventana.configure(bg="#1E1E1E")
        self.ventana.transient(parent)  # La ventana siempre está sobre la parent
        self.ventana.grab_set()  # Modal
        self.ventana.focus()  # Focus en esta ventana

        self._construir_formulario()

        if producto:
            self._cargar_datos()

    def _construir_formulario(self):
        main_frame = tk.Frame(self.ventana, bg="#1E1E1E")
        main_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_frame, bg="#1E1E1E", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable = tk.Frame(canvas, bg="#1E1E1E")
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        titulo = tk.Label(
            scrollable,
            text="INFORMACIÓN DEL PRODUCTO",
            font=("Segoe UI", 13, "bold"),
            bg="#1976D2",
            fg="white",
            pady=12,
        )
        titulo.pack(fill=tk.X)

        contenido = tk.Frame(scrollable, bg="#1E1E1E")
        contenido.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.entry_nombre = self._crear_input(contenido, "Nombre *")
        self.entry_precio = self._crear_input(contenido, "Precio *")

        tk.Label(
            contenido,
            text="Descripción",
            font=("Segoe UI", 10, "bold"),
            bg="#1E1E1E",
            fg="white",
        ).pack(anchor=tk.W, pady=(15, 5))

        self.text_descripcion = scrolledtext.ScrolledText(
            contenido,
            height=6,
            font=("Segoe UI", 10),
            bg="#2E2E2E",
            fg="white",
            insertbackground="#81D4FA",
        )
        self.text_descripcion.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            contenido,
            text="Imagen",
            font=("Segoe UI", 10, "bold"),
            bg="#1E1E1E",
            fg="white",
        ).pack(anchor=tk.W, pady=(20, 5))

        barra_imagen = tk.Frame(contenido, bg="#1E1E1E")
        barra_imagen.pack(fill=tk.X)

        tk.Button(
            barra_imagen,
            text="📷 Seleccionar",
            command=self.seleccionar_imagen,
            bg="#FF9800",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
            padx=15,
            pady=8,
            cursor="hand2",
        ).pack(side=tk.LEFT)

        tk.Button(
            barra_imagen,
            text="🌐 URL",
            command=self.ingresar_url_imagen,
            bg="#2196F3",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
            padx=15,
            pady=8,
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=5)

        self.label_imagen = tk.Label(
            barra_imagen,
            text="Sin imagen",
            font=("Segoe UI", 9),
            bg="#1E1E1E",
            fg="#B0BEC5",
        )
        self.label_imagen.pack(side=tk.LEFT, padx=10)

        self.preview = tk.Label(contenido, bg="#2E2E2E", height=180)
        self.preview.pack(fill=tk.X, pady=10)

        acciones = tk.Frame(contenido, bg="#1E1E1E")
        acciones.pack(fill=tk.X, pady=20)

        tk.Button(
            acciones,
            text="💾 GUARDAR",
            command=self.guardar,
            bg="#4CAF50",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            borderwidth=0,
            padx=25,
            pady=12,
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            acciones,
            text="✖️ CANCELAR",
            command=self.ventana.destroy,
            bg="#E91E63",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            borderwidth=0,
            padx=25,
            pady=12,
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=5)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _crear_input(self, parent, etiqueta):
        tk.Label(
            parent,
            text=etiqueta,
            font=("Segoe UI", 10, "bold"),
            bg="#1E1E1E",
            fg="white",
        ).pack(anchor=tk.W, pady=(10, 5))

        entry = tk.Entry(
            parent,
            font=("Segoe UI", 11),
            bg="#2E2E2E",
            fg="white",
            insertbackground="#81D4FA",
        )
        entry.pack(fill=tk.X)
        return entry

    def _cargar_datos(self):
        self.entry_nombre.insert(0, self.producto["nombre"])
        self.entry_precio.insert(0, str(self.producto["precio"]))
        self.text_descripcion.insert("1.0", self.producto.get("descripcion") or "")

        if self.imagen_guardada:
            self.label_imagen.config(text=self.imagen_guardada, fg="#4DD0E1")
            ruta = os.path.join(CARPETA_IMAGENES, self.imagen_guardada)
            self._mostrar_preview(ruta)

    def seleccionar_imagen(self):
        archivo = filedialog.askopenfilename(
            parent=self.ventana,
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp"), ("Todos", "*.*")],
        )

        if not archivo:
            return

        self.nueva_imagen = archivo
        self.label_imagen.config(text=os.path.basename(archivo), fg="#4DD0E1")
        self._mostrar_preview(archivo)

    def ingresar_url_imagen(self):
        """Abre un diálogo para ingresar URL de imagen"""
        ventana_url = tk.Toplevel(self.ventana)
        ventana_url.title("Ingresar URL de Imagen")
        ventana_url.geometry("500x150")
        ventana_url.configure(bg="#1E1E1E")
        ventana_url.transient(self.ventana)
        ventana_url.grab_set()

        tk.Label(
            ventana_url,
            text="Ingresa la URL de la imagen:",
            font=("Segoe UI", 10),
            bg="#1E1E1E",
            fg="white",
        ).pack(pady=10)

        entry_url = tk.Entry(
            ventana_url,
            font=("Segoe UI", 10),
            bg="#2E2E2E",
            fg="white",
            insertbackground="white",
        )
        entry_url.pack(fill=tk.X, padx=20, pady=10)
        entry_url.focus()

        def cargar_url():
            url = entry_url.get().strip()
            if not url:
                messagebox.showwarning("Atención", "Por favor ingresa una URL", parent=ventana_url)
                return

            try:
                # Descargar imagen de URL
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                    urllib.request.urlretrieve(url, tmp.name)
                    self.nueva_imagen = tmp.name
                    self.label_imagen.config(text=url[:40] + "...", fg="#4DD0E1")
                    self._mostrar_preview(tmp.name)
                    ventana_url.destroy()
                    messagebox.showinfo("Éxito", "Imagen cargada correctamente")
            except URLError as e:
                messagebox.showerror("Error", f"No se pudo descargar la imagen:\n{str(e)[:100]}", parent=ventana_url)
            except Exception as e:
                messagebox.showerror("Error", f"Error al procesar URL:\n{str(e)[:100]}", parent=ventana_url)

        tk.Button(
            ventana_url,
            text="Cargar",
            command=cargar_url,
            bg="#4CAF50",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8,
        ).pack(pady=10)

    def _mostrar_preview(self, ruta):
        if not ruta or not HAS_PIL or not os.path.exists(ruta):
            self.preview.config(image="", text="(Vista previa no disponible)", fg="#B0BEC5")
            self.preview.image = None
            return

        try:
            imagen = Image.open(ruta)
            imagen.thumbnail((360, 260), Image.Resampling.LANCZOS)
            foto = ImageTk.PhotoImage(imagen)
            self.preview.config(image=foto, text="")
            self.preview.image = foto
        except Exception:
            self.preview.config(image="", text="(Vista previa no disponible)", fg="#B0BEC5")
            self.preview.image = None

    def guardar(self):
        nombre = self.entry_nombre.get().strip()
        precio_str = self.entry_precio.get().strip()
        descripcion = self.text_descripcion.get("1.0", tk.END).strip()

        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return

        try:
            precio = float(precio_str)
            if precio < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Precio inválido")
            return

        try:
            if self.modo == "crear":
                self.db.crear_producto(nombre, precio, descripcion, self.nueva_imagen)
                mensaje = "Producto creado correctamente"
            else:
                self.db.actualizar_producto(
                    self.producto["id"], nombre, precio, descripcion, self.nueva_imagen
                )
                mensaje = "Producto actualizado correctamente"

            self.callback()
            self.ventana.destroy()
            messagebox.showinfo("Éxito", mensaje)
        except Exception as error:
            messagebox.showerror("Error", str(error))


class VentanaVistaPrevia:
    """Ventana para mostrar la vista previa de impresión con imágenes."""

    def __init__(self, parent, productos):
        self.productos = productos
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Vista Previa - Impresión")
        self.ventana.geometry("1000x700")
        self.ventana.configure(bg="#1E1E1E")
        self.ventana.transient(parent)
        self.ventana.grab_set()
        self.ventana.focus()
        
        self.pagina_actual = 0
        self._construir_vista()

    def _construir_vista(self):
        # Header
        header = tk.Frame(self.ventana, bg="#1976D2")
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="🖨️ VISTA PREVIA DE IMPRESIÓN",
            font=("Segoe UI", 14, "bold"),
            bg="#1976D2",
            fg="white",
            pady=10,
        ).pack()

        # Toolbar
        toolbar = tk.Frame(self.ventana, bg="#2A2A2A")
        toolbar.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(
            toolbar,
            text="◀ Anterior",
            command=self.pagina_anterior,
            bg="#FF9800",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
            padx=15,
            pady=8,
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=5)

        self.label_pagina = tk.Label(
            toolbar,
            text=f"Página 1 de {len(self.productos)}",
            font=("Segoe UI", 10),
            bg="#2A2A2A",
            fg="white",
        )
        self.label_pagina.pack(side=tk.LEFT, padx=20)

        tk.Button(
            toolbar,
            text="Siguiente ▶",
            command=self.pagina_siguiente,
            bg="#FF9800",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
            padx=15,
            pady=8,
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            toolbar,
            text="🖨️ IMPRIMIR",
            command=self.imprimir,
            bg="#4CAF50",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
            padx=15,
            pady=8,
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            toolbar,
            text="✖️ CERRAR",
            command=self.ventana.destroy,
            bg="#E53935",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
            padx=15,
            pady=8,
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=5)

        # Área de vista previa
        self.preview_frame = tk.Frame(self.ventana, bg="#1E1E1E")
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.mostrar_pagina()

    def mostrar_pagina(self):
        """Muestra la página actual"""
        # Limpiar frame anterior
        for widget in self.preview_frame.winfo_children():
            widget.destroy()

        if not self.productos:
            tk.Label(self.preview_frame, text="No hay productos para mostrar", bg="#1E1E1E", fg="white").pack()
            return

        # Obtener producto actual
        producto = self.productos[self.pagina_actual]

        # Actualizar label de página
        self.label_pagina.config(text=f"Página {self.pagina_actual + 1} de {len(self.productos)}")

        # Frame principal para el producto
        main = tk.Frame(self.preview_frame, bg="white", relief=tk.RAISED, bd=2)
        main.pack(fill=tk.BOTH, expand=True)

        # Header
        header = tk.Frame(main, bg="#1976D2")
        header.pack(fill=tk.X, padx=20, pady=15)

        tk.Label(
            header,
            text=f"Producto: {producto['nombre']}",
            font=("Segoe UI", 16, "bold"),
            bg="#1976D2",
            fg="white",
        ).pack()

        # Contenido
        contenido = tk.Frame(main, bg="white")
        contenido.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Fila 1: Imagen y datos principales
        fila1 = tk.Frame(contenido, bg="white")
        fila1.pack(fill=tk.X, pady=(0, 20))

        # Imagen
        img_frame = tk.Frame(fila1, bg="#F0F0F0", relief=tk.SUNKEN, bd=1)
        img_frame.pack(side=tk.LEFT, padx=(0, 30))

        imagen_path = os.path.join(CARPETA_IMAGENES, producto.get('imagen_path', ''))
        if os.path.exists(imagen_path):
            try:
                img = Image.open(imagen_path)
                img.thumbnail((250, 250), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                label_img = tk.Label(img_frame, image=photo, bg="#F0F0F0")
                label_img.image = photo
                label_img.pack(padx=5, pady=5)
            except:
                tk.Label(img_frame, text="No se puede cargar la imagen", bg="#F0F0F0", fg="#999").pack(padx=20, pady=20)
        else:
            tk.Label(img_frame, text="📷\nSin imagen", font=("Arial", 20), bg="#F0F0F0", fg="#CCC").pack(padx=20, pady=20)

        # Datos principales
        datos = tk.Frame(fila1, bg="white")
        datos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            datos,
            text=f"ID: {producto['id']}",
            font=("Segoe UI", 11),
            bg="white",
            fg="#666",
        ).pack(anchor=tk.W, pady=5)

        tk.Label(
            datos,
            text=f"Nombre: {producto['nombre']}",
            font=("Segoe UI", 13, "bold"),
            bg="white",
            fg="#333",
        ).pack(anchor=tk.W, pady=5)

        tk.Label(
            datos,
            text=f"Precio: ${producto['precio']:.2f}",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#4CAF50",
        ).pack(anchor=tk.W, pady=5)

        # Descripción
        tk.Label(
            contenido,
            text="Descripción:",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#333",
        ).pack(anchor=tk.W, pady=(10, 5))

        tk.Label(
            contenido,
            text=producto.get('descripcion', 'Sin descripción'),
            font=("Segoe UI", 10),
            bg="white",
            fg="#666",
            wraplength=700,
            justify=tk.LEFT,
        ).pack(anchor=tk.W, pady=(0, 20))

        # Footer
        footer = tk.Frame(main, bg="#F5F5F5")
        footer.pack(fill=tk.X, padx=20, pady=15)

        tk.Label(
            footer,
            text=f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            font=("Segoe UI", 9),
            bg="#F5F5F5",
            fg="#999",
        ).pack(anchor=tk.W)

    def pagina_anterior(self):
        """Va a la página anterior"""
        if self.pagina_actual > 0:
            self.pagina_actual -= 1
            self.mostrar_pagina()

    def pagina_siguiente(self):
        """Va a la página siguiente"""
        if self.pagina_actual < len(self.productos) - 1:
            self.pagina_actual += 1
            self.mostrar_pagina()

    def imprimir(self):
        """Imprime los productos seleccionados con GTK nativo"""
        try:
            # Mostrar un diálogo informando que se está abriendo el diálogo nativo
            messagebox.showinfo(
                "Impresión - Diálogo GTK Nativo", 
                f"Abriendo el diálogo de impresión nativo de GNOME...\n"
                f"Se imprimirán {len(self.productos)} producto(s)."
            )
            
            try:
                # Llamar al método de impresión (usa GTK obligatoriamente)
                Impresora.imprimir_productos_seleccionados(self.productos)
                messagebox.showinfo(
                    "Impresión", 
                    "✓ Operación completada.\n"
                    "Verifica si se envió a imprimir o si cancelaste la operación."
                )
            except Exception as gtk_error:
                # Si hay error específico de GTK, mostrar detalles
                messagebox.showerror(
                    "Error en Impresión", 
                    f"✗ Error: {str(gtk_error)}"
                )
                
        except Exception as error:
            # Error general (que no debería ocurrir)
            messagebox.showerror(
                "Error en Impresión", 
                f"✗ Error inesperado: {str(error)}\n\n"
                "GTK es REQUERIDO para imprimir.\n\n"
                "Instalación necesaria:\n"
                "- Debian/Ubuntu: sudo apt install python3-gi gir1.2-gtk-3.0\n"
                "- Fedora: sudo dnf install python3-gobject gtk3-devel\n"
                "- O en venv: pip install PyGObject"
            )


class VentanaProductoIndividual:
    """Ventana para ver detalles completos de un producto (doble click)"""

    def __init__(self, parent, db, producto):
        self.db = db
        self.producto = producto
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title(f"Producto: {producto['nombre']}")
        self.ventana.geometry("900x700")
        self.ventana.configure(bg="#1E1E1E")
        self.ventana.transient(parent)
        self.ventana.grab_set()
        self.ventana.focus()
        
        self._construir_vista()

    def _construir_vista(self):
        """Construye la vista del producto individual"""
        # Header
        header = tk.Frame(self.ventana, bg="#1976D2")
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text=f"📦 DETALLES DEL PRODUCTO - ID: {self.producto['id']}",
            font=("Segoe UI", 14, "bold"),
            bg="#1976D2",
            fg="white",
            pady=10,
        ).pack()

        # Contenido principal
        main_frame = tk.Frame(self.ventana, bg="#1E1E1E")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Dos columnas: imagen izquierda, datos derecha
        col_izq = tk.Frame(main_frame, bg="#1E1E1E")
        col_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 20))

        col_der = tk.Frame(main_frame, bg="#1E1E1E")
        col_der.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # COLUMNA IZQUIERDA - Imagen grande
        self._crear_seccion_imagen(col_izq)

        # COLUMNA DERECHA - Información
        self._crear_seccion_info(col_der)

        # Footer con botones
        footer = tk.Frame(self.ventana, bg="#2A2A2A")
        footer.pack(fill=tk.X, padx=20, pady=15)

        tk.Button(
            footer,
            text="✏️ EDITAR",
            command=self.cerrar_y_editar,
            bg="#2196F3",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            footer,
            text="🖨️ IMPRIMIR",
            command=self.imprimir_producto,
            bg="#FF9800",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            footer,
            text="❌ CERRAR",
            command=self.ventana.destroy,
            bg="#666666",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2",
        ).pack(side=tk.RIGHT, padx=5)

    def _crear_seccion_imagen(self, parent):
        """Crea la sección de imagen grande"""
        frame = tk.Frame(parent, bg="#2E2E2E", relief=tk.SUNKEN, bd=2)
        frame.pack(fill=tk.BOTH)

        # Imagen grande (300x300)
        img_label = tk.Label(frame, bg="#1A1A1A", height=12, width=30)
        img_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Cargar imagen
        imagen_path = self.producto.get("imagen_path")
        if imagen_path:
            try:
                # Si es URL o archivo local
                if imagen_path.startswith(('http://', 'https://')):
                    # Descargar desde URL
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                        urllib.request.urlretrieve(imagen_path, tmp.name)
                        imagen = Image.open(tmp.name)
                else:
                    # Archivo local
                    imagen = Image.open(imagen_path)

                imagen.thumbnail((300, 300), Image.Resampling.LANCZOS)
                foto = ImageTk.PhotoImage(imagen)
                img_label.config(image=foto, text="")
                img_label.image = foto
            except Exception:
                img_label.config(text="❌\nNo se pudo cargar", fg="#FF6B6B")
        else:
            img_label.config(text="📷\nSin imagen", fg="#999999")

    def _crear_seccion_info(self, parent):
        """Crea la sección de información del producto"""
        # Nombre
        tk.Label(
            parent,
            text="NOMBRE",
            font=("Segoe UI", 9, "bold"),
            bg="#1E1E1E",
            fg="#90CAF9",
        ).pack(anchor=tk.W, pady=(0, 3))

        tk.Label(
            parent,
            text=self.producto["nombre"],
            font=("Segoe UI", 16, "bold"),
            bg="#1E1E1E",
            fg="white",
            wraplength=400,
            justify=tk.LEFT,
        ).pack(anchor=tk.W, pady=(0, 15))

        # Precio
        tk.Label(
            parent,
            text="PRECIO",
            font=("Segoe UI", 9, "bold"),
            bg="#1E1E1E",
            fg="#90CAF9",
        ).pack(anchor=tk.W, pady=(0, 3))

        tk.Label(
            parent,
            text=f"${self.producto.get('precio', 0):.2f}",
            font=("Segoe UI", 20, "bold"),
            bg="#1E1E1E",
            fg="#4CAF50",
        ).pack(anchor=tk.W, pady=(0, 15))

        # Descripción
        tk.Label(
            parent,
            text="DESCRIPCIÓN",
            font=("Segoe UI", 9, "bold"),
            bg="#1E1E1E",
            fg="#90CAF9",
        ).pack(anchor=tk.W, pady=(0, 5))

        desc_frame = tk.Frame(parent, bg="#2E2E2E", relief=tk.SUNKEN, bd=1)
        desc_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        desc_text = scrolledtext.ScrolledText(
            desc_frame,
            font=("Segoe UI", 10),
            bg="#2E2E2E",
            fg="white",
            height=6,
            state=tk.DISABLED,
        )
        desc_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        desc_text.config(state=tk.NORMAL)
        desc_text.insert(tk.END, self.producto.get("descripcion", "Sin descripción"))
        desc_text.config(state=tk.DISABLED)

        # Metadatos
        meta_frame = tk.Frame(parent, bg="#1E1E1E")
        meta_frame.pack(fill=tk.X, pady=10)

        # Fecha creación
        tk.Label(
            meta_frame,
            text="Creado:",
            font=("Segoe UI", 9),
            bg="#1E1E1E",
            fg="#999999",
        ).pack(anchor=tk.W)

        tk.Label(
            meta_frame,
            text=self.producto.get("fecha_creacion", "N/A"),
            font=("Segoe UI", 9),
            bg="#1E1E1E",
            fg="#CCCCCC",
        ).pack(anchor=tk.W, pady=(0, 5))

        # Fecha actualización
        tk.Label(
            meta_frame,
            text="Actualizado:",
            font=("Segoe UI", 9),
            bg="#1E1E1E",
            fg="#999999",
        ).pack(anchor=tk.W)

        tk.Label(
            meta_frame,
            text=self.producto.get("fecha_actualizacion", "N/A"),
            font=("Segoe UI", 9),
            bg="#1E1E1E",
            fg="#CCCCCC",
        ).pack(anchor=tk.W)

    def cerrar_y_editar(self):
        """Cierra esta ventana y abre la de edición"""
        self.ventana.destroy()
        # La ventana padre se encargará de abrir el editor

    def imprimir_producto(self):
        """Imprime solo este producto"""
        try:
            Impresora.imprimir_productos_seleccionados([self.producto])
            messagebox.showinfo("Impresión", "✓ Producto enviado a imprimir")
        except Exception as e:
            messagebox.showerror("Error", f"Error al imprimir: {str(e)[:100]}")


def main():
    root = tk.Tk()
    GestorProductos(root)
    root.mainloop()


if __name__ == "__main__":
    main()

