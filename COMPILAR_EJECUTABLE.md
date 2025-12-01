# Compilar Gestor de Productos como Ejecutable Linux

Este documento explica cómo convertir la aplicación Python en un ejecutable Linux independiente.

## Requisitos Previos

### Dependencias del Sistema
```bash
sudo apt update
sudo apt install -y \
    python3 \
    python3-pip \
    python3-dev \
    libgtk-3-0 \
    libcairo2 \
    libglib2.0-0 \
    libpango-1.0-0
```

### Dependencias de Python
```bash
pip3 install -r requirements.txt
pip3 install pyinstaller
```

## Compilar el Ejecutable

### Opción 1: Script Automático (RECOMENDADO)

```bash
cd /ruta/a/gestor_productos
python3 build_executable.py
```

Este script:
- ✅ Compila la aplicación con PyInstaller
- ✅ Incluye todas las dependencias necesarias
- ✅ Empaqueta el archivo `server_config.txt`
- ✅ Crea un ejecutable en `dist/GestorProductos`

### Opción 2: Manual con PyInstaller

```bash
cd /ruta/a/gestor_productos

pyinstaller main.py \
    --name=GestorProductos \
    --onefile \
    --windowed \
    --add-data="server_config.txt:." \
    --add-data="config.py:." \
    --add-data="src:src" \
    --hidden-import=psycopg2 \
    --hidden-import=PIL \
    --hidden-import=gi \
    --collect-all=gi \
    --collect-all=cairo \
    --collect-all=PIL \
    --collect-all=psycopg2
```

## Resultado

Después de compilar, encontrarás:

```
gestor_productos/
├── dist/
│   └── GestorProductos          ← Ejecutable final
├── build/                        ← Archivos temporales
├── GestorProductos.spec         ← Especificaciones de PyInstaller
└── ... (otros archivos)
```

## Ejecutar la Aplicación

### Desde el Ejecutable Compilado

```bash
./dist/GestorProductos
```

### Usando el Script `ejecutar.sh`

```bash
chmod +x ejecutar.sh
./ejecutar.sh
```

El script `ejecutar.sh` automáticamente:
1. Busca el ejecutable compilado en `dist/GestorProductos`
2. Si existe, lo ejecuta
3. Si no existe, ejecuta con Python 3 como fallback

## Distribuir la Aplicación

Para distribuir a otros usuarios:

```bash
# Crear carpeta de distribución
mkdir GestorProductos_v1.0
cp dist/GestorProductos GestorProductos_v1.0/
cp server_config.txt GestorProductos_v1.0/
cp ejecutar.sh GestorProductos_v1.0/

# Hacer ejecutables
chmod +x GestorProductos_v1.0/GestorProductos
chmod +x GestorProductos_v1.0/ejecutar.sh

# Comprimir
tar -czf GestorProductos_v1.0.tar.gz GestorProductos_v1.0/
```

Los usuarios pueden descargar, extraer y ejecutar:

```bash
tar -xzf GestorProductos_v1.0.tar.gz
cd GestorProductos_v1.0
./ejecutar.sh
```

## Configuración del Servidor

Antes de distribuir, actualiza `server_config.txt` con los datos correctos:

```ini
# Configuración del servidor remoto
SERVER_IP=WIN-E6SQ6ALCVS5
SERVER_USER=postgres
SERVER_PASSWORD=postgres123
SERVER_PORT=5432
```

## Solución de Problemas

### Error: "Cannot find module psycopg2"

```bash
pip3 install psycopg2-binary
python3 build_executable.py
```

### Error: "GTK not found"

```bash
sudo apt install libgtk-3-0 gir1.2-gtk-3.0
python3 build_executable.py
```

### Ejecutable muy grande (> 500 MB)

Esto es normal con PyInstaller + GTK. Para reducir tamaño:

```bash
strip dist/GestorProductos
upx dist/GestorProductos  # Requiere: sudo apt install upx
```

### Problemas de conexión a PostgreSQL

Verifica que:
1. PostgreSQL esté corriendo en Windows Server
2. El hostname `WIN-E6SQ6ALCVS5` sea accesible desde Linux
3. Las credenciales en `server_config.txt` sean correctas

Prueba la conexión:
```bash
ping WIN-E6SQ6ALCVS5
psql -h WIN-E6SQ6ALCVS5 -U postgres -d gestor_productos
```

## Actualizaciones Futuras

Para recompilar después de cambios:

1. Edita el código Python normalmente
2. Ejecuta: `python3 build_executable.py`
3. El nuevo ejecutable estará en `dist/GestorProductos`

## Compatibilidad

El ejecutable funciona en:
- ✅ Ubuntu 20.04 LTS+
- ✅ Ubuntu 22.04 LTS+
- ✅ Fedora 37+
- ✅ Debian 11+
- ✅ Cualquier distro Linux moderna con libgtk-3-0

## Notas de Rendimiento

- **Primera ejecución**: Puede tardar más (se desempaquetan archivos)
- **Uso de memoria**: Similar al script Python (~80-120 MB)
- **Velocidad**: Idéntica al Python puro
- **Tamaño**: ~400-500 MB (incluye todas las librerías)
