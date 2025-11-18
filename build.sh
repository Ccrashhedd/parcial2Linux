#!/bin/bash
# Script to build a single-file executable using PyInstaller.
# Sistema POS Restaurante v2.1
# Actualizado: Noviembre 2025
# Usage: ./build.sh

set -e
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "Sistema POS Restaurante - Build Script"
echo "Versión 2.1 - Noviembre 2025"
echo "=========================================="
echo ""

# Verificar que Python3 esté instalado
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 no está instalado"
    exit 1
fi

echo "✓ Python version: $(python3 --version)"
echo ""

# Verificar dependencias
echo "Verificando dependencias..."
python3 -c "import psycopg2" 2>/dev/null && echo "✓ psycopg2 instalado" || echo "✗ psycopg2 falta"
python3 -c "import tkinter" 2>/dev/null && echo "✓ tkinter instalado" || echo "✗ tkinter falta"
echo ""

# Instalar/actualizar PyInstaller
echo "Instalando PyInstaller (si es necesario)..."
python3 -m pip install --upgrade pyinstaller
echo ""

# Limpiar builds anteriores
if [ -d "build" ]; then
    echo "Limpiando directorio build anterior..."
    rm -rf build
fi

if [ -d "dist" ]; then
    echo "Limpiando directorio dist anterior..."
    rm -rf dist
fi
echo ""

# Compilar usando el archivo .spec actualizado
echo "Compilando aplicación con PyInstaller..."
echo "Usando archivo de especificación: parcial2.spec"
python3 -m PyInstaller parcial2.spec --clean

echo ""
echo "=========================================="
echo "✓ Build completado exitosamente!"
echo "=========================================="
echo ""
echo "Ejecutable generado en: $SCRIPT_DIR/dist/parcial2"
echo ""

# Mostrar tamaño del ejecutable
if [ -f "$SCRIPT_DIR/dist/parcial2" ]; then
    SIZE=$(du -h "$SCRIPT_DIR/dist/parcial2" | cut -f1)
    echo "Tamaño del ejecutable: $SIZE"
    echo ""
    echo "Para ejecutar:"
    echo "  ./dist/parcial2"
fi

echo ""
echo "=========================================="
