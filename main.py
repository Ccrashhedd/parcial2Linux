#!/usr/bin/env python3
"""
Aplicacion principal - Sistema POS Restaurante
POS (Punto de Venta) para Restaurante con interfaz grafica Tkinter
Optimizado para Linux con soporte de impresion CUPS
Actualizado: Noviembre 2025
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Usar interfaz del restaurante con pestañas
from interfaz_restaurante import InterfazRestaurante


def verificar_dependencias():
    """Verifica que todas las dependencias necesarias estén instaladas"""
    dependencias = {
        'psycopg2': 'psycopg2-binary',
        'tkinter': 'python3-tkinter (viene con Python)'
    }
    
    faltantes = []
    for modulo, paquete in dependencias.items():
        try:
            if modulo == 'tkinter':
                import tkinter
            else:
                __import__(modulo)
            logger.info(f"✓ {modulo} disponible")
        except ImportError:
            faltantes.append(paquete)
            logger.error(f"✗ {modulo} no encontrado")
    
    return faltantes


def main():
    """Funcion principal que inicia la aplicacion"""
    logger.info("=" * 60)
    logger.info("Iniciando Sistema POS Restaurante")
    logger.info("=" * 60)
    
    try:
        # Verificar dependencias
        faltantes = verificar_dependencias()
        if faltantes:
            mensaje = "Dependencias faltantes:\n" + "\n".join(f"- {pkg}" for pkg in faltantes)
            mensaje += "\n\nInstalar con: pip install -r requirements.txt"
            logger.error(mensaje)
            
            # Mostrar ventana de error
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error de Dependencias", mensaje)
            root.destroy()
            sys.exit(1)
        
        logger.info("Todas las dependencias están disponibles")
        
        # Crear e inicializar la interfaz del POS
        logger.info("Creando interfaz principal...")
        app = InterfazRestaurante()
        
        # Ejecutar la aplicacion
        logger.info("Ejecutando aplicación...")
        app.ejecutar()
        
        logger.info("Aplicación cerrada correctamente")
        
    except ImportError as e:
        error_msg = f"Error de importacion: {e}"
        logger.error(error_msg)
        logger.error("Asegurate de instalar las dependencias con: pip install -r requirements.txt")
        
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error de Importación", error_msg + "\n\nVer archivo app.log para más detalles")
        root.destroy()
        sys.exit(1)
        
    except Exception as e:
        error_msg = f"Error al ejecutar la aplicacion: {e}"
        logger.error(error_msg)
        import traceback
        logger.error(traceback.format_exc())
        
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error Fatal", error_msg + "\n\nVer archivo app.log para más detalles")
            root.destroy()
        except:
            pass
        
        sys.exit(1)


if __name__ == "__main__":
    main()
