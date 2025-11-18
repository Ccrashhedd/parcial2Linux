#!/bin/bash
# Script de instalación completa del sistema POS con PostgreSQL

set -e  # Salir si hay algún error

echo "============================================================"
echo "INSTALACIÓN COMPLETA - SISTEMA POS RESTAURANTE + PostgreSQL"
echo "============================================================"
echo ""

# Verificar si se está ejecutando como root
if [ "$EUID" -eq 0 ]; then 
    echo "⚠️  No ejecutes este script como root"
    exit 1
fi

# 1. Instalar dependencias del sistema
echo "Paso 1: Instalando dependencias del sistema..."
echo "Se solicitará tu contraseña de sudo"
sudo dnf install -y python3 python3-pip python3-tkinter postgresql-server postgresql-contrib || {
    echo "✗ Error al instalar dependencias"
    exit 1
}
echo "✓ Dependencias instaladas"
echo ""

# 2. Inicializar PostgreSQL si no está inicializado
echo "Paso 2: Configurando PostgreSQL..."
if [ ! -d "/var/lib/pgsql/data/base" ]; then
    sudo postgresql-setup --initdb
fi

# Iniciar y habilitar PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql
echo "✓ PostgreSQL iniciado"
echo ""

# 3. Configurar autenticación de PostgreSQL
echo "Paso 3: Configurando autenticación..."
sudo cp /var/lib/pgsql/data/pg_hba.conf /var/lib/pgsql/data/pg_hba.conf.backup
sudo sed -i 's/peer/md5/g; s/ident/md5/g' /var/lib/pgsql/data/pg_hba.conf
sudo systemctl restart postgresql
sleep 2
echo "✓ Autenticación configurada"
echo ""

# 4. Configurar contraseña de PostgreSQL
echo "Paso 4: Configurando contraseña de PostgreSQL..."
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';" 2>/dev/null || {
    echo "⚠️  Configurando contraseña manualmente..."
    echo "postgres" | sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';"
}
echo "✓ Contraseña: postgres"
echo ""

# 5. Instalar dependencias de Python
echo "Paso 5: Instalando dependencias de Python..."
pip3 install --user psycopg2-binary pyinstaller 2>&1 | grep -i "successfully\|already" || true
echo "✓ Dependencias de Python instaladas"
echo ""

# 6. Crear base de datos
echo "Paso 6: Creando base de datos 'parcial2'..."
python3 setup_database.py || {
    echo "✗ Error al crear la base de datos"
    echo ""
    echo "Solución manual:"
    echo "1. Ejecuta: sudo -u postgres psql"
    echo "2. Luego: ALTER USER postgres WITH PASSWORD 'postgres';"
    echo "3. Escribe: \\q"
    echo "4. Ejecuta: python3 setup_database.py"
    exit 1
}
echo ""

echo "============================================================"
echo "✓ INSTALACIÓN COMPLETADA EXITOSAMENTE"
echo "============================================================"
echo ""
echo "📊 Base de Datos PostgreSQL:"
echo "   - Host: localhost:5432"
echo "   - Base de datos: parcial2"
echo "   - Usuario: postgres"
echo "   - Contraseña: postgres"
echo ""
echo "👤 Login de la aplicación:"
echo "   - Usuario: admin"
echo "   - Contraseña: 123"
echo ""
echo "🚀 Para ejecutar:"
echo "   python3 main.py"
echo ""
echo "📦 Para compilar ejecutable:"
echo "   ./build.sh"
echo ""
