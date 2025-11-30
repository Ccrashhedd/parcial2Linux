"""
Módulo para la conexión y operaciones con PostgreSQL
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import sys
import os
import logging
import shutil
from datetime import datetime

# Agregar la ruta para importar config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_CONFIG

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ruta para guardar imágenes
CARPETA_IMAGENES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'imagenes')
if not os.path.exists(CARPETA_IMAGENES):
    os.makedirs(CARPETA_IMAGENES)


class BaseDatos:
    """Clase para manejar todas las operaciones con la base de datos"""

    def __init__(self):
        self.conexion = None
        self.conectar()

    def conectar(self):
        """Establece conexión con la base de datos"""
        from config import ENVIRONMENT, DB_CONFIG_LOCAL
        
        # Si estamos en modo remoto y falla, auto-cambiar a local
        intentos_fallidos = 0
        config_actual = DB_CONFIG
        
        while intentos_fallidos < 2:
            try:
                self.conexion = psycopg2.connect(**config_actual)
                logger.info(f"Conexión a la base de datos establecida ({config_actual['host']})")
                return
                
            except UnicodeDecodeError as ue:
                logger.warning(f"Problema de encoding en {config_actual['host']}")
                intentos_fallidos += 1
                
                # Si era remota, intentar con local
                if config_actual['host'] != 'localhost' and intentos_fallidos == 1:
                    logger.info("Intentando con BD local como fallback...")
                    config_actual = DB_CONFIG_LOCAL
                else:
                    break
                    
            except (Exception, psycopg2.DatabaseError) as error:
                logger.error(f"Error al conectar a {config_actual['host']}: {error}")
                intentos_fallidos += 1
                
                # Si era remota, intentar con local
                if config_actual['host'] != 'localhost' and intentos_fallidos == 1:
                    logger.info("Intentando con BD local como fallback...")
                    config_actual = DB_CONFIG_LOCAL
                else:
                    break
        
        # Si llegamos aquí, ambas fallaron
        raise RuntimeError("No se puede conectar a ninguna base de datos")

    def desconectar(self):
        """Cierra la conexión con la base de datos"""
        if self.conexion:
            self.conexion.close()
            logger.info("Conexión cerrada")

    def obtener_todos_productos(self):
        """Obtiene todos los productos de la base de datos"""
        try:
            cursor = self.conexion.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM productos ORDER BY id DESC")
            productos = cursor.fetchall()
            cursor.close()
            return productos
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(f"Error al obtener productos: {error}")
            return []

    def obtener_producto(self, producto_id):
        """Obtiene un producto específico por ID"""
        try:
            cursor = self.conexion.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM productos WHERE id = %s", (producto_id,))
            producto = cursor.fetchone()
            cursor.close()
            return producto
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(f"Error al obtener producto: {error}")
            return None

    def crear_producto(self, nombre, precio, descripcion, imagen_path=None):
        """Crea un nuevo producto"""
        try:
            # Guardar imagen si se proporciona
            imagen_guardada = None
            if imagen_path and os.path.exists(imagen_path):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                extension = os.path.splitext(imagen_path)[1]
                nombre_imagen = f"producto_{timestamp}{extension}"
                ruta_guardada = os.path.join(CARPETA_IMAGENES, nombre_imagen)
                shutil.copy2(imagen_path, ruta_guardada)
                imagen_guardada = nombre_imagen
            
            cursor = self.conexion.cursor()
            cursor.execute(
                """INSERT INTO productos (nombre, precio, descripcion, imagen_path)
                   VALUES (%s, %s, %s, %s) RETURNING id""",
                (nombre, precio, descripcion, imagen_guardada)
            )
            producto_id = cursor.fetchone()[0]
            self.conexion.commit()
            cursor.close()
            logger.info(f"Producto creado con ID: {producto_id}")
            return producto_id
        except (Exception, psycopg2.DatabaseError) as error:
            self.conexion.rollback()
            logger.error(f"Error al crear producto: {error}")
            raise

    def actualizar_producto(self, producto_id, nombre, precio, descripcion, imagen_path=None):
        """Actualiza un producto existente"""
        try:
            imagen_guardada = None
            
            # Si se proporciona una nueva imagen, guardarla
            if imagen_path and os.path.exists(imagen_path):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                extension = os.path.splitext(imagen_path)[1]
                nombre_imagen = f"producto_{timestamp}{extension}"
                ruta_guardada = os.path.join(CARPETA_IMAGENES, nombre_imagen)
                shutil.copy2(imagen_path, ruta_guardada)
                imagen_guardada = nombre_imagen
            elif imagen_path:
                # Si es un nombre de archivo (ya guardado), mantenerlo
                imagen_guardada = imagen_path
            
            cursor = self.conexion.cursor()
            cursor.execute(
                """UPDATE productos 
                   SET nombre = %s, precio = %s, descripcion = %s, 
                       imagen_path = %s, fecha_actualizacion = CURRENT_TIMESTAMP
                   WHERE id = %s""",
                (nombre, precio, descripcion, imagen_guardada, producto_id)
            )
            self.conexion.commit()
            cursor.close()
            logger.info(f"Producto {producto_id} actualizado")
        except (Exception, psycopg2.DatabaseError) as error:
            self.conexion.rollback()
            logger.error(f"Error al actualizar producto: {error}")
            raise

    def eliminar_producto(self, producto_id):
        """Elimina un producto"""
        try:
            cursor = self.conexion.cursor()
            cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
            self.conexion.commit()
            cursor.close()
            logger.info(f"Producto {producto_id} eliminado")
        except (Exception, psycopg2.DatabaseError) as error:
            self.conexion.rollback()
            logger.error(f"Error al eliminar producto: {error}")
            raise

    def buscar_productos(self, termino):
        """Busca productos por nombre"""
        try:
            cursor = self.conexion.cursor(cursor_factory=RealDictCursor)
            cursor.execute(
                "SELECT * FROM productos WHERE nombre ILIKE %s ORDER BY id DESC",
                (f"%{termino}%",)
            )
            productos = cursor.fetchall()
            cursor.close()
            return productos
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(f"Error al buscar productos: {error}")
            return []

    @staticmethod
    def obtener_ruta_imagen(nombre_imagen):
        """Obtiene la ruta completa de una imagen"""
        if nombre_imagen:
            return os.path.join(CARPETA_IMAGENES, nombre_imagen)
        return None