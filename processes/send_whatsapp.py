# Este proceso se encargará de enviar mensajes de WhatsApp a los usuarios que tengan su cumpleaños en el día de hoy desde PostgreSQL

import os
from datetime import date
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

from utils.logger import logger
from utils.postgresql.main import PostgreSQLManager
from utils.birthday import BirthdayCalculator
from utils.whatsapp.main import send_whatsapp

# Obtener variables de entorno de WhatsApp
WHATSAPP_URL = os.getenv('WHATSAPP_URL')
WHATSAPP_USER = os.getenv('WHATSAPP_USER')
WHATSAPP_PASS = os.getenv('WHATSAPP_PASS')

def send_birthday_whatsapp(nombre, telefono):
    """
    Envía un mensaje de WhatsApp de cumpleaños
    
    Args:
        nombre (str): Nombre de la persona
        telefono (str): Número de teléfono del destinatario
        
    Returns:
        bool: True si se envió exitosamente, False en caso contrario
    """
    try:
        # Datos para el template
        data = {
            "nombre": nombre
        }
        
        # Enviar mensaje de WhatsApp de cumpleaños
        logger.info(f"Enviando mensaje de WhatsApp de cumpleaños a {telefono}")
        
        success = send_whatsapp(
            to=telefono,
            data=data,
            purpose="cumple"
        )
        
        if success:
            logger.success(f"Mensaje de WhatsApp de cumpleaños enviado exitosamente a {nombre}")
            return True
        else:
            logger.error(f"Error al enviar mensaje de WhatsApp de cumpleaños a {nombre}")
            return False
            
    except Exception as e:
        logger.error(f"Error al enviar mensaje de WhatsApp de cumpleaños: {e}")
        return False

def read_personas_from_db(db_manager):
    """
    Lee todas las personas de la tabla 'persona'
    
    Args:
        db_manager: Instancia de PostgreSQLManager
        
    Returns:
        list: Lista de diccionarios con los datos de las personas
    """
    query = "SELECT nombre, fecha_nacimiento, correo, telefono FROM persona;"
    return db_manager.execute_query(query)

def write_to_bitacora(db_manager, nombre, dias_para_cumple, notificacion_enviada):
    """
    Escribe un registro en la tabla 'bitacora'
    
    Args:
        db_manager: Instancia de PostgreSQLManager
        nombre (str): Nombre de la persona
        dias_para_cumple (int): Días para el cumpleaños
        notificacion_enviada (bool): Si se envió la notificación
        
    Returns:
        bool: True si se guardó exitosamente, False en caso contrario
    """
    query = """
        INSERT INTO bitacora (fecha, nombre, dias_para_cumple, notificacion_enviada)
        VALUES (%s, %s, %s, %s);
    """
    return db_manager.execute_command(
        query, 
        (date.today(), nombre, dias_para_cumple, notificacion_enviada)
    )

