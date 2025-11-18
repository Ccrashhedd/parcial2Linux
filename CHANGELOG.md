# Changelog - Sistema POS Restaurante

Todas las actualizaciones notables del proyecto serán documentadas en este archivo.

---

## [2.1] - 17 de Noviembre de 2025

### 🎉 Nuevas Características

#### Formulario de Productos Mejorado
- **Campo de Descripción Multilínea**: Text widget completo para ingresar detalles extensos del producto
- **Contador de Caracteres**: Muestra en tiempo real los caracteres usados (máx. 150)
- **Placeholder Inteligente**: Texto de ejemplo que se elimina automáticamente
- **Validación Mejorada**: Verifica precio, nombre y descripción antes de guardar
- **Scroll Interno**: Permite escribir descripciones largas cómodamente

#### Sistema de Conexión Mejorado
- **Context Managers**: Implementación de context managers (`with` statements) para gestión automática de conexiones
- **Método `ejecutar_query_dict()`**: Nuevo método que retorna resultados como diccionarios para facilitar el acceso a datos
- **`obtener_version_db()`**: Método para verificar la versión de PostgreSQL

#### Sistema de Logging Avanzado
- Logging estructurado con timestamps y niveles de severidad
- Archivo `database.log` para todas las operaciones de base de datos
- Archivo `app.log` para eventos de la aplicación
- Formato mejorado: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`

#### Gestión de Productos Completa
- **Visualización TODOS los productos**: Lista completa sin límites con scroll mejorado
- **Contador Total**: Muestra el número total de productos en la base de datos
- **Numeración Visual**: Cada producto tiene un número para fácil identificación
- **Botón Actualizar**: Permite refrescar la lista de productos manualmente
- **Diseño Mejorado**: Cards con bordes elevados para mejor visualización

### 🔧 Mejoras

#### Manejo de Errores
- Try-catch mejorado en todas las operaciones de base de datos
- Rollback automático en caso de errores de transacción
- Mensajes de error más descriptivos con contexto completo
- Ventanas de diálogo informativas para el usuario final

#### Inicialización de Aplicación
- Verificación automática de dependencias al inicio
- Mensajes visuales de error con `messagebox`
- Validación de módulos requeridos (psycopg2, tkinter)
- Logging detallado del proceso de inicio

#### Compilación y Distribución
- Script `build.sh` mejorado con más información
- Archivo `.spec` actualizado con todas las dependencias
- Modo sin consola para aplicación GUI limpia
- Limpieza automática de builds anteriores
- Visualización del tamaño del ejecutable

### 📝 Documentación

#### README.md
- Sección de "Actualizaciones Recientes" agregada
- Versión actualizada a 2.1
- Fecha actualizada a Noviembre 2025
- Lista detallada de cambios

#### requirements.txt
- Comentarios descriptivos para cada dependencia
- Versiones específicas documentadas
- Nota sobre tkinter (incluido con Python)

#### Código Fuente
- Docstrings mejorados en todas las funciones
- Comentarios en español para mejor comprensión
- Headers de archivo actualizados con fecha

### 🐛 Correcciones

- Pool de conexiones ahora se cierra correctamente (`_connection_pool = None`)
- Mejor manejo de recursos con `finally` blocks
- Importación de `psycopg2.extras` para DictCursor
- Logging configurado antes de cualquier operación

### 🔒 Seguridad

- Transacciones con commit/rollback automático
- Cierre seguro de cursores y conexiones
- Validación de parámetros en queries SQL
- Protección contra fugas de recursos

### 📦 Archivos Actualizados

- `conexionDB.py` - Sistema de conexión completamente refactorizado
- `main.py` - Inicialización con verificaciones y logging
- `requirements.txt` - Documentación de dependencias
- `parcial2.spec` - Configuración de PyInstaller mejorada
- `build.sh` - Script de compilación con más información
- `README.md` - Documentación actualizada

### 📊 Estadísticas

- **Tamaño del ejecutable**: 66MB
- **Tiempo de compilación**: ~40 segundos
- **Python**: 3.13.9
- **PyInstaller**: 6.16.0
- **PostgreSQL**: 16+

---

## [2.0] - Versión Anterior

### Características
- Sistema POS completo con PostgreSQL
- 39 productos pre-cargados
- Sistema de promociones por día
- Menú rotativo automático
- Interfaz gráfica con Tkinter
- Sistema de impresión CUPS

---

## Formato

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/)

### Tipos de Cambios
- `🎉 Nuevas Características` - para nueva funcionalidad
- `🔧 Mejoras` - para cambios en funcionalidad existente
- `🐛 Correcciones` - para corrección de bugs
- `🔒 Seguridad` - para vulnerabilidades
- `📝 Documentación` - para cambios en documentación
- `🗑️ Obsoleto` - para características que serán removidas
