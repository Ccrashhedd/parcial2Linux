# 🔧 Cambiar IP del Servidor Remoto

Si cambias de red/internet y la IP del servidor Windows cambió, sigue estos pasos:

## 📝 Opción 1: Editar server_config.txt (RECOMENDADO)

1. Abre el archivo `server_config.txt` en el editor de texto
2. Busca la línea `SERVER_IP=192.168.50.126`
3. Reemplaza la IP con la nueva IP del servidor Windows
4. Guarda el archivo
5. Reinicia la aplicación

**Ejemplo:**
```
# Antes:
SERVER_IP=192.168.50.126

# Después (si la nueva IP es 192.168.1.50):
SERVER_IP=192.168.1.50
```

## 🖥️ ¿Cómo encontrar la IP del servidor Windows?

**En Windows (servidor):**
1. Abre cmd o PowerShell
2. Ejecuta: `ipconfig`
3. Busca "IPv4 Address" en "Ethernet adapter"

**Desde Linux (cliente):**
1. En terminal: `ping nombre-del-pc-windows` (si está en la red)
2. O usa: `arp -a` para listar IPs activas

## 🔄 Opciones de Conexión

- **LOCAL**: `APP_ENV=local python3 main.py` (BD en localhost)
- **REMOTO**: `APP_ENV=remote python3 main.py` (BD en servidor Windows)
- **AUTO** (default): Intenta remota, fallback a local

## 💡 Alternativas futuras

Para evitar cambios de IP:
1. Usar **hostname** en lugar de IP (si el router lo permite)
2. Configurar **IP estática** en el servidor Windows
3. Usar **DNS dinámico** si el servidor tiene dominio

