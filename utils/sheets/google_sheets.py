import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import datetime
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar logger
from utils.logger import logger

class GoogleSheetsManager:
    """
    Clase para manejar todas las operaciones con Google Sheets
    """
    
    def __init__(self, service_account_file: Optional[str] = None, spreadsheet_id: Optional[str] = None):
        """
        Inicializa el manager de Google Sheets
        
        Args:
            service_account_file (str): Ruta al archivo de credenciales de la cuenta de servicio
            spreadsheet_id (str): ID del Google Sheets
        """
        # Obtener configuraciones desde variables de entorno o parámetros
        self.service_account_file = service_account_file or os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE', 'cuenta_servicio.json')
        self.spreadsheet_id = spreadsheet_id or os.getenv('GOOGLE_SHEETS_ID')
        
        # Validar que el spreadsheet_id esté configurado
        if not self.spreadsheet_id:
            raise ValueError("GOOGLE_SHEETS_ID no está configurado en las variables de entorno")
        
        self.gc = None
        
        # Scopes necesarios para Google Sheets
        self.scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
    
    def connect(self) -> bool:
        """
        Establece conexión con Google Sheets usando cuenta de servicio
        
        Returns:
            bool: True si la conexión fue exitosa, False en caso contrario
        """
        try:
            # Cargar credenciales desde archivo JSON
            credentials = Credentials.from_service_account_file(
                self.service_account_file,
                scopes=self.scope
            )
            
            # Crear cliente de gspread
            self.gc = gspread.authorize(credentials)
            
            logger.success("Conexión exitosa con Google Sheets")
            return True
            
        except FileNotFoundError:
            logger.error(f"No se encontró el archivo '{self.service_account_file}'")
            logger.error("Asegúrate de que esté en la raíz del proyecto")
            return False
        except Exception as e:
            logger.error(f"Error al conectar con Google Sheets: {str(e)}")
            return False
    
    def read_main_sheet(self) -> Optional[pd.DataFrame]:
        """
        Lee los datos de la hoja principal del Google Sheets
        
        Returns:
            pd.DataFrame: DataFrame con los datos o None si hay error
        """
        if not self.gc:
            logger.error("No hay conexión establecida. Llama a connect() primero.")
            return None
        
        try:
            # Abrir el spreadsheet
            logger.info(f"Abriendo Google Sheets: {self.spreadsheet_id}")
            spreadsheet = self.gc.open_by_key(self.spreadsheet_id)
            
            # Obtener la primera hoja (worksheet)
            worksheet = spreadsheet.sheet1
            logger.info(f"Hoja seleccionada: {worksheet.title}")
            
            # Obtener todos los datos
            logger.info("Obteniendo datos")
            data = worksheet.get_all_records()
            
            # Convertir a DataFrame
            df = pd.DataFrame(data)
            
            logger.success("Datos obtenidos exitosamente")
            logger.info(f"Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
            
            return df
            
        except Exception as e:
            logger.error(f"Error al leer los datos: {str(e)}")
            return None
    
    def ensure_bitacora_sheet(self) -> Optional[gspread.Worksheet]:
        """
        Asegura que existe la hoja "bitacora" y la retorna
        
        Returns:
            gspread.Worksheet: La hoja de bitácora o None si hay error
        """
        if not self.gc:
            logger.error("No hay conexión establecida.")
            return None
        
        try:
            # Abrir el spreadsheet
            spreadsheet = self.gc.open_by_key(self.spreadsheet_id)
            
            # Intentar obtener la hoja "bitacora"
            try:
                bitacora_sheet = spreadsheet.worksheet("bitacora")
                logger.success("Hoja 'bitacora' encontrada")
                return bitacora_sheet
            except gspread.WorksheetNotFound:
                # Crear la hoja si no existe
                bitacora_sheet = spreadsheet.add_worksheet(title="bitacora", rows="100", cols="20")
                logger.success("Hoja 'bitacora' creada")
                
                # Agregar headers
                headers = [['fecha', 'nombre', 'dias_para_cumple', 'correo_enviado']]
                bitacora_sheet.update('A1:D1', headers)
                logger.success("Headers agregados a la hoja 'bitacora'")
                
                return bitacora_sheet
                
        except Exception as e:
            logger.error(f"Error al manejar hoja bitacora: {e}")
            return None
    
    def write_to_bitacora(self, nombre: str, dias_para_cumple: int, correo_enviado: bool = False) -> bool:
        """
        Escribe un registro en la hoja "bitacora"
        
        Args:
            nombre (str): Nombre de la persona
            dias_para_cumple (int): Días que faltan para el cumpleaños
            correo_enviado (bool): Si se envió correo de cumpleaños
            
        Returns:
            bool: True si se escribió exitosamente, False en caso contrario
        """
        try:
            # Obtener la hoja de bitácora
            bitacora_sheet = self.ensure_bitacora_sheet()
            if not bitacora_sheet:
                return False
            
            # Obtener la fecha actual en formato YYYYMMDD
            fecha_actual = datetime.now().strftime("%Y%m%d")
            
            # Preparar datos a insertar
            nueva_fila = [fecha_actual, nombre, dias_para_cumple, "SI" if correo_enviado else "NO"]
            
            # Agregar nueva fila
            bitacora_sheet.append_row(nueva_fila)
            
            logger.success("Datos guardados en bitacora")
            logger.info(f"Fecha: {fecha_actual}")
            logger.info(f"Nombre: {nombre}")
            logger.info(f"Días para cumpleaños: {dias_para_cumple}")
            logger.info(f"Correo enviado: {'SI' if correo_enviado else 'NO'}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error al escribir en bitacora: {e}")
            return False
    
    def get_bitacora_data(self) -> Optional[pd.DataFrame]:
        """
        Lee los datos de la hoja "bitacora"
        
        Returns:
            pd.DataFrame: DataFrame con los datos de bitácora o None si hay error
        """
        try:
            bitacora_sheet = self.ensure_bitacora_sheet()
            if not bitacora_sheet:
                return None
            
            # Obtener todos los datos
            data = bitacora_sheet.get_all_records()
            
            # Convertir a DataFrame
            df = pd.DataFrame(data)
            
            logger.success(f"Datos de bitácora obtenidos: {df.shape[0]} registros")
            return df
            
        except Exception as e:
            logger.error(f"Error al leer bitácora: {e}")
            return None
    
    def get_spreadsheet_info(self) -> Dict[str, Any]:
        """
        Obtiene información del spreadsheet
        
        Returns:
            Dict: Información del spreadsheet
        """
        if not self.gc:
            return {"error": "No hay conexión establecida"}
        
        try:
            spreadsheet = self.gc.open_by_key(self.spreadsheet_id)
            
            info = {
                "title": spreadsheet.title,
                "id": spreadsheet.id,
                "url": spreadsheet.url,
                "worksheets": [ws.title for ws in spreadsheet.worksheets()],
                "worksheet_count": len(spreadsheet.worksheets())
            }
            
            return info
            
        except Exception as e:
            return {"error": str(e)}
    
    def display_dataframe_info(self, df: pd.DataFrame, title: str = "DATAFRAME") -> None:
        """
        Muestra información detallada de un DataFrame
        
        Args:
            df (pd.DataFrame): DataFrame a mostrar
            title (str): Título para la visualización
        """
        if df is None:
            logger.error("No hay datos para mostrar")
            return
        
        logger.info("="*60)
        logger.info(f"INFORMACIÓN DEL {title}")
        logger.info("="*60)
        
        # Información básica
        logger.info(f"Número de filas: {df.shape[0]}")
        logger.info(f"Número de columnas: {df.shape[1]}")
        logger.info(f"Columnas: {list(df.columns)}")
        
        # Mostrar DataFrame completo
        #logger.info("Datos completos:")
        #logger.info(str(df)) 