-- Esquema de base de datos para el sistema de cumpleaños
-- Ejecutar este script en PostgreSQL para crear las tablas necesarias

-- Tabla para almacenar información de personas
CREATE TABLE IF NOT EXISTS persona (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    correo VARCHAR(255),
    telefono VARCHAR(20),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla para registrar bitácora de procesamiento
CREATE TABLE IF NOT EXISTS bitacora (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    dias_para_cumple INTEGER NOT NULL,
    notificacion_enviada BOOLEAN NOT NULL,
    tipo_notificacion VARCHAR(20) DEFAULT 'whatsapp', -- 'email' o 'whatsapp'
    fecha_procesamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para mejorar rendimiento
CREATE INDEX IF NOT EXISTS idx_persona_fecha_nacimiento ON persona(fecha_nacimiento);
CREATE INDEX IF NOT EXISTS idx_persona_activo ON persona(activo);
CREATE INDEX IF NOT EXISTS idx_bitacora_fecha ON bitacora(fecha);
CREATE INDEX IF NOT EXISTS idx_bitacora_nombre ON bitacora(nombre);

-- Comentarios en las tablas
COMMENT ON TABLE persona IS 'Tabla para almacenar información de personas para el sistema de cumpleaños';
COMMENT ON TABLE bitacora IS 'Tabla para registrar el procesamiento diario de cumpleaños';

-- Datos de ejemplo (opcional)
-- INSERT INTO persona (nombre, fecha_nacimiento, correo, telefono) VALUES
--     ('Juan Pérez', '1990-05-15', 'juan@example.com', '+34612345678'),
--     ('María García', '1985-12-03', 'maria@example.com', '+34687654321'),
--     ('Carlos López', '1992-08-22', 'carlos@example.com', '+34611223344'),
--     ('Ana Martínez', '1988-03-10', 'ana@example.com', '+34655667788');

-- Función para actualizar fecha_actualizacion automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para actualizar fecha_actualizacion
CREATE TRIGGER update_persona_updated_at 
    BEFORE UPDATE ON persona 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Vista útil para ver personas con cumpleaños próximos
CREATE OR REPLACE VIEW v_cumpleanos_proximos AS
SELECT 
    nombre,
    fecha_nacimiento,
    correo,
    telefono,
    EXTRACT(YEAR FROM AGE(CURRENT_DATE, fecha_nacimiento)) as edad_actual,
    EXTRACT(DOY FROM fecha_nacimiento) - EXTRACT(DOY FROM CURRENT_DATE) as dias_para_cumple
FROM persona 
WHERE activo = TRUE
ORDER BY dias_para_cumple;

-- Vista para estadísticas de bitácora
CREATE OR REPLACE VIEW v_estadisticas_bitacora AS
SELECT 
    fecha,
    COUNT(*) as total_procesados,
    SUM(CASE WHEN notificacion_enviada THEN 1 ELSE 0 END) as notificaciones_enviadas,
    SUM(CASE WHEN not notificacion_enviada THEN 1 ELSE 0 END) as sin_notificar
FROM bitacora 
GROUP BY fecha 
ORDER BY fecha DESC; 