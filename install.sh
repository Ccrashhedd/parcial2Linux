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
echo "Para ejecutar la aplicación desde terminal, usa:"
echo "  python3 main.py"
echo "  o"
echo "  ./main.py"
echo ""

# Preguntar si se quiere instalar como aplicación de escritorio
read -p "¿Deseas instalar esta aplicación como una APP de escritorio en Linux? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo ""
    echo "====== Instalación como Aplicación de Escritorio ======"
    echo ""
    
    # Asegurarse de que build.sh existe
    if [ ! -f "build.sh" ]; then
        echo "⚠️  build.sh no encontrado. Creando..."
        cat > build.sh <<'BASH'
#!/bin/bash
set -e
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"
echo "Instalando PyInstaller..."
python3 -m pip install pyinstaller
echo "Construyendo ejecutable (puede tardar 1-2 minutos)..."
python3 -m PyInstaller --onefile --add-data "DB:DB" --name parcial2 main.py
echo "✅ Build finished: $SCRIPT_DIR/dist/parcial2"
BASH
        chmod +x build.sh
    fi

    echo "Construyendo ejecutable (puede tardar 1-2 minutos)..."
    ./build.sh
    echo ""

    # Copiar el binario a /usr/local/bin
    if [ -f "dist/parcial2" ]; then
        echo "📋 Instalando ejecutable en /usr/local/bin/ (se pedirá contraseña sudo)..."
        sudo cp dist/parcial2 /usr/local/bin/parcial2
        sudo chmod +x /usr/local/bin/parcial2
        echo "✅ Ejecutable instalado en /usr/local/bin/parcial2"
    else
        echo "❌ No se encontró dist/parcial2. Abortando.";
        exit 1
    fi

    # Crear lanzador de escritorio
    DESKTOP_DIR="$HOME/.local/share/applications"
    mkdir -p "$DESKTOP_DIR"
    
    cat > "$DESKTOP_DIR/parcial2.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Parcial2 - SO Parcial 2
Comment=Aplicación de Sistema Operativo Parcial 2 con GUI Tkinter
Exec=/usr/local/bin/parcial2
Icon=application-default-icon
Terminal=false
Categories=Utility;Education;
Version=1.0
EOF

    echo "✅ Lanzador creado: $DESKTOP_DIR/parcial2.desktop"
    echo ""
    echo "====== Instalación Completada ======"
    echo ""
    echo "Ahora puedes ejecutar la aplicación de 3 formas:"
    echo ""
    echo "1️⃣  DESDE TERMINAL:"
    echo "    parcial2"
    echo "    o"
    echo "    /usr/local/bin/parcial2"
    echo ""
    echo "2️⃣  DESDE EL MENÚ DE APLICACIONES:"
    echo "    Busca 'Parcial2' en tu menú de aplicaciones o lanzador (Activities)"
    echo ""
    echo "3️⃣  DESDE VISUAL STUDIO CODE:"
    echo "    Abre la terminal integrada (Ctrl+ñ) en VS Code y escribe:"
    echo "    parcial2"
    echo ""
    echo "Para desinstalar:"
    echo "    sudo rm /usr/local/bin/parcial2"
    echo "    rm $DESKTOP_DIR/parcial2.desktop"
    echo ""
fi
