#!/usr/bin/env python3
"""
Aplicacion principal - Sistema Operativo Parcial 2
POS (Punto de Venta) para Restaurante con interfaz grafica Tkinter
Optimizado para Linux con soporte de impresion CUPS
"""

import tkinter as tk
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Usar interfaz del restaurante con pestañas
from interfaz_restaurante import InterfazRestaurante


def main():
    """Funcion principal que inicia la aplicacion"""
    try:
        # Crear e inicializar la interfaz del POS
        app = InterfazRestaurante()
        
        # Ejecutar la aplicacion
        app.ejecutar()
        
    except ImportError as e:
        print(f"Error de importacion: {e}", file=sys.stderr)
        print("Asegurate de instalar las dependencias con: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error al ejecutar la aplicacion: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
