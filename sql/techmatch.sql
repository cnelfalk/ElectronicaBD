-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema techmatch
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema techmatch
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `techmatch` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `techmatch` ;

-- -----------------------------------------------------
-- Table `techmatch`.`marcas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `techmatch`.`marcas` (
  `id_marca` INT NOT NULL AUTO_INCREMENT,
  `nombre_marca` VARCHAR(45) NULL DEFAULT NULL,
  `url_marca` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id_marca`))
ENGINE = InnoDB
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `techmatch`.`categorias`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `techmatch`.`categorias` (
  `id_categoria` INT NOT NULL AUTO_INCREMENT,
  `nombre_categoria` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id_categoria`))
ENGINE = InnoDB
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `techmatch`.`productos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `techmatch`.`productos` (
  `id_producto` INT NOT NULL AUTO_INCREMENT,
  `modelo_producto` VARCHAR(500) NULL DEFAULT NULL,
  `img_url` VARCHAR(1000) NULL DEFAULT NULL,
  `id_marca` INT NOT NULL,
  `id_categoria` INT NOT NULL,
  PRIMARY KEY (`id_producto`),
  INDEX `fk_Componentes_Marcas1_idx` (`id_marca` ASC) VISIBLE,
  INDEX `fk_Productos_Categorias1_idx` (`id_categoria` ASC) VISIBLE,
  CONSTRAINT `fk_Componentes_Marcas1`
    FOREIGN KEY (`id_marca`)
    REFERENCES `techmatch`.`marcas` (`id_marca`),
  CONSTRAINT `fk_Productos_Categorias1`
    FOREIGN KEY (`id_categoria`)
    REFERENCES `techmatch`.`categorias` (`id_categoria`))
ENGINE = InnoDB
AUTO_INCREMENT = 115
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `techmatch`.`almacenamiento`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `techmatch`.`almacenamiento` (
  `id_almacenamiento` INT NOT NULL AUTO_INCREMENT,
  `capacidad_gb_almacenamiento` INT NULL DEFAULT NULL,
  `tipo_almacenamiento` VARCHAR(45) NULL DEFAULT NULL,
  `vel_lectura` INT NULL DEFAULT NULL,
  `vel_escritura` INT NULL DEFAULT NULL,
  `id_producto` INT NOT NULL,
  PRIMARY KEY (`id_almacenamiento`, `id_producto`),
  INDEX `fk_Almacenamiento_Productos1_idx` (`id_producto` ASC) VISIBLE,
  CONSTRAINT `fk_Almacenamiento_Productos1`
    FOREIGN KEY (`id_producto`)
    REFERENCES `techmatch`.`productos` (`id_producto`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `techmatch`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `techmatch`.`usuarios` (
  `id_usuario` INT NOT NULL AUTO_INCREMENT,
  `nombre_usuario` VARCHAR(100) NULL DEFAULT NULL,
  `contrasenia_usuario` VARCHAR(255) NULL DEFAULT NULL,
  `fec_registro` DATETIME NULL DEFAULT NULL,
  `email_usuario` VARCHAR(150) NULL DEFAULT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE INDEX `email_usuario_UNIQUE` (`email_usuario` ASC) VISIBLE,
  UNIQUE INDEX `nombre_usuario_UNIQUE` (`nombre_usuario` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `techmatch`.`codigos_recuperacion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `techmatch`.`codigos_recuperacion` (
  `id_codigo`      INT          NOT NULL AUTO_INCREMENT,
  `id_usuario`     INT          NOT NULL,
  `codigo`         VARCHAR(6)   NOT NULL,
  `fec_expiracion` DATETIME     NOT NULL,
  `token`          VARCHAR(64)  NULL DEFAULT NULL,
  `usado`          TINYINT(1)   NOT NULL DEFAULT 0,
  PRIMARY KEY (`id_codigo`),
  INDEX `fk_codigos_recuperacion_usuarios_idx` (`id_usuario` ASC) VISIBLE,
  CONSTRAINT `fk_codigos_recuperacion_usuarios`
    FOREIGN KEY (`id_usuario`)
    REFERENCES `techmatch`.`usuarios` (`id_usuario`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `techmatch`.`comparaciones_guardadas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `techmatch`.`comparaciones_guardadas` (
  `id_comparacion` INT NOT NULL AUTO_INCREMENT,
  `fec_creacion_comp` DATETIME NULL DEFAULT NULL,
  `id_categoria` INT NOT NULL,
  `id_usuario` INT NOT NULL,
  PRIMARY KEY (`id_comparacion`),
  INDEX `fk_Comparaciones_Guardadas_Categorias1_idx` (`id_categoria` ASC) VISIBLE,
  INDEX `fk_Comparaciones_Guardadas_Usuarios1_idx` (`id_usuario` ASC) VISIBLE,
  CONSTRAINT `fk_Comparaciones_Guardadas_Categorias1`
    FOREIGN KEY (`id_categoria`)
    REFERENCES `techmatch`.`categorias` (`id_categoria`),
  CONSTRAINT `fk_Comparaciones_Guardadas_Usuarios1`
    FOREIGN KEY (`id_usuario`)
    REFERENCES `techmatch`.`usuarios` (`id_usuario`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `techmatch`.`producto_comparacion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `techmatch`.`producto_comparacion` (
  `id_producto` INT NOT NULL,
  `id_comparacion` INT NOT NULL,
  PRIMARY KEY (`id_producto`, `id_comparacion`),
  INDEX `fk_Componentes_has_Comparaciones_Guardadas_Comparaciones_Gu_idx` (`id_comparacion` ASC) VISIBLE,
  INDEX `fk_Componentes_has_Comparaciones_Guardadas_Componentes2_idx` (`id_producto` ASC) VISIBLE,
  CONSTRAINT `fk_Componentes_has_Comparaciones_Guardadas_Comparaciones_Guar2`
    FOREIGN KEY (`id_comparacion`)
    REFERENCES `techmatch`.`comparaciones_guardadas` (`id_comparacion`),
  CONSTRAINT `fk_Componentes_has_Comparaciones_Guardadas_Componentes2`
    FOREIGN KEY (`id_producto`)
    REFERENCES `techmatch`.`productos` (`id_producto`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `techmatch`.`cpu`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `techmatch`.`cpu` (
  `id_CPU` INT NOT NULL AUTO_INCREMENT,
  `nucleos` INT NULL DEFAULT NULL,
  `hilos` INT NULL DEFAULT NULL,
  `frecuencia_base` DECIMAL(4,2) NULL DEFAULT NULL,
  `frecuencia_turbo` DECIMAL(4,2) NULL DEFAULT NULL,
  `tdp` INT NULL DEFAULT NULL,
  `id_producto` INT NOT NULL,
  PRIMARY KEY (`id_CPU`),
  INDEX `fk_CPU_Productos1_idx` (`id_producto` ASC) VISIBLE,
  CONSTRAINT `fk_CPU_Productos1`
    FOREIGN KEY (`id_producto`)
    REFERENCES `techmatch`.`productos` (`id_producto`))
ENGINE = InnoDB
AUTO_INCREMENT = 93
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `techmatch`.`gpu`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `techmatch`.`gpu` (
  `id_GPU` INT NOT NULL AUTO_INCREMENT,
  `vram` INT NULL DEFAULT NULL,
  `tipo_memoria` VARCHAR(45) NULL DEFAULT NULL,
  `consumo_wh` INT NULL DEFAULT NULL,
  `id_producto` INT NOT NULL,
  PRIMARY KEY (`id_GPU`),
  INDEX `fk_GPU_Productos1_idx` (`id_producto` ASC) VISIBLE,
  CONSTRAINT `fk_GPU_Productos1`
    FOREIGN KEY (`id_producto`)
    REFERENCES `techmatch`.`productos` (`id_producto`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `techmatch`.`guarda_favorito`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `techmatch`.`guarda_favorito` (
  `id_producto` INT NOT NULL,
  `id_usuario` INT NOT NULL,
  `fecha_agregado_fav` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id_producto`, `id_usuario`),
  INDEX `fk_Componentes_has_Usuarios_Usuarios2_idx` (`id_usuario` ASC) VISIBLE,
  INDEX `fk_Componentes_has_Usuarios_Componentes2_idx` (`id_producto` ASC) VISIBLE,
  CONSTRAINT `fk_Componentes_has_Usuarios_Componentes2`
    FOREIGN KEY (`id_producto`)
    REFERENCES `techmatch`.`productos` (`id_producto`),
  CONSTRAINT `fk_Componentes_has_Usuarios_Usuarios2`
    FOREIGN KEY (`id_usuario`)
    REFERENCES `techmatch`.`usuarios` (`id_usuario`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `techmatch`.`laptops`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `techmatch`.`laptops` (
  `id_laptop` INT NOT NULL AUTO_INCREMENT,
  `peso_kg` DECIMAL(4,2) NULL DEFAULT NULL,
  `tamanio_pantalla` DECIMAL(4,1) NULL DEFAULT NULL,
  `tasa_refresco_hz` INT NULL DEFAULT NULL,
  `capacidad_bateria_wh` INT NULL DEFAULT NULL,
  `id_producto` INT NOT NULL,
  `cpu_modelo` VARCHAR(100) NULL DEFAULT NULL,
  `gpu_modelo` VARCHAR(100) NULL DEFAULT NULL,
  `ram_gb` INT NULL DEFAULT NULL,
  `almacenamiento_gb` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id_laptop`),
  INDEX `fk_Laptops_Productos1_idx` (`id_producto` ASC) VISIBLE,
  CONSTRAINT `fk_Laptops_Productos1`
    FOREIGN KEY (`id_producto`)
    REFERENCES `techmatch`.`productos` (`id_producto`))
ENGINE = InnoDB
AUTO_INCREMENT = 23
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `techmatch`.`perfiles_uso`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `techmatch`.`perfiles_uso` (
  `id_perfil` INT NOT NULL AUTO_INCREMENT,
  `nombre_perfil` ENUM('gaming', 'ofimatica', 'diseño', 'Desarrollo de Software') NOT NULL,
  PRIMARY KEY (`id_perfil`))
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb3;



-- -----------------------------------------------------
-- Table `techmatch`.`productos_perfiles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `techmatch`.`productos_perfiles` (
  `id_perfil` INT NOT NULL,
  `id_producto` INT NOT NULL,
  PRIMARY KEY (`id_perfil`, `id_producto`),
  INDEX `fk_Perfiles_Uso_has_Productos_Productos1_idx` (`id_producto` ASC) VISIBLE,
  INDEX `fk_Perfiles_Uso_has_Productos_Perfiles_Uso1_idx` (`id_perfil` ASC) VISIBLE,
  CONSTRAINT `fk_Perfiles_Uso_has_Productos_Perfiles_Uso1`
    FOREIGN KEY (`id_perfil`)
    REFERENCES `techmatch`.`perfiles_uso` (`id_perfil`),
  CONSTRAINT `fk_Perfiles_Uso_has_Productos_Productos1`
    FOREIGN KEY (`id_producto`)
    REFERENCES `techmatch`.`productos` (`id_producto`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `techmatch`.`ram`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `techmatch`.`ram` (
  `id_RAM` INT NOT NULL AUTO_INCREMENT,
  `capacidad_gb_ram` INT NULL DEFAULT NULL,
  `velocidad_mhz` INT NULL DEFAULT NULL,
  `latencia_cl` INT NULL DEFAULT NULL,
  `tipo_ram` ENUM('DDR3', 'DDR4', 'DDR5') NULL DEFAULT NULL,
  `id_producto` INT NOT NULL,
  PRIMARY KEY (`id_RAM`),
  INDEX `fk_RAM_Productos1_idx` (`id_producto` ASC) VISIBLE,
  CONSTRAINT `fk_RAM_Productos1`
    FOREIGN KEY (`id_producto`)
    REFERENCES `techmatch`.`productos` (`id_producto`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `techmatch`.`tiendas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `techmatch`.`tiendas` (
  `id_tienda` INT NOT NULL AUTO_INCREMENT,
  `nombre_tienda` VARCHAR(45) NULL DEFAULT NULL,
  `url_tienda` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id_tienda`))
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `techmatch`.`producto_tienda`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `techmatch`.`producto_tienda` (
  `id_producto` INT NOT NULL,
  `id_tienda` INT NOT NULL,
  `precio` DECIMAL(12,2) NULL DEFAULT NULL,
  `url_producto` VARCHAR(2083) NULL DEFAULT NULL,
  `fec_actualizacion` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id_producto`, `id_tienda`),
  INDEX `fk_Componentes_has_Tiendas_Tiendas1_idx` (`id_tienda` ASC) VISIBLE,
  INDEX `fk_Componentes_has_Tiendas_Componentes1_idx` (`id_producto` ASC) VISIBLE,
  CONSTRAINT `fk_Componentes_has_Tiendas_Componentes1`
    FOREIGN KEY (`id_producto`)
    REFERENCES `techmatch`.`productos` (`id_producto`),
  CONSTRAINT `fk_Componentes_has_Tiendas_Tiendas1`
    FOREIGN KEY (`id_tienda`)
    REFERENCES `techmatch`.`tiendas` (`id_tienda`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;

-- -----------------------------------------------------
-- Procedimiento Almacenado
-- -----------------------------------------------------

DELIMITER $$

-- Elimina una comparación borrando primero el detalle y luego la cabecera.
DROP PROCEDURE IF EXISTS `sp_eliminar_comparacion`$$
CREATE PROCEDURE `sp_eliminar_comparacion`(
    IN p_id_comparacion INT
)
BEGIN
    -- 1. Borrar el detalle (tabla hija) para respetar la clave foránea
    DELETE FROM producto_comparacion WHERE id_comparacion = p_id_comparacion;

    -- 2. Borrar la cabecera
    DELETE FROM comparaciones_guardadas WHERE id_comparacion = p_id_comparacion;
END$$

-- Guarda una comparación en cascada: cabecera + dos filas de detalle.
DROP PROCEDURE IF EXISTS `sp_guardar_comparacion`$$
CREATE PROCEDURE `sp_guardar_comparacion`(
    IN p_id_usuario     INT,
    IN p_id_producto_a  INT,
    IN p_id_producto_b  INT,
    IN p_id_categoria   INT
)
BEGIN
    DECLARE v_id_comparacion INT;

    -- 1. Insertar cabecera — MySQL genera el id por AUTO_INCREMENT
    INSERT INTO comparaciones_guardadas (fec_creacion_comp, id_categoria, id_usuario)
    VALUES (NOW(), p_id_categoria, p_id_usuario);

    -- 2. Capturar el ID recién generado
    SET v_id_comparacion = LAST_INSERT_ID();

    -- 3. Insertar los dos productos en la tabla de detalle
    INSERT IGNORE INTO producto_comparacion (id_producto, id_comparacion)
    VALUES (p_id_producto_a, v_id_comparacion);

    INSERT IGNORE INTO producto_comparacion (id_producto, id_comparacion)
    VALUES (p_id_producto_b, v_id_comparacion);

    -- 4. Devolver el ID generado para confirmación
    SELECT v_id_comparacion AS id_comparacion;
END$$

DELIMITER ;


-- -----------------------------------------------------
-- Vista
-- -----------------------------------------------------

-- Presenta el catálogo completo con categoría, marca y precio mínimo disponible.
-- Centraliza la consulta más frecuente del sistema para simplificar futuras queries.
CREATE OR REPLACE VIEW `vista_catalogo_completo` AS
SELECT
    p.id_producto,
    p.modelo_producto,
    p.img_url,
    c.nombre_categoria,
    m.nombre_marca,
    MIN(s.precio)        AS precio_minimo,
    COUNT(s.id_tienda)   AS cantidad_tiendas
FROM productos p
JOIN  categorias    c ON p.id_categoria = c.id_categoria
JOIN  marcas        m ON p.id_marca     = m.id_marca
LEFT JOIN producto_tienda s ON p.id_producto = s.id_producto
GROUP BY
    p.id_producto, p.modelo_producto, p.img_url,
    c.nombre_categoria, m.nombre_marca;


-- -----------------------------------------------------
-- Trigger
-- -----------------------------------------------------

DELIMITER $$

-- Valida que los productos de una comparación sean de la misma categoría.
-- Se dispara BEFORE INSERT en producto_comparacion, antes de confirmar el segundo producto.
DROP TRIGGER IF EXISTS `trg_validar_categoria_comparacion`$$
CREATE TRIGGER `trg_validar_categoria_comparacion`
BEFORE INSERT ON `producto_comparacion`
FOR EACH ROW
BEGIN
    DECLARE v_categoria_nuevo     INT;
    DECLARE v_categoria_existente INT;
    DECLARE v_count               INT;

    -- Ver si ya hay al menos un producto en esta comparación
    SELECT COUNT(*) INTO v_count
    FROM producto_comparacion
    WHERE id_comparacion = NEW.id_comparacion;

    IF v_count > 0 THEN
        -- Categoría del producto que se quiere insertar
        SELECT id_categoria INTO v_categoria_nuevo
        FROM productos
        WHERE id_producto = NEW.id_producto;

        -- Categoría del producto ya existente en la comparación
        SELECT p.id_categoria INTO v_categoria_existente
        FROM producto_comparacion c
        JOIN productos p ON c.id_producto = p.id_producto
        WHERE c.id_comparacion = NEW.id_comparacion
        LIMIT 1;

        IF v_categoria_nuevo <> v_categoria_existente THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Los productos de una comparación deben ser de la misma categoría.';
        END IF;
    END IF;
END$$

DELIMITER ;


-- -----------------------------------------------------
-- Datos iniciales: Tiendas conocidas
-- (requerido para que los scrapers guarden precios en producto_tienda)
-- -----------------------------------------------------
INSERT IGNORE INTO `techmatch`.`tiendas` (`nombre_tienda`, `url_tienda`) VALUES
('Mercado Libre',  'https://www.mercadolibre.com.ar'),
('Compra Gamer',   'https://www.compragamer.com'),
('Asus Oficial',   'https://www.asus.com/ar'),
('Lenovo Oficial', 'https://www.lenovo.com/ar');


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
