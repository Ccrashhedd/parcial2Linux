# 🍽️ POS Restaurante - Parcial 2

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/)
[![Linux](https://img.shields.io/badge/platform-Linux-orange.svg)](https://www.linux.org/)

Sistema de Punto de Venta (POS) para restaurantes con interfaz gráfica completa, gestión de menú, carrito de compras, generación de facturas e impresión en Linux.

## 🎯 Características

✨ **Gestión de Menú**
- ✅ CRUD completo (Crear, Leer, Actualizar, Eliminar)
- ✅ Categorización de platos
- ✅ Precios y descripciones
- ✅ Interfaz intuitiva

🛒 **Sistema de Venta**
- ✅ Carrito de compra interactivo
- ✅ Modificar cantidades sobre la marcha
- ✅ Eliminar items
- ✅ Cálculo automático de totales

💰 **Facturas y Pagos**
- ✅ Generación de facturas profesionales
- ✅ Múltiples formas de pago (Efectivo, Tarjeta, Transferencia)
- ✅ Cálculo automático de IVA (19%)
- ✅ Número de factura único por transacción

🖨️ **Impresión en Linux**
- ✅ Integración con CUPS
- ✅ Impresión térmica y estándar
- ✅ Exportar a archivo (.txt, .pdf)

---

## 🚀 Instalación Rápida

### Opción 1: Instalación Automática (Recomendado)

```bash
git clone https://github.com/Ccrashhedd/parcial2Linux.git
cd parcial2Linux
chmod +x install.sh
./install.sh

# Responde 's' cuando pregunta si quieres instalar como aplicación
```

Luego ejecuta desde cualquier terminal:
```bash
parcial2
```

### Opción 2: Ejecutable Precompilado

```bash
sudo cp ./dist/parcial2 /usr/local/bin/parcial2
parcial2
```

### Opción 3: Desde Código Fuente

```bash
git clone https://github.com/Ccrashhedd/parcial2Linux.git
cd parcial2Linux
python3 main.py
```

---

## 📖 Guía de Uso Rápida

### 1. **Tomar un Pedido**

1. Abre la pestaña **"Venta"** (📦)
2. Selecciona una **categoría** del menú
3. Haz clic en un plato
4. Ajusta la **cantidad**
5. Haz clic en **➕ Agregar al Carrito**
6. Repite para más items
7. Haz clic en **💰 COBRAR**

### 2. **Procesar Pago**

1. En la ventana de factura
2. Elige la **forma de pago**
3. Haz clic en **🖨️ Imprimir** o **💾 Guardar**

### 3. **Gestionar Menú**

1. Abre la pestaña **"Menú"** (🍽️)
2. Haz clic en:
   - **➕ Nuevo Item** - Agregar plato
   - **✏️ Editar** - Modificar plato
   - **❌ Eliminar** - Remover plato

---

## 📋 Requisitos del Sistema

- **Python:** 3.7 o superior
- **SO:** Linux (Ubuntu, Fedora, Arch, Debian)
- **Librerías Python:** Tkinter (incluido en Python)
- **Impresora:** Opcional (requiere CUPS instalado)

### Instalación de Dependencias del Sistema

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk python3-pip cups
```

**Fedora:**
```bash
sudo dnf install python3-tkinter python3-pip cups
```

**Arch:**
```bash
sudo pacman -S tk python-pip cups
```

---

## 📂 Estructura del Proyecto

```
parcial2Linux/
├── main.py                      # Punto de entrada
├── interfaz_restaurante.py      # GUI del POS
├── modelo_restaurante.py        # Clases de datos
├── dist/
│   └── parcial2                 # Ejecutable compilado (14 MB)
├── requirements.txt             # Dependencias Python
├── install.sh                   # Script de instalación automática
├── build.sh                     # Reconstruir ejecutable
├── DB/
│   └── DB.sql                   # Scripts SQL
├── POS-RESTAURANTE.md           # Documentación completa
├── QUICK-START.md               # Guía rápida
├── README-APP.md                # Guía de instalación
└── README                        # Documentación antigua
```

---

## 🛠️ Estructura de Clases

### `MenuItem`
Representa un plato del menú

```python
item = MenuItem(id="1", nombre="Hamburguesa", precio=35000, 
                categoria="Platos Principales", descripcion="Con queso")
```

### `Pedido`
Maneja un carrito de compra

```python
pedido = Pedido()
pedido.agregar_item(menu_item, cantidad=2)
print(pedido.total)  # Con IVA incluido
```

### `Factura`
Genera facturas profesionales

```python
factura = Factura(pedido, forma_pago="Efectivo")
print(factura.generar_texto())  # Imprime factura
factura.guardar_factura("/ruta/factura.txt")
```

### `Menu`
Gestiona todos los items

```python
menu = Menu()
menu.agregar_item("Pizza", 28000, "Platos Principales")
menu.listar_por_categoria("Platos Principales")
```

---

## 🖨️ Impresión

### Configurar Impresora

```bash
# Ver impresoras disponibles
lpstat -p -d

# Establecer impresora por defecto
lpadmin -d nombre_impresora
```

### Imprimir desde la Aplicación

1. Genera una venta normalmente
2. En la factura, haz clic en **🖨️ Imprimir**
3. Se enviará a la impresora configurada

### Guardar Factura

1. En la factura, haz clic en **💾 Guardar**
2. Elige ubicación y formato (.txt o .pdf)

---

## ⚙️ Configuración del Negocio

1. Menú → **Configuración** → **Datos del Negocio**
2. Actualiza:
   - Nombre del Negocio
   - NIT
3. Estos datos aparecerán en todas las facturas

---

## 🔄 Reconstruir Ejecutable

Si haces cambios en el código:

```bash
cd parcial2Linux
./build.sh
```

Esto genera un nuevo ejecutable en `dist/parcial2`

---

## 📝 Ejemplo de Factura

```
==================================================
                   RESTAURANTE                    
==================================================

NIT: 123456789
FACTURA Nº: A1B2C3D4E5
FECHA: 16/11/2025 14:30:45

--------------------------------------------------
DESCRIPCIÓN                      CANT   PRECIO    TOTAL
--------------------------------------------------
Hamburguesa                       2 $35000.00 $70000.00
Jugo Natural                      2  $8000.00 $16000.00
--------------------------------------------------
SUBTOTAL:                                      $86000.00
IVA 19%:                                       $16340.00
==================================================
TOTAL:                                        $102340.00
==================================================

FORMA DE PAGO: Efectivo

             ¡GRACIAS POR SU COMPRA!
```

---

## 🐛 Solución de Problemas

### Error: "parcial2: command not found"

```bash
# Verifica que esté instalado
which parcial2

# Si no, instálalo manualmente
sudo cp ./dist/parcial2 /usr/local/bin/parcial2
```

### Error: "No se puede imprimir"

```bash
# Instala CUPS
sudo apt-get install cups

# Verifica impresoras
lpstat -p -d
```

### La aplicación no inicia

```bash
# Verifica Tkinter
python3 -c "import tkinter; print('OK')"

# Ejecuta desde terminal para ver errores
python3 main.py
```

---

## 📚 Documentación Completa

- **[POS-RESTAURANTE.md](POS-RESTAURANTE.md)** - Guía completa con ejemplos
- **[QUICK-START.md](QUICK-START.md)** - Inicio en 30 segundos
- **[README-APP.md](README-APP.md)** - Guía de instalación manual

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NuevaFeature`)
3. Commit tus cambios (`git commit -m 'Add NuevaFeature'`)
4. Push a la rama (`git push origin feature/NuevaFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto es de código abierto y libre de usar.

---

## 👨‍💻 Autor

**Parcial 2 - Sistema Operativo**

Desarrollado como proyecto educativo en Python y Tkinter

---

## 📞 Soporte

Si encuentras algún problema:

```bash
# Crea un issue en GitHub
# o ejecuta desde terminal para ver logs
parcial2 2>&1 | tee /tmp/debug.log
```

---

**¡Disfruta tu POS Restaurante!** 🍽️💻

Para más información, visita: [GitHub](https://github.com/Ccrashhedd/parcial2Linux)
