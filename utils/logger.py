import logging
import os
from datetime import datetime
from pathlib import Path

class Logger:
    """
    Clase para manejar logging centralizado en el proyecto
    """
    
    def __init__(self, name: str = "envio_mensaje", level: str = "INFO"):
        """
        Inicializa el logger
        
        Args:
            name (str): Nombre del logger
            level (str): Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # Evitar duplicar handlers
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """Configura los handlers para el logger"""
        # Crear directorio de logs si no existe
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Handler para archivo
        log_file = log_dir / f"envio_mensaje_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formato
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str):
        """Log de información"""
        self.logger.info(message)
    
    def debug(self, message: str):
        """Log de debug"""
        self.logger.debug(message)
    
    def warning(self, message: str):
        """Log de advertencia"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log de error"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log crítico"""
        self.logger.critical(message)
    
    def success(self, message: str):
        """Log de éxito (usando INFO)"""
        self.logger.info(f"SUCCESS: {message}")
    
    def failure(self, message: str):
        """Log de fallo (usando ERROR)"""
        self.logger.error(f"FAILURE: {message}")

# Instancia global del logger
logger = Logger() 