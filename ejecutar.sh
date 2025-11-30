mir#!/bin/bash

# Script para ejecutar el Gestor de Productos

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Iniciando Gestor de Productos..."
python3 main.py
