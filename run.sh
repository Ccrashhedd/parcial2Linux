#!/bin/bash
# Script rápido para ejecutar la aplicación
# Uso: ./run.sh

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Ejecutar la aplicación
exec python3 main.py
