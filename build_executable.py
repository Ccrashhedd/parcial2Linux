#!/usr/bin/env python3
"""
Script para compilar Gestor de Productos como ejecutable Linux
Usa PyInstaller para crear un binario independiente
"""

import PyInstaller.__main__
import os
import sys

# Directorio base del proyecto
base_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(base_dir, 'src')

# Argumentos para PyInstaller
args = [
    'main.py',
    f'--name=GestorProductos',
    f'--distpath={os.path.join(base_dir, "dist")}',
    f'--workpath={os.path.join(base_dir, "build")}',
    f'--specpath={base_dir}',
    '--onefile',  # Crear un solo archivo ejecutable
    '--windowed',  # No mostrar ventana de consola
    f'--add-data={os.path.join(base_dir, "server_config.txt")}:.',
    f'--add-data={os.path.join(base_dir, "config.py")}:.',
    f'--add-data={src_dir}:src',
    '--hidden-import=psycopg2',
    '--hidden-import=PIL',
    '--hidden-import=gi',
    '--collect-all=gi',
    '--collect-all=cairo',
    '--collect-all=PIL',
    '--collect-all=psycopg2',
]

print("🔨 Compilando Gestor de Productos...")
print(f"   Directorio: {base_dir}")
print(f"   Nombre: GestorProductos")
print()

try:
    PyInstaller.__main__.run(args)
    print("\n✅ ¡Ejecutable creado exitosamente!")
    print(f"\n📍 Ubicación: {os.path.join(base_dir, 'dist/GestorProductos')}")
    print("\n💡 Uso:")
    print(f"   ./dist/GestorProductos")
    print(f"\n📝 Nota: Asegúrate de que 'server_config.txt' esté en la carpeta 'dist/'")
    
except Exception as e:
    print(f"\n❌ Error al compilar: {e}")
    sys.exit(1)
