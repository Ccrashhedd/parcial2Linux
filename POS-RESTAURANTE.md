# 🍽️ POS Restaurante - Documentación

## 📋 Descripción

**POS Restaurante** es un sistema de punto de venta completo para restaurantes, construido con Python y Tkinter. Permite gestionar menú, carrito de compras, generación de facturas e impresión en Linux.

---

## 🚀 Características

✅ **Gestión de Menú**
- Crear, editar y eliminar items del menú
- Organizar items por categorías
- Agregar descripción y precio a cada plato

✅ **Sistema de Venta**
- Carrito de compra interactivo
- Seleccionar cantidad de items
- Editar cantidades en el carrito
- Eliminar items del carrito

✅ **Cálculo Automático**
- Subtotal de cada item
- Cálculo de IVA (19%)
- Total final

✅ **Formas de Pago**
- Efectivo
- Tarjeta Débito
- Tarjeta Crédito
- Transferencia

✅ **Generación de Facturas**
- Formato profesional con datos del negocio
- Detalles de items, cantidades y precios
- Subtotal, impuestos y total
- Número de factura único

✅ **Impresión en Linux**
- Integración con sistema CUPS
- Impresión de facturas
- Guardar en archivo

---

## 🔧 Instalación

### Requisitos Previos

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk python3-pip cups

# Fedora
sudo dnf install python3-tkinter python3-pip cups

# Arch
sudo pacman -S tk python-pip cups
```

### Instalación de la Aplicación

**Opción 1: Desde el proyecto**
```bash
cd /ruta/del/proyecto
./install.sh
# Responde 's' cuando pregunta
```

**Opción 2: Clonar desde GitHub**
```bash
git clone https://github.com/Ccrashhedd/parcial2Linux.git
cd parcial2Linux
./install.sh
```

**Opción 3: Ejecutable precompilado**
```bash
sudo cp ./dist/parcial2 /usr/local/bin/parcial2
parcial2
```

---

## 📖 Uso

### 1. **Iniciar la Aplicación**

```bash
parcial2
```

### 2. **Pestaña "Venta" (📦)**

#### Agregar Items al Carrito
1. Selecciona una **categoría** en el dropdown
2. Haz clic en un item del menú
3. Ajusta la **cantidad** con el spinner
4. Haz clic en **➕ Agregar al Carrito**

#### Editar Carrito
- **Editar Cantidad**: Selecciona un item y ajusta
- **Eliminar**: Selecciona y haz clic en ❌

#### Procesar Pago
1. Selecciona **Forma de Pago**
2. Haz clic en **💰 COBRAR**
3. Se abrirá ventana con factura

#### Acciones en Factura
- **💾 Guardar**: Exportar a archivo .txt o .pdf
- **🖨️ Imprimir**: Enviar a impresora del sistema
- **❌ Cerrar**: Cerrar ventana

### 3. **Pestaña "Menú" (🍽️)**

#### Crear Nuevo Item
1. Haz clic en **➕ Nuevo Item**
2. Completa: Nombre, Precio, Categoría, Descripción
3. Haz clic en **Guardar**

#### Editar Item
1. Selecciona un item en la tabla
2. Haz clic en **✏️ Editar**
3. Modifica los datos
4. Haz clic en **Guardar**

#### Eliminar Item
1. Selecciona un item en la tabla
2. Haz clic en **❌ Eliminar**
3. Confirma la eliminación

---

## ⚙️ Configuración

### Datos del Negocio

1. Menú → **Configuración** → **Datos del Negocio**
2. Actualiza:
   - Nombre del Negocio
   - NIT
3. Haz clic en **Guardar**

Esta información aparecerá en todas las facturas.

---

## 📊 Estructuraas de Archivos

### Archivos Principales

```
parcial2Linux/
├── main.py                  # Punto de entrada
├── interfaz_restaurante.py  # GUI completa del POS
├── modelo_restaurante.py    # Clases de modelo (Menu, Pedido, Factura)
├── dist/parcial2            # Ejecutable compilado
└── requirements.txt         # Dependencias Python
```

### Clases del Modelo

**`MenuItem`** - Representa un plato del menú
```python
item = MenuItem(id, nombre, precio, categoria, descripcion)
```

**`LineaPedido`** - Representa un item en el carrito
```python
linea = LineaPedido(menu_item, cantidad)
```

**`Pedido`** - Representa una venta
```python
pedido = Pedido()
pedido.agregar_item(item, cantidad)
pedido.total  # Precio total con IVA
```

**`Factura`** - Representa la factura de venta
```python
factura = Factura(pedido, forma_pago)
factura.generar_texto()  # Retorna texto de factura
factura.guardar_factura(ruta)  # Guarda a archivo
```

**`Menu`** - Gestiona todos los items
```python
menu = Menu()
menu.agregar_item(nombre, precio, categoria)
menu.editar_item(id, nombre=None, precio=None)
menu.eliminar_item(id)
menu.listar_por_categoria(categoria)
```

---

## 🖨️ Impresión en Linux

### Requisitos

```bash
# Instalar CUPS (Common Unix Printing System)
sudo apt-get install cups  # Ubuntu/Debian
sudo dnf install cups      # Fedora
sudo pacman -S cups        # Arch
```

### Configurar Impresora

```bash
# Ver impresoras disponibles
lpstat -p -d

