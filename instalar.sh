#!/bin/bash

# ==========================================
# Instalador del Gestor de Productos Linux
# Instala todas las dependencias automáticamente
# ==========================================

set -e  # Salir si hay error

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Banner
echo -e "${BLUE}"
echo "╔════════════════════════════════════════╗"
echo "║  INSTALADOR GESTOR DE PRODUCTOS v1.0  ║"
echo "║          Sistema Linux                 ║"
echo "╚════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Detectar distribución Linux
if [ -f /etc/os-release ]; then
    . /etc/os-release
    DISTRO=$ID
else
    echo -e "${RED}✗ No se pudo detectar la distribución Linux${NC}"
    exit 1
fi

echo -e "${YELLOW}📦 Distribución detectada: $PRETTY_NAME${NC}"
echo ""

# ==========================================
# INSTALAR DEPENDENCIAS DEL SISTEMA
# ==========================================

echo -e "${BLUE}▶ Instalando dependencias del sistema...${NC}"

case "$DISTRO" in
    ubuntu|debian)
        echo -e "${YELLOW}  → Actualizando repositorios...${NC}"
        sudo apt-get update -qq
        
        echo -e "${YELLOW}  → Instalando paquetes...${NC}"
        sudo apt-get install -y \
            python3 \
            python3-pip \
            python3-dev \
            python3-gi \
            python3-gi-cairo \
            gir1.2-gtk-3.0 \
            libgtk-3-0 \
            libcairo2 \
            libcairo2-dev \
            libpango-1.0-0 \
            libpango-cairo-1.0-0 \
            libpangoft2-1.0-0 \
            libglib2.0-0 \
            libglib2.0-dev \
            libffi-dev \
            libssl-dev \
            postgresql-client \
            > /dev/null 2>&1
        ;;
        
    fedora)
        echo -e "${YELLOW}  → Instalando paquetes con dnf...${NC}"
        sudo dnf install -y \
            python3 \
            python3-pip \
            python3-devel \
            python3-gobject \
            gtk3 \
            cairo \
            cairo-devel \
            pango \
            pango-devel \
            glib2 \
            glib2-devel \
            libffi-devel \
            openssl-devel \
            postgresql \
            > /dev/null 2>&1
        ;;
        
    arch)
        echo -e "${YELLOW}  → Instalando paquetes con pacman...${NC}"
        sudo pacman -S --noconfirm \
            python \
            python-pip \
            python-gobject \
            gtk3 \
            cairo \
            pango \
            glib2 \
            libffi \
            openssl \
            postgresql-libs \
            > /dev/null 2>&1
        ;;
        
    *)
        echo -e "${RED}✗ Distribución no soportada: $DISTRO${NC}"
        echo "Por favor instala manualmente:"
        echo "  - Python 3.8+"
        echo "  - GTK3"
        echo "  - Cairo"
        echo "  - PostgreSQL Client"
        exit 1
        ;;
esac

echo -e "${GREEN}✓ Dependencias del sistema instaladas${NC}"
echo ""

# ==========================================
# INSTALAR DEPENDENCIAS DE PYTHON
# ==========================================

echo -e "${BLUE}▶ Instalando dependencias de Python...${NC}"

# Actualizar pip
echo -e "${YELLOW}  → Actualizando pip...${NC}"
python3 -m pip install --upgrade pip setuptools wheel -q > /dev/null 2>&1

# Instalar requirements
echo -e "${YELLOW}  → Instalando paquetes Python...${NC}"
cd "$SCRIPT_DIR"

if [ -f requirements.txt ]; then
    python3 -m pip install -r requirements.txt -q > /dev/null 2>&1
else
    echo -e "${RED}✗ No se encontró requirements.txt${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Dependencias de Python instaladas${NC}"
echo ""

# ==========================================
# VERIFICAR INSTALACIÓN
# ==========================================

echo -e "${BLUE}▶ Verificando instalación...${NC}"

# Verificar Python
python3_version=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${YELLOW}  → Python: $python3_version${NC}"

