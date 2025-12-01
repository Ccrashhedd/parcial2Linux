#!/bin/bash

# ==========================================
# Script para ejecutar el Gestor de Productos
# Intenta ejecutar el binario compilado primero
# Si no existe, ejecuta con Python
# ==========================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}╔════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Gestor de Productos v1.0.0      ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════╝${NC}"
echo ""

# Verificar si existe el ejecutable compilado
if [ -f "./dist/GestorProductos" ]; then
    echo -e "${YELLOW}▶ Ejecutando versión compilada...${NC}"
    ./dist/GestorProductos
else
    # Si no existe el ejecutable, ejecutar con Python
    if command -v python3 &> /dev/null; then
        echo -e "${YELLOW}▶ Ejecutando con Python 3...${NC}"
        python3 main.py
    else
        echo -e "${RED}✗ Error: No se encontró Python 3${NC}"
        echo "Por favor instala Python 3:"
        echo "  sudo apt install python3 python3-pip"
        exit 1
    fi
fi
