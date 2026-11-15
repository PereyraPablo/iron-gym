

-- ==========================================================
-- PROYECTO: IRON GYM
-- BASE DE DATOS: iron_gym
-- MOTOR: InnoDB
-- CODIFICACION: utf8mb4
-- ==========================================================

-- Crear la base de datos si todavía no existe.
CREATE DATABASE IF NOT EXISTS iron_gym
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE iron_gym;


-- ==========================================================
-- 1. TABLA: ROLES
-- Almacena los roles de todas las personas que utilizan el sistema.
-- ==========================================================

CREATE TABLE roles (
    nombre_rol VARCHAR(20) PRIMARY KEY,
    descripcion VARCHAR(150) NOT NULL
) ENGINE=InnoDB;

-- Roles iniciales del sistema.
INSERT INTO roles (nombre_rol, descripcion) VALUES
('ADMIN', 'Administrador del gimnasio'),
('SOCIO', 'Socio del gimnasio'),
('INSTRUCTOR', 'Instructor del gimnasio');

-- ==========================================================
-- 2. TABLA: USUARIOS
-- Almacena los datos personales, las cuentas de acceso
-- y los roles de todas las personas que utilizan el sistema.
-- MODIFICACIÓN:
-- Se incorporan nombre, apellido y telefono.
-- Estos datos ya no se repiten en socios e instructores.
-- ==========================================================


CREATE TABLE usuarios (
    dni CHAR(8) PRIMARY KEY,
    nombre VARCHAR(60) NOT NULL,
    apellido VARCHAR(60) NOT NULL,
    telefono VARCHAR(25) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol VARCHAR(20) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso DATETIME NULL,

    CONSTRAINT fk_usuarios_roles
        FOREIGN KEY (rol)
        REFERENCES roles(nombre_rol)
        ON UPDATE CASCADE
        ON DELETE RESTRICT

) ENGINE=InnoDB;


-- ==========================================================
-- 3. TABLA: SOCIOS
-- Almacena los datos específicos de los socios.
-- Cada socio debe tener una cuenta de usuario.
-- MODIFICACIÓN:
-- Se eliminan nombre, apellido y telefono.
-- Ahora esos datos se obtienen desde usuarios mediante DNI.
-- Se conserva activo porque representa el estado de la
-- condición de socio, independientemente de la cuenta.
-- ==========================================================

CREATE TABLE socios (
    dni CHAR(8) PRIMARY KEY,
    fecha_alta DATE NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT fk_socios_usuarios
        FOREIGN KEY (dni)
        REFERENCES usuarios(dni)
        ON UPDATE CASCADE
        ON DELETE RESTRICT -- Impide borrar un usuario si existen socios que lo están referenciando.

) ENGINE=InnoDB;


-- ==========================================================
-- 4. TABLA: INSTRUCTORES
-- Almacena los datos específicos de los instructores.
-- Cada instructor debe tener una cuenta de usuario.
-- MODIFICACIÓN:
-- Se eliminan nombre, apellido y telefono.
-- Se elimina email_contacto porque utilizaremos el email
-- almacenado en usuarios.
-- Se conservan especialidad, activo y fecha_alta.
-- ==========================================================

CREATE TABLE instructores (
    dni CHAR(8) PRIMARY KEY,
    especialidad VARCHAR(100) NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_alta DATE NOT NULL,

    CONSTRAINT fk_instructores_usuarios
        FOREIGN KEY (dni)
        REFERENCES usuarios(dni)
        ON UPDATE CASCADE
        ON DELETE RESTRICT

) ENGINE=InnoDB;



-- ==========================================================
-- 5. TABLA: PLANES
-- Almacena los planes y tarifas del gimnasio.
-- MODIFICACIÓN:
-- Se elimina id_plan AUTO_INCREMENT.
-- El campo nombre pasa a ser la clave primaria (PK).
-- De esta manera identificamos cada plan directamente
-- por su nombre, por ejemplo: 'Plan trimestral'.
-- ==========================================================

CREATE TABLE planes (
    nombre VARCHAR(60) PRIMARY KEY,
    descripcion VARCHAR(255) NULL,
    precio DECIMAL(10,2) NOT NULL,
    duracion_valor INT NOT NULL,
    unidad_duracion ENUM('DIA', 'MES') NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT chk_planes_precio
        CHECK (precio > 0),

    CONSTRAINT chk_planes_duracion -- Permite asignar un nombre a una restricción.
        CHECK (duracion_valor > 0)  -- Valida condiciones

) ENGINE=InnoDB;


-- ==========================================================
-- 6. TABLA: SOLICITUDES_INSCRIPCION
-- Registra las solicitudes de personas interesadas.
-- Todavía no son socios registrados.
-- MODIFICACIÓN:
-- Se reemplaza id_plan por nombre_plan.
-- La clave foránea ahora referencia planes(nombre).
-- ==========================================================

