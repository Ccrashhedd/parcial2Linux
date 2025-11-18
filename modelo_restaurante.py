"""
modelo_restaurante.py - Clases de modelo de datos para el sistema POS de restaurante
"""

from datetime import datetime
from typing import List, Dict, Optional
import uuid
from conexionDB import db_manager


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
    """Almacena y gestiona los items del menú desde la base de datos"""
    
    def __init__(self):
        self.items: Dict[str, MenuItem] = {}
        self._cargar_menu_desde_db()
    
    def _cargar_menu_desde_db(self):
        """Carga el menú desde la base de datos PostgreSQL"""
        try:
            # Obtener todos los productos de la base de datos
            query = """
                SELECT idProducto, nombre, precio, descripcion
                FROM PRODUCTO
                ORDER BY nombre
            """
            productos = db_manager.ejecutar_query(query, fetch=True)
            
            if productos:
                for producto in productos:
                    id_producto, nombre, precio, descripcion = producto
                    # Determinar categoría basada en el tipo de producto
                    categoria = self._obtener_categoria_por_nombre(nombre)
                    item = MenuItem(id_producto, nombre, float(precio), categoria, descripcion)
                    self.items[id_producto] = item
                print(f"✓ Cargados {len(self.items)} productos desde la base de datos")
            else:
                print("⚠ No se encontraron productos en la base de datos")
                self._cargar_menu_ejemplo()
        except Exception as e:
            print(f"✗ Error al cargar menú desde BD: {e}")
            print("  Cargando menú de ejemplo...")
            self._cargar_menu_ejemplo()
    
    def _obtener_categoria_por_nombre(self, nombre: str) -> str:
        """Determina la categoría del producto basándose en su nombre"""
        # Bebidas
        if any(palabra in nombre.lower() for palabra in ['café', 'té', 'jugo', 'coca', 'agua', 'cerveza', 'vino', 'mojito', 'limonada', 'batido', 'smoothie', 'cappuccino', 'horchata', 'frappé']):
            return "Bebidas"
        # Postres
        elif any(palabra in nombre.lower() for palabra in ['tiramisú', 'cheesecake', 'brownie', 'flan', 'leches', 'helado', 'torta', 'crème', 'mousse', 'pavlova', 'churros', 'sorbet']):
            return "Postres"
        # Ensaladas
        elif 'ensalada' in nombre.lower():
            return "Ensaladas"
        # Acompañamientos
        elif any(palabra in nombre.lower() for palabra in ['papas', 'arroz', 'vegetales', 'pan', 'macarrones', 'puré', 'plátano', 'yuca']):
            return "Acompañamientos"
        # Por defecto: Platos Principales
        else:
            return "Platos Principales"
    
    def _cargar_menu_ejemplo(self):
        """Carga un menú completo de restaurante premium (fallback)"""
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
    
    def crear_producto(self, nombre: str, precio: float, tipo: str, descripcion: str = "", imagen: str = "") -> str:
        """
        Crea un nuevo producto en la base de datos
        
        Returns:
            ID del producto creado o None si falla
        """
        try:
            from datetime import datetime
            
            # Generar ID único para el producto
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            id_producto = f"PROD{timestamp}{nombre[:10].replace(' ', '')}"
            
            # Obtener el ID del tipo de comida
            query_tipo = "SELECT idTipo FROM TIPO_COMIDA WHERE nombre = %s"
            resultado = db_manager.ejecutar_query_uno(query_tipo, (tipo,))
            
            if not resultado:
                print(f"✗ Tipo de comida '{tipo}' no encontrado")
                return None
            
            id_tipo = resultado[0]
            
            # Insertar producto
            query_producto = """
                INSERT INTO PRODUCTO (idProducto, nombre, precio, imagen, descripcion)
                VALUES (%s, %s, %s, %s, %s)
            """
            db_manager.ejecutar_query(query_producto, (id_producto, nombre, precio, imagen, descripcion), fetch=False)
            
            # Agregar a todos los días del menú (disponible siempre)
            query_menu = """
                INSERT INTO MENU_PRODUCTO (idProducto, idTipo, idDiaMenu, activo)
                SELECT %s, %s, idDiaMenu, TRUE
                FROM MENU_DIA
            """
            db_manager.ejecutar_query(query_menu, (id_producto, id_tipo), fetch=False)
            
            print(f"✓ Producto '{nombre}' creado con ID: {id_producto}")
            return id_producto
            
        except Exception as e:
            print(f"✗ Error al crear producto: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def actualizar_producto(self, id_producto: str, nombre: str, precio: float, descripcion: str = "", imagen: str = "") -> bool:
        """
        Actualiza un producto existente en la base de datos
        
        Returns:
            True si se actualizó correctamente, False si falla
        """
        try:
            query = """
                UPDATE PRODUCTO
                SET nombre = %s, precio = %s, descripcion = %s, imagen = %s
                WHERE idProducto = %s
            """
            db_manager.ejecutar_query(query, (nombre, precio, descripcion, imagen, id_producto), fetch=False)
            
            print(f"✓ Producto {id_producto} actualizado")
            return True
            
        except Exception as e:
            print(f"✗ Error al actualizar producto: {e}")
            return False
    
    def eliminar_producto(self, id_producto: str) -> bool:
        """
        Elimina un producto de la base de datos
        
        Returns:
            True si se eliminó correctamente, False si falla
        """
        try:
            # Primero eliminar referencias en MENU_PRODUCTO
            query_menu = "DELETE FROM MENU_PRODUCTO WHERE idProducto = %s"
            db_manager.ejecutar_query(query_menu, (id_producto,), fetch=False)
            
            # Eliminar referencias en EXCEPCION_PRODUCTO si existen
            query_exc = "DELETE FROM EXCEPCION_PRODUCTO WHERE idProducto = %s"
            db_manager.ejecutar_query(query_exc, (id_producto,), fetch=False)
            
            # Finalmente eliminar el producto
            query_prod = "DELETE FROM PRODUCTO WHERE idProducto = %s"
            db_manager.ejecutar_query(query_prod, (id_producto,), fetch=False)
            
            print(f"✓ Producto {id_producto} eliminado")
            return True
            
        except Exception as e:
            print(f"✗ Error al eliminar producto: {e}")
            return False
    
    def obtener_todos_productos(self) -> List[Dict]:
        """
        Obtiene TODOS los productos de la base de datos sin límite
        
        Returns:
            Lista de diccionarios con todos los productos
        """
        try:
            # Query sin LIMIT para traer TODOS los productos
            query = """
                SELECT idProducto, nombre, precio, imagen, descripcion
                FROM PRODUCTO
                ORDER BY nombre ASC
            """
            productos = db_manager.ejecutar_query(query, fetch=True)
            
            resultado = []
            if productos:
                print(f"✓ Se obtuvieron {len(productos)} productos de la base de datos")
                for prod in productos:
                    resultado.append({
                        'id_producto': prod[0],
                        'nombre': prod[1],
                        'precio': float(prod[2]),
                        'imagen': prod[3],
                        'descripcion': prod[4]
                    })
            else:
                print("⚠ No se encontraron productos en la base de datos")
            
            return resultado
            
        except Exception as e:
            print(f"✗ Error al obtener productos: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def obtener_tipo_producto(self, id_producto: str) -> str:
        """
        Obtiene el tipo de comida de un producto
        
        Returns:
            Nombre del tipo de comida o None
        """
        try:
            query = """
                SELECT tc.nombre
                FROM MENU_PRODUCTO mp
                JOIN TIPO_COMIDA tc ON mp.idTipo = tc.idTipo
                WHERE mp.idProducto = %s
                LIMIT 1
            """
            resultado = db_manager.ejecutar_query_uno(query, (id_producto,))
            
            return resultado[0] if resultado else None
            
        except Exception as e:
            print(f"✗ Error al obtener tipo de producto: {e}")
            return None
    
    def obtener_productos_en_menu_dia(self, dia_id: int) -> List[Dict]:
        """
        Obtiene los productos asignados a un día específico
        
        Returns:
            Lista de productos del menú del día
        """
        try:
            query = """
                SELECT p.idProducto, p.nombre, p.precio, tc.nombre as tipo
                FROM MENU_PRODUCTO mp
                JOIN PRODUCTO p ON mp.idProducto = p.idProducto
                JOIN TIPO_COMIDA tc ON mp.idTipo = tc.idTipo
                WHERE mp.idDiaMenu = %s AND mp.activo = TRUE
                ORDER BY tc.idTipo, p.nombre
            """
            productos = db_manager.ejecutar_query(query, (dia_id,), fetch=True)
            
            resultado = []
            if productos:
                for prod in productos:
                    resultado.append({
                        'id_producto': prod[0],
                        'nombre': prod[1],
                        'precio': float(prod[2]),
                        'tipo': prod[3]
                    })
            
            return resultado
            
        except Exception as e:
            print(f"✗ Error al obtener productos del menú del día: {e}")
            return []
    
    def agregar_producto_a_menu_dia(self, id_producto: str, tipo: str, dia_id: int) -> bool:
        """
        Agrega un producto al menú de un día específico
        
        Returns:
            True si se agregó correctamente
        """
        try:
            # Obtener ID del tipo
            query_tipo = "SELECT idTipo FROM TIPO_COMIDA WHERE nombre = %s"
            resultado = db_manager.ejecutar_query_uno(query_tipo, (tipo,))
            
            if not resultado:
                print(f"✗ Tipo '{tipo}' no encontrado")
                return False
            
            id_tipo = resultado[0]
            
            # Verificar si ya existe
            query_existe = """
                SELECT 1 FROM MENU_PRODUCTO 
                WHERE idProducto = %s AND idTipo = %s AND idDiaMenu = %s
            """
            existe = db_manager.ejecutar_query_uno(query_existe, (id_producto, id_tipo, dia_id))
            
            if existe:
                # Actualizar a activo si ya existe
                query_update = """
                    UPDATE MENU_PRODUCTO 
                    SET activo = TRUE
                    WHERE idProducto = %s AND idTipo = %s AND idDiaMenu = %s
                """
                db_manager.ejecutar_query(query_update, (id_producto, id_tipo, dia_id), fetch=False)
            else:
                # Insertar nuevo registro
                query_insert = """
                    INSERT INTO MENU_PRODUCTO (idProducto, idTipo, idDiaMenu, activo)
                    VALUES (%s, %s, %s, TRUE)
                """
                db_manager.ejecutar_query(query_insert, (id_producto, id_tipo, dia_id), fetch=False)
            
            print(f"✓ Producto agregado al menú del día {dia_id}")
            return True
            
        except Exception as e:
            print(f"✗ Error al agregar producto al menú: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def quitar_producto_de_menu_dia(self, id_producto: str, dia_id: int) -> bool:
        """
        Quita un producto del menú de un día específico
        
        Returns:
            True si se quitó correctamente
        """
        try:
            query = """
                DELETE FROM MENU_PRODUCTO
                WHERE idProducto = %s AND idDiaMenu = %s
            """
            db_manager.ejecutar_query(query, (id_producto, dia_id), fetch=False)
            
            print(f"✓ Producto quitado del menú del día {dia_id}")
            return True
            
        except Exception as e:
            print(f"✗ Error al quitar producto del menú: {e}")
            return False
    
    def obtener_menu_del_dia(self, dia_semana: int = None, tipo_comida: str = None) -> List[Dict]:
        """
        Obtiene el menú del día desde la base de datos
        
        Args:
            dia_semana: 1=Lunes, 2=Martes, ..., 7=Domingo (None = día actual)
            tipo_comida: Nombre del tipo ("Desayuno", "Almuerzo", etc.) (None = todos)
        
        Returns:
            Lista de diccionarios con productos del menú del día
        """
        try:
            # Si no se especifica día, usar el día actual
            if dia_semana is None:
                from datetime import datetime
                dia_semana = datetime.now().isoweekday()  # 1=Lunes, 7=Domingo
            
            # Construir query con JOIN a TIPO_COMIDA para obtener el nombre
            query = """
                SELECT DISTINCT p.idProducto, p.nombre, p.precio, p.descripcion, tc.nombre as tipo, tc.idTipo
                FROM PRODUCTO p
                INNER JOIN MENU_PRODUCTO mp ON p.idProducto = mp.idProducto
                INNER JOIN TIPO_COMIDA tc ON mp.idTipo = tc.idTipo
                WHERE mp.idDiaMenu = %s AND mp.activo = TRUE
            """
            params = [dia_semana]
            
            if tipo_comida is not None and tipo_comida != "Todos":
                query += " AND tc.nombre = %s"
                params.append(tipo_comida)
            
            query += " ORDER BY tc.idTipo, p.nombre"
            
            productos = db_manager.ejecutar_query(query, tuple(params), fetch=True)
            
            menu_items = []
            if productos:
                for producto in productos:
                    id_producto, nombre, precio, descripcion, tipo, id_tipo = producto
                    menu_items.append({
                        'id_producto': id_producto,
                        'nombre': nombre,
                        'precio': float(precio),
                        'descripcion': descripcion,
                        'tipo': tipo
                    })
            
            return menu_items
        except Exception as e:
            print(f"✗ Error al obtener menú del día: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def obtener_tipos_comida(self) -> List[str]:
        """Obtiene los nombres de tipos de comida desde la base de datos"""
        try:
            query = "SELECT nombre FROM TIPO_COMIDA ORDER BY idTipo"
            tipos = db_manager.ejecutar_query(query, fetch=True)
            
            return [tipo[0] for tipo in tipos] if tipos else []
        except Exception as e:
            print(f"✗ Error al obtener tipos de comida: {e}")
            return ["Desayuno", "Almuerzo", "Cena", "Bebidas", "Postres"]
    
    def verificar_login(self, usuario: str, contrasena: str) -> Optional[Dict]:
        """
        Verifica las credenciales de login desde la base de datos
        
        Returns:
            Diccionario con datos del usuario si login exitoso, None si falla
        """
        try:
            query = """
                SELECT idUsuario, usuario, nombre
                FROM USUARIO
                WHERE usuario = %s AND contrasen = %s
            """
            resultado = db_manager.ejecutar_query_uno(query, (usuario, contrasena))
            
            if resultado:
                return {
                    "id": resultado[0],
                    "usuario": resultado[1],
                    "nombre": resultado[2]
                }
            return None
        except Exception as e:
            print(f"✗ Error al verificar login: {e}")
            # Fallback para desarrollo
            if usuario == "admin" and contrasena == "123":
                return {"id": "USR001", "usuario": "admin", "nombre": "Administrador"}
            return None
    
    def obtener_excepciones_activas(self, fecha: str = None) -> List[Dict]:
        """
        Obtiene las excepciones de menú activas para una fecha
        
        Args:
            fecha: Fecha en formato YYYY-MM-DD (None = hoy)
        
        Returns:
            Lista de diccionarios con excepciones activas
        """
        try:
            if fecha is None:
                from datetime import datetime
                fecha = datetime.now().strftime('%Y-%m-%d')
            
            query = """
                SELECT idExcepcion, nombre, descripcion, descuento_porcentaje
                FROM MENU_EXCEPCION
                WHERE activo = TRUE
                  AND fecha_inicio <= %s
                  AND fecha_fin >= %s
                ORDER BY descuento_porcentaje DESC
            """
            excepciones = db_manager.ejecutar_query(query, (fecha, fecha), fetch=True)
            
            resultado = []
            if excepciones:
                for exc in excepciones:
                    resultado.append({
                        "id": exc[0],
                        "nombre": exc[1],
                        "descripcion": exc[2],
                        "descuento": float(exc[3])
                    })
            
            return resultado
        except Exception as e:
            print(f"✗ Error al obtener excepciones: {e}")
            return []
    
    def obtener_productos_con_descuento(self, id_excepcion: int = None) -> List[Dict]:
        """
        Obtiene productos con sus precios especiales de promoción
        
        Args:
            id_excepcion: ID de la excepción (None = todas las activas hoy)
        
        Returns:
            Lista de productos con precio original y precio especial
        """
        try:
            from datetime import datetime
            fecha_hoy = datetime.now().strftime('%Y-%m-%d')
            
            if id_excepcion:
                query = """
                    SELECT p.idProducto, p.nombre, p.precio, 
                           ep.precio_especial, me.descuento_porcentaje, me.nombre,
                           tc.nombre as tipo
                    FROM PRODUCTO p
                    INNER JOIN EXCEPCION_PRODUCTO ep ON p.idProducto = ep.idProducto
                    INNER JOIN MENU_EXCEPCION me ON ep.idExcepcion = me.idExcepcion
                    LEFT JOIN MENU_PRODUCTO mp ON p.idProducto = mp.idProducto
                    LEFT JOIN TIPO_COMIDA tc ON mp.idTipo = tc.idTipo
                    WHERE me.idExcepcion = %s
                      AND me.activo = TRUE
                      AND me.fecha_inicio <= %s
                      AND me.fecha_fin >= %s
                    GROUP BY p.idProducto, p.nombre, p.precio, ep.precio_especial, 
                             me.descuento_porcentaje, me.nombre, tc.nombre
                    ORDER BY p.nombre
                """
                params = (id_excepcion, fecha_hoy, fecha_hoy)
            else:
                query = """
                    SELECT p.idProducto, p.nombre, p.precio, 
                           ep.precio_especial, me.descuento_porcentaje, me.nombre,
                           tc.nombre as tipo
                    FROM PRODUCTO p
                    INNER JOIN EXCEPCION_PRODUCTO ep ON p.idProducto = ep.idProducto
                    INNER JOIN MENU_EXCEPCION me ON ep.idExcepcion = me.idExcepcion
                    LEFT JOIN MENU_PRODUCTO mp ON p.idProducto = mp.idProducto
                    LEFT JOIN TIPO_COMIDA tc ON mp.idTipo = tc.idTipo
                    WHERE me.activo = TRUE
                      AND me.fecha_inicio <= %s
                      AND me.fecha_fin >= %s
                    GROUP BY p.idProducto, p.nombre, p.precio, ep.precio_especial,
                             me.descuento_porcentaje, me.nombre, tc.nombre
                    ORDER BY me.descuento_porcentaje DESC, p.nombre
                """
                params = (fecha_hoy, fecha_hoy)
            
            productos = db_manager.ejecutar_query(query, params, fetch=True)
            
            resultado = []
            if productos:
                for prod in productos:
                    resultado.append({
                        "id_producto": prod[0],
                        "nombre": prod[1],
                        "precio_original": float(prod[2]),
                        "precio_especial": float(prod[3]),
                        "descuento": float(prod[4]),
                        "promocion": prod[5],
                        "tipo": prod[6] if prod[6] else "General"
                    })
            
            return resultado
        except Exception as e:
            print(f"✗ Error al obtener productos con descuento: {e}")
            return []
    
    def obtener_precio_producto(self, id_producto: str) -> Dict:
        """
        Obtiene el precio actual de un producto (con descuento si aplica)
        
        Returns:
            Dict con precio_original, precio_final, tiene_descuento, descuento_porcentaje
        """
        try:
            from datetime import datetime
            fecha_hoy = datetime.now().strftime('%Y-%m-%d')
            
            # Verificar si tiene descuento activo
            query = """
                SELECT p.precio, ep.precio_especial, me.descuento_porcentaje, me.nombre
                FROM PRODUCTO p
                LEFT JOIN EXCEPCION_PRODUCTO ep ON p.idProducto = ep.idProducto
                LEFT JOIN MENU_EXCEPCION me ON ep.idExcepcion = me.idExcepcion
                    AND me.activo = TRUE
                    AND me.fecha_inicio <= %s
                    AND me.fecha_fin >= %s
                WHERE p.idProducto = %s
                ORDER BY me.descuento_porcentaje DESC
                LIMIT 1
            """
            resultado = db_manager.ejecutar_query_uno(query, (fecha_hoy, fecha_hoy, id_producto))
            
            if resultado:
                precio_original = float(resultado[0])
                precio_especial = float(resultado[1]) if resultado[1] else None
                descuento = float(resultado[2]) if resultado[2] else 0
                promocion = resultado[3] if resultado[3] else None
                
                return {
                    "precio_original": precio_original,
                    "precio_final": precio_especial if precio_especial else precio_original,
                    "tiene_descuento": precio_especial is not None,
                    "descuento_porcentaje": descuento,
                    "promocion": promocion
                }
            
            return {
                "precio_original": 0,
                "precio_final": 0,
                "tiene_descuento": False,
                "descuento_porcentaje": 0,
                "promocion": None
            }
        except Exception as e:
            print(f"✗ Error al obtener precio: {e}")
            return {
                "precio_original": 0,
                "precio_final": 0,
                "tiene_descuento": False,
                "descuento_porcentaje": 0,
                "promocion": None
            }


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
