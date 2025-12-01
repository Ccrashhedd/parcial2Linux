#!/bin/bash

# Instalador Simple - Gestor de Productos

echo "════════════════════════════════════════"
echo "  GESTOR DE PRODUCTOS - INSTALACIÓN"
echo "════════════════════════════════════════"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📍 Ubicación: $SCRIPT_DIR"
echo ""

# 1. Verificar Python
echo "▶ Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    echo "Instálalo: sudo apt install python3 python3-pip"
    exit 1
fi
python3_version=$(python3 --version)
echo "✓ $python3_version encontrado"
echo ""

# 2. Verificar y instalar dependencias del sistema
echo "▶ Verificando librerías del sistema..."
if ! dpkg -l | grep -q "libpq-dev\|libgtk-3-0\|libcairo2"; then
    echo ""
    echo "⚠️  Se necesitan instalar librerías del sistema"
    echo "   Ejecuta este comando (requiere sudo):"
    echo ""
    echo "   sudo apt-get install -y python3-dev libpq-dev libgtk-3-0 libcairo2 libcairo2-dev python3-gi"
    echo ""
    read -p "¿Deseas continuar sin instalar? (s/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        exit 1
    fi
fi
echo ""

# 3. Instalar dependencias Python
echo "▶ Instalando paquetes Python..."
echo "  (esto puede tardar unos minutos)"
echo ""

python3 -m pip install --user --upgrade pip > /dev/null 2>&1

if [ -f "requirements.txt" ]; then
    python3 -m pip install --user -r requirements.txt
    if [ $? -eq 0 ]; then
        echo ""
        echo "✓ Dependencias instaladas"
    else
        echo ""
        echo "⚠️  Hubo problemas al instalar. Intentando alternativa..."
        python3 -m pip install --user --no-build-isolation -r requirements.txt
        if [ $? -ne 0 ]; then
            echo "❌ Error al instalar dependencias"
            exit 1
        fi
    fi
else
    echo "❌ No se encontró requirements.txt"
    exit 1
fi
echo ""

# 4. Hacer ejecutables
echo "▶ Configurando permisos..."
chmod +x "$SCRIPT_DIR/main.py" 2>/dev/null || true
chmod +x "$SCRIPT_DIR/ejecutar.sh" 2>/dev/null || true
echo "✓ Permisos configurados"
echo ""

# 5. Verificar config
echo "▶ Verificando configuración..."
if [ ! -f "$SCRIPT_DIR/server_config.txt" ]; then
    echo "⚠️  server_config.txt no encontrado, creando..."
    cat > "$SCRIPT_DIR/server_config.txt" << 'EOF'
# Configuración del servidor remoto
SERVER_IP=WIN-E6SQ6ALCVS5
SERVER_USER=postgres
SERVER_PASSWORD=postgres123
SERVER_PORT=5432
EOF
    echo "✓ Archivo de configuración creado"
else
    echo "✓ Configuración encontrada"
fi
echo ""

# 6. Resumen
echo "════════════════════════════════════════"
echo "✓ INSTALACIÓN COMPLETADA"
echo "════════════════════════════════════════"
echo ""
echo "▶ Para ejecutar la aplicación:"
echo ""
echo "  Opción 1: Script (RECOMENDADO)"
echo "    $ ./ejecutar.sh"
echo ""
echo "  Opción 2: Python directo"
echo "    $ python3 main.py"
echo ""
echo "▶ Cambiar servidor:"
echo "    $ nano server_config.txt"
echo ""
echo "¡Listo! 🎉"
echo ""
