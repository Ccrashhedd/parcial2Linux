"""
Módulo optimizado para carga rápida de productos con lazy loading
"""
import tkinter as tk
from tkinter import ttk


class VisorProductosOptimizado:
    """Visor de productos con carga optimizada"""
    
    def __init__(self, parent, colores, productos, callback_agregar):
        self.parent = parent
        self.colores = colores
        self.productos = productos
        self.callback_agregar = callback_agregar
        self.visible_items = []
        self.max_items_visible = 30
        
    def crear_grid(self, categoria="Todos"):
        """Crear grid de productos de forma optimizada"""
        # Limpiar widgets previos
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Filtrar productos por categoría
        items_filtrados = self._filtrar_productos(categoria)
        
        if not items_filtrados:
            self._mostrar_vacio()
            return
        
        # Crear canvas scrollable para mejor rendimiento
        canvas = tk.Canvas(self.parent, bg=self.colores['fondo_principal'], 
                          highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colores['fondo_principal'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Crear grid de productos en batches
        row = 0
        col = 0
        for idx, item in enumerate(items_filtrados):
            if idx >= self.max_items_visible:
                break
            
            self._crear_card_optimizada(scrollable_frame, item, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1
        
        # Empacar canvas y scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _filtrar_productos(self, categoria):
        """Filtrar productos por categoría"""
        if categoria == "Todos":
            return self.productos
        return [p for p in self.productos if p.get('categoria') == categoria]
    
    def _crear_card_optimizada(self, parent, item, row, col):
        """Crear card de producto de forma optimizada"""
        card = tk.Frame(parent, bg=self.colores['fondo_card'], relief=tk.FLAT)
        card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
        
        # Nombre (sin truncate excesivo)
        nombre = item.get('nombre', 'Producto')
        tk.Label(card, text=nombre, font=('Inter', 10, 'bold'),
                fg=self.colores['texto_principal'],
                bg=self.colores['fondo_card'], 
                wraplength=150, justify=tk.CENTER).pack(pady=(10, 3), padx=10)
        
        # Precio
        precio = item.get('precio', 0)
        tk.Label(card, text=f"${precio:,.0f}", font=('Inter', 11, 'bold'),
                fg=self.colores['acento_dorado'],
                bg=self.colores['fondo_card']).pack(pady=3)
        
        # Botón
        tk.Button(card, text="Agregar", bg=self.colores['verde_success'],
                 fg='white', font=('Inter', 8, 'bold'), relief='flat',
                 padx=15, pady=6,
                 command=lambda: self.callback_agregar(item)).pack(fill=tk.X, padx=8, pady=(3, 8))
    
    def _mostrar_vacio(self):
        """Mostrar mensaje de sin productos"""
        msg_frame = tk.Frame(self.parent, bg=self.colores['fondo_principal'])
        msg_frame.pack(fill=tk.BOTH, expand=True, pady=50)
        tk.Label(msg_frame, text="❌ Sin productos en esta categoría",
                font=('Inter', 14), fg=self.colores['texto_secundario'],
                bg=self.colores['fondo_principal']).pack()