# Establecer impresora por defecto
lpadmin -d nombre_impresora
```

### Imprimir desde la Aplicación

1. En la factura, haz clic en **🖨️ Imprimir**
2. Se usará el comando `lp` automáticamente
3. La factura se enviará a la impresora por defecto

---

## 💾 Guardar Facturas

### Opción 1: Desde la Aplicación

1. En la factura, haz clic en **💾 Guardar**
2. Elige ubicación y formato (.txt o .pdf)
3. Se guardará automáticamente

### Opción 2: Desde Terminal

```bash
# Ver últimas facturas
ls /tmp/factura*

# Guardar factura a archivo específico
factura > ~/Documentos/factura_2025_11_16.txt
```

---

## 🔄 Gestión de Datos

### Exportar Menú

El menú se carga desde el modelo interno. Para exportar:

```bash
python3 -c "
from modelo_restaurante import Menu
import json
menu = Menu()
items = {id: {'nombre': item.nombre, 'precio': item.precio} 
         for id, item in menu.items.items()}
print(json.dumps(items, indent=2, ensure_ascii=False))
" > menu.json
```

### Importar Menú desde JSON

```python
import json
from modelo_restaurante import Menu

menu = Menu()
with open('menu.json', 'r') as f:
    datos = json.load(f)
    for id, item in datos.items():
        menu.agregar_item(item['nombre'], item['precio'])
```

---

## ⚠️ Solución de Problemas

### Error: "No se puede imprimir"

**Problema:** Comando `lp` no disponible

**Solución:**
```bash
# Instalar CUPS
sudo apt-get install cups
# o
sudo dnf install cups
```

### Error: "Impresora no configurada"

**Solución:**
```bash
# Ver impresoras
lpstat -p -d

# Configurar por defecto
lpadmin -d nombre_impresora
```

### La aplicación no inicia

**Verificar:**
```bash
python3 -c "import tkinter; print('OK')"
python3 -c "from modelo_restaurante import Menu; print('OK')"
python3 main.py
```

### Factura no se guarda

**Verificar permisos:**
```bash
touch /tmp/test.txt  # Debe funcionar
```

---

## 🎯 Casos de Uso

### Caso 1: Tomar un Pedido

1. Abre la pestaña **Venta**
2. Selecciona categoría "Platos Principales"
3. Agrega Hamburguesa (x1)
4. Agrega Jugo (x1)
5. Haz clic en **COBRAR**
6. Elige "Efectivo"
7. Imprime factura

### Caso 2: Agregar Nuevo Plato

1. Ve a pestaña **Menú**
2. Haz clic en **➕ Nuevo Item**
3. Nombre: "Tacos de Carne"
4. Precio: 20000
5. Categoría: "Platos Principales"
6. Guardar

### Caso 3: Corregir Precio

1. Pestaña **Menú**
2. Selecciona "Pizza Margarita"
3. Haz clic en **✏️ Editar**
4. Cambia precio a 30000
5. Guardar

---

## 📞 Soporte

Para reportar bugs o sugerencias:

```bash
git clone https://github.com/Ccrashhedd/parcial2Linux.git
# Edita el código y haz un pull request
```

---

## 📄 Licencia

Este proyecto es de código abierto. Úsalo libremente en tu restaurante.

---

**¡Disfruta tu POS Restaurante! 🍽️💻**
