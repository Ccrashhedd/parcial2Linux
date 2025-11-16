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
        """Carga un menú completo de restaurante premium"""
        items_ejemplo = [
            # ENTRADAS
            MenuItem("1", "Bruschetta Italiana", 15000, "Entradas", "Pan tostado con tomate, albahaca y mozzarella"),
            MenuItem("2", "Aros de Cebolla", 12000, "Entradas", "Crujientes aros de cebolla con salsa BBQ"),
            MenuItem("3", "Tabla de Quesos", 25000, "Entradas", "Selección de quesos nacionales e importados"),
            MenuItem("4", "Alitas Buffalo", 18000, "Entradas", "8 alitas picantes con salsa ranch"),
            MenuItem("5", "Nachos Supremos", 20000, "Entradas", "Con guacamole, pico de gallo y queso derretido"),
            MenuItem("49", "Tabla de Embutidos", 28000, "Entradas", "Jamón serrano, salami y quesos variados"),
            MenuItem("50", "Camarones al Ajillo", 22000, "Entradas", "Camarones frescos con ajo y mantequilla"),
            MenuItem("51", "Tabla de Crudités", 16000, "Entradas", "Vegetales frescos con dips caseros"),
            MenuItem("52", "Tabla Mixta Premium", 45000, "Entradas", "Quesos, embutidos, camarones y vegetales"),
            
            # PLATOS PRINCIPALES
            MenuItem("6", "Hamburguesa Gourmet", 28000, "Platos Principales", "Carne angus, queso brie, rúgula y tomate"),
            MenuItem("7", "Pizza Margherita", 24000, "Platos Principales", "Tomate, mozzarella, albahaca fresca"),
            MenuItem("8", "Pizza Pepperoni", 26000, "Platos Principales", "Pepperoni, mozzarella y orégano"),
            MenuItem("9", "Lasaña Boloñesa", 32000, "Platos Principales", "Pasta, carne, bechamel y queso gratinado"),
            MenuItem("10", "Salmón Grillado", 38000, "Platos Principales", "Con vegetales salteados y arroz"),
            MenuItem("11", "Churrasco Premium", 45000, "Platos Principales", "500g de carne con papas y ensalada"),
            MenuItem("12", "Pollo a la Parrilla", 25000, "Platos Principales", "Pechuga marinada con hierbas"),
            MenuItem("13", "Paella Valenciana", 35000, "Platos Principales", "Arroz con mariscos y pollo"),
            MenuItem("14", "Pasta Carbonara", 22000, "Platos Principales", "Pasta con bacon, crema y parmesano"),
            MenuItem("15", "Filete de Pescado", 30000, "Platos Principales", "Con salsa de limón y vegetales"),
            MenuItem("53", "Steak Argentino", 50000, "Platos Principales", "500g de carne de res premium"),
            MenuItem("54", "Costillas BBQ", 40000, "Platos Principales", "Costillas a la parrilla con salsa BBQ"),
            MenuItem("55", "Pechuga Rellena", 32000, "Platos Principales", "Pechuga rellena de jamón y queso"),
            MenuItem("56", "Camarones a la Criolla", 36000, "Platos Principales", "Camarones en salsa de cebolla y tomate"),
            MenuItem("57", "Robalo a la Sal", 42000, "Platos Principales", "Pescado entero cocido en sal marina"),
            MenuItem("58", "Fettuccine Alfredo", 26000, "Platos Principales", "Pasta fresca con salsa de crema y queso"),
            MenuItem("59", "Ravioles de Ricotta", 28000, "Platos Principales", "Ravioles caseros con salsa boloñesa"),
            
            # ENSALADAS
            MenuItem("16", "Ensalada César", 18000, "Ensaladas", "Lechuga, pollo, crutones y parmesano"),
            MenuItem("17", "Ensalada Griega", 16000, "Ensaladas", "Tomate, aceitunas, queso feta y orégano"),
            MenuItem("18", "Ensalada de Salmón", 22000, "Ensaladas", "Mix de verdes con salmón ahumado"),
            MenuItem("19", "Ensalada Tropical", 15000, "Ensaladas", "Frutas frescas con vinagreta de mango"),
            MenuItem("60", "Ensalada de Remolacha", 17000, "Ensaladas", "Remolacha, queso de cabra y nueces"),
            MenuItem("61", "Ensalada de Espinacas", 16000, "Ensaladas", "Espinacas frescas, fresas y almendras"),
            MenuItem("62", "Ensalada Caprese", 19000, "Ensaladas", "Tomate, mozzarella fresca y albahaca"),
            
            # BEBIDAS SIN ALCOHOL
            MenuItem("20", "Jugo Natural", 8000, "Bebidas", "Naranja, manzana, fresa o mango"),
            MenuItem("21", "Limonada Natural", 7000, "Bebidas", "Limón fresco con hierbabuena"),
            MenuItem("22", "Smoothie Tropical", 12000, "Bebidas", "Mango, piña y maracuyá"),
            MenuItem("23", "Coca-Cola", 5000, "Bebidas", "350ml - Regular o Zero"),
            MenuItem("24", "Agua con Gas", 4000, "Bebidas", "500ml - San Pellegrino"),
            MenuItem("25", "Café Americano", 6000, "Bebidas", "Café premium colombiano"),
            MenuItem("26", "Cappuccino", 8000, "Bebidas", "Espresso con leche vaporizada"),
            MenuItem("27", "Té Chai Latte", 9000, "Bebidas", "Té especiado con leche y canela"),
            MenuItem("63", "Batido de Fresa", 10000, "Bebidas", "Fresas frescas con leche y hielo"),
            MenuItem("64", "Horchata", 6000, "Bebidas", "Bebida tradicional con arroz"),
            MenuItem("65", "Frappé de Vainilla", 11000, "Bebidas", "Café congelado con crema"),
            MenuItem("66", "Té Helado", 7000, "Bebidas", "Té refrescante con limón"),
            
            # BEBIDAS CON ALCOHOL
            MenuItem("28", "Cerveza Nacional", 8000, "Bebidas Alcohólicas", "Poker, Águila o Club Colombia"),
            MenuItem("29", "Cerveza Importada", 12000, "Bebidas Alcohólicas", "Stella Artois, Corona o Heineken"),
            MenuItem("30", "Vino Tinto", 15000, "Bebidas Alcohólicas", "Copa de vino tinto reserva"),
            MenuItem("31", "Vino Blanco", 15000, "Bebidas Alcohólicas", "Copa de vino blanco seco"),
            MenuItem("32", "Mojito Clásico", 18000, "Bebidas Alcohólicas", "Ron, hierbabuena, limón y soda"),
            MenuItem("33", "Piña Colada", 20000, "Bebidas Alcohólicas", "Ron, piña, coco y hielo"),
            MenuItem("34", "Margarita", 19000, "Bebidas Alcohólicas", "Tequila, triple sec y limón"),
            MenuItem("67", "Daiquirí", 18000, "Bebidas Alcohólicas", "Ron blanco, limón y azúcar"),
            MenuItem("68", "Caipirinha", 16000, "Bebidas Alcohólicas", "Cachaça, limón fresco y azúcar"),
            MenuItem("69", "Cosmopolitan", 20000, "Bebidas Alcohólicas", "Vodka, naranja y cranberry"),
            MenuItem("70", "Cuba Libre", 15000, "Bebidas Alcohólicas", "Ron, Coca-Cola y limón"),
            
            # POSTRES
            MenuItem("35", "Tiramisú", 16000, "Postres", "Clásico postre italiano con café"),
            MenuItem("36", "Cheesecake de Frutos", 14000, "Postres", "Con salsa de frutos rojos"),
            MenuItem("37", "Brownie con Helado", 12000, "Postres", "Brownie caliente con helado de vainilla"),
            MenuItem("38", "Flan de Caramelo", 10000, "Postres", "Tradicional flan casero"),
            MenuItem("39", "Tres Leches", 11000, "Postres", "Torta húmeda con tres leches"),
            MenuItem("40", "Helado Artesanal", 8000, "Postres", "Vainilla, chocolate o fresa - 2 bolas"),
            MenuItem("41", "Torta de Chocolate", 13000, "Postres", "Torta húmeda con ganache"),
            MenuItem("42", "Crème Brûlée", 15000, "Postres", "Crema quemada con azúcar caramelizada"),
            MenuItem("71", "Mousse de Chocolate", 12000, "Postres", "Mousse ligero y delicioso"),
            MenuItem("72", "Pavlova", 14000, "Postres", "Merengue crujiente con frutas"),
            MenuItem("73", "Fresa con Champaña", 18000, "Postres", "Fresas frescas con champaña"),
            MenuItem("74", "Sorbet de Limón", 9000, "Postres", "Granizado refrescante de limón"),
            MenuItem("75", "Churros con Chocolate", 11000, "Postres", "Churros recién hechos con chocolate caliente"),
            
            # ACOMPAÑAMIENTOS
            MenuItem("43", "Papas Francesas", 8000, "Acompañamientos", "Papas crujientes con sal de mar"),
            MenuItem("44", "Papas Rústicas", 9000, "Acompañamientos", "Con romero y ajo"),
            MenuItem("45", "Arroz Blanco", 6000, "Acompañamientos", "Arroz jazmín cocido"),
            MenuItem("46", "Vegetales Grillados", 10000, "Acompañamientos", "Mix de vegetales de temporada"),
            MenuItem("47", "Pan de Ajo", 7000, "Acompañamientos", "Pan tostado con mantequilla y ajo"),
            MenuItem("48", "Ensalada Mixta", 8000, "Acompañamientos", "Lechuga, tomate y cebolla"),
            MenuItem("76", "Macarrones con Queso", 9000, "Acompañamientos", "Pasta con queso cheddar"),
            MenuItem("77", "Puré de Papa", 7000, "Acompañamientos", "Cremoso puré casero"),
            MenuItem("78", "Papas al Horno", 8000, "Acompañamientos", "Con cáscara, crema agria y cebollín"),
            MenuItem("79", "Plátano Maduro Frito", 6000, "Acompañamientos", "Plátano caramelizado"),
            MenuItem("80", "Yuca Frita", 8000, "Acompañamientos", "Yuca crujiente con salsa de ajo"),
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


class PedidoRestaurante:
    """Clase simplificada para la interfaz del restaurante"""
    
    def __init__(self):
        self.items = []
        self.numero = None
    
    def agregar_item(self, nombre: str, precio: float, cantidad: int):
        """Agregar item al carrito con nombre, precio y cantidad"""
        # Buscar si el item ya existe
        for item in self.items:
            if item['nombre'] == nombre:
                item['cantidad'] += cantidad
                return
        
        # Agregar nuevo item
        self.items.append({
            'nombre': nombre,
            'precio': precio,
            'cantidad': cantidad
        })
    
    def calcular_total(self) -> float:
        """Calcular el total del pedido"""
        return sum(item['precio'] * item['cantidad'] for item in self.items)
    
    def limpiar(self):
        """Limpiar el pedido"""
        self.items.clear()
