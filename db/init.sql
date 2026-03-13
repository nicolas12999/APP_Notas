-- =========================================
-- Inicialización de la base de datos
-- =========================================

USE app_db;

CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Datos de ejemplo
INSERT INTO items (nombre, descripcion) VALUES
    ('Elemento 1', 'Descripción del primer elemento de ejemplo'),
    ('Elemento 2', 'Descripción del segundo elemento de ejemplo'),
    ('Elemento 3', 'Descripción del tercer elemento de ejemplo');