CREATE TABLE solicitudes_inscripcion (
    id_solicitud INT AUTO_INCREMENT PRIMARY KEY,
    dni CHAR(8) NOT NULL,
    nombre VARCHAR(60) NOT NULL,
    apellido VARCHAR(60) NOT NULL,
    email VARCHAR(120) NOT NULL,
    telefono VARCHAR(25) NOT NULL,
    nombre_plan VARCHAR(60) NOT NULL,
    -- Se conserva el precio y la duración informados
    -- al momento de realizar la solicitud.
    precio_solicitado DECIMAL(10,2) NOT NULL,
    duracion_solicitada INT NOT NULL,
    unidad_duracion ENUM('DIA', 'MES') NOT NULL,

    estado ENUM('PENDIENTE', 'APROBADA', 'RECHAZADA')
        NOT NULL DEFAULT 'PENDIENTE',

    fecha_solicitud DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    revisado_por CHAR(8) NULL,
    fecha_revision DATETIME NULL,

    CONSTRAINT fk_solicitudes_planes
        FOREIGN KEY (nombre_plan)
        REFERENCES planes(nombre)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,

    CONSTRAINT fk_solicitudes_usuarios
        FOREIGN KEY (revisado_por)
        REFERENCES usuarios(dni)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_solicitudes_precio
        CHECK (precio_solicitado > 0),

    CONSTRAINT chk_solicitudes_duracion
        CHECK (duracion_solicitada > 0)

) ENGINE=InnoDB;


-- ==========================================================
-- 7. TABLA: MAQUINAS
-- Catálogo de equipamiento del gimnasio.
-- ==========================================================

CREATE TABLE maquinas (
    id_maquina INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    marca VARCHAR(60) NULL,
    modelo VARCHAR(60) NULL,
    descripcion TEXT NULL,
    carga_minima DECIMAL(6,2) NULL,
    carga_maxima DECIMAL(6,2) NULL,
    imagen VARCHAR(255) NULL,

    estado ENUM('ACTIVA', 'INACTIVA', 'REPARACION')
        NOT NULL DEFAULT 'ACTIVA',

    fecha_alta DATE NOT NULL,

    CONSTRAINT chk_maquinas_cargas
        CHECK (
            (carga_minima IS NULL AND carga_maxima IS NULL)
            OR
            (
                carga_minima IS NOT NULL
                AND carga_maxima IS NOT NULL
                AND carga_minima >= 0
                AND carga_maxima >= carga_minima
            )
        )

) ENGINE=InnoDB;


-- ==========================================================
-- 8. TABLA: GRUPOS_MUSCULARES
-- Clasificación de los grupos musculares.
-- ==========================================================

CREATE TABLE grupos_musculares (
    id_grupo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(60) NOT NULL UNIQUE,
    descripcion VARCHAR(255) NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE

) ENGINE=InnoDB;


-- ==========================================================
-- 9. TABLA: MAQUINA_GRUPO_MUSCULAR
-- Resuelve la relación muchos a muchos entre máquinas
-- y grupos musculares.
-- ==========================================================

CREATE TABLE maquina_grupo_muscular (
    id_maquina INT NOT NULL,
    id_grupo INT NOT NULL,
    tipo_trabajo ENUM('PRINCIPAL', 'SECUNDARIO') NOT NULL,

    PRIMARY KEY (id_maquina, id_grupo),

    CONSTRAINT fk_mgm_maquinas
        FOREIGN KEY (id_maquina)
        REFERENCES maquinas(id_maquina)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_mgm_grupos
        FOREIGN KEY (id_grupo)
        REFERENCES grupos_musculares(id_grupo)
        ON UPDATE CASCADE
        ON DELETE RESTRICT

) ENGINE=InnoDB;


-- ==========================================================
-- 10. TABLA: MEMBRESIAS
-- Registra las membresías contratadas por los socios.
-- MODIFICACIÓN:
-- Se reemplaza id_plan por nombre_plan.
-- La clave foránea ahora referencia planes(nombre).
-- Se conserva importe_contratado y duracion_contratada
-- para mantener el historial de las condiciones contratadas.
-- ==========================================================