# Verificar módulos Python
for module in psycopg2 PIL gi cairo; do
    if python3 -c "import $module" 2>/dev/null; then
        echo -e "${GREEN}  ✓ Módulo $module${NC}"
    else
        echo -e "${RED}  ✗ Falta módulo $module${NC}"
    fi
done

echo ""

# ==========================================
# HACER EJECUTABLES
# ==========================================

echo -e "${BLUE}▶ Configurando permisos...${NC}"

chmod +x "$SCRIPT_DIR/main.py" 2>/dev/null || true
chmod +x "$SCRIPT_DIR/ejecutar.sh" 2>/dev/null || true

echo -e "${GREEN}✓ Permisos configurados${NC}"
echo ""

# ==========================================
# VERIFICAR CONFIGURACIÓN
# ==========================================

echo -e "${BLUE}▶ Verificando configuración...${NC}"

if [ ! -f "$SCRIPT_DIR/server_config.txt" ]; then
    echo -e "${YELLOW}  ! No se encontró server_config.txt${NC}"
    echo -e "${YELLOW}    Creando configuración por defecto...${NC}"
    
    cat > "$SCRIPT_DIR/server_config.txt" << 'EOF'
# Configuración del servidor remoto
# Si cambias de red, actualiza el hostname o IP aquí

# IP o hostname del servidor Windows
SERVER_IP=WIN-E6SQ6ALCVS5

# Usuario PostgreSQL en el servidor
SERVER_USER=postgres

# Contraseña PostgreSQL en el servidor
SERVER_PASSWORD=postgres123

# Puerto PostgreSQL (por defecto 5432)
SERVER_PORT=5432
EOF
    echo -e "${GREEN}✓ server_config.txt creado${NC}"
else
    echo -e "${GREEN}✓ server_config.txt encontrado${NC}"
fi

echo ""

# ==========================================
# CREAR ACCESO DIRECTO (DESKTOP)
# ==========================================

echo -e "${BLUE}▶ Creando acceso directo en el escritorio...${NC}"

DESKTOP_FILE="/home/$(whoami)/.local/share/applications/GestorProductos.desktop"
mkdir -p "/home/$(whoami)/.local/share/applications"

cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Gestor de Productos
Comment=Aplicación para gestionar productos con PostgreSQL
Exec=$SCRIPT_DIR/ejecutar.sh
Icon=document-properties
Terminal=false
Categories=Utility;Office;
Path=$SCRIPT_DIR
EOF

chmod +x "$DESKTOP_FILE"
echo -e "${GREEN}✓ Acceso directo creado${NC}"

echo ""

# ==========================================
# RESUMEN FINAL
# ==========================================

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   ✓ INSTALACIÓN COMPLETADA            ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

echo "📍 Ubicación: $SCRIPT_DIR"
echo ""

echo -e "${YELLOW}▶ Para ejecutar la aplicación:${NC}"
echo ""
echo -e "  ${BLUE}Opción 1: Con el script${NC}"
echo "  $ cd $SCRIPT_DIR"
echo "  $ ./ejecutar.sh"
echo ""
echo -e "  ${BLUE}Opción 2: Directamente con Python${NC}"
echo "  $ cd $SCRIPT_DIR"
echo "  $ python3 main.py"
echo ""
echo -e "  ${BLUE}Opción 3: Desde el menú de aplicaciones${NC}"
echo "  Busca 'Gestor de Productos' en tu menú"
echo ""

echo -e "${YELLOW}⚙️  Configuración:${NC}"
echo "  Edita: $SCRIPT_DIR/server_config.txt"
echo "  Para cambiar el servidor remoto"
echo ""

echo -e "${YELLOW}📋 Próximos pasos:${NC}"
echo "  1. Verifica que PostgreSQL esté corriendo en Windows Server"
echo "  2. Prueba la conexión: ping WIN-E6SQ6ALCVS5"
echo "  3. Ejecuta la aplicación: ./ejecutar.sh"
echo ""

echo -e "${GREEN}¡Listo para usar! 🎉${NC}"
echo ""
