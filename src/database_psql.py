"""
Módulo para conexión a PostgreSQL usando psql (línea de comandos)
Evita problemas de encoding con psycopg2
"""

import subprocess
import json
import os
import logging
import csv
from io import StringIO
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ruta para guardar imágenes
CARPETA_IMAGENES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'imagenes')
if not os.path.exists(CARPETA_IMAGENES):
    os.makedirs(CARPETA_IMAGENES)


class BaseDatos:
    """Conexión a PostgreSQL usando psql en lugar de psycopg2"""

    def __init__(self, host='localhost', user='postgres', password='postgres', database='gestor_productos', port=5432):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.conectado = False
        self.conectar()

    def conectar(self):
        """Verifica conexión a la base de datos"""
        try:
            # Comando para verificar conexión
            resultado = self._ejecutar_query("SELECT 1;")
            if resultado is not None:
                self.conectado = True
                logger.info(f"✓ Conectado a {self.host}:{self.port}")
            else:
                raise Exception("No se pudo ejecutar query de prueba")
        except Exception as e:
            logger.error(f"Error al conectar: {e}")
            raise

    def desconectar(self):
        """Cierra la conexión"""
        self.conectado = False
        logger.info("Desconectado de la base de datos")

    def _ejecutar_query(self, query):
        """
        Ejecuta una consulta SQL usando psql
        Retorna resultados como diccionarios con tipos convertidos
        """
        try:
            # Preparar variables de entorno
            env = os.environ.copy()
            env['PGPASSWORD'] = self.password
            # Configurar encoding para soportar LATIN1 del servidor Windows
            env['PGCLIENTENCODING'] = 'UTF8'
            env['LANG'] = 'C.UTF-8'  # UTF-8 for Python
            env['LC_ALL'] = 'C.UTF-8'

            # Comando psql con salida en formato expandido SQL
            cmd = [
                'psql',
                '-h', str(self.host),
                '-p', str(self.port),
                '-U', self.user,
                '-d', self.database,
                '--csv',  # Salida CSV (máxima compatibilidad)
                '-c', query
            ]

            # Ejecutar comando
            resultado = subprocess.run(
                cmd,
                env=env,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',  # Reemplazar caracteres inválidos
                timeout=10
            )

            if resultado.returncode == 0:
                if resultado.stdout.strip():
                    # Parsear CSV
                    lines = resultado.stdout.strip().split('\n')
                    if len(lines) < 2:  # Sin headers
                        return []
                    
                    reader = csv.DictReader(StringIO(resultado.stdout.strip()))
                    resultados = list(reader)
                    
                    # Convertir tipos de datos
                    for row in resultados:
                        # Convertir precio a float
                        if 'precio' in row and row['precio']:
                            try:
                                row['precio'] = float(row['precio'])
                            except (ValueError, TypeError):
                                pass
                        
                        # Convertir id a int
                        if 'id' in row and row['id']:
                            try:
                                row['id'] = int(row['id'])
                            except (ValueError, TypeError):
                                pass
                    
                    return resultados
                return []
            else:
                logger.error(f"Error psql: {resultado.stderr}")
                return []

        except subprocess.TimeoutExpired:
            logger.error("Timeout en consulta")
            return []
        except Exception as e:
            logger.error(f"Error ejecutando query: {e}")
            return []

    def obtener_todos_productos(self):
        """Obtiene todos los productos (con imagen_data codificado en base64)"""
        query = """
        SELECT 
            id, 
            nombre, 
            precio, 
            descripcion, 
            encode(imagen_data, 'base64') as imagen_data,
            fecha_creacion,
            fecha_actualizacion
        FROM productos 
        ORDER BY id DESC
        """
        resultado = self._ejecutar_query(query)
        return resultado if resultado else []

    def obtener_producto(self, producto_id):
        """Obtiene un producto específico (incluye imagen_data)"""
        query = f"""
        SELECT 
            id, 
            nombre, 
            precio, 
            descripcion, 
            encode(imagen_data, 'base64') as imagen_data,
            fecha_creacion,
            fecha_actualizacion
        FROM productos 
        WHERE id = {producto_id}
        LIMIT 1
        """
        resultado = self._ejecutar_query(query)
        if resultado and len(resultado) > 0:
            return resultado[0]
        return None

    def crear_producto(self, nombre, precio, descripcion, imagen_bytes=None):
        """Crea un nuevo producto con imagen en BYTEA"""
        try:
            # Escapar valores
            nombre = nombre.replace("'", "''")
            descripcion = descripcion.replace("'", "''")
            
            # Convertir bytes a formato PostgreSQL base64
            imagen_str = ""
            if imagen_bytes:
                import base64
                imagen_b64 = base64.b64encode(imagen_bytes).decode('utf-8')
                imagen_str = f"decode('{imagen_b64}', 'base64')"
            else:
                imagen_str = "NULL"

            query = f"""
            INSERT INTO productos (nombre, precio, descripcion, imagen_data)
            VALUES ('{nombre}', {precio}, '{descripcion}', {imagen_str})
            RETURNING id
            """

            resultado = self._ejecutar_query(query)
            if resultado and len(resultado) > 0:
                producto_id = int(resultado[0].get('id', 0))
                logger.info(f"Producto creado con ID: {producto_id}")
                return producto_id
            return None

        except Exception as e:
            logger.error(f"Error al crear producto: {e}")
            return None

    def actualizar_producto(self, producto_id, nombre, precio, descripcion, imagen_bytes=None):
        """Actualiza un producto existente"""
        try:
            # Escapar valores
            nombre = nombre.replace("'", "''")
            descripcion = descripcion.replace("'", "''")
            
            # Convertir bytes a formato PostgreSQL base64
            imagen_str = ""
            if imagen_bytes is not None:
                import base64
                imagen_b64 = base64.b64encode(imagen_bytes).decode('utf-8')
                imagen_str = f", imagen_data = decode('{imagen_b64}', 'base64')"
            # Si imagen_bytes es None, no actualizar la imagen

            query = f"""
            UPDATE productos 
            SET 
                nombre = '{nombre}',
                precio = {precio},
                descripcion = '{descripcion}'
                {imagen_str},
                fecha_actualizacion = CURRENT_TIMESTAMP
            WHERE id = {producto_id}
            """

            resultado = self._ejecutar_query(query)
            logger.info(f"Producto {producto_id} actualizado")
            return True

        except Exception as e:
            logger.error(f"Error al actualizar producto: {e}")
            return False

    def eliminar_producto(self, producto_id):
        """Elimina un producto"""
        try:
            query = f"DELETE FROM productos WHERE id = {producto_id}"
            self._ejecutar_query(query)
            logger.info(f"Producto {producto_id} eliminado")
            return True

        except Exception as e:
            logger.error(f"Error al eliminar producto: {e}")
            return False

    def buscar_productos(self, termino):
        """Busca productos por nombre (con imagen_data)"""
        try:
            termino = termino.replace("'", "''")
            query = f"""
            SELECT 
                id, 
                nombre, 
                precio, 
                descripcion, 
                encode(imagen_data, 'base64') as imagen_data,
                fecha_creacion,
                fecha_actualizacion
            FROM productos 
            WHERE nombre ILIKE '%{termino}%'
            ORDER BY id DESC
            """
            resultado = self._ejecutar_query(query)
            return resultado if resultado else []

        except Exception as e:
            logger.error(f"Error al buscar productos: {e}")
            return []

    @staticmethod
    def obtener_ruta_imagen(nombre_imagen):
        """Obtiene la ruta completa de una imagen (DEPRECATED - ahora están en DB)"""
        if nombre_imagen:
            return os.path.join(CARPETA_IMAGENES, nombre_imagen)
        return None
