"""
conexionDB.py - Módulo de conexión a PostgreSQL
Maneja la conexión y operaciones con la base de datos del restaurante
Actualizado: Noviembre 2025
"""

import psycopg2
from psycopg2 import pool, extras
from typing import Optional, List, Tuple, Any, Dict
from contextlib import contextmanager
import logging
import sys

# Configurar logging mejorado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('database.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


class ConexionDB:
    """Clase para manejar la conexión a PostgreSQL"""
    
    _connection_pool = None
    
    # Configuración de la base de datos
    DB_CONFIG = {
        'host': 'localhost',
        'port': 5432,
        'database': 'parcial2',
        'user': 'postgres',
        'password': 'postgres'  # Contraseña de PostgreSQL
    }
    
    @classmethod
    def inicializar_pool(cls, minconn=1, maxconn=10):
        """Inicializa el pool de conexiones"""
        try:
            if cls._connection_pool is None:
                cls._connection_pool = psycopg2.pool.SimpleConnectionPool(
                    minconn,
                    maxconn,
                    **cls.DB_CONFIG
                )
                logger.info("Pool de conexiones creado exitosamente")
        except psycopg2.Error as e:
            logger.error(f"Error al crear pool de conexiones: {e}")
            raise
    
    @classmethod
    def obtener_conexion(cls):
        """Obtiene una conexión del pool"""
        if cls._connection_pool is None:
            cls.inicializar_pool()
        return cls._connection_pool.getconn()
    
    @classmethod
    def devolver_conexion(cls, conexion):
        """Devuelve una conexión al pool"""
        if cls._connection_pool is not None:
            cls._connection_pool.putconn(conexion)
    
    @classmethod
    def cerrar_pool(cls):
        """Cierra todas las conexiones del pool"""
        if cls._connection_pool is not None:
            cls._connection_pool.closeall()
            cls._connection_pool = None
            logger.info("Pool de conexiones cerrado")
    
    @classmethod
    @contextmanager
    def obtener_cursor(cls):
        """Context manager para obtener cursor automáticamente"""
        conexion = None
        cursor = None
        try:
            conexion = cls.obtener_conexion()
            cursor = conexion.cursor()
            yield cursor, conexion
            conexion.commit()
        except Exception as e:
            if conexion:
                conexion.rollback()
            logger.error(f"Error en transacción: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conexion:
                cls.devolver_conexion(conexion)


class DatabaseManager:
    """Clase para manejar operaciones de base de datos con métodos mejorados"""
    
    def __init__(self):
        ConexionDB.inicializar_pool()
        logger.info("DatabaseManager inicializado correctamente")
    
    def ejecutar_query(self, query: str, params: Tuple = None, fetch: bool = True) -> Optional[List[Tuple]]:
        """
        Ejecuta una query y retorna los resultados usando context manager
        
        Args:
            query: La consulta SQL a ejecutar
            params: Parámetros para la consulta
            fetch: Si True, retorna los resultados (SELECT), si False no retorna nada (INSERT/UPDATE/DELETE)
        
        Returns:
            Lista de tuplas con los resultados si fetch=True, None si fetch=False
        """
        try:
            with ConexionDB.obtener_cursor() as (cursor, conexion):
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                if fetch:
                    resultados = cursor.fetchall()
                    return resultados
                else:
                    return None
                    
        except psycopg2.Error as e:
            logger.error(f"Error ejecutando query: {e}")
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            raise
    
    def ejecutar_query_uno(self, query: str, params: Tuple = None) -> Optional[Tuple]:
        """
        Ejecuta una query y retorna solo el primer resultado
        """
        resultados = self.ejecutar_query(query, params, fetch=True)
        return resultados[0] if resultados else None
    
    def insertar(self, tabla: str, datos: dict) -> int:
        """
        Inserta un registro en una tabla
        
        Args:
            tabla: Nombre de la tabla
            datos: Diccionario con columnas y valores
        
        Returns:
            Número de filas afectadas
        """
        columnas = ', '.join(datos.keys())
        placeholders = ', '.join(['%s'] * len(datos))
        query = f"INSERT INTO {tabla} ({columnas}) VALUES ({placeholders})"
        
        self.ejecutar_query(query, tuple(datos.values()), fetch=False)
        return 1
    
    def actualizar(self, tabla: str, datos: dict, condicion: str, params_condicion: Tuple = None) -> int:
        """
        Actualiza registros en una tabla
        
        Args:
            tabla: Nombre de la tabla
            datos: Diccionario con columnas y nuevos valores
            condicion: Condición WHERE (ej: "id = %s")
            params_condicion: Parámetros para la condición
        
        Returns:
            Número de filas afectadas
        """
        set_clause = ', '.join([f"{col} = %s" for col in datos.keys()])
        query = f"UPDATE {tabla} SET {set_clause} WHERE {condicion}"
        
        params = tuple(datos.values())
        if params_condicion:
            params += params_condicion
        
        self.ejecutar_query(query, params, fetch=False)
        return 1
    
    def eliminar(self, tabla: str, condicion: str, params: Tuple = None) -> int:
        """
        Elimina registros de una tabla
        
        Args:
            tabla: Nombre de la tabla
            condicion: Condición WHERE
            params: Parámetros para la condición
        
        Returns:
            Número de filas afectadas
        """
        query = f"DELETE FROM {tabla} WHERE {condicion}"
        self.ejecutar_query(query, params, fetch=False)
        return 1
    
    def ejecutar_query_dict(self, query: str, params: Tuple = None) -> Optional[List[Dict]]:
        """
        Ejecuta una query y retorna los resultados como lista de diccionarios
        
        Args:
            query: La consulta SQL a ejecutar
            params: Parámetros para la consulta
        
        Returns:
            Lista de diccionarios con los resultados
        """
        try:
            with ConexionDB.obtener_cursor() as (cursor, conexion):
                # Usar DictCursor para obtener resultados como diccionarios
                cursor = conexion.cursor(cursor_factory=extras.DictCursor)
                
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                resultados = cursor.fetchall()
                return [dict(row) for row in resultados] if resultados else []
                    
        except psycopg2.Error as e:
            logger.error(f"Error ejecutando query_dict: {e}")
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            raise
    
    def verificar_conexion(self) -> bool:
        """
        Verifica que la conexión a la base de datos funcione
        
        Returns:
            True si la conexión es exitosa, False en caso contrario
        """
        try:
            resultado = self.ejecutar_query("SELECT 1", fetch=True)
            return resultado is not None
        except Exception as e:
            logger.error(f"Error al verificar conexión: {e}")
            return False
    
    def obtener_version_db(self) -> Optional[str]:
        """Obtiene la versión de PostgreSQL"""
        try:
            resultado = self.ejecutar_query("SELECT version()", fetch=True)
            return resultado[0][0] if resultado else None
        except Exception as e:
            logger.error(f"Error al obtener versión: {e}")
            return None
    
    def cerrar(self):
        """Cierra el pool de conexiones"""
        ConexionDB.cerrar_pool()
        logger.info("DatabaseManager cerrado correctamente")


# Crear instancia global del gestor de base de datos
db_manager = DatabaseManager()


if __name__ == "__main__":
    # Prueba de conexión
    try:
        db = DatabaseManager()
        if db.verificar_conexion():
            print("✓ Conexión a PostgreSQL exitosa")
            
            # Probar algunas queries básicas
            resultado = db.ejecutar_query("SELECT current_database(), current_user", fetch=True)
            if resultado:
                print(f"✓ Base de datos: {resultado[0][0]}")
                print(f"✓ Usuario: {resultado[0][1]}")
        else:
            print("✗ No se pudo conectar a PostgreSQL")
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        db.cerrar()
