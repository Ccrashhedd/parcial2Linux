"""
Configuración de la base de datos PostgreSQL
Soporta conexión local (Linux) y remota (Windows Server)
Con fallback automático si la remota no está disponible
"""

import os
import logging

logger = logging.getLogger(__name__)

# Variable de entorno para seleccionar el entorno
ENVIRONMENT = os.getenv('APP_ENV', 'auto')  # 'local', 'remote' o 'auto' (default)

# Configuración LOCAL (PostgreSQL en Linux local)
DB_CONFIG_LOCAL = {
    'host': 'localhost',
    'database': 'gestor_productos',
    'user': 'postgres',
    'password': 'postgres',
    'port': 5432
}

# Leer configuración del servidor remoto desde archivo
def _cargar_config_servidor():
    """Lee la configuración del servidor desde server_config.txt"""
    config_file = os.path.join(os.path.dirname(__file__), 'server_config.txt')
    config = {
        'host': '192.168.1.100',
        'user': 'postgres',
        'password': 'postgres123',
        'port': 5432,
        'database': 'gestor_productos'
    }
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                for linea in f:
                    linea = linea.strip()
                    # Ignorar comentarios y líneas vacías
                    if not linea or linea.startswith('#'):
                        continue
                    
                    if '=' in linea:
                        clave, valor = linea.split('=', 1)
                        clave = clave.strip()
                        valor = valor.strip()
                        
                        if clave == 'SERVER_IP':
                            config['host'] = valor
                        elif clave == 'SERVER_USER':
                            config['user'] = valor
                        elif clave == 'SERVER_PASSWORD':
                            config['password'] = valor
                        elif clave == 'SERVER_PORT':
                            try:
                                config['port'] = int(valor)
                            except ValueError:
                                pass
        except Exception as e:
            logger.warning(f"No se pudo leer server_config.txt: {e}")
    
    return config

# Configuración REMOTA (PostgreSQL en Windows Server)
DB_CONFIG_REMOTE = _cargar_config_servidor()

def _test_connection(config):
    """Prueba si la conexión a BD es posible"""
    try:
        import psycopg2
        
        conn = psycopg2.connect(
            host=config['host'],
            database=config['database'],
            user=config['user'],
            password=config['password'],
            port=config['port'],
            connect_timeout=5
        )
        conn.close()
        return True
    except Exception as e:
        return False

# Seleccionar configuración según el entorno
if ENVIRONMENT == 'auto':
    # Intentar remota primero, fallback a local si falla
    if _test_connection(DB_CONFIG_REMOTE):
        DB_CONFIG = DB_CONFIG_REMOTE
        print(f"✓ Usando conexión REMOTA (Windows Server: {DB_CONFIG_REMOTE['host']}:{DB_CONFIG_REMOTE['port']})")
    else:
        DB_CONFIG = DB_CONFIG_LOCAL
        print(f"⚠️  Servidor Windows ({DB_CONFIG_REMOTE['host']}) no disponible")
        print(f"   Usando BD LOCAL (localhost)")
        print(f"   💡 Para cambiar la IP: edita 'server_config.txt'")
elif ENVIRONMENT == 'remote':
    DB_CONFIG = DB_CONFIG_REMOTE
    print(f"ℹ️  Usando conexión REMOTA: {DB_CONFIG_REMOTE['host']}:{DB_CONFIG_REMOTE['port']}")
else:  # 'local'
    DB_CONFIG = DB_CONFIG_LOCAL
    print(f"ℹ️  Usando conexión LOCAL (localhost)")

# Configuración de la aplicación
APP_CONFIG = {
    'title': 'Gestor de Productos',
    'version': '1.0.0',
    'theme': 'modern',
    'window_width': 1800,
    'window_height': 1000,
}
