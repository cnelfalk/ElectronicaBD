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
  UNIQUE INDEX `email_usuario_UNIQUE` (`email_usuario` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 4
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
-- Table `techmatch`.`contiene`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `techmatch`.`contiene` (
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
-- Table `techmatch`.`socket`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `techmatch`.`socket` (
  `id_socket` INT NOT NULL AUTO_INCREMENT,
  `nombre_socket` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id_socket`))
ENGINE = InnoDB
AUTO_INCREMENT = 7
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
  `id_socket` INT NOT NULL,
  `id_producto` INT NOT NULL,
  PRIMARY KEY (`id_CPU`),
  INDEX `fk_CPU_Socket1_idx` (`id_socket` ASC) VISIBLE,
  INDEX `fk_CPU_Productos1_idx` (`id_producto` ASC) VISIBLE,
  CONSTRAINT `fk_CPU_Productos1`
    FOREIGN KEY (`id_producto`)
    REFERENCES `techmatch`.`productos` (`id_producto`),
  CONSTRAINT `fk_CPU_Socket1`
    FOREIGN KEY (`id_socket`)
    REFERENCES `techmatch`.`socket` (`id_socket`))
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
-- Table `techmatch`.`placa_madre`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `techmatch`.`placa_madre` (
  `id_placa_madre` INT NOT NULL AUTO_INCREMENT,
  `formato_placa` VARCHAR(20) NULL DEFAULT NULL,
  `tipo_ram_soportada` VARCHAR(45) NULL DEFAULT NULL,
  `id_socket` INT NOT NULL,
  `id_producto` INT NOT NULL,
  PRIMARY KEY (`id_placa_madre`),
  INDEX `fk_Placa_Madre_Socket1_idx` (`id_socket` ASC) VISIBLE,
  INDEX `fk_Placa_Madre_Productos1_idx` (`id_producto` ASC) VISIBLE,
  CONSTRAINT `fk_Placa_Madre_Productos1`
    FOREIGN KEY (`id_producto`)
    REFERENCES `techmatch`.`productos` (`id_producto`),
  CONSTRAINT `fk_Placa_Madre_Socket1`
    FOREIGN KEY (`id_socket`)
    REFERENCES `techmatch`.`socket` (`id_socket`))
ENGINE = InnoDB
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
-- Table `techmatch`.`se_vende_en`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `techmatch`.`se_vende_en` (
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
-- Procedimientos Almacenados y Funciones
-- -----------------------------------------------------

DELIMITER $$

-- 1. Procedimiento para registrar o actualizar el precio de venta de un producto en una tienda
DROP PROCEDURE IF EXISTS `sp_registrar_precio_producto`$$
CREATE PROCEDURE `sp_registrar_precio_producto`(
    IN p_id_producto INT,
    IN p_id_tienda INT,
    IN p_precio DECIMAL(12,2),
    IN p_url_producto VARCHAR(2083)
)
BEGIN
    INSERT INTO `se_vende_en` (`id_producto`, `id_tienda`, `precio`, `url_producto`, `fec_actualizacion`)
    VALUES (p_id_producto, p_id_tienda, p_precio, p_url_producto, NOW())
    ON DUPLICATE KEY UPDATE 
        `precio` = p_precio, 
        `url_producto` = p_url_producto, 
        `fec_actualizacion` = NOW();
END$$

-- 2. Procedimiento para obtener un reporte estadístico de precios de un producto
DROP PROCEDURE IF EXISTS `sp_obtener_reporte_precios`$$
CREATE PROCEDURE `sp_obtener_reporte_precios`(
    IN p_id_producto INT
)
BEGIN
    SELECT 
        p.id_producto,
        p.modelo_producto,
        MIN(s.precio) AS precio_minimo,
        MAX(s.precio) AS precio_maximo,
        AVG(s.precio) AS precio_promedio,
        COUNT(s.id_tienda) AS cantidad_tiendas
    FROM `productos` p
    LEFT JOIN `se_vende_en` s ON p.id_producto = s.id_producto
    WHERE p.id_producto = p_id_producto
    GROUP BY p.id_producto, p.modelo_producto;
END$$

-- 3. Procedimiento para guardar/actualizar un favorito
DROP PROCEDURE IF EXISTS `sp_guardar_favorito`$$
CREATE PROCEDURE `sp_guardar_favorito`(
    IN p_id_usuario INT,
    IN p_id_producto INT
)
BEGIN
    INSERT INTO `guarda_favorito` (`id_producto`, `id_usuario`, `fecha_agregado_fav`)
    VALUES (p_id_producto, p_id_usuario, NOW())
    ON DUPLICATE KEY UPDATE 
        `fecha_agregado_fav` = NOW();
END$$

-- 4. Función para obtener el precio mínimo de un producto
DROP FUNCTION IF EXISTS `fn_obtener_precio_minimo`$$
CREATE FUNCTION `fn_obtener_precio_minimo`(
    p_id_producto INT
) RETURNS DECIMAL(12,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_precio_min DECIMAL(12,2);
    
    SELECT MIN(`precio`) INTO v_precio_min
    FROM `se_vende_en`
    WHERE `id_producto` = p_id_producto;
    
    RETURN v_precio_min;
END$$

-- 5. Función para calcular un puntaje sintético (0-100) para un CPU
DROP FUNCTION IF EXISTS `fn_calcular_puntaje_cpu`$$
CREATE FUNCTION `fn_calcular_puntaje_cpu`(
    p_id_cpu INT
) RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_nucleos INT;
    DECLARE v_hilos INT;
    DECLARE v_turbo DECIMAL(4,2);
    DECLARE v_puntaje INT DEFAULT 0;
    
    SELECT `nucleos`, `hilos`, `frecuencia_turbo`
    INTO v_nucleos, v_hilos, v_turbo
    FROM `cpu`
    WHERE `id_CPU` = p_id_cpu;
    
    -- Si no existe el CPU, retornamos 0
    IF v_nucleos IS NULL THEN
        RETURN 0;
    END IF;
    
    -- Algoritmo simple ponderado: núcleos (40%), hilos (20%), turbo frequency (40%)
    SET v_puntaje = (v_nucleos * 4) + (v_hilos * 1.5) + (COALESCE(v_turbo, 2.0) * 10);
    
    -- Limitar puntaje máximo a 100
    IF v_puntaje > 100 THEN
        SET v_puntaje = 100;
    END IF;
    
    RETURN v_puntaje;
END$$

-- 6. Función para verificar compatibilidad de sockets entre CPU y Placa Madre
DROP FUNCTION IF EXISTS `fn_verificar_compatibilidad_socket`$$
CREATE FUNCTION `fn_verificar_compatibilidad_socket`(
    p_id_cpu INT,
    p_id_placa INT
) RETURNS TINYINT(1)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_socket_cpu INT;
    DECLARE v_socket_placa INT;
    
    SELECT `id_socket` INTO v_socket_cpu FROM `cpu` WHERE `id_CPU` = p_id_cpu;
    SELECT `id_socket` INTO v_socket_placa FROM `placa_madre` WHERE `id_placa_madre` = p_id_placa;
    
    IF v_socket_cpu IS NOT NULL AND v_socket_placa IS NOT NULL AND v_socket_cpu = v_socket_placa THEN
        RETURN 1;
    ELSE
        RETURN 0;
    END IF;
END$$

-- 4b. Procedimiento alternativo para obtener el precio mínimo (evita error de binary logging/privilegios)
DROP PROCEDURE IF EXISTS `sp_obtener_precio_minimo`$$
CREATE PROCEDURE `sp_obtener_precio_minimo`(
    IN p_id_producto INT,
    OUT p_precio_min DECIMAL(12,2)
)
BEGIN
    SELECT MIN(`precio`) INTO p_precio_min
    FROM `se_vende_en`
    WHERE `id_producto` = p_id_producto;
END$$

-- 5b. Procedimiento alternativo para calcular el puntaje de CPU (evita error de binary logging/privilegios)
DROP PROCEDURE IF EXISTS `sp_calcular_puntaje_cpu`$$
CREATE PROCEDURE `sp_calcular_puntaje_cpu`(
    IN p_id_cpu INT,
    OUT p_puntaje INT
)
BEGIN
    DECLARE v_nucleos INT;
    DECLARE v_hilos INT;
    DECLARE v_turbo DECIMAL(4,2);
    
    SELECT `nucleos`, `hilos`, `frecuencia_turbo`
    INTO v_nucleos, v_hilos, v_turbo
    FROM `cpu`
    WHERE `id_CPU` = p_id_cpu;
    
    IF v_nucleos IS NULL THEN
        SET p_puntaje = 0;
    ELSE
        SET p_puntaje = (v_nucleos * 4) + (v_hilos * 1.5) + (COALESCE(v_turbo, 2.0) * 10);
        IF p_puntaje > 100 THEN
            SET p_puntaje = 100;
        END IF;
    END IF;
END$$

-- 6b. Procedimiento alternativo para verificar compatibilidad de sockets (evita error de binary logging/privilegios)
DROP PROCEDURE IF EXISTS `sp_verificar_compatibilidad_socket`$$
CREATE PROCEDURE `sp_verificar_compatibilidad_socket`(
    IN p_id_cpu INT,
    IN p_id_placa INT,
    OUT p_compatible TINYINT(1)
)
BEGIN
    DECLARE v_socket_cpu INT;
    DECLARE v_socket_placa INT;
    
    SELECT `id_socket` INTO v_socket_cpu FROM `cpu` WHERE `id_CPU` = p_id_cpu;
    SELECT `id_socket` INTO v_socket_placa FROM `placa_madre` WHERE `id_placa_madre` = p_id_placa;
    
    IF v_socket_cpu IS NOT NULL AND v_socket_placa IS NOT NULL AND v_socket_cpu = v_socket_placa THEN
        SET p_compatible = 1;
    ELSE
        SET p_compatible = 0;
    END IF;
END$$

DELIMITER ;


-- -----------------------------------------------------
-- Datos iniciales: Tiendas conocidas
-- (requerido para que los scrapers guarden precios en se_vende_en)
-- -----------------------------------------------------
INSERT IGNORE INTO `techmatch`.`tiendas` (`nombre_tienda`, `url_tienda`) VALUES
('Mercado Libre',  'https://www.mercadolibre.com.ar'),
('Compra Gamer',   'https://www.compragamer.com'),
('Asus Oficial',   'https://www.asus.com/ar'),
('Lenovo Oficial', 'https://www.lenovo.com/ar');


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
