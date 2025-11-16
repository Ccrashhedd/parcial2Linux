#!/bin/bash
# Script de instalación y ejecución para Linux

set -e  # Salir si hay error

echo "=================================================="
echo "Sistema Operativo - Parcial 2"
echo "Instalador para Linux"
echo "=================================================="
echo ""

# Verificar si Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    echo "Instálalo con: sudo apt-get install python3"
    exit 1
fi

echo "✅ Python 3 encontrado: $(python3 --version)"
echo ""

# Verificar si pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 no está instalado"
    echo "Instálalo con: sudo apt-get install python3-pip"
    exit 1
fi

echo "✅ pip3 encontrado"
echo ""

# Obtener la ruta del script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "📁 Directorio del proyecto: $SCRIPT_DIR"
echo ""

# Verificar TKinter
echo "Verificando TKinter..."
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "⚠️  TKinter no está instalado"
    echo "Instálalo con uno de estos comandos:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "  Fedora/RHEL: sudo dnf install python3-tkinter"
    echo "  Arch: sudo pacman -S tk"
    echo ""
    read -p "¿Deseas continuar de todas formas? (s/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        exit 1
    fi
else
    echo "✅ TKinter está instalado"
fi

echo ""

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
    echo "✅ Entorno virtual creado"
else
    echo "✅ Entorno virtual ya existe"
fi

echo ""

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

echo "✅ Entorno virtual activado"
echo ""

# Instalar dependencias
if [ -f "requirements.txt" ]; then
    echo "📦 Instalando dependencias..."
    pip install -r requirements.txt
    echo "✅ Dependencias instaladas"
else
    echo "⚠️  requirements.txt no encontrado"
fi

echo ""
echo "=================================================="
echo "✅ Instalación completada"
echo "=================================================="
echo ""
echo "Para ejecutar la aplicación, usa:"
echo "  python3 main.py"
echo "  o"
echo "  ./main.py"
echo ""
