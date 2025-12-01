# 🎯 Gestor de Productos - Instalación y Ejecución

## ✅ ¿Qué se instaló?

La aplicación **Gestor de Productos** está lista para usar. Aquí está lo que se configuró:

### 📦 Paquetes Instalados:
- ✅ Python 3.13.9
- ✅ psycopg2-binary (driver PostgreSQL)
- ✅ Pillow (procesamiento de imágenes)
- ✅ PyGObject y PyCAIRO (GTK para interfaz gráfica)

### 🗄️ Base de Datos:
- Conecta a **WIN-E6SQ6ALCVS5** (servidor Windows)
- Usuario: `postgres`
- Contraseña: `postgres123`
- Puerto: `5432`
- BD: `gestor_productos`

---

## 🚀 ¿Cómo Ejecutar?

### Opción 1️⃣: Desde el Escritorio (RECOMENDADO)
1. Busca el icono **"GestorProductos"** en tu escritorio
2. Haz doble clic para ejecutar

### Opción 2️⃣: Desde el Menú de Aplicaciones
1. Abre el menú de aplicaciones
2. Busca **"Gestor de Productos"**
3. Haz clic para ejecutar

### Opción 3️⃣: Desde la Terminal
```bash
cd "/home/angelbroce/Documentos/linux phyton/gestor_productos"
./ejecutar.sh
```

### Opción 4️⃣: Directamente con Python
```bash
cd "/home/angelbroce/Documentos/linux phyton/gestor_productos"
python3 main.py
```

---

## ⚙️ Configuración

### Cambiar Servidor (BD Remota)

Si la IP del servidor Windows cambia:

```bash
# Edita el archivo de configuración
nano /home/angelbroce/Documentos/linux\ phyton/gestor_productos/server_config.txt
```

Cambia estos valores:
```ini
SERVER_IP=WIN-E6SQ6ALCVS5      # Hostname del servidor
SERVER_USER=postgres            # Usuario PostgreSQL
SERVER_PASSWORD=postgres123      # Contraseña
SERVER_PORT=5432                # Puerto PostgreSQL
```

Luego reinicia la aplicación.

### Usar Base de Datos Local

Si prefieres usar PostgreSQL en tu máquina Linux:

```bash
# Inicia PostgreSQL
sudo systemctl start postgresql

# Configura la BD local
cd /home/angelbroce/Documentos/linux\ phyton/gestor_productos
chmod +x setup_db.sh
./setup_db.sh
```

---

## 🔍 Verificar Conexión

### Verificar que el servidor Windows es accesible:
```bash
ping WIN-E6SQ6ALCVS5
```

### Verificar que PostgreSQL responde:
```bash
psql -h WIN-E6SQ6ALCVS5 -U postgres -d gestor_productos -c "SELECT 1"
```

---

## 📋 Características de la Aplicación

✨ **Gestión de Productos:**
- Crear, editar, eliminar productos
- Buscar y filtrar productos
- Seleccionar múltiples productos

🖼️ **Gestión de Imágenes:**
- Subir imágenes desde archivos
- Ingresar URLs de imágenes
- Previsualizar imágenes en tiempo real
- Las imágenes se guardan en la base de datos

🖨️ **Impresión:**
- Imprimir productos individuales
- Imprimir múltiples productos seleccionados
- Etiquetas de productos

---

## 🛠️ Compilar como Ejecutable (Opcional)

Si quieres crear un ejecutable independiente:

```bash
cd /home/angelbroce/Documentos/linux\ phyton/gestor_productos
python3 build_executable.py
```

El ejecutable se creará en: `dist/GestorProductos`

---

## ⚠️ Solución de Problemas

### Problema: "No puedo conectar al servidor Windows"

**Solución:**
```bash
# Verifica que el servidor está en línea
ping WIN-E6SQ6ALCVS5

# Verifica que PostgreSQL está corriendo en Windows
# (Pídele al administrador del servidor que lo reinicie)
```

### Problema: "La aplicación se congela al iniciar"

**Solución:**
```bash
# Ejecuta directamente con Python para ver los errores
python3 main.py

# Si dice "servidor no disponible", usa BD local:
./setup_db.sh
```

### Problema: "No veo las imágenes que guardé"

**Solución:**
Reinicia la aplicación. Las imágenes se cargan desde la BD al abrir.

---

## 📚 Documentación Adicional

- **`COMPILAR_EJECUTABLE.md`** - Crear ejecutables Linux
- **`CAMBIAR_IP_SERVIDOR.md`** - Cambiar servidor dinámicamente
- **`README.md`** - Información general del proyecto

---

## 📞 Resumen Técnico

**Ubicación:** `/home/angelbroce/Documentos/linux phyton/gestor_productos`

**Archivos Importantes:**
- `main.py` - Punto de entrada
- `ejecutar.sh` - Script para ejecutar
- `server_config.txt` - Configuración del servidor
- `config.py` - Configuración de BD
- `src/gui.py` - Interfaz gráfica
- `src/database_psql.py` - Operaciones de BD
- `src/impresora.py` - Funcionalidad de impresión

**Dependencias:**
- Python 3.8+
- PostgreSQL (local o remoto)
- GTK 3.0
- Cairo

---

## ✅ Estado Actual

✓ Instalación completada
✓ Dependencias Python instaladas
✓ Acceso directo en el escritorio creado
✓ Configuración del servidor remota lista
✓ Aplicación lista para usar

**¡Ahora puedes hacer doble clic en GestorProductos en el escritorio para ejecutar!** 🎉

