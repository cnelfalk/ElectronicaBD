-- =====================================================================
-- TechMatch - Esquema MVP (Tercera Forma Normal)
-- Alcance: Login de usuarios + datos actualizados por los bots
-- (precios actuales y especificaciones técnicas)
-- Regla de negocio: NO se guarda historial de precios.
-- =====================================================================

DROP DATABASE IF EXISTS techmatch;
CREATE DATABASE techmatch CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE techmatch;

-- ---------------------------------------------------------------------
-- 1) MÓDULO DE USUARIOS (Login / Registro)
-- ---------------------------------------------------------------------
CREATE TABLE usuarios (
    id_usuario        INT AUTO_INCREMENT PRIMARY KEY,
    nombre            VARCHAR(100)  NOT NULL,
    email             VARCHAR(150)  NOT NULL UNIQUE,
    contrasenia_hash  VARCHAR(255)  NOT NULL,   -- hash bcrypt/argon2, NUNCA texto plano
    fec_registro      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;


-- ---------------------------------------------------------------------
-- 2) CATÁLOGO DE REFERENCIA (Marcas, Tiendas, Categorías)
--    Separadas para respetar 3FN: el nombre de una marca/tienda/categoría
--    depende solo de su propio ID, no del producto.
-- ---------------------------------------------------------------------
CREATE TABLE marcas (
    id_marca  INT AUTO_INCREMENT PRIMARY KEY,
    nombre    VARCHAR(80)  NOT NULL UNIQUE    -- AMD, Intel, Lenovo, Asus
) ENGINE=InnoDB;

CREATE TABLE tiendas (
    id_tienda  INT AUTO_INCREMENT PRIMARY KEY,
    nombre     VARCHAR(80)   NOT NULL UNIQUE, -- Compra Gamer, Mercado Libre
    url_base   VARCHAR(255)  NOT NULL
) ENGINE=InnoDB;

CREATE TABLE categorias (
    id_categoria  INT AUTO_INCREMENT PRIMARY KEY,
    nombre        VARCHAR(60) NOT NULL UNIQUE  -- Notebook, CPU, GPU, RAM, etc.
) ENGINE=InnoDB;


-- ---------------------------------------------------------------------
-- 3) PRODUCTOS (super-tipo) + ESPECIALIZACIONES (sub-tipos)
--    Aplicamos el patrón supertipo/subtipo:
--      - Atributos comunes a todos los productos => tabla `productos`.
--      - Atributos específicos de cada tipo     => tabla por subtipo.
--    Esto evita columnas NULL y respeta 3FN.
-- ---------------------------------------------------------------------
CREATE TABLE productos (
    id_producto              INT AUTO_INCREMENT PRIMARY KEY,
    id_marca                 INT           NOT NULL,
    id_categoria             INT           NOT NULL,
    modelo                   VARCHAR(150)  NOT NULL,
    imagen_url               VARCHAR(500),
    fec_actualizacion_specs  DATETIME,     -- última vez que el bot de specs lo tocó
    CONSTRAINT uk_marca_modelo UNIQUE (id_marca, modelo),
    CONSTRAINT fk_prod_marca     FOREIGN KEY (id_marca)     REFERENCES marcas(id_marca),
    CONSTRAINT fk_prod_categoria FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
) ENGINE=InnoDB;

-- Subtipo: Notebooks
CREATE TABLE notebooks (
    id_producto          INT PRIMARY KEY,
    peso_kg              DECIMAL(4,2),
    tamanio_pantalla     DECIMAL(4,1),   -- en pulgadas
    tasa_refresco_hz     INT,
    capacidad_bateria_wh INT,
    CONSTRAINT fk_notebook_producto FOREIGN KEY (id_producto)
        REFERENCES productos(id_producto) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Subtipo: CPU
CREATE TABLE cpus (
    id_producto        INT PRIMARY KEY,
    nucleos            INT,
    hilos              INT,
    frecuencia_base    DECIMAL(4,2),   -- GHz
    frecuencia_turbo   DECIMAL(4,2),   -- GHz
    tdp                INT,            -- watts
    socket             VARCHAR(30),    -- AM5, LGA1700, etc.
    CONSTRAINT fk_cpu_producto FOREIGN KEY (id_producto)
        REFERENCES productos(id_producto) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Subtipo: GPU
CREATE TABLE gpus (
    id_producto    INT PRIMARY KEY,
    vram_gb        INT,
    tipo_memoria   VARCHAR(20),    -- GDDR6, GDDR6X, etc.
    consumo_w      INT,
    CONSTRAINT fk_gpu_producto FOREIGN KEY (id_producto)
        REFERENCES productos(id_producto) ON DELETE CASCADE
) ENGINE=InnoDB;


-- ---------------------------------------------------------------------
-- 4) PRECIOS ACTUALES (sin historial)
--    PK compuesta (producto, tienda): un único precio vigente por combo.
--    Cuando el bot corre, hace UPSERT (INSERT ... ON DUPLICATE KEY UPDATE).
-- ---------------------------------------------------------------------
CREATE TABLE precios_actuales (
    id_producto         INT           NOT NULL,
    id_tienda           INT           NOT NULL,
    precio              DECIMAL(12,2) NOT NULL,
    url_producto        VARCHAR(500)  NOT NULL,
    fec_actualizacion   DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
                                      ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id_producto, id_tienda),
    CONSTRAINT fk_precio_producto FOREIGN KEY (id_producto)
        REFERENCES productos(id_producto) ON DELETE CASCADE,
    CONSTRAINT fk_precio_tienda   FOREIGN KEY (id_tienda)
        REFERENCES tiendas(id_tienda)
) ENGINE=InnoDB;


-- ---------------------------------------------------------------------
-- 5) DATOS SEMILLA (marcas, tiendas y categorías que el enunciado exige)
-- ---------------------------------------------------------------------
INSERT INTO marcas (nombre) VALUES ('AMD'), ('Intel'), ('Lenovo'), ('Asus');

INSERT INTO tiendas (nombre, url_base) VALUES
    ('Compra Gamer',   'https://compragamer.com'),
    ('Mercado Libre',  'https://www.mercadolibre.com.ar');

INSERT INTO categorias (nombre) VALUES ('Notebook'), ('CPU'), ('GPU');