def main():
    """
    Función principal que ejecuta todo el proceso de envío de WhatsApp
    """
    logger.info("Iniciando sistema de envío de mensajes de WhatsApp")
    logger.info("="*60)
    
    try:
        # Inicializar manager de PostgreSQL
        db_manager = PostgreSQLManager()
        
        # Conectar con PostgreSQL
        if not db_manager.connect():
            logger.error("No se pudo establecer conexión con PostgreSQL")
            return
        
        # Obtener información de la base de datos
        db_info = db_manager.get_database_info()
        logger.info(f"Conectado a PostgreSQL: {db_info['database']} en {db_info['host']}:{db_info['port']}")
        
        # Verificar que existe la tabla persona
        if not db_manager.table_exists('persona'):
            logger.error("La tabla 'persona' no existe en la base de datos")
            logger.error("Crea la tabla con: CREATE TABLE persona (nombre VARCHAR(255), fecha_nacimiento DATE, correo VARCHAR(255), telefono VARCHAR(20));")
            return
        
        # Verificar que existe la tabla bitacora
        if not db_manager.table_exists('bitacora'):
            logger.error("La tabla 'bitacora' no existe en la base de datos")
            logger.error("Crea la tabla con: CREATE TABLE bitacora (fecha DATE, nombre VARCHAR(255), dias_para_cumple INT, notificacion_enviada BOOLEAN);")
            return
        
        # Leer datos de personas
        personas = read_personas_from_db(db_manager)
        if personas is None:
            logger.error("No se pudieron leer los datos de la tabla 'persona'")
            return
        
        logger.info(f"DATOS PRINCIPALES - {len(personas)} personas encontradas")
        logger.info("="*60)
        
        # Procesar cada persona
        mensajes_enviados = 0
        personas_procesadas = 0
        
        for persona in personas:
            nombre = persona['nombre']
            fecha_nacimiento = persona['fecha_nacimiento']
            telefono = persona['telefono']
            
            logger.info(f"Procesando: {nombre}")
            logger.info(f"Fecha de nacimiento: {fecha_nacimiento}")
            logger.info(f"Teléfono: {telefono}")
            
            # Convertir fecha de PostgreSQL a string para BirthdayCalculator
            fecha_str = fecha_nacimiento.strftime('%d/%m/%Y')
            
            # Obtener información completa del cumpleaños usando el módulo
            birthday_info = BirthdayCalculator.get_birthday_info(nombre, fecha_str)
            
            if 'error' not in birthday_info:
                logger.info(f"Días para cumpleaños: {birthday_info['dias_para_cumple']}")
                logger.info(f"Edad actual: {birthday_info['edad_actual']} años")
                logger.info(birthday_info['mensaje'])
                
                # Variable para tracking si se envió mensaje
                mensaje_enviado = False
                
                # Enviar mensaje si es cumpleaños
                if birthday_info['enviar_correo'] and telefono:
                    logger.info("Enviando mensaje de WhatsApp de felicitación")
                    mensaje_enviado = send_birthday_whatsapp(nombre, telefono)
                    if mensaje_enviado:
                        mensajes_enviados += 1
                elif not telefono:
                    logger.warning(f"No hay número de teléfono para {nombre}")
                
                # Escribir en bitácora
                logger.info("Guardando en bitácora")
                success = write_to_bitacora(
                    db_manager,
                    nombre, 
                    birthday_info['dias_para_cumple'], 
                    mensaje_enviado
                )
                
                if success:
                    logger.success("Datos guardados exitosamente en bitácora")
                    personas_procesadas += 1
                else:
                    logger.error("Error al guardar en bitácora")
            else:
                logger.error(f"Error: {birthday_info['error']}")
        
        # Resumen final
        logger.info("RESUMEN DE PROCESAMIENTO")
        logger.info("="*60)
        logger.info(f"Personas procesadas: {personas_procesadas}")
        logger.info(f"Mensajes de WhatsApp enviados: {mensajes_enviados}")
        logger.info(f"WhatsApp configurado: {WHATSAPP_USER}")
        
        # Mostrar información de las tablas
        persona_count = db_manager.execute_query("SELECT COUNT(*) as total FROM persona;")
        bitacora_count = db_manager.execute_query("SELECT COUNT(*) as total FROM bitacora;")
        
        if persona_count:
            logger.info(f"Total de personas en BD: {persona_count[0]['total']}")
        if bitacora_count:
            logger.info(f"Total de registros en bitácora: {bitacora_count[0]['total']}")
        
        logger.success("Proceso completado exitosamente")
        logger.info("Revisa la tabla 'bitacora' en PostgreSQL para ver los resultados")
        if mensajes_enviados > 0:
            logger.info(f"Se enviaron {mensajes_enviados} mensaje(s) de WhatsApp de cumpleaños automáticamente")
    
    except Exception as e:
        logger.error(f"Error inesperado en el proceso: {e}")
    finally:
        # Cerrar conexión
        if 'db_manager' in locals():
            db_manager.disconnect()

if __name__ == "__main__":
    main() 