CREATE TABLE membresias (
    id_membresia INT AUTO_INCREMENT PRIMARY KEY,
    dni_socio CHAR(8) NOT NULL,
    nombre_plan VARCHAR(60) NOT NULL,
    registrado_por CHAR(8) NOT NULL,
    fecha_inicio DATE NULL,
    fecha_vencimiento DATE NULL,
    importe_contratado DECIMAL(10,2) NOT NULL,
    duracion_contratada INT NOT NULL,
    unidad_duracion ENUM('DIA', 'MES') NOT NULL,

    estado ENUM('PENDIENTE', 'VIGENTE', 'VENCIDA', 'CANCELADA')
        NOT NULL DEFAULT 'PENDIENTE',

    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_membresias_socios
        FOREIGN KEY (dni_socio)
        REFERENCES socios(dni)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_membresias_planes
        FOREIGN KEY (nombre_plan)
        REFERENCES planes(nombre)
        ON UPDATE RESTRICT
        ON DELETE RESTRICT,

    CONSTRAINT fk_membresias_usuarios
        FOREIGN KEY (registrado_por)
        REFERENCES usuarios(dni)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_membresias_importe
        CHECK (importe_contratado > 0),

    CONSTRAINT chk_membresias_duracion
        CHECK (duracion_contratada > 0),

    CONSTRAINT chk_membresias_fechas
        CHECK (
            (estado = 'PENDIENTE'
                AND fecha_inicio IS NULL -- Comprueba que la fecha de inicio no tenga ningún valor asignado.
                AND fecha_vencimiento IS NULL) -- Comprueba que tampoco exista una fecha de vencimiento
            OR
            (estado IN ('VIGENTE', 'VENCIDA')
                AND fecha_inicio IS NOT NULL -- Exige que la membresía tenga una fecha de inicio
                AND fecha_vencimiento IS NOT NULL -- Exige que también tenga una fecha de vencimiento
                AND fecha_vencimiento >= fecha_inicio)
            OR
            (estado = 'CANCELADA')
        )

) ENGINE=InnoDB;


-- ==========================================================
-- 11. TABLA: PAGOS
-- Registra los pagos verificados por el administrador.
-- ==========================================================

CREATE TABLE pagos (
    id_pago INT AUTO_INCREMENT PRIMARY KEY,
    id_membresia INT NOT NULL,
    dni_administrador CHAR(8) NOT NULL,
    fecha_pago DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    importe DECIMAL(10,2) NOT NULL,
    medio_pago ENUM('EFECTIVO', 'TRANSFERENCIA') NOT NULL,
    referencia VARCHAR(100) NULL,
    observaciones TEXT NULL,

    CONSTRAINT fk_pagos_membresias
        FOREIGN KEY (id_membresia)
        REFERENCES membresias(id_membresia)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_pagos_usuarios
        FOREIGN KEY (dni_administrador)
        REFERENCES usuarios(dni)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_pagos_importe
        CHECK (importe > 0)

) ENGINE=InnoDB;


-- ==========================================================
-- 12. TABLA: NOTIFICACIONES
-- Registra las notificaciones internas y los emails.
-- ==========================================================

CREATE TABLE notificaciones (
    id_notificacion INT AUTO_INCREMENT PRIMARY KEY,
    id_membresia INT NOT NULL,
    tipo ENUM('PROXIMO_VENCIMIENTO', 'VENCIMIENTO') NOT NULL,
    canal ENUM('INTERNO', 'EMAIL') NOT NULL,
    dias_anticipacion INT NOT NULL,
    mensaje VARCHAR(500) NOT NULL,
    fecha_programada DATETIME NOT NULL,
    fecha_envio DATETIME NULL,
    estado ENUM('PENDIENTE', 'ENVIADA', 'ERROR')
        NOT NULL DEFAULT 'PENDIENTE',

    leida BOOLEAN NOT NULL DEFAULT FALSE,
    detalle_error TEXT NULL,

    CONSTRAINT fk_notificaciones_membresias
        FOREIGN KEY (id_membresia)
        REFERENCES membresias(id_membresia)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    -- Evita generar dos veces el mismo aviso
    -- para una misma membresía y canal.
    CONSTRAINT uq_notificaciones
        UNIQUE (
            id_membresia,
            tipo,
            canal,
            dias_anticipacion
        ),

    CONSTRAINT chk_notificaciones_dias
    CHECK (
        (tipo = 'PROXIMO_VENCIMIENTO'
            AND dias_anticipacion IN (1, 3, 7))
        OR
        (tipo = 'VENCIMIENTO'
            AND dias_anticipacion = 0)
    )

) ENGINE=InnoDB;


-- ==========================================================
-- ÍNDICES ADICIONALES
-- Mejoran las búsquedas y consultas frecuentes.
-- MODIFICACIÓN:
-- Se reemplazan los índices de socios e instructores
-- por un único índice sobre usuarios(apellido).
-- Ambos tipos de personas comparten ahora ese campo.
-- ==========================================================

CREATE INDEX idx_usuarios_apellido
ON usuarios(apellido);

CREATE INDEX idx_maquinas_estado
ON maquinas(estado);

CREATE INDEX idx_membresias_socio_estado
ON membresias(dni_socio, estado);

CREATE INDEX idx_membresias_vencimiento
ON membresias(fecha_vencimiento);

CREATE INDEX idx_pagos_fecha
ON pagos(fecha_pago);

CREATE INDEX idx_notificaciones_estado_fecha
ON notificaciones(estado, fecha_programada);


-- ==========================================================
-- FIN DE LA ESTRUCTURA DE LA BASE DE DATOS
-- ==========================================================
