#!/usr/bin/env python3
"""
Aplicación principal - Sistema Operativo Parcial 2
Programa en Python que corre en Linux con interfaz gráfica en TKinter
y conexión a base de datos PostgreSQL
"""

import tkinter as tk
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from interfaze import InterfazPrincipal


def main():
    """Función principal que inicia la aplicación"""
    try:
        # Crear la ventana raíz
        ventana_raiz = tk.Tk()
        
        # Crear e inicializar la interfaz
        app = InterfazPrincipal(ventana_raiz)
        
        # Ejecutar la aplicación
        app.ejecutar()
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}", file=sys.stderr)
        print("Asegúrate de instalar las dependencias con: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error al ejecutar la aplicación: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
