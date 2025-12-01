#!/bin/bash

# Script para crear acceso directo en el escritorio con icono

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESKTOP_DIR="$HOME/Desktop"
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"

echo "════════════════════════════════════════"
echo "  Crear Acceso Directo - Aplicación"
echo "════════════════════════════════════════"
echo ""

# Si no existe Desktop, usar el directorio home
if [ ! -d "$DESKTOP_DIR" ]; then
    DESKTOP_DIR="$HOME"
    echo "📁 Desktop no encontrado, usando: $DESKTOP_DIR"
else
    echo "📁 Desktop: $DESKTOP_DIR"
fi

echo ""

# Crear directorio de iconos
mkdir -p "$ICON_DIR"

# Crear icono SVG
ICON_FILE="$HOME/.local/share/icons/hicolor/256x256/apps/gestor-productos.svg"

cat > "$ICON_FILE" << 'ICONEOF'
<?xml version="1.0" encoding="UTF-8"?>
<svg width="256" height="256" viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg">
  <rect width="256" height="256" rx="64" fill="#4CAF50"/>
  <g transform="translate(128, 128)">
    <rect x="-60" y="-50" width="120" height="100" rx="8" fill="white" opacity="0.9"/>
    <line x1="-60" y1="-20" x2="60" y2="-20" stroke="white" stroke-width="3"/>
    <circle cx="-30" cy="-35" r="12" fill="#4CAF50"/>
    <circle cx="0" cy="-35" r="12" fill="#4CAF50"/>
    <circle cx="30" cy="-35" r="12" fill="#4CAF50"/>
    <line x1="-30" y1="-8" x2="-30" y2="50" stroke="#4CAF50" stroke-width="2"/>
    <line x1="0" y1="-8" x2="0" y2="50" stroke="#4CAF50" stroke-width="2"/>
    <line x1="30" y1="-8" x2="30" y2="50" stroke="#4CAF50" stroke-width="2"/>
  </g>
</svg>
ICONEOF

chmod 644 "$ICON_FILE"
echo "✓ Icono creado"
echo ""

# Crear archivo .desktop para el escritorio
DESKTOP_FILE="$DESKTOP_DIR/GestorProductos.desktop"

cat > "$DESKTOP_FILE" << 'DESKTOPEOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Gestor de Productos
GenericName=Gestor de Productos
Comment=Gestión de productos con PostgreSQL
Exec=/home/angelbroce/Documentos/linux\ phyton/gestor_productos/ejecutar.sh
Icon=gestor-productos
Terminal=false
Categories=Utility;Office;Application;Database;
StartupNotify=true
Keywords=productos;gestor;database;postgresql;
DESKTOPEOF

chmod +x "$DESKTOP_FILE"
echo "✓ Acceso directo en escritorio: $DESKTOP_FILE"
echo ""

# También crear en las aplicaciones del menú
APP_DIR="$HOME/.local/share/applications"
mkdir -p "$APP_DIR"

APP_FILE="$APP_DIR/gestor-productos.desktop"

cat > "$APP_FILE" << 'APPEOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Gestor de Productos
GenericName=Gestor de Productos
Comment=Gestión de productos con PostgreSQL
Exec=/home/angelbroce/Documentos/linux\ phyton/gestor_productos/ejecutar.sh
Icon=gestor-productos
Terminal=false
Categories=Utility;Office;Application;Database;
StartupNotify=true
Keywords=productos;gestor;database;postgresql;
APPEOF

chmod +x "$APP_FILE"
echo "✓ Aplicación registrada en menú"
echo ""

# Actualizar la base de datos de escritorio
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
fi

# Actualizar iconos si es posible
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache "$HOME/.local/share/icons/hicolor" 2>/dev/null || true
fi

echo "════════════════════════════════════════"
echo "✓ ACCESO DIRECTO CREADO"
echo "════════════════════════════════════════"
echo ""
echo "Ahora puedes:"
echo "  1. 🖱️  Hacer doble clic en GestorProductos en el escritorio"
echo "  2. 📱 Buscar 'Gestor de Productos' en el menú"
echo "  3. 💻 Terminal: ./ejecutar.sh"
echo ""
echo "¡Listo! 🎉"
echo ""
