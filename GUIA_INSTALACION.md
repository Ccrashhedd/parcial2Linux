# 📚 GUÍA DE INSTALACIÓN Y USO - Gestor de Productos

## 🎯 Pasos Iniciales

### Paso 1: Instalar PostgreSQL (si no está instalado)

```bash
sudo dnf install postgresql postgresql-server postgresql-contrib
```

O si usas Debian/Ubuntu:

```bash
sudo apt install postgresql postgresql-contrib
```

### Paso 2: Iniciar el servicio de PostgreSQL

```bash
# Fedora
sudo systemctl start postgresql

# Debian/Ubuntu
sudo service postgresql start
```

Verificar que está corriendo:

```bash
sudo systemctl status postgresql
```

### Paso 3: Instalar Python 3 y pip (si no está instalado)

```bash
# Fedora
sudo dnf install python3 python3-pip

# Debian/Ubuntu
sudo apt install python3 python3-pip
```

### Paso 4: Ir al directorio del proyecto

```bash
cd "/home/angelbroce/Documentos/linux phyton/gestor_productos"
```

### Paso 5: Instalar las dependencias de Python

```bash
./instalar.sh
```

O manualmente:

```bash
pip3 install -r requirements.txt
```

### Paso 6: Crear la base de datos

```bash
./database/crear_bd.sh
```

El script te pedirá:
- **Usuario PostgreSQL**: postgres (presiona Enter para el default)
- **Contraseña**: tu_contraseña_postgres

### Paso 7: Ejecutar la aplicación

```bash
./ejecutar.sh
```

O directamente:

```bash
python3 main.py
```

## 🎨 Cómo Usar la Aplicación

### Crear un nuevo producto

1. Click en botón verde **✨ NUEVO**
2. Completa los campos:
   - **Nombre**: Nombre del producto
   - **Precio**: Precio en formato numérico (ej: 99.99)
   - **Descripción**: Descripción detallada
3. Click en **💾 GUARDAR**

### Editar un producto existente

1. **Doble clic** en el producto en la tabla
2. El formulario se llenará con los datos
3. Modifica lo que quieras
4. Click en **💾 GUARDAR**

### Eliminar un producto

1. Selecciona el producto en la tabla
2. Click en **🗑️ ELIMINAR**
3. Confirma la acción en el diálogo

### Buscar productos

1. Escribe en el campo **🔍 Buscar producto**
2. Los resultados se filtran en tiempo real
3. Click en **❌ Limpiar** para ver todos

### Imprimir todos los productos

1. Click en botón naranja **🖨️ IMPRIMIR**
2. Se abrirá un documento HTML bonito en tu navegador
3. Usa Ctrl+P o el menú de impresión del navegador

## 🔐 Cambiar Contraseña de Base de Datos

Si quieres cambiar la contraseña de PostgreSQL:

1. Edita `config.py`:
   ```python
   DB_CONFIG = {
       'password': 'tu_nueva_contraseña',
       ...
   }
   ```

2. También cambia en PostgreSQL:
   ```bash
   sudo -u postgres psql
   # En la consola de PostgreSQL:
   ALTER USER postgres WITH PASSWORD 'tu_nueva_contraseña';
   \q
   ```

## 🆘 Solución de Problemas

### Problema: "No se puede conectar a la base de datos"

**Solución 1**: Verificar que PostgreSQL está corriendo
```bash
sudo systemctl status postgresql
```

Si no está corriendo, inicia:
```bash
sudo systemctl start postgresql
```

**Solución 2**: Verificar credenciales en `config.py`
- Usuario: postgres (default)
- Password: la que ingresaste en la instalación

**Solución 3**: Recrear la base de datos
```bash
./database/crear_bd.sh
```

### Problema: "ModuleNotFoundError: psycopg2"

```bash
pip3 install -r requirements.txt
```

### Problema: "No se puede ejecutar main.py"

```bash
chmod +x main.py
python3 main.py
```

### Problema: "Puerto 5432 ya en uso"

```bash
sudo systemctl restart postgresql
```

## 📁 Estructura de Archivos Importante

```
gestor_productos/
├── main.py                 ← Ejecuta aquí para iniciar
├── config.py              ← Edita credenciales DB aquí
├── requirements.txt       ← Dependencias de Python
├── ejecutar.sh            ← Script para ejecutar
├── instalar.sh            ← Script para instalar
├── database/
│   ├── schema.sql         ← Estructura de BD
│   └── crear_bd.sh        ← Ejecuta para crear BD
└── src/
    ├── gui.py             ← Interfaz gráfica
    ├── database.py        ← Conexión a BD
    └── impresora.py       ← Funcionalidad de impresión
```

## 🎯 Comandos Rápidos

```bash
# Abrir la aplicación
cd /home/angelbroce/Documentos/linux\ phyton/gestor_productos
./ejecutar.sh

# Crear la BD por primera vez
./database/crear_bd.sh

# Conectar directamente a PostgreSQL
psql -U postgres -d gestor_productos

# Ver todas las tablas en la BD
# (Dentro de psql):
\dt

# Salir de psql
\q

# Resetear la BD completa
dropdb -U postgres gestor_productos
./database/crear_bd.sh
```

## 📊 Ejemplo de Datos

La aplicación viene con ejemplos:
- Laptop Dell - $799.99
- Mouse Logitech - $25.50
- Teclado Mecánico - $89.99
- Monitor LG 24" - $199.99
- Webcam Logitech - $45.00

Puedes eliminarlos y crear los tuyos.

## 🎨 Personalización

### Cambiar colores

Edita `src/gui.py` línea 55-60:
```python
self.color_primario = "#2196F3"  # Azul
self.color_exito = "#4CAF50"     # Verde
self.color_error = "#F44336"     # Rojo
```

### Cambiar tamaño de ventana

Edita `config.py` línea 16-17:
```python
'window_width': 1200,
'window_height': 700,
```

## 📞 Contacto y Soporte

Si tienes problemas:

1. Verifica los logs en la consola
2. Comprueba que PostgreSQL está corriendo
3. Verifica las credenciales en `config.py`
4. Intenta recrear la base de datos

## ✅ Checklist de Instalación

- [ ] PostgreSQL instalado y corriendo
- [ ] Python 3.8+ instalado
- [ ] pip3 instalado
- [ ] Dependencias instaladas (./instalar.sh)
- [ ] Base de datos creada (./database/crear_bd.sh)
- [ ] Contraseña de config.py coincide con PostgreSQL
- [ ] Puedo ejecutar la aplicación (./ejecutar.sh)

---

¡Listo! Tu Gestor de Productos está funcionando. 🎉
