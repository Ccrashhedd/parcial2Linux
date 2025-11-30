# 📦 Gestor de Productos

Una aplicación moderna y completa para gestionar productos con interfaz gráfica basada en Python, PostgreSQL e interfaz tkinter.

## ✨ Características

- ✅ **Interfaz moderna y bonita** con tkinter
- ✅ **Gestión CRUD** (Crear, Leer, Actualizar, Eliminar)
- ✅ **Base de datos PostgreSQL** robusta
- ✅ **Búsqueda en tiempo real** de productos
- ✅ **Impresión nativa** usando el diálogo oficial de GNOME
- ✅ **Previas HTML/PDF automáticas** como respaldo
- ✅ **Validaciones** de datos
- ✅ **Interfaz responsiva** y profesional

## 📋 Requisitos

- Python 3.8 o superior
- PostgreSQL 12 o superior
- pip (gestor de paquetes de Python)
- tkinter (generalmente viene con Python)
- PyGObject (GTK+3), Cairo y Pango instalados en el sistema (`sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-pango-1.0 libcairo2`)

## 🚀 Instalación Rápida

### 1. Clonar o descargar el proyecto

```bash
cd gestor_productos
```

### 2. Instalar dependencias de Python

```bash
chmod +x instalar.sh
./instalar.sh
```

O manualmente:

```bash
pip3 install -r requirements.txt
```

### 3. Crear la base de datos

```bash
chmod +x database/crear_bd.sh
./database/crear_bd.sh
```

Se te pedirá:
- Usuario de PostgreSQL (default: postgres)
- Contraseña de PostgreSQL

### 4. Ejecutar la aplicación

```bash
chmod +x ejecutar.sh
./ejecutar.sh
```

O directamente:

```bash
python3 main.py
```

## 📁 Estructura del Proyecto

```
gestor_productos/
├── main.py                 # Punto de entrada principal
├── config.py              # Configuración de la aplicación
├── requirements.txt       # Dependencias de Python
├── instalar.sh            # Script de instalación
├── ejecutar.sh            # Script para ejecutar la app
├── database/
│   ├── schema.sql         # Esquema de base de datos
│   └── crear_bd.sh        # Script para crear la BD
├── src/
│   ├── gui.py             # Interfaz gráfica
│   ├── database.py        # Operaciones de base de datos
│   └── impresora.py       # Módulo de impresión
└── images/                # Imágenes de productos
```

## 🔧 Configuración

Edita el archivo `config.py` para cambiar la conexión de base de datos:

### Conexión LOCAL (PostgreSQL en Linux local)

```python
# En config.py, la aplicación usará:
DB_CONFIG_LOCAL = {
    'host': 'localhost',
    'database': 'gestor_productos',
    'user': 'postgres',
    'password': 'tu_contraseña',
    'port': 5432
}

# Ejecutar con:
APP_ENV=local python3 main.py
```

### Conexión REMOTA (PostgreSQL en Windows Server)

```python
# En config.py, modifica DB_CONFIG_REMOTE con:
DB_CONFIG_REMOTE = {
    'host': '192.168.1.100',  # IP o hostname de Windows Server
    'database': 'gestor_productos',
    'user': 'postgres',
    'password': 'tu_contraseña',
    'port': 5432
}

# Ejecutar con (por defecto):
python3 main.py
# O explícitamente:
APP_ENV=remote python3 main.py
```

### Cambiar entre LOCAL y REMOTO

```bash
# Usar base de datos LOCAL (Linux)
export APP_ENV=local
python3 main.py

# Usar base de datos REMOTA (Windows Server) - por defecto
unset APP_ENV
python3 main.py
```

## 📖 Uso de la Aplicación

### Crear un nuevo producto

1. Haz clic en el botón **✨ NUEVO**
2. Completa los campos: Nombre, Precio y Descripción
3. Si la imagen está en internet, usa el botón **🌐 URL** y pega la dirección (http/https). La aplicación guardará esa URL tal cual, sin copiar archivos temporales.
4. Haz clic en **💾 GUARDAR**

