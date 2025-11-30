-- Crear base de datos
CREATE DATABASE IF NOT EXISTS gestor_productos;

-- Conectar a la base de datos
\c gestor_productos;

-- Crear tabla de productos
CREATE TABLE IF NOT EXISTS productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    descripcion TEXT,
    imagen_data BYTEA,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear índice para búsquedas rápidas
CREATE INDEX IF NOT EXISTS idx_nombre ON productos(nombre);

-- Insertar datos de ejemplo
INSERT INTO productos (nombre, precio, descripcion, imagen_data) VALUES
('Laptop Dell', 799.99, 'Laptop de 15 pulgadas con procesador Intel i7', NULL),
('Mouse Logitech', 25.50, 'Mouse inalámbrico ergonómico', NULL),
('Teclado Mecánico', 89.99, 'Teclado mecánico RGB 87 teclas', NULL),
('Monitor LG 24"', 199.99, 'Monitor IPS Full HD 1920x1080', NULL),
('Webcam Logitech', 45.00, 'Cámara web 1080p con micrófono integrado', NULL);

-- Crear tabla de auditoría (opcional)
CREATE TABLE IF NOT EXISTS auditoria_productos (
    id SERIAL PRIMARY KEY,
    producto_id INTEGER,
    accion VARCHAR(50),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    detalles TEXT
);
