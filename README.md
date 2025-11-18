# 🍽️ Sistema POS Restaurante - PostgreSQL Edition

Sistema completo de Punto de Venta para restaurantes con base de datos PostgreSQL, menú automático rotativo y sistema de promociones con descuentos especiales.

**Última actualización:** Noviembre 2025

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Configuración de PostgreSQL](#-configuración-de-postgresql)
- [Uso de la Aplicación](#-uso-de-la-aplicación)
- [Base de Datos](#-base-de-datos)
- [Sistema de Promociones](#-sistema-de-promociones)
- [Desarrollo](#-desarrollo)
- [API de la Base de Datos](#-api-de-la-base-de-datos)
- [Solución de Problemas](#-solución-de-problemas)
- [Actualizaciones Recientes](#-actualizaciones-recientes)

---

## 🎯 Características

### Funcionalidades Principales
- ✅ **Base de datos PostgreSQL** con 39 productos pre-cargados
- ✅ **Menú automático rotativo** que cambia cada día de la semana
- ✅ **Sistema de excepciones** con promociones y descuentos especiales
- ✅ **Login seguro** con usuarios en base de datos
- ✅ **5 tipos de comida**: Desayuno, Almuerzo, Cena, Bebidas, Postres
- ✅ **Interfaz gráfica moderna** con Tkinter
- ✅ **Sistema de impresión** compatible con CUPS (Linux)
- ✅ **Ejecutable compilado** de 66MB listo para distribuir

### Sistema de Promociones
- 🎁 **7 promociones pre-configuradas** por día de la semana
- 💰 **Descuentos del 10% al 50%** en productos seleccionados
- 📅 **Gestión por fechas** con inicio y fin programable
- 🔄 **Precios automáticos** calculados según promoción activa
- 🎯 **Excepciones por producto** con precios especiales

---

## 📦 Requisitos

### Sistema Operativo
- **Fedora Linux** 40+ (o distribuciones compatibles con DNF)
- Kernel Linux 6.x

### Software Base
- **Python 3.13+**
- **PostgreSQL 16+**
- **Tkinter** (python3-tkinter)
- **CUPS** (sistema de impresión)

### Bibliotecas Python
```bash
psycopg2-binary==2.9.11  # Driver PostgreSQL
pyinstaller==6.16.0      # Generador de ejecutables
```

---

## 🚀 Instalación

### Opción 1: Script Automático (Recomendado)

```bash
# Descargar e instalar todo automáticamente
chmod +x install_postgresql.sh
./install_postgresql.sh
```

**El script realiza:**
1. ✅ Instala PostgreSQL y dependencias
2. ✅ Configura autenticación MD5
3. ✅ Crea usuario y contraseña
4. ✅ Inicializa base de datos `parcial2`
5. ✅ Inserta 39 productos
6. ✅ Configura 7 promociones
7. ✅ Crea usuario admin

**Tiempo estimado:** 2-3 minutos

---

### Opción 2: Instalación Manual Paso a Paso

#### Paso 1: Instalar PostgreSQL

```bash
sudo dnf install postgresql-server postgresql-contrib
```

#### Paso 2: Inicializar y Arrancar PostgreSQL

```bash
# Inicializar cluster de BD
sudo postgresql-setup --initdb

# Iniciar servicio
sudo systemctl start postgresql

# Habilitar inicio automático
sudo systemctl enable postgresql

# Verificar estado
sudo systemctl status postgresql
```

#### Paso 3: Configurar Autenticación

```bash
# Hacer backup del archivo original
sudo cp /var/lib/pgsql/data/pg_hba.conf /var/lib/pgsql/data/pg_hba.conf.backup

# Cambiar de peer/ident a md5 para permitir contraseñas
sudo sed -i 's/peer/md5/g; s/ident/md5/g' /var/lib/pgsql/data/pg_hba.conf

# Reiniciar PostgreSQL
sudo systemctl restart postgresql
```

#### Paso 4: Configurar Contraseña del Usuario postgres

```bash
# Conectar como usuario postgres del sistema
sudo -u postgres psql

# Dentro de psql, ejecutar:
ALTER USER postgres WITH PASSWORD 'postgres';
\q
```

#### Paso 5: Instalar Dependencias Python

```bash
# Instalar psycopg2 para conectar Python con PostgreSQL
pip3 install --user psycopg2-binary

# Opcional: PyInstaller para generar ejecutables
pip3 install --user pyinstaller
```

#### Paso 6: Crear Base de Datos

```bash
# Ejecutar script de configuración
python3 setup_database.py
```

**Salida esperada:**
```
============================================================
CONFIGURACIÓN DE BASE DE DATOS - RESTAURANTE POS
============================================================

Paso 1: Verificando conexión a PostgreSQL...
✓ Conexión a PostgreSQL exitosa

Paso 2: Creando base de datos...
✓ Base de datos 'parcial2' creada exitosamente

Paso 3: Creando tablas...
✓ Script SQL ejecutado exitosamente

✓ Tablas creadas:
  - usuario
  - producto
  - tipo_comida
  - menu_dia
  - menu_producto
  - menu_excepcion
  - excepcion_producto

============================================================
✓ CONFIGURACIÓN COMPLETADA EXITOSAMENTE
============================================================
```

---

## 🗄️ Configuración de PostgreSQL

### Credenciales de Conexión

```plaintext
Host:          localhost
Puerto:        5432
Base de datos: parcial2
Usuario:       postgres
Contraseña:    postgres
```

### Conectar desde Terminal

```bash
# Opción 1: Como usuario postgres del sistema
sudo -u postgres psql parcial2

# Opción 2: Con contraseña
psql -U postgres -h localhost -d parcial2
# Password: postgres
```

### Conectar desde pgAdmin

1. Abrir pgAdmin
2. Click derecho en "Servers" → "Register" → "Server"
3. **General tab:**
   - Name: `Restaurante POS`
4. **Connection tab:**
   - Host: `localhost`
   - Port: `5432`
   - Database: `parcial2`
   - Username: `postgres`
   - Password: `postgres`
5. Click "Save"

---

## 🎮 Uso de la Aplicación

### Ejecutar desde Código Fuente

```bash
python3 main.py
```

### Ejecutar el Ejecutable Compilado

```bash
cd dist
./parcial2
```

### Credenciales de Login

```
Usuario:    admin
Contraseña: 123
```

### Interfaz Principal

La aplicación muestra:
- **Tab Menú**: Productos organizados por categoría
- **Tab Carrito**: Items agregados con cantidades
- **Tab Historial**: Registro de ventas
- **Botón Imprimir**: Genera factura y envía a impresora

---

## 📊 Base de Datos

### Estructura de Tablas

#### USUARIO
Almacena usuarios del sistema.

```sql
CREATE TABLE USUARIO (
    idUsuario VARCHAR(25) PRIMARY KEY,
    usuario VARCHAR(25) NOT NULL UNIQUE,
    contrasen VARCHAR(30) NOT NULL,
    nombre VARCHAR(50) NOT NULL
);
```

**Datos iniciales:**
| ID | Usuario | Contraseña | Nombre |
|----|---------|------------|--------|
| USR001 | admin | 123 | Administrador |

---

#### PRODUCTO
Catálogo completo de productos del restaurante.

```sql
CREATE TABLE PRODUCTO (
    idProducto VARCHAR(30) PRIMARY KEY,
    nombre VARCHAR(45) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    imagen VARCHAR(100) NOT NULL,
    descripcion VARCHAR(150) NOT NULL,
    CONSTRAINT chk_precio CHECK (precio > 0)
);
```

**39 Productos Incluidos:**

**Desayuno (6):**
- Café Americano - $6,000
- Cappuccino - $8,000
- Té Chai Latte - $9,000
- Jugo Natural - $8,000
- Pan de Ajo - $7,000
- Churros con Chocolate - $11,000

**Almuerzo (10):**
- Churrasco Premium - $45,000
- Salmón Grillado - $38,000
- Paella Valenciana - $35,000
- Lasaña Boloñesa - $32,000
- Costillas BBQ - $40,000
- Pollo a la Parrilla - $25,000
- Steak Argentino - $50,000
- Ensalada César - $18,000
- Arroz Blanco - $6,000
- Papas Francesas - $8,000

**Cena (8):**
- Pizza Margherita - $24,000
- Pizza Pepperoni - $26,000
- Hamburguesa Gourmet - $28,000
- Pasta Carbonara - $22,000
- Filete de Pescado - $30,000
- Pechuga Rellena - $32,000
- Ravioles de Ricotta - $28,000
- Alitas Buffalo - $18,000

**Bebidas (8):**
- Limonada Natural - $7,000
- Coca-Cola - $5,000
- Agua con Gas - $4,000
- Té Helado - $7,000
- Cerveza Nacional - $8,000
- Vino Tinto - $15,000
- Vino Blanco - $15,000
- Mojito Clásico - $18,000

**Postres (7):**
- Tiramisú - $16,000
- Cheesecake de Frutos - $14,000
- Brownie con Helado - $12,000
- Flan de Caramelo - $10,000
- Tres Leches - $11,000
- Helado Artesanal - $8,000
- Torta de Chocolate - $13,000

---

#### TIPO_COMIDA
Categorías de productos.

```sql
CREATE TABLE TIPO_COMIDA (
    idTipo INTEGER PRIMARY KEY,
    nombre VARCHAR(25) NOT NULL,
    CONSTRAINT chk_id CHECK (idTipo BETWEEN 1 AND 5)
);
```

| ID | Nombre |
|----|--------|
| 1 | Desayuno |
| 2 | Almuerzo |
| 3 | Cena |
| 4 | Bebidas |
| 5 | Postres |

---

#### MENU_DIA
Días de la semana.

```sql
CREATE TABLE MENU_DIA (
    idDiaMenu INTEGER PRIMARY KEY,
    nombreDia VARCHAR(15) NOT NULL,
    CONSTRAINT chk_idDiaMenu CHECK (idDiaMenu BETWEEN 1 AND 7)
);
```

| ID | Día |
|----|-----|
| 1 | Lunes |
| 2 | Martes |
| 3 | Miércoles |
| 4 | Jueves |
| 5 | Viernes |
| 6 | Sábado |
| 7 | Domingo |

---

#### MENU_PRODUCTO
Relación entre productos, tipos y días (185 registros).

```sql
CREATE TABLE MENU_PRODUCTO (
    idMenuProducto SERIAL PRIMARY KEY,
    idProducto VARCHAR(30) NOT NULL,
    idTipo INTEGER NOT NULL,
    idDiaMenu INTEGER NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (idProducto) REFERENCES PRODUCTO(idProducto),
    FOREIGN KEY (idTipo) REFERENCES TIPO_COMIDA(idTipo),
    FOREIGN KEY (idDiaMenu) REFERENCES MENU_DIA(idDiaMenu),
    UNIQUE(idProducto, idTipo, idDiaMenu)
);
```

**Lógica del Menú Automático:**
- **Desayunos**: Todos disponibles todos los días
- **Almuerzos**: Rota plato principal cada día + ensalada/acompañamientos fijos
- **Cenas**: Rota plato principal cada día
- **Bebidas y Postres**: Todos disponibles todos los días

---

#### MENU_EXCEPCION
Promociones especiales con descuentos.

```sql
CREATE TABLE MENU_EXCEPCION (
    idExcepcion SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    descuento_porcentaje DECIMAL(5,2) DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE,
    CONSTRAINT chk_descuento CHECK (descuento_porcentaje BETWEEN 0 AND 100),
    CONSTRAINT chk_fechas CHECK (fecha_fin >= fecha_inicio)
);
```

---

#### EXCEPCION_PRODUCTO
Productos incluidos en cada promoción.

```sql
CREATE TABLE EXCEPCION_PRODUCTO (
    idExcepcionProducto SERIAL PRIMARY KEY,
    idExcepcion INTEGER NOT NULL,
    idProducto VARCHAR(30) NOT NULL,
    precio_especial DECIMAL(10,2),
    FOREIGN KEY (idExcepcion) REFERENCES MENU_EXCEPCION(idExcepcion),
    FOREIGN KEY (idProducto) REFERENCES PRODUCTO(idProducto),
    UNIQUE(idExcepcion, idProducto)
);
```

---

## 🎁 Sistema de Promociones

### Promociones Pre-configuradas

#### 1️⃣ Lunes de Carnes (20% descuento)
**Productos:**
- Churrasco Premium: ~~$45,000~~ → **$36,000**
- Steak Argentino: ~~$50,000~~ → **$40,000**
- Costillas BBQ: ~~$40,000~~ → **$32,000**

**Vigencia:** Todos los lunes hasta 31/12/2025

---

#### 2️⃣ Martes de Pizzas (30% descuento)
**Productos:**
- Pizza Margherita: ~~$24,000~~ → **$16,800**
- Pizza Pepperoni: ~~$26,000~~ → **$18,200**

**Vigencia:** Todos los martes hasta 31/12/2025

---

#### 3️⃣ Miércoles de Mariscos (15% descuento)
**Productos:**
- Salmón Grillado: ~~$38,000~~ → **$32,300**
- Paella Valenciana: ~~$35,000~~ → **$29,750**
- Filete de Pescado: ~~$30,000~~ → **$25,500**

**Vigencia:** Todos los miércoles hasta 31/12/2025

---

#### 4️⃣ Jueves de Pastas (25% descuento)
**Productos:**
- Pasta Carbonara: ~~$22,000~~ → **$16,500**
- Lasaña Boloñesa: ~~$32,000~~ → **$24,000**
- Ravioles de Ricotta: ~~$28,000~~ → **$21,000**

**Vigencia:** Todos los jueves hasta 31/12/2025

---

#### 5️⃣ Viernes Social - 2x1 Bebidas (50% descuento)
**Productos:**
- Cerveza Nacional: ~~$8,000~~ → **$4,000**
- Vino Tinto: ~~$15,000~~ → **$7,500**
- Vino Blanco: ~~$15,000~~ → **$7,500**
- Mojito Clásico: ~~$18,000~~ → **$9,000**

**Vigencia:** Todos los viernes hasta 31/12/2025

---

#### 6️⃣ Fin de Semana Familiar (10% descuento)
**Productos:**
- Hamburguesa Gourmet: ~~$28,000~~ → **$25,200**
- Pollo a la Parrilla: ~~$25,000~~ → **$22,500**
- Pechuga Rellena: ~~$32,000~~ → **$28,800**

**Vigencia:** Sábados y domingos hasta 31/12/2025

---

#### 7️⃣ Happy Hour Postres (20% descuento)
**Horario:** 3pm - 6pm todos los días

**Productos:**
- Tiramisú: ~~$16,000~~ → **$12,800**
- Cheesecake de Frutos: ~~$14,000~~ → **$11,200**
- Brownie con Helado: ~~$12,000~~ → **$9,600**
- Tres Leches: ~~$11,000~~ → **$8,800**

**Vigencia:** Diario 15:00-18:00 hasta 31/12/2025

---

### Consultar Promociones Activas

**SQL:**
```sql
SELECT 
    me.nombre,
    me.descripcion,
    me.descuento_porcentaje,
    COUNT(ep.idProducto) as total_productos
FROM MENU_EXCEPCION me
LEFT JOIN EXCEPCION_PRODUCTO ep ON me.idExcepcion = ep.idExcepcion
WHERE me.activo = TRUE
  AND me.fecha_inicio <= CURRENT_DATE
  AND me.fecha_fin >= CURRENT_DATE
GROUP BY me.idExcepcion, me.nombre, me.descripcion, me.descuento_porcentaje
ORDER BY me.descuento_porcentaje DESC;
```

**Python:**
```python
from modelo_restaurante import Menu

menu = Menu()
promociones = menu.obtener_excepciones_activas()

for promo in promociones:
    print(f"{promo['nombre']}: {promo['descuento']}% de descuento")
```

---

### Crear Nueva Promoción

```sql
-- 1. Crear la promoción
INSERT INTO MENU_EXCEPCION 
(nombre, descripcion, fecha_inicio, fecha_fin, descuento_porcentaje, activo)
VALUES 
('Black Friday', 'Descuento especial Black Friday', '2025-11-29', '2025-11-29', 40, TRUE);

-- 2. Asignar productos
INSERT INTO EXCEPCION_PRODUCTO (idExcepcion, idProducto, precio_especial)
SELECT 
    (SELECT idExcepcion FROM MENU_EXCEPCION WHERE nombre = 'Black Friday'),
    idProducto,
    precio * 0.60
FROM PRODUCTO
WHERE nombre IN ('Churrasco Premium', 'Salmón Grillado', 'Tiramisú');
```

---

## 👨‍💻 Desarrollo

### Estructura del Proyecto

```
parcial2Linux-main/
├── main.py                      # Punto de entrada
├── interfaz_restaurante.py      # GUI principal con Tkinter
├── modelo_restaurante.py        # Lógica de negocio + BD
├── conexionDB.py                # Conexión PostgreSQL
├── dialogo_login.py             # Ventana de login
├── dialogo_impresion.py         # Sistema de impresión CUPS
├── visor_productos.py           # Visualizador de productos
├── setup_database.py            # Inicializador de BD
├── DB/
│   └── DB.sql                   # Schema + datos iniciales
├── dist/
│   └── parcial2                 # Ejecutable compilado (66MB)
├── build/                       # Archivos temporales PyInstaller
├── parcial2.spec                # Configuración PyInstaller
├── install_postgresql.sh        # Instalador automático
├── cambiar_password_postgres.sh # Helper contraseña
├── build.sh                     # Compilador ejecutable
└── README.md                    # Esta documentación
```

---

### Archivos Clave

#### `conexionDB.py`
Maneja la conexión con PostgreSQL usando pool de conexiones.

**Métodos principales:**
```python
db_manager.ejecutar_query(query, params, fetch=True)
db_manager.ejecutar_query_uno(query, params)
db_manager.insertar(tabla, datos)
db_manager.actualizar(tabla, datos, condicion, params)
db_manager.eliminar(tabla, condicion, params)
db_manager.verificar_conexion()
```

---

#### `modelo_restaurante.py`
Clases de modelo y lógica de negocio.

**Clases principales:**
- `MenuItem`: Representa un producto
- `LineaPedido`: Item en el carrito
- `Pedido`: Pedido completo
- `Factura`: Factura de venta
- `Menu`: Gestor del menú (carga desde BD)

**Métodos del Menu:**
```python
menu.obtener_menu_del_dia(dia_semana, tipo_comida)
menu.obtener_tipos_comida()
menu.verificar_login(usuario, contrasena)
menu.obtener_excepciones_activas(fecha)
menu.obtener_productos_con_descuento(id_excepcion)
menu.obtener_precio_producto(id_producto)
```

---

#### `setup_database.py`
Script para crear/reinicializar la base de datos.

```python
python3 setup_database.py
```

**Funciones:**
- `crear_base_datos()`: Crea BD si no existe
- `ejecutar_script_sql()`: Ejecuta DB/DB.sql
- `verificar_conexion()`: Prueba conectividad

---

### Compilar Ejecutable

```bash
# Opción 1: Script automático
./build.sh

# Opción 2: Manual
pyinstaller --clean --noconfirm parcial2.spec
```

**Resultado:**
- Ejecutable: `dist/parcial2`
- Tamaño: ~66 MB
- Incluye: Python + PostgreSQL driver + Tkinter + CUPS

---

## 🔌 API de la Base de Datos

### Función: Menú Automático

```sql
SELECT asignar_menu_automatico();
```

**Qué hace:**
1. Limpia asignaciones previas
2. Asigna desayunos a todos los días
3. Rota almuerzos por día de semana
4. Rota cenas por día de semana
5. Asigna bebidas y postres a todos los días

---

### Consultas Útiles

#### Ver menú del día actual

```sql
SELECT 
    p.nombre,
    p.precio,
    tc.nombre as tipo,
    md.nombreDia
FROM PRODUCTO p
JOIN MENU_PRODUCTO mp ON p.idProducto = mp.idProducto
JOIN TIPO_COMIDA tc ON mp.idTipo = tc.idTipo
JOIN MENU_DIA md ON mp.idDiaMenu = md.idDiaMenu
WHERE md.idDiaMenu = EXTRACT(ISODOW FROM CURRENT_DATE)
ORDER BY tc.idTipo, p.nombre;
```

---

#### Productos con descuento hoy

```sql
SELECT 
    p.nombre,
    p.precio as precio_normal,
    ep.precio_especial,
    me.descuento_porcentaje,
    me.nombre as promocion
FROM PRODUCTO p
JOIN EXCEPCION_PRODUCTO ep ON p.idProducto = ep.idProducto
JOIN MENU_EXCEPCION me ON ep.idExcepcion = me.idExcepcion
WHERE me.activo = TRUE
  AND me.fecha_inicio <= CURRENT_DATE
  AND me.fecha_fin >= CURRENT_DATE
ORDER BY me.descuento_porcentaje DESC;
```

---

#### Estadísticas de promociones

```sql
SELECT 
    me.nombre,
    COUNT(ep.idProducto) as total_productos,
    ROUND(AVG(p.precio - ep.precio_especial), 2) as ahorro_promedio,
    ROUND(AVG(me.descuento_porcentaje), 2) as descuento_promedio
FROM MENU_EXCEPCION me
JOIN EXCEPCION_PRODUCTO ep ON me.idExcepcion = ep.idExcepcion
JOIN PRODUCTO p ON ep.idProducto = p.idProducto
WHERE me.activo = TRUE
GROUP BY me.idExcepcion, me.nombre
ORDER BY ahorro_promedio DESC;
```

---

### Python API

#### Obtener promociones activas

```python
from modelo_restaurante import Menu
from datetime import datetime

menu = Menu()

# Promociones de hoy
excepciones = menu.obtener_excepciones_activas()
for exc in excepciones:
    print(f"{exc['nombre']}: {exc['descuento']}%")

# Promociones de una fecha específica
excepciones = menu.obtener_excepciones_activas('2025-12-25')
```

---

#### Obtener productos con descuento

```python
# Todos los productos en promoción hoy
productos = menu.obtener_productos_con_descuento()

for prod in productos:
    print(f"{prod['nombre']}")
    print(f"  Precio normal: ${prod['precio_original']:,.0f}")
    print(f"  Precio oferta: ${prod['precio_especial']:,.0f}")
    print(f"  Ahorro: {prod['descuento']}%")
    print(f"  Promoción: {prod['promocion']}")

# Productos de una promoción específica
productos = menu.obtener_productos_con_descuento(id_excepcion=1)
```

---

#### Calcular precio con descuento

```python
# Obtener precio actual (con descuento si aplica)
info_precio = menu.obtener_precio_producto('PROD2025ChurrascoPremium')

if info_precio['tiene_descuento']:
    print(f"Precio normal: ${info_precio['precio_original']:,.0f}")
    print(f"Precio especial: ${info_precio['precio_final']:,.0f}")
    print(f"Descuento: {info_precio['descuento_porcentaje']}%")
    print(f"Promoción: {info_precio['promocion']}")
else:
    print(f"Precio: ${info_precio['precio_final']:,.0f}")
```

---

## 🐛 Solución de Problemas

### PostgreSQL no inicia

**Error:** `Connection refused` o servicio no corre

```bash
# Verificar estado
sudo systemctl status postgresql

# Si está stopped, iniciarlo
sudo systemctl start postgresql

# Ver logs
sudo journalctl -u postgresql -n 50
```

---

### Error de autenticación

**Error:** `FATAL: authentication failed for user "postgres"`

**Solución:**
```bash
# Verificar configuración
cat /var/lib/pgsql/data/pg_hba.conf | grep -v "^#" | grep -v "^$"

# Debe tener líneas como:
# local   all   postgres   md5
# host    all   all   127.0.0.1/32   md5

# Si tiene 'peer' o 'ident', cambiar:
sudo sed -i 's/peer/md5/g; s/ident/md5/g' /var/lib/pgsql/data/pg_hba.conf
sudo systemctl restart postgresql
```

---

### No se detectan impresoras

**Error:** `⚠️ No se detectaron impresoras`

**Solución:**
```bash
# Instalar CUPS
sudo dnf install cups

# Iniciar servicio
sudo systemctl start cups
sudo systemctl enable cups

# Verificar impresoras
lpstat -p -d
```

---

### Error al importar psycopg2

**Error:** `ModuleNotFoundError: No module named 'psycopg2'`

**Solución:**
```bash
# Reinstalar
pip3 uninstall psycopg2 psycopg2-binary
pip3 install --user psycopg2-binary

# Verificar instalación
python3 -c "import psycopg2; print(psycopg2.__version__)"
```

---

### Base de datos no se crea

**Error:** Script `setup_database.py` falla

**Solución:**
```bash
# Verificar configuración en setup_database.py
# Debe tener:
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': 'postgres'
}

# Probar conexión manualmente
psql -U postgres -h localhost -c "SELECT version();"

# Si pide contraseña, ingresarla
```

---

### Ejecutable no inicia

**Error:** Ejecutable no arranca o error al cargar

```bash
# Ver errores en terminal
cd dist
./parcial2

# Si hay error de librerías faltantes, instalar:
sudo dnf install gtk3 gobject-introspection

# Recompilar
cd ..
pyinstaller --clean --noconfirm parcial2.spec
```

---

## 📞 Soporte y Contacto

### Logs del Sistema

```bash
# Logs de PostgreSQL
sudo journalctl -u postgresql -f

# Logs de CUPS (impresión)
sudo journalctl -u cups -f

# Verificar tabla de productos
psql -U postgres -h localhost -d parcial2 -c "SELECT COUNT(*) FROM producto;"
```

---

### Información del Sistema

```bash
# Versión de PostgreSQL
psql --version

# Versión de Python
python3 --version

# Módulos Python instalados
pip3 list | grep -i "psycopg\|pyinstaller"

# Estado de servicios
systemctl status postgresql cups
```

---

### Reiniciar Todo

```bash
# Detener servicios
sudo systemctl stop postgresql

# Eliminar base de datos
sudo -u postgres psql -c "DROP DATABASE IF EXISTS parcial2;"

# Reiniciar PostgreSQL
sudo systemctl start postgresql

# Recrear base de datos
python3 setup_database.py
```

---

## 📚 Referencias

### Documentación Oficial

- [PostgreSQL 16 Documentation](https://www.postgresql.org/docs/16/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
- [Python Tkinter](https://docs.python.org/3/library/tkinter.html)
- [CUPS Documentation](https://www.cups.org/doc/)
- [PyInstaller Manual](https://pyinstaller.org/en/stable/)

### SQL Recursos

- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
- [SQL Cheat Sheet](https://www.postgresql.org/docs/16/sql-commands.html)

---

## 📄 Licencia

**Proyecto Educativo** - Parcial 2 - Sistemas Operativos

Desarrollado para demostrar integración de:
- Python 3.13
- PostgreSQL 16
- Tkinter GUI
- Sistema de promociones dinámicas
- Compilación con PyInstaller

---

## 🏆 Características Destacadas

- ✅ **39 productos** organizados en 5 categorías
- ✅ **185 asignaciones** de menú automático
- ✅ **7 promociones** pre-configuradas
- ✅ **Descuentos del 10% al 50%**
- ✅ **Menú rotativo** por día de semana
- ✅ **Login seguro** con base de datos
- ✅ **Sistema de impresión** CUPS integrado
- ✅ **Ejecutable portable** de 66MB
- ✅ **Instalación automatizada** en 3 minutos

---

## 🆕 Actualizaciones Recientes

### Versión 2.1 - Noviembre 2025

#### Mejoras en Conexión a Base de Datos
- ✅ **Context Managers**: Manejo automático de conexiones con `with` statements
- ✅ **Logging Mejorado**: Sistema de logs detallado en `database.log` y `app.log`
- ✅ **Manejo de Errores**: Mejor captura y reporte de excepciones
- ✅ **Query con Diccionarios**: Nuevo método `ejecutar_query_dict()` para resultados estructurados
- ✅ **Pool de Conexiones**: Gestión automática y cierre seguro de conexiones

#### Mejoras en la Aplicación Principal
- ✅ **Verificación de Dependencias**: Chequeo automático al iniciar
- ✅ **Mensajes de Error Visuales**: Dialogs informativos para el usuario
- ✅ **Logging de Aplicación**: Registro completo de eventos en `app.log`
- ✅ **Documentación Actualizada**: Comentarios y docstrings mejorados

#### Archivos Actualizados
- `conexionDB.py` - Sistema de conexión mejorado
- `main.py` - Inicialización con verificaciones
- `requirements.txt` - Dependencias documentadas
- `README.md` - Documentación actualizada

---

**Versión:** 2.1 con Sistema de Promociones y Conexiones Mejoradas  
**Fecha:** 17 de noviembre de 2025  
**Plataforma:** Fedora Linux 40+  
**Base de Datos:** PostgreSQL 16.9

---

¡Gracias por usar el Sistema POS Restaurante! 🍽️
