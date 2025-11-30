# Conexión a PostgreSQL en Windows Server

## Estado Actual

**✅ IP alcanzable:** `192.168.50.126` (ping OK)  
**✅ Puerto abierto:** `5432` (TCP conecta)  
**⚠️ Problema de Encoding:** UnicodeDecodeError en handshake PostgreSQL  
**✅ Solución Implementada:** Fallback automático a BD local

## Problema Identificado

```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xed in position 80
```

Este error ocurre en el handshake inicial de psycopg2 con PostgreSQL en Windows.

**Causa probable:** La BD en Windows Server usa un encoding diferente a UTF-8 (ej: LATIN1, CP1252)

## Solución Actual: Fallback Automático

La aplicación ahora usa una estrategia inteligente:

```bash
# Por defecto (RECOMENDADO):
python3 main.py
# → Intenta Windows Server → Si falla → USA BD LOCAL automáticamente

# Forzar local:
APP_ENV=local python3 main.py

# Forzar remoto (solo si está configurado en Windows):
APP_ENV=remote python3 main.py
```

## Configuración en Windows Server (Para Solucionar)

Si deseas arreglarlo en Windows y usar la conexión remota:

### 1. Verificar Encoding de la BD

```sql
-- En pgAdmin o psql de Windows:
SELECT datname, pg_encoding_to_char(encoding) 
FROM pg_database 
WHERE datname='gestor_productos';
```

Si no es **UTF8**, recrear:
```sql
DROP DATABASE gestor_productos;

CREATE DATABASE gestor_productos 
  ENCODING 'UTF8'
  LC_COLLATE 'C'
  LC_CTYPE 'C';

-- O con locale específica:
CREATE DATABASE gestor_productos 
  ENCODING 'UTF8'
  LC_COLLATE 'en_US.UTF-8'
  LC_CTYPE 'en_US.UTF-8';
```

### 2. Revisar Configuración de PostgreSQL

En `C:\Program Files\PostgreSQL\XX\data\postgresql.conf`:

```conf
# Uncomment and set to UTF-8:
lc_messages = 'C'
lc_monetary = 'C'
lc_numeric = 'C'
lc_time = 'C'
```

### 3. Reiniciar PostgreSQL

```powershell
Restart-Service postgresql-x64-XX
# O desde Services (services.msc)
```

### 4. Probar Conexión Local en Windows

```powershell
# En Windows Server:
psql -U postgres -d gestor_productos -c "SELECT version();"
```

### 5. Probar desde Linux

```bash
APP_ENV=remote python3 main.py
```

## Arquitectura de Fallback

```
┌─────────────────────────────────┐
│ Aplicación (main.py)            │
└──────────────┬──────────────────┘
               │
        Selecciona BD
               │
        ┌──────┴──────┐
        │             │
        ▼             ▼
   Windows Server   LocalHost
  (192.168.50.126)  (localhost)
        │             │
        │ Error?      │
        └─────┬───────┘
              │
              ▼
        Usa BD LOCAL
        (Always works!)
```

## Archivos Relevantes

- `config.py` - Configuración de conexión (LOCAL vs REMOTE)
- `src/database.py` - Clase BaseDatos que maneja la conexión
- `README.md` - Documentación general

## Estado del Proyecto

✅ **Aplicación funcionando con BD local**  
✅ **Fallback automático implementado**  
✅ **IP y puerto Windows accesibles**  
⏳ **Esperando configuración UTF-8 en Windows Server para usar remoto**



