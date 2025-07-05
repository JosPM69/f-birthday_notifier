#!/usr/bin/env python3
"""
Sistema de gestión de cumpleaños y mensajes automáticos
Punto de entrada principal del proyecto
"""

import argparse
import sys
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Agregar el directorio raíz al path para importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.logger import logger

def validate_email_config():
    """
    Valida que las variables de entorno necesarias para el proceso de email estén configuradas
    """
    gmail_user = os.getenv('GMAIL_USER')
    gmail_app_password = os.getenv('GMAIL_APP_PASSWORD')
    
    if not gmail_user or not gmail_app_password:
        logger.error("Variables de entorno GMAIL_USER y GMAIL_APP_PASSWORD no están configuradas")
        logger.error("Asegúrate de tener un archivo .env con estas variables")
        return False
    
    logger.info(f"Configuración de Gmail validada: {gmail_user}")
    return True

def validate_whatsapp_config():
    """
    Valida que las variables de entorno necesarias para el proceso de WhatsApp estén configuradas
    """
    whatsapp_url = os.getenv('WHATSAPP_URL')
    whatsapp_user = os.getenv('WHATSAPP_USER')
    whatsapp_pass = os.getenv('WHATSAPP_PASS')
    
    if not whatsapp_url or not whatsapp_user or not whatsapp_pass:
        logger.error("Variables de entorno WHATSAPP_URL, WHATSAPP_USER y WHATSAPP_PASS no están configuradas")
        logger.error("Asegúrate de tener un archivo .env con estas variables")
        return False
    
    logger.info(f"Configuración de WhatsApp validada: {whatsapp_user}")
    return True

def main():
    """
    Función principal que maneja los argumentos de línea de comandos
    y ejecuta el proceso correspondiente
    """
    parser = argparse.ArgumentParser(
        description="Sistema de gestión de cumpleaños y mensajes automáticos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py --process send_email     # Ejecutar proceso de envío de emails
  python main.py --process send_whatsapp  # Ejecutar proceso de envío de WhatsApp
  python main.py -p send_email            # Forma abreviada
        """
    )
    
    parser.add_argument(
        '--process', '-p',
        type=str,
        required=True,
        choices=['send_email', 'send_whatsapp'],
        help='Proceso a ejecutar: send_email o send_whatsapp'
    )
    
    args = parser.parse_args()
    
    logger.info("="*60)
    logger.info("SISTEMA DE GESTIÓN DE CUMPLEAÑOS Y MENSAJES")
    logger.info("="*60)
    
    try:
        if args.process == 'send_email':
            logger.info("Ejecutando proceso: Envío de emails de cumpleaños")
            logger.info("-"*40)
            
            # Validar configuración de email
            if not validate_email_config():
                sys.exit(1)
            
            # Importar y ejecutar el proceso de envío de emails
            from processes.send_email import main as send_email_main
            send_email_main()
            
        elif args.process == 'send_whatsapp':
            logger.info("Ejecutando proceso: Envío de mensajes de WhatsApp")
            logger.info("-"*40)
            
            # Validar configuración de WhatsApp
            if not validate_whatsapp_config():
                sys.exit(1)
            
            # Importar y ejecutar el proceso de envío de WhatsApp
            from processes.send_whatsapp import main as send_whatsapp_main
            send_whatsapp_main()
            
        else:
            logger.error(f"Proceso '{args.process}' no reconocido")
            sys.exit(1)
            
    except ImportError as e:
        logger.error(f"Error al importar el proceso '{args.process}': {e}")
        logger.error("Asegúrate de que el archivo del proceso existe y es accesible")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error inesperado durante la ejecución: {e}")
        sys.exit(1)
    
    logger.info("="*60)
    logger.success("Proceso completado")

if __name__ == "__main__":
    main()
