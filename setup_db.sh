#!/bin/bash

# Script para actualizar/crear la base de datos local

echo "════════════════════════════════════════"
echo "  Configuración de Base de Datos"
echo "════════════════════════════════════════"
echo ""

# Verificar si psql está disponible
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL client no está instalado"
    echo "Instálalo con: sudo apt install postgresql-client"
    echo ""
    echo "La aplicación puede conectar a un servidor remoto sin instalar PostgreSQL."
    echo "Edita server_config.txt para configurar el servidor remoto."
    exit 0
fi

echo "▶ Verificando conexión a PostgreSQL local..."

# Intentar conectar
if psql -U postgres -c "\l" > /dev/null 2>&1; then
    echo "✓ PostgreSQL accesible"
    echo ""
    
    echo "▶ Actualizando base de datos..."
    
    # Crear o actualizar la BD
    psql -U postgres << EOF
-- Crear BD si no existe
CREATE DATABASE IF NOT EXISTS gestor_productos;

-- Conectar a la BD
\c gestor_productos

-- Crear tabla (reemplazar si existe)
DROP TABLE IF EXISTS productos CASCADE;
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    descripcion TEXT,
    imagen_data BYTEA,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear índice
CREATE INDEX idx_nombre ON productos(nombre);

-- Insertar datos de ejemplo
INSERT INTO productos (nombre, precio, descripcion) VALUES
('Laptop Dell', 799.99, 'Laptop de 15 pulgadas con procesador Intel i7'),
('Mouse Logitech', 25.50, 'Mouse inalámbrico ergonómico'),
('Teclado Mecánico', 89.99, 'Teclado mecánico RGB 87 teclas'),
('Monitor LG 24"', 199.99, 'Monitor IPS Full HD 1920x1080'),
('Webcam Logitech', 45.00, 'Cámara web 1080p con micrófono integrado');

EOF
    
    if [ $? -eq 0 ]; then
        echo "✓ Base de datos actualizada"
    else
        echo "⚠️  Hubo un error al actualizar la BD"
        echo "Intenta manualmente:"
        echo "  psql -U postgres -f database/schema.sql"
    fi
else
    echo "⚠️  PostgreSQL no está corriendo localmente"
    echo ""
    echo "Opciones:"
    echo "  1. Inicia PostgreSQL: sudo systemctl start postgresql"
    echo "  2. O configura un servidor remoto en server_config.txt"
fi

echo ""
echo "════════════════════════════════════════"
