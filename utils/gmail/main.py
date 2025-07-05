import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, Optional
import os
from pathlib import Path
from utils.logger import logger

class Gmail:
    def __init__(self, sender_email: str, sender_password: str):
        """
        Inicializa la clase Gmail
        
        Args:
            sender_email: Email del remitente
            sender_password: Contraseña de aplicación o contraseña del email
        """
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = "smtp.gmail.com"
        self.port = 587
        
        # Diccionario de títulos por template
        self.template_titles = {
            "cumple": "🎉 ¡Feliz cumpleaños!"
        }
        
        # Directorio de templates
        self.templates_dir = Path(__file__).parent / "templates"
        self._create_templates_directory()
    
    def _create_templates_directory(self):
        """Crea el directorio de templates si no existe"""
        if not self.templates_dir.exists():
            self.templates_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_template_content(self, template_name: str) -> str:
        """
        Obtiene el contenido del template
        
        Args:
            template_name: Nombre del template
            
        Returns:
            Contenido del template HTML
        """
        template_path = self.templates_dir / f"{template_name}.html"
        
        if not template_path.exists():
            return self._get_default_template(template_name)
        
        with open(template_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    def _get_default_template(self, template_name: str) -> str:
        """
        Maneja cuando no se encuentra un template
        
        Args:
            template_name: Nombre del template
            
        Returns:
            Template HTML básico o lanza excepción
        """
        raise FileNotFoundError(f"Template '{template_name}' no encontrado en {self.templates_dir}")
    
    
    def _format_template(self, template_content: str, data: Dict) -> str:
        """
        Formatea el template con los datos proporcionados
        Convierte sintaxis {{variable}} a {variable} y luego formatea
        
        Args:
            template_content: Contenido HTML del template
            data: Diccionario con los datos para reemplazar
            
        Returns:
            Template formateado
        """
        try:
            # Convertir {{variable}} a {variable}
            import re
            # Reemplazar {{variable}} por {variable}
            template_content = re.sub(r'\{\{(\w+)\}\}', r'{\1}', template_content)
            
            return template_content.format(**data)
        except KeyError as e:
            logger.warning(f"Falta la variable {e} en los datos proporcionados")
            return template_content
    
    def send_email(self, email: str, template: str, data: Dict, 
                   custom_title: Optional[str] = None, 
                   attachments: Optional[list] = None) -> bool:
        """
        Envía un correo usando el template especificado
        
        Args:
            email: Email del destinatario
            template: Nombre del template a usar
            data: Diccionario con los datos para el template
            custom_title: Título personalizado (opcional)
            attachments: Lista de archivos adjuntos (opcional)
            
        Returns:
            True si el envío fue exitoso, False en caso contrario
        """
        try:
            # Crear mensaje
            message = MIMEMultipart("alternative")
            message["Subject"] = custom_title or self.template_titles.get(template, f"Mensaje - {template}")
            message["From"] = self.sender_email
            message["To"] = email
            
            # Obtener y formatear template
            template_content = self._get_template_content(template)
            html_content = self._format_template(template_content, data)
            
            # Crear parte HTML
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Agregar archivos adjuntos si existen
            if attachments:
                for file_path in attachments:
                    self._add_attachment(message, file_path)
            
            # Crear conexión SSL y enviar
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, email, message.as_string())
            
            logger.success(f"Correo enviado exitosamente a {email}")
            return True
            
        except FileNotFoundError as e:
            logger.error(f"Error: {str(e)}")
            logger.error(f"Crea el archivo de template: {self.templates_dir}/{template}.html")
            return False
        except Exception as e:
            logger.error(f"Error al enviar correo a {email}: {str(e)}")
            return False
    
    def _add_attachment(self, message: MIMEMultipart, file_path: str):
        """
        Agrega un archivo adjunto al mensaje
        
        Args:
            message: Mensaje MIME
            file_path: Ruta del archivo a adjuntar
        """
        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {os.path.basename(file_path)}'
            )
            message.attach(part)
            
        except Exception as e:
            logger.warning(f"No se pudo adjuntar el archivo {file_path}: {str(e)}")
    
    def add_template_title(self, template_name: str, title: str):
        """
        Agrega un nuevo título para un template
        
        Args:
            template_name: Nombre del template
            title: Título del correo
        """
        self.template_titles[template_name] = title
    
    def get_available_templates(self) -> Dict[str, str]:
        """
        Obtiene la lista de templates disponibles y sus títulos
        
        Returns:
            Diccionario con templates y títulos
        """
        return self.template_titles.copy()
    
    def create_template_file(self, template_name: str, html_content: str):
        """
        Crea un archivo de template HTML
        
        Args:
            template_name: Nombre del template
            html_content: Contenido HTML del template
        """
        template_path = self.templates_dir / f"{template_name}.html"
        
        with open(template_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
        
        logger.success(f"Template '{template_name}' creado en {template_path}")
