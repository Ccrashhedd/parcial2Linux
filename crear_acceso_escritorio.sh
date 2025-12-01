#!/bin/bash

# Script para crear acceso directo en el escritorio

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESKTOP_DIR="$HOME/Desktop"

echo "════════════════════════════════════════"
echo "  Crear Acceso Directo en Escritorio"
echo "════════════════════════════════════════"
echo ""

# Si no existe Desktop, usar el directorio home
if [ ! -d "$DESKTOP_DIR" ]; then
    DESKTOP_DIR="$HOME"
    echo "📁 Escritorio no encontrado, usando: $DESKTOP_DIR"
else
    echo "📁 Escritorio: $DESKTOP_DIR"
fi

echo ""

# Crear archivo .desktop
DESKTOP_FILE="$DESKTOP_DIR/GestorProductos.desktop"

cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Gestor de Productos
Comment=Gestión de productos con PostgreSQL
Exec=$SCRIPT_DIR/ejecutar.sh
Icon=document-properties
Terminal=false
Categories=Utility;Office;
Path=$SCRIPT_DIR
EOF

# Hacer ejecutable
chmod +x "$DESKTOP_FILE"

# También crear en las aplicaciones
APP_DIR="$HOME/.local/share/applications"
mkdir -p "$APP_DIR"
cp "$DESKTOP_FILE" "$APP_DIR/"
chmod +x "$APP_DIR/GestorProductos.desktop"

echo "✓ Acceso directo creado:"
echo "  📌 $DESKTOP_FILE"
echo "  📌 $APP_DIR/GestorProductos.desktop"
echo ""
echo "Ahora puedes:"
echo "  1. Hacer doble clic en el icono del escritorio"
echo "  2. O buscar 'Gestor de Productos' en el menú de aplicaciones"
echo ""
echo "¡Listo! 🎉"
echo ""
