#!/usr/bin/env python3
"""
setup_database.py - Script para inicializar la base de datos
Ejecuta el script SQL para crear todas las tablas
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys
import os

# Configuración de conexión
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': 'postgres'  # Contraseña de PostgreSQL
}

def crear_base_datos():
    """Elimina y crea la base de datos parcial2 desde cero"""
    try:
        # Conectar al servidor PostgreSQL (base postgres por defecto)
        conexion = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database='postgres'
        )
        conexion.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conexion.cursor()
        
        # Verificar si la base de datos existe
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='parcial2'")
        existe = cursor.fetchone()
        
        if existe:
            print("⚠️  Base de datos 'parcial2' existe. Eliminando...")
            # Terminar conexiones activas
            cursor.execute("""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = 'parcial2'
                  AND pid <> pg_backend_pid()
            """)
            # Eliminar base de datos
            cursor.execute("DROP DATABASE parcial2")
            print("✓ Base de datos anterior eliminada")
        
        print("Creando base de datos 'parcial2'...")
        cursor.execute("CREATE DATABASE parcial2")
        print("✓ Base de datos 'parcial2' creada exitosamente")
        
        cursor.close()
        conexion.close()
        return True
        
    except psycopg2.Error as e:
        print(f"✗ Error al crear la base de datos: {e}")
        return False

def ejecutar_script_sql():
    """Ejecuta el script SQL para crear las tablas"""
    try:
        # Conectar a la base de datos parcial2
        conexion = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database='parcial2'
        )
        cursor = conexion.cursor()
        
        # Leer el archivo SQL
        script_path = os.path.join(os.path.dirname(__file__), 'DB', 'DB.sql')
        print(f"Leyendo script SQL desde: {script_path}")
        
        with open(script_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()
        
        # Ejecutar el script
        print("Ejecutando script SQL...")
        cursor.execute(sql_script)
        conexion.commit()
        
        print("✓ Script SQL ejecutado exitosamente")
        
        # Verificar las tablas creadas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        
        tablas = cursor.fetchall()
        print("\n✓ Tablas creadas:")
        for tabla in tablas:
            print(f"  - {tabla[0]}")
        
        cursor.close()
        conexion.close()
        return True
        
    except psycopg2.Error as e:
        print(f"✗ Error al ejecutar el script SQL: {e}")
        return False
    except FileNotFoundError:
        print(f"✗ No se encontró el archivo DB/DB.sql")
        return False

def verificar_conexion():
    """Verifica que PostgreSQL esté accesible"""
    try:
        conexion = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database='postgres'
        )
        conexion.close()
        print("✓ Conexión a PostgreSQL exitosa")
        return True
    except psycopg2.Error as e:
        print(f"✗ Error al conectar con PostgreSQL: {e}")
        print("\nAsegúrate de que:")
        print("1. PostgreSQL esté instalado y ejecutándose")
        print("2. El usuario y contraseña sean correctos")
        print("3. El servidor esté escuchando en localhost:5432")
        return False

def main():
    print("=" * 60)
    print("CONFIGURACIÓN DE BASE DE DATOS - RESTAURANTE POS")
    print("=" * 60)
    print()
    
    # Paso 1: Verificar conexión
    print("Paso 1: Verificando conexión a PostgreSQL...")
    if not verificar_conexion():
        sys.exit(1)
    print()
    
    # Paso 2: Crear base de datos
    print("Paso 2: Creando base de datos...")
    if not crear_base_datos():
        sys.exit(1)
    print()
    
    # Paso 3: Ejecutar script SQL
    print("Paso 3: Creando tablas...")
    if not ejecutar_script_sql():
        sys.exit(1)
    print()
    
    print("=" * 60)
    print("✓ CONFIGURACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 60)
    print("\nLa base de datos está lista para usar.")
    print("Puedes ejecutar la aplicación con: python3 main.py")

if __name__ == "__main__":
    main()