### Editar un producto

1. Haz doble clic en la fila del producto en la tabla
2. El producto se cargará en el formulario
3. Modifica los campos
4. Haz clic en **💾 GUARDAR**

### Eliminar un producto

1. Selecciona el producto en la tabla
2. Haz clic en **🗑️ ELIMINAR**
3. Confirma la eliminación

### Buscar productos

1. Escribe en el campo **🔍 Buscar producto**
2. Los resultados se filtran automáticamente
3. Haz clic en **❌ Limpiar** para ver todos

### Imprimir productos

1. Selecciona uno o varios productos (Ctrl+clic para selección múltiple)
2. Haz clic en el botón **🖨️ IMPRIMIR**
3. Se abrirá el **diálogo de impresión nativo de GNOME** mostrando una página por producto
4. Desde allí puedes elegir impresora, rango de páginas o guardar en PDF
5. Si el entorno no tiene GTK disponible, la app genera automáticamente un PDF/HTML como respaldo y lo abre con el visor predeterminado

## 📊 Base de Datos

### Tabla: productos

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | SERIAL | Identificador único |
| nombre | VARCHAR(255) | Nombre del producto |
| precio | DECIMAL(10,2) | Precio del producto |
| descripcion | TEXT | Descripción detallada |
| imagen_data | BYTEA | Datos de imagen comprimida |
| fecha_creacion | TIMESTAMP | Fecha de creación |
| fecha_actualizacion | TIMESTAMP | Fecha de última actualización |

## 🎨 Diseño

La aplicación utiliza:

- **Tema moderno** con colores profesionales
- **Interfaz responsiva** que se ajusta al tamaño de la ventana
- **Iconos emoji** para mejor visualización
- **Colores consistentes**:
  - Azul (#2196F3) - Primario
  - Verde (#4CAF50) - Éxito
  - Rojo (#F44336) - Error
  - Naranja (#FF9800) - Advertencia

## 🐛 Solución de Problemas

### Error: "No se puede conectar a PostgreSQL"

1. Verifica que PostgreSQL esté instalado: `psql --version`
2. Verifica que el servicio está corriendo: `sudo service postgresql status`
3. Comprueba las credenciales en `config.py`

### Error: "Módulo no encontrado"

```bash
pip3 install -r requirements.txt
```

### Error: "Port 5432 ya está en uso"

```bash
sudo service postgresql restart
```

## 📝 Comandos Útiles

```bash
# Ver estado de PostgreSQL
sudo service postgresql status

# Reiniciar PostgreSQL
sudo service postgresql restart

# Conectar directamente a la BD
psql -U postgres -d gestor_productos

# Ver todas las bases de datos
psql -l

# Eliminar la base de datos (PELIGRO)
dropdb -U postgres gestor_productos
```

## 📦 Dependencias

- **psycopg2-binary** - Driver de PostgreSQL para Python
- **Pillow** - Manejo y compresión de imágenes en la interfaz

## 🔐 Seguridad

- La contraseña de PostgreSQL no se almacena en el código (edítala en config.py)
- Se usan consultas parametrizadas para prevenir SQL injection
- Los datos se validan antes de guardar

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso personal y educativo.

## 👨‍💻 Desarrollo

Para extender la aplicación:

1. Agrega nuevos campos a `database/schema.sql`
2. Actualiza `src/database.py` con los nuevos métodos
3. Modifica `src/gui.py` para agregar nuevos campos a la interfaz

## 📞 Soporte

Para reportar problemas o sugerencias, revisa:
- Los logs en la consola
- El estado de PostgreSQL
- Las credenciales en `config.py`

---

**Versión:** 1.0.0  
**Última actualización:** Noviembre 2025  
**Desarrollado con:** Python 3 + PostgreSQL + tkinter
