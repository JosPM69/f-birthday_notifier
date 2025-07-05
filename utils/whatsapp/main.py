import os
import logging
import requests
import re
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def extract_numeric_characters(text: str) -> str:
    """
    Extract only numeric characters from a string.
    
    Args:
        text (str): Input text that may contain non-numeric characters.
        
    Returns:
        str: String containing only numeric characters.
    """
    return re.sub(r'[^0-9]', '', text)

def load_template(purpose: str, data: dict, template_type: str = "whatsapp") -> str:
    """
    Load and format a message template.
    
    Args:
        purpose (str): Purpose of the message (e.g., 'cumple', 'bienvenida').
        data (dict): Data to substitute in the template.
        template_type (str): Type of template (default: 'whatsapp').
        
    Returns:
        str: Formatted message or None if template not found.
    """
    try:
        # Templates simples para WhatsApp
        templates = {
            "cumple": "¡Feliz cumpleaños {nombre}! 🎂🎉\n\nEsperamos que tengas un día maravilloso lleno de alegría y buenos momentos. Que todos tus deseos se cumplan en este nuevo año de vida.\n\n¡Que la pases súper! 🎈✨",
            "bienvenida": "¡Bienvenido {nombre}! 👋\n\nNos alegra tenerte con nosotros. Esperamos que disfrutes de todos nuestros servicios.\n\n¡Que tengas un excelente día! 😊",
            "confirmacion": "Hola {nombre}, 👋\n\nTu solicitud ha sido confirmada exitosamente. Te mantendremos informado sobre cualquier actualización.\n\n¡Gracias por confiar en nosotros! 🙏"
        }
        
        template = templates.get(purpose)
        if not template:
            logging.error(f"Template not found for purpose: {purpose}")
            return None
            
        # Formatear el template con los datos
        formatted_message = template.format(**data)
        return formatted_message
        
    except Exception as e:
        logging.error(f"Error loading template: {e}")
        return None

def send_whatsapp(to: str, data: dict, purpose: str = None) -> bool:
    """
    Sends a WhatsApp message using an API.

    Args:
        to (str): Recipient's phone number.
        data (dict): Data to include in the message template.
        purpose (str, optional): Purpose of the message (to load the appropriate template).

    Returns:
        bool: True if the message was successfully sent, False otherwise.
    """
    try:
        # Validar parámetros
        if not to or not isinstance(to, str):
            logging.error("Invalid phone number.")
            return False
        if not data or not isinstance(data, dict):
            logging.error("Invalid message data.")
            return False
            
        # Obtener variables de entorno
        whatsapp_url = os.getenv('WHATSAPP_URL')
        whatsapp_user = os.getenv('WHATSAPP_USER')
        whatsapp_pass = os.getenv('WHATSAPP_PASS')
        
        if not whatsapp_url or not whatsapp_user or not whatsapp_pass:
            logging.error("WhatsApp environment variables not configured.")
            logging.error("Please set WHATSAPP_URL, WHATSAPP_USER, and WHATSAPP_PASS in your .env file.")
            return False
        
        # Cargar template
        message = load_template(purpose, data, template_type="whatsapp")
        if not message:
            logging.error(f"Failed to load template for purpose: {purpose}")
            return False
            
        # Configurar URL y credenciales
        url = f"{whatsapp_url.rstrip('/')}/send/message"
        credentials = (whatsapp_user, whatsapp_pass)
        
        # Preparar payload
        payload = {
            "phone": f"{extract_numeric_characters(to)}@s.whatsapp.net",
            "message": message,
        }
        
        # Enviar mensaje
        logging.info(f"Sending WhatsApp message to {to}")
        response = requests.post(url, json=payload, auth=credentials, timeout=10)
        response.raise_for_status()
        
        response_data = response.json()
        if response_data.get("code") == "SUCCESS":
            logging.info(f"WhatsApp message sent successfully to {to}")
            return True
        else:
            logging.error(f"WhatsApp API error: {response_data}")
            return False
            
    except requests.Timeout:
        logging.error("The request to the WhatsApp API timed out.")
    except requests.ConnectionError:
        logging.error("Failed to connect to the WhatsApp API.")
    except requests.HTTPError as e:
        logging.error(f"HTTP error while sending WhatsApp message: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        logging.error(f"Unexpected error while sending WhatsApp message: {str(e)}")
    return False