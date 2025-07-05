# Importaciones principales
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importaciones de módulos locales
from utils.sheets import GoogleSheetsManager
from utils.birthday import BirthdayCalculator
from utils.gmail.main import Gmail
from utils.logger import logger

# Obtener variables de entorno
GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')

# Validar que las variables estén configuradas
if not GMAIL_USER or not GMAIL_APP_PASSWORD:
    logger.error("Variables de entorno GMAIL_USER y GMAIL_APP_PASSWORD no están configuradas")
    logger.error("Asegúrate de tener un archivo .env con estas variables")
    exit(1)

# Las funciones de Google Sheets y cumpleaños ahora están en módulos separados

def send_birthday_email(nombre, email):
    """
    Envía un correo de cumpleaños usando la clase Gmail
    
    Args:
        nombre (str): Nombre de la persona
        email (str): Email del destinatario
        
    Returns:
        bool: True si se envió exitosamente, False en caso contrario
    """
    try:
        # Crear instancia de Gmail
        gmail = Gmail(GMAIL_USER, GMAIL_APP_PASSWORD)
        
        # Datos para el template
        data = {
            "nombre": nombre
        }
        
        # Enviar correo de cumpleaños
        logger.info(f"Enviando correo de cumpleaños a {email}")
        
        success = gmail.send_email(
            email=email,
            template="cumple",
            data=data
        )
        
        if success:
            logger.success(f"Correo de cumpleaños enviado exitosamente a {nombre}")
            return True
        else:
            logger.error(f"Error al enviar correo de cumpleaños a {nombre}")
            return False
            
    except Exception as e:
        logger.error(f"Error al enviar correo de cumpleaños: {e}")
        return False

# Las funciones de bitácora y display están ahora en el módulo de sheets

def main():
    """
    Función principal que ejecuta todo el proceso usando módulos modularizados
    """
    logger.info("Iniciando sistema de cumpleaños modularizado")
    logger.info("="*60)
    
    # Inicializar managers
    sheets_manager = GoogleSheetsManager()
    
    # Conectar con Google Sheets
    if not sheets_manager.connect():
        logger.error("No se pudo establecer conexión con Google Sheets")
        return
    
    # Leer datos principales
    df = sheets_manager.read_main_sheet()
    if df is None:
        logger.error("No se pudieron leer los datos")
        return
    
    # Mostrar información del DataFrame
    sheets_manager.display_dataframe_info(df, "DATOS PRINCIPALES")
    
    # Procesar cada persona
    #logger.info("PROCESANDO CUMPLEAÑOS CON MÓDULOS")
    logger.info("="*60)
    
    correos_enviados = 0
    personas_procesadas = 0
    
    for index, row in df.iterrows():
        nombre = row['nombre']
        fecha_nacimiento = row['fecha_nacimiento']
        correo = row['correo']
        
        logger.info(f"Procesando: {nombre}")
        logger.info(f"Fecha de nacimiento: {fecha_nacimiento}")
        logger.info(f"Correo: {correo}")
        
        # Obtener información completa del cumpleaños usando el módulo
        birthday_info = BirthdayCalculator.get_birthday_info(nombre, fecha_nacimiento)
        
        if 'error' not in birthday_info:
            logger.info(f"Días para cumpleaños: {birthday_info['dias_para_cumple']}")
            logger.info(f"Edad actual: {birthday_info['edad_actual']} años")
            logger.info(birthday_info['mensaje'])
            
            # Variable para tracking si se envió correo
            correo_enviado = False
            
            # Enviar correo si es cumpleaños
            if birthday_info['enviar_correo']:
                logger.info("Enviando correo de felicitación")
                correo_enviado = send_birthday_email(nombre, correo)
                if correo_enviado:
                    correos_enviados += 1
            
            # Escribir en bitácora usando el manager
            logger.info("Guardando en bitácora")
            success = sheets_manager.write_to_bitacora(
                nombre, 
                birthday_info['dias_para_cumple'], 
                correo_enviado
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
    logger.info(f"Correos enviados: {correos_enviados}")
    logger.info(f"Gmail configurado: {GMAIL_USER}")
    
    # Mostrar información del spreadsheet
    info = sheets_manager.get_spreadsheet_info()
    if 'error' not in info:
        logger.info(f"Hojas en el documento: {', '.join(info['worksheets'])}")
    
    logger.success("Proceso completado exitosamente")
    logger.info("Revisa la hoja 'bitacora' en tu Google Sheets para ver los resultados")
    if correos_enviados > 0:
        logger.info(f"Se enviaron {correos_enviados} correo(s) de cumpleaños automáticamente")

if __name__ == "__main__":
    main()

