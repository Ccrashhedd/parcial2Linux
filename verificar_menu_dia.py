#!/usr/bin/env python3
"""
Script para verificar que los productos se guarden correctamente en el menú por día
"""

from conexionDB import db_manager

def verificar_productos_por_dia():
    """Muestra los productos asignados a cada día de la semana"""
    
    dias = {
        1: "Lunes",
        2: "Martes", 
        3: "Miércoles",
        4: "Jueves",
        5: "Viernes",
        6: "Sábado",
        7: "Domingo"
    }
    
    print("\n" + "="*70)
    print("PRODUCTOS EN EL MENÚ POR DÍA DE LA SEMANA")
    print("="*70)
    
    for dia_id, dia_nombre in dias.items():
        query = """
            SELECT p.nombre, tc.nombre as tipo, p.precio
            FROM MENU_PRODUCTO mp
            JOIN PRODUCTO p ON mp.idProducto = p.idProducto
            JOIN TIPO_COMIDA tc ON mp.idTipo = tc.idTipo
            WHERE mp.idDiaMenu = %s AND mp.activo = TRUE
            ORDER BY tc.idTipo, p.nombre
        """
        
        productos = db_manager.ejecutar_query(query, (dia_id,), fetch=True)
        
        print(f"\n📅 {dia_nombre.upper()}")
        print("-" * 70)
        
        if productos:
            # Agrupar por tipo
            tipo_actual = None
            contador = 0
            
            for prod in productos:
                nombre, tipo, precio = prod
                
                if tipo != tipo_actual:
                    if tipo_actual:
                        print()
                    print(f"\n  🍽️  {tipo}:")
                    tipo_actual = tipo
                    contador = 0
                
                contador += 1
                print(f"    {contador}. {nombre} - ${precio:.2f}")
            
            print(f"\n  ✓ Total: {len(productos)} productos")
        else:
            print("  ⚠️  No hay productos en este día")
    
    print("\n" + "="*70 + "\n")

def contar_total_productos():
    """Cuenta el total de productos en la base de datos"""
    query = "SELECT COUNT(*) FROM PRODUCTO"
    resultado = db_manager.ejecutar_query_uno(query)
    
    print(f"📦 Total de productos en la base de datos: {resultado[0]}")

def verificar_integridad():
    """Verifica que no haya productos sin tipo"""
    query = """
        SELECT p.idProducto, p.nombre
        FROM PRODUCTO p
        LEFT JOIN MENU_PRODUCTO mp ON p.idProducto = mp.idProducto
        WHERE mp.idProducto IS NULL
    """
    
    productos_sin_menu = db_manager.ejecutar_query(query, fetch=True)
    
    if productos_sin_menu:
        print(f"\n⚠️  Advertencia: {len(productos_sin_menu)} productos no tienen tipo asignado:")
        for prod in productos_sin_menu:
            print(f"  - {prod[1]} (ID: {prod[0]})")
    else:
        print("\n✓ Todos los productos tienen tipo asignado")

if __name__ == "__main__":
    try:
        contar_total_productos()
        verificar_integridad()
        verificar_productos_por_dia()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
