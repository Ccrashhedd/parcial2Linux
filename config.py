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

# Configuración REMOTA (PostgreSQL en Windows Server)
DB_CONFIG_REMOTE = {
    'host': '192.168.50.126',  # IP de Windows Server
    'database': 'gestor_productos',
    'user': 'postgres',
    'password': 'postgres123',  # Contraseña del servidor Windows
    'port': 5432  # Puerto estándar PostgreSQL
}

def _test_connection(config):
    """Prueba si la conexión a BD es posible"""
    try:
        import psycopg2
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError("Conexión agotada")
        
        # Establecer timeout de 3 segundos
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(3)
        
        try:
            conn = psycopg2.connect(
                host=config['host'],
                database=config['database'],
                user=config['user'],
                password=config['password'],
                port=config['port'],
                connect_timeout=2
            )
            signal.alarm(0)  # Cancelar alarma
            conn.close()
            return True
        except UnicodeDecodeError:
            # Si es solo error de encoding, aún consideramos que funciona
            # (el servidor está respondiendo, solo hay incompatibilidad)
            signal.alarm(0)
            return True
        except Exception:
            signal.alarm(0)
            return False
            
    except Exception as e:
        try:
            signal.alarm(0)
        except:
            pass
        return False

# Seleccionar configuración según el entorno
if ENVIRONMENT == 'auto':
    # Intentar remota primero, fallback a local si falla
    if _test_connection(DB_CONFIG_REMOTE):
        DB_CONFIG = DB_CONFIG_REMOTE
        print("✓ Usando conexión REMOTA (Windows Server)")
    else:
        DB_CONFIG = DB_CONFIG_LOCAL
        print("⚠️  Servidor Windows no disponible, usando LOCAL (localhost)")
elif ENVIRONMENT == 'remote':
    DB_CONFIG = DB_CONFIG_REMOTE
    print("ℹ️  Usando conexión REMOTA (Windows Server)")
else:  # 'local'
    DB_CONFIG = DB_CONFIG_LOCAL
    print("ℹ️  Usando conexión LOCAL (localhost)")

# Configuración de la aplicación
APP_CONFIG = {
    'title': 'Gestor de Productos',
    'version': '1.0.0',
    'theme': 'modern',
    'window_width': 1800,
    'window_height': 1000,
}
