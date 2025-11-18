#!/usr/bin/env python3
"""Script de prueba para verificar la base de datos"""

from modelo_restaurante import Menu

m = Menu()

print("✓ Tipos de comida:", m.obtener_tipos_comida())
print()

excepciones = m.obtener_excepciones_activas()
print(f"✓ Promociones activas: {len(excepciones)}")
for e in excepciones[:3]:
    print(f"  - {e['nombre']}: {e['descuento']}%")
print()

productos = m.obtener_productos_con_descuento()
print(f"✓ Productos con descuento: {len(productos)}")
for p in productos[:5]:
    print(f"  - {p['nombre']}: ${p['precio_original']:,.0f} → ${p['precio_especial']:,.0f}")
print()

menu_hoy = m.obtener_menu_del_dia(1)
print(f"✓ Productos en menú del lunes: {len(menu_hoy)}")
print()

menu_almuerzo = m.obtener_menu_del_dia(1, "Almuerzo")
print(f"✓ Almuerzos disponibles el lunes: {len(menu_almuerzo)}")
