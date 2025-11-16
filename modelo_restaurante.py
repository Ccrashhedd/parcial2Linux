"""
modelo_restaurante.py - Clases de modelo de datos para el sistema POS de restaurante
"""

from datetime import datetime
from typing import List, Dict
import uuid


class MenuItem:
    """Representa un plato en el menú"""
    
    def __init__(self, id: str, nombre: str, precio: float, categoria: str = "General", descripcion: str = ""):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.descripcion = descripcion
    
    def __repr__(self):
        return f"{self.nombre} (${self.precio:.2f})"


class LineaPedido:
    """Representa un item en el carrito/pedido"""
    
    def __init__(self, menu_item: MenuItem, cantidad: int):
        self.menu_item = menu_item
        self.cantidad = cantidad
    
    @property
    def subtotal(self) -> float:
        return self.menu_item.precio * self.cantidad
    
    def __repr__(self):
        return f"{self.menu_item.nombre} x{self.cantidad} = ${self.subtotal:.2f}"


class Pedido:
    """Representa un pedido/venta"""
    
    def __init__(self, id: str = None):
        self.id = id or str(uuid.uuid4())[:8]
        self.lineas: List[LineaPedido] = []
        self.fecha = datetime.now()
        self.estado = "pendiente"  # pendiente, completado, cancelado
    
    def agregar_item(self, menu_item: MenuItem, cantidad: int):
        """Agregar o actualizar un item en el pedido"""
        for linea in self.lineas:
            if linea.menu_item.id == menu_item.id:
                linea.cantidad += cantidad
                return
        self.lineas.append(LineaPedido(menu_item, cantidad))
    
    def remover_item(self, menu_item_id: str):
        """Remover un item del pedido"""
        self.lineas = [l for l in self.lineas if l.menu_item.id != menu_item_id]
    
    def actualizar_cantidad(self, menu_item_id: str, nueva_cantidad: int):
        """Actualizar cantidad de un item"""
        for linea in self.lineas:
            if linea.menu_item.id == menu_item_id:
                if nueva_cantidad <= 0:
                    self.remover_item(menu_item_id)
                else:
                    linea.cantidad = nueva_cantidad
                return
    
    @property
    def subtotal(self) -> float:
        return sum(linea.subtotal for linea in self.lineas)
    
    @property
    def impuesto(self) -> float:
        """IVA del 19% (puedes cambiar este valor)"""
        return self.subtotal * 0.19
    
    @property
    def total(self) -> float:
        return self.subtotal + self.impuesto
    
    def limpiar(self):
        """Limpiar el carrito"""
        self.lineas = []
        self.id = str(uuid.uuid4())[:8]


class Factura:
    """Representa una factura de venta"""
    
    def __init__(self, pedido: Pedido, forma_pago: str = "Efectivo"):
        self.numero = str(uuid.uuid4())[:10].upper()
        self.pedido = pedido
        self.fecha = datetime.now()
        self.forma_pago = forma_pago
        self.estado = "emitida"
    
    def generar_texto(self, nombre_negocio: str = "RESTAURANTE", nit: str = "123456789") -> str:
        """Genera factura en formato de texto"""
        
        texto = []
        texto.append("=" * 50)
        texto.append(nombre_negocio.center(50))
        texto.append("=" * 50)
        texto.append("")
        texto.append(f"NIT: {nit}")
        texto.append(f"FACTURA Nº: {self.numero}")
        texto.append(f"FECHA: {self.fecha.strftime('%d/%m/%Y %H:%M:%S')}")
        texto.append("")
        texto.append("-" * 50)
        texto.append("DESCRIPCIÓN                      CANT   PRECIO    TOTAL")
        texto.append("-" * 50)
        
        # Items
        for linea in self.pedido.lineas:
            nombre = linea.menu_item.nombre[:30]
            cantidad = linea.cantidad
            precio = linea.menu_item.precio
            total = linea.subtotal
            
            texto.append(f"{nombre:<30} {cantidad:>4} ${precio:>8.2f} ${total:>8.2f}")
        
        texto.append("-" * 50)
        texto.append(f"SUBTOTAL: {'':>36} ${self.pedido.subtotal:>8.2f}")
        texto.append(f"IVA 19%:  {'':>36} ${self.pedido.impuesto:>8.2f}")
        texto.append("=" * 50)
        texto.append(f"TOTAL:    {'':>36} ${self.pedido.total:>8.2f}")
        texto.append("=" * 50)
        texto.append("")
        texto.append(f"FORMA DE PAGO: {self.forma_pago}")
        texto.append("")
        texto.append("¡GRACIAS POR SU COMPRA!".center(50))
        texto.append("")
        
        return "\n".join(texto)
    
    def guardar_factura(self, ruta: str = "/tmp/factura.txt") -> bool:
        """Guardar factura a archivo"""
        try:
            with open(ruta, "w") as f:
                f.write(self.generar_texto())
            return True
        except Exception as e:
            print(f"Error al guardar factura: {e}")
            return False
    
    def __repr__(self):
        return f"Factura #{self.numero} - Total: ${self.pedido.total:.2f}"


class Menu:
    """Almacena y gestiona los items del menú"""
    
    def __init__(self):
        self.items: Dict[str, MenuItem] = {}
        self._cargar_menu_ejemplo()
    
    def _cargar_menu_ejemplo(self):
        """Carga un menú de ejemplo"""
        items_ejemplo = [
            MenuItem("1", "Hamburguesa", 35000, "Platos Principales", "Con queso y tomate"),
            MenuItem("2", "Pizza Margarita", 28000, "Platos Principales", "Tomate, mozzarella y albahaca"),
            MenuItem("3", "Ensalada César", 18000, "Ensaladas", "Con pollo y queso parmesano"),
            MenuItem("4", "Jugo Natural", 8000, "Bebidas", "Naranja, manzana o fresa"),
            MenuItem("5", "Cerveza", 12000, "Bebidas", "Barril o embotellada"),
            MenuItem("6", "Postre del Día", 15000, "Postres", "Consultar disponibilidad"),
        ]
        for item in items_ejemplo:
            self.items[item.id] = item
    
    def agregar_item(self, nombre: str, precio: float, categoria: str = "General", descripcion: str = ""):
        """Agregar un nuevo item al menú"""
        item_id = str(len(self.items) + 1)
        item = MenuItem(item_id, nombre, precio, categoria, descripcion)
        self.items[item_id] = item
        return item
    
    def editar_item(self, item_id: str, nombre: str = None, precio: float = None, 
                   categoria: str = None, descripcion: str = None):
        """Editar un item del menú"""
        if item_id not in self.items:
            return False
        
        item = self.items[item_id]
        if nombre:
            item.nombre = nombre
        if precio:
            item.precio = precio
        if categoria:
            item.categoria = categoria
        if descripcion:
            item.descripcion = descripcion
        
        return True
    
    def eliminar_item(self, item_id: str) -> bool:
        """Eliminar un item del menú"""
        if item_id in self.items:
            del self.items[item_id]
            return True
        return False
    
    def obtener_item(self, item_id: str) -> MenuItem:
        """Obtener un item del menú"""
        return self.items.get(item_id)
    
    def listar_por_categoria(self, categoria: str = None) -> List[MenuItem]:
        """Listar items por categoría"""
        if categoria:
            return [item for item in self.items.values() if item.categoria == categoria]
        return list(self.items.values())
    
    def obtener_categorias(self) -> List[str]:
        """Obtener lista de categorías únicas"""
        return sorted(set(item.categoria for item in self.items.values()))
