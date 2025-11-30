#!/bin/bash

# Script de instalación de dependencias

echo "========================================="
echo "Instalador - Gestor de Productos"
echo "========================================="
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Verificar si pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}Error: pip3 no está instalado${NC}"
    echo "Instálalo con: sudo apt install python3-pip"
    exit 1
fi

echo -e "${YELLOW}Instalando dependencias de Python...${NC}"
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencias instaladas exitosamente${NC}"
else
    echo -e "${RED}Error al instalar dependencias${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}Configurando base de datos...${NC}"
chmod +x database/crear_bd.sh

echo ""
echo -e "${GREEN}✓ Instalación completada${NC}"
echo ""
echo -e "${YELLOW}Próximos pasos:${NC}"
echo "1. Crear la base de datos: ./database/crear_bd.sh"
echo "2. Ejecutar la aplicación: python3 main.py"
echo ""
