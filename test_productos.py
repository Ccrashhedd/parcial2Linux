#!/usr/bin/env python3
"""
Script de prueba para verificar que se obtienen los productos de la BD
"""

from conexionDB import db_manager
from modelo_restaurante import Menu

print("=" * 70)
print("PRUEBA DE OBTENCIÓN DE PRODUCTOS")
print("=" * 70)

# Verificar conexión
print("\n1. Verificando conexión a la base de datos...")
if db_manager.verificar_conexion():
    print("   ✓ Conexión exitosa a PostgreSQL")
else:
    print("   ✗ No se pudo conectar a PostgreSQL")
    exit(1)

# Obtener productos directamente con query
print("\n2. Obteniendo productos con query directa...")
try:
    query = "SELECT idProducto, nombre, precio, imagen, descripcion FROM PRODUCTO ORDER BY nombre"
    productos = db_manager.ejecutar_query(query, fetch=True)
    print(f"   ✓ Query ejecutada: {len(productos) if productos else 0} productos encontrados")
    
    if productos:
        print("\n   Primeros 5 productos:")
        for i, prod in enumerate(productos[:5], 1):
            print(f"   {i}. {prod[1]} - ${prod[2]}")
    else:
        print("   ⚠ La tabla PRODUCTO está vacía")
except Exception as e:
    print(f"   ✗ Error en query: {e}")
    import traceback
    traceback.print_exc()

# Obtener productos usando la clase Menu
print("\n3. Obteniendo productos usando clase Menu...")
try:
    menu = Menu()
    productos_menu = menu.obtener_todos_productos()
    print(f"   ✓ Método obtener_todos_productos(): {len(productos_menu) if productos_menu else 0} productos")
    
    if productos_menu:
        print("\n   Primeros 5 productos:")
        for i, prod in enumerate(productos_menu[:5], 1):
            print(f"   {i}. {prod['nombre']} - ${prod['precio']}")
except Exception as e:
    print(f"   ✗ Error en Menu: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("FIN DE LA PRUEBA")
print("=" * 70)
