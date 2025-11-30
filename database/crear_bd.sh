#!/bin/bash

# Script para crear la base de datos PostgreSQL
# Este script debe ejecutarse con permisos de usuario PostgreSQL

echo "========================================="
echo "Creador de Base de Datos - Gestor Productos"
echo "========================================="
echo ""

# Colores para salida
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # Sin color

# Verificar si PostgreSQL está instalado
if ! command -v psql &> /dev/null; then
    echo -e "${RED}Error: PostgreSQL no está instalado.${NC}"
    echo "Instálalo con: sudo apt install postgresql postgresql-contrib"
    exit 1
fi

# Preguntar por credenciales
echo -e "${YELLOW}Ingresa los datos de conexión a PostgreSQL:${NC}"
read -p "Usuario PostgreSQL (default: postgres): " DB_USER
DB_USER=${DB_USER:-postgres}

read -sp "Contraseña de PostgreSQL: " DB_PASSWORD
echo ""

# Exportar la contraseña para psql
export PGPASSWORD=$DB_PASSWORD

# Obtener la ruta del archivo SQL
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SQL_FILE="$SCRIPT_DIR/schema.sql"

if [ ! -f "$SQL_FILE" ]; then
    echo -e "${RED}Error: No se encontró el archivo $SQL_FILE${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}Conectando a PostgreSQL...${NC}"

# Ejecutar el archivo SQL
psql -U "$DB_USER" -h localhost -f "$SQL_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ Base de datos creada exitosamente${NC}"
    echo -e "${GREEN}✓ Tablas creadas${NC}"
    echo -e "${GREEN}✓ Datos de ejemplo insertados${NC}"
    echo ""
    echo -e "${YELLOW}Información de conexión:${NC}"
    echo "Host: localhost"
    echo "Base de datos: gestor_productos"
    echo "Usuario: $DB_USER"
    echo ""
else
    echo -e "${RED}Error: No se pudo crear la base de datos${NC}"
    exit 1
fi

# Deshacer la exportación
unset PGPASSWORD
