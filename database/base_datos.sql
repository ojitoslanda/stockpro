-- Crear base de datos
CREATE DATABASE IF NOT EXISTS stockpro CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE stockpro;

-- Tabla de usuarios (login)
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol ENUM('admin', 'usuario') NOT NULL DEFAULT 'usuario',
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de categorías de productos
CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

-- Tabla de productos
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50) NOT NULL UNIQUE,
    nombre VARCHAR(150) NOT NULL,
    categoria_id INT,
    precio DECIMAL(10,2) NOT NULL DEFAULT 0,
    stock_actual INT NOT NULL DEFAULT 0,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

-- Tabla de movimientos de stock (entradas/salidas)
CREATE TABLE movimientos_stock (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT NOT NULL,
    tipo ENUM('entrada', 'salida') NOT NULL,
    cantidad INT NOT NULL,
    motivo VARCHAR(255),
    usuario_id INT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (producto_id) REFERENCES productos(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);



-- Usuario admin de prueba (contraseña: admin123, luego la hasheamos bien desde Python)
INSERT INTO usuarios (nombre, email, password_hash, rol)
VALUES ('Administrador', 'admin@stockpro.com', 'temporal', 'admin');

-- Categorías
INSERT INTO categorias (nombre) VALUES
('Abarrotes'), ('Bebidas'), ('Limpieza');

-- Productos
INSERT INTO productos (codigo, nombre, categoria_id, precio, stock_actual) VALUES
('P001', 'Arroz 1kg', 1, 4.50, 100),
('P002', 'Coca Cola 500ml', 2, 3.00, 50),
('P003', 'Detergente 1kg', 3, 12.00, 30);

-- Movimiento de ejemplo
INSERT INTO movimientos_stock (producto_id, tipo, cantidad, motivo, usuario_id)
VALUES (1, 'entrada', 100, 'Stock inicial', 1);