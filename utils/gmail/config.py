import os
from typing import Optional
from utils.logger import logger

class GmailConfig:
    """Configuración para Gmail"""
    
    def __init__(self):
        # Cargar desde variables de entorno
        self.SENDER_EMAIL = os.getenv('GMAIL_SENDER_EMAIL', '')
        self.SENDER_PASSWORD = os.getenv('GMAIL_SENDER_PASSWORD', '')
        
        # Configuración SMTP
        self.SMTP_SERVER = "smtp.gmail.com"
        self.SMTP_PORT = 587
        
        # Validar configuración
        if not self.SENDER_EMAIL or not self.SENDER_PASSWORD:
            self._show_setup_instructions()
    
    def _show_setup_instructions(self):
        """Muestra instrucciones de configuración"""
        logger.warning("CONFIGURACIÓN REQUERIDA:")
        logger.warning("1. Configura las variables de entorno:")
        logger.warning("   - GMAIL_SENDER_EMAIL: tu_email@gmail.com")
        logger.warning("   - GMAIL_SENDER_PASSWORD: tu_contraseña_de_aplicacion")
        logger.warning("2. Para obtener una contraseña de aplicación:")
        logger.warning("   - Ve a tu cuenta de Google")
        logger.warning("   - Seguridad → Verificación en 2 pasos")
        logger.warning("   - Contraseñas de aplicaciones")
        logger.warning("   - Generar nueva contraseña")
        logger.warning("3. O configura manualmente:")
        logger.warning("   config = GmailConfig()")
        logger.warning("   config.SENDER_EMAIL = 'tu_email@gmail.com'")
        logger.warning("   config.SENDER_PASSWORD = 'tu_contraseña'")
    
    def is_configured(self) -> bool:
        """Verifica si la configuración está completa"""
        return bool(self.SENDER_EMAIL and self.SENDER_PASSWORD)
    
    def get_credentials(self) -> tuple:
        """Obtiene las credenciales configuradas"""
        if not self.is_configured():
            raise ValueError("Gmail no está configurado correctamente")
        return self.SENDER_EMAIL, self.SENDER_PASSWORD

# Configuración global
config = GmailConfig() 