-- ═══════════════════════════════════════════════════════════════════════════
-- TABLAS NUEVAS PARA GPU, RAM Y ALMACENAMIENTO
-- Ejecutar este script en MySQL antes de desplegar las actualizaciones.
-- Base de datos: techmatch
-- ═══════════════════════════════════════════════════════════════════════════

USE techmatch;

-- ── Tabla GPU ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS gpu (
    id_gpu INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT NOT NULL,
    vram_gb INT DEFAULT 8,
    tipo_memoria VARCHAR(20) DEFAULT 'GDDR6',
    bus_bits INT DEFAULT 128,
    tdp_w INT DEFAULT 150,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── Tabla RAM ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ram (
    id_ram INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT NOT NULL,
    capacidad_gb INT DEFAULT 8,
    tipo_memoria VARCHAR(10) DEFAULT 'DDR4',
    velocidad_mhz INT DEFAULT 3200,
    cantidad_modulos INT DEFAULT 1,
    latencia INT DEFAULT NULL,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── Tabla Almacenamiento ───────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS almacenamiento (
    id_almacenamiento INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT NOT NULL,
    capacidad_gb INT DEFAULT 512,
    tipo_disco VARCHAR(20) DEFAULT 'SSD',
    interfaz VARCHAR(30) DEFAULT 'SATA III',
    velocidad_lectura INT DEFAULT 550,
    formato VARCHAR(20) DEFAULT '2.5"',
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── Seed de marcas adicionales (si no existen) ─────────────────────────────
INSERT INTO marcas (nombre_marca, url_marca) VALUES 
    ('Kingston', 'https://www.kingston.com'),
    ('Corsair', 'https://www.corsair.com'),
    ('Samsung', 'https://www.samsung.com'),
    ('Western Digital', 'https://www.westerndigital.com'),
    ('Crucial', 'https://www.crucial.com'),
    ('Seagate', 'https://www.seagate.com')
ON DUPLICATE KEY UPDATE url_marca = VALUES(url_marca);

-- ═══════════════════════════════════════════════════════════════════════════
-- VERIFICACIÓN: Confirmar que las tablas se crearon correctamente
-- ═══════════════════════════════════════════════════════════════════════════
SELECT 'gpu' AS tabla, COUNT(*) AS registros FROM gpu
UNION ALL
SELECT 'ram', COUNT(*) FROM ram
UNION ALL
SELECT 'almacenamiento', COUNT(*) FROM almacenamiento;
