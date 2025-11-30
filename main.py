#!/usr/bin/env python3
"""
Gestor de Productos - Aplicación Principal
Interfaz moderna para gestionar productos con PostgreSQL
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.gui import main


if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print(f"Error de importación: {e}")
        print("\nInstala las dependencias requeridas:")
        print("pip3 install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
