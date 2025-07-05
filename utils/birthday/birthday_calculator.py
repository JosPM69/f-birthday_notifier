from datetime import datetime, date
from typing import Optional, Dict, Tuple
from utils.logger import logger

class BirthdayCalculator:
    """
    Clase para manejar cálculos relacionados con cumpleaños
    """
    
    @staticmethod
    def calculate_days_to_birthday(fecha_nacimiento: str) -> Optional[int]:
        """
        Calcula los días que faltan para el cumpleaños
        
        Args:
            fecha_nacimiento (str): Fecha en formato DD/MM/YYYY
            
        Returns:
            int: Días que faltan para el cumpleaños, None si hay error
        """
        try:
            # Convertir string a datetime
            birth_date = datetime.strptime(fecha_nacimiento, "%d/%m/%Y")
            
            # Obtener día y mes de nacimiento
            birth_day = birth_date.day
            birth_month = birth_date.month
            
            # Fecha actual
            today = date.today()
            
            # Cumpleaños de este año
            birthday_this_year = date(today.year, birth_month, birth_day)
            
            # Si ya pasó el cumpleaños este año, calcular para el próximo año
            if birthday_this_year < today:
                birthday_next_year = date(today.year + 1, birth_month, birth_day)
                days_to_birthday = (birthday_next_year - today).days
            else:
                days_to_birthday = (birthday_this_year - today).days
            
            return days_to_birthday
            
        except Exception as e:
            logger.error(f"Error al calcular días para cumpleaños: {e}")
            return None
    
    @staticmethod
    def get_birthday_message(nombre: str, dias_para_cumple: int) -> str:
        """
        Genera un mensaje personalizado según los días que faltan para el cumpleaños
        
        Args:
            nombre (str): Nombre de la persona
            dias_para_cumple (int): Días que faltan para el cumpleaños
            
        Returns:
            str: Mensaje personalizado
        """
        if dias_para_cumple == 0:
            return f"¡HOY ES EL CUMPLEAÑOS DE {nombre.upper()}!"
        elif dias_para_cumple == 1:
            return f"🎈 ¡Mañana es el cumpleaños de {nombre}!"
        elif dias_para_cumple <= 7:
            return f"🎁 El cumpleaños de {nombre} es muy pronto ({dias_para_cumple} días)"
        elif dias_para_cumple <= 30:
            return f"📅 El cumpleaños de {nombre} es este mes ({dias_para_cumple} días)"
        else:
            return f"⏰ Faltan {dias_para_cumple} días para el cumpleaños de {nombre}"
    
    @staticmethod
    def should_send_birthday_email(dias_para_cumple: int) -> bool:
        """
        Determina si se debe enviar correo de cumpleaños
        
        Args:
            dias_para_cumple (int): Días que faltan para el cumpleaños
            
        Returns:
            bool: True si se debe enviar correo, False en caso contrario
        """
        return dias_para_cumple == 0
    
    @staticmethod
    def get_age_from_birthdate(fecha_nacimiento: str) -> Optional[int]:
        """
        Calcula la edad actual de una persona
        
        Args:
            fecha_nacimiento (str): Fecha en formato DD/MM/YYYY
            
        Returns:
            int: Edad actual, None si hay error
        """
        try:
            birth_date = datetime.strptime(fecha_nacimiento, "%d/%m/%Y").date()
            today = date.today()
            
            age = today.year - birth_date.year
            
            # Ajustar si no ha llegado el cumpleaños este año
            if today < date(today.year, birth_date.month, birth_date.day):
                age -= 1
                
            return age
            
        except Exception as e:
            logger.error(f"Error al calcular edad: {e}")
            return None
    
    @staticmethod
    def get_birthday_info(nombre: str, fecha_nacimiento: str) -> Dict[str, any]:
        """
        Obtiene información completa sobre el cumpleaños de una persona
        
        Args:
            nombre (str): Nombre de la persona
            fecha_nacimiento (str): Fecha en formato DD/MM/YYYY
            
        Returns:
            Dict: Información completa del cumpleaños
        """
        dias_para_cumple = BirthdayCalculator.calculate_days_to_birthday(fecha_nacimiento)
        edad_actual = BirthdayCalculator.get_age_from_birthdate(fecha_nacimiento)
        
        if dias_para_cumple is None:
            return {
                "error": "No se pudo calcular información del cumpleaños",
                "nombre": nombre,
                "fecha_nacimiento": fecha_nacimiento
            }
        
        info = {
            "nombre": nombre,
            "fecha_nacimiento": fecha_nacimiento,
            "dias_para_cumple": dias_para_cumple,
            "edad_actual": edad_actual,
            "edad_siguiente": edad_actual + 1 if edad_actual else None,
            "es_cumpleanos_hoy": dias_para_cumple == 0,
            "enviar_correo": BirthdayCalculator.should_send_birthday_email(dias_para_cumple),
            "mensaje": BirthdayCalculator.get_birthday_message(nombre, dias_para_cumple)
        }
        
        return info
    
    @staticmethod
    def get_upcoming_birthdays(personas_data: list, days_ahead: int = 30) -> list:
        """
        Obtiene lista de cumpleaños próximos
        
        Args:
            personas_data (list): Lista de diccionarios con datos de personas
            days_ahead (int): Días hacia adelante a considerar
            
        Returns:
            list: Lista de personas con cumpleaños próximos
        """
        upcoming = []
        
        for persona in personas_data:
            nombre = persona.get('nombre', '')
            fecha_nacimiento = persona.get('fecha_nacimiento', '')
            
            dias_para_cumple = BirthdayCalculator.calculate_days_to_birthday(fecha_nacimiento)
            
            if dias_para_cumple is not None and dias_para_cumple <= days_ahead:
                info = BirthdayCalculator.get_birthday_info(nombre, fecha_nacimiento)
                upcoming.append(info)
        
        # Ordenar por días restantes
        upcoming.sort(key=lambda x: x['dias_para_cumple'])
        
        return upcoming 