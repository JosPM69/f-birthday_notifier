import os
import psycopg2
import psycopg2.extras
import logging
from dotenv import load_dotenv
from typing import Optional, List, Dict, Any, Union
from contextlib import contextmanager

# Cargar variables de entorno
load_dotenv()

class PostgreSQLManager:
    """
    Clase para manejar conexiones y operaciones con PostgreSQL
    """
    
    def __init__(self):
        """
        Inicializa el manager de PostgreSQL con las variables de entorno
        """
        self.host = os.getenv('POSTGRESQL_HOST', 'localhost')
        self.database = os.getenv('POSTGRESQL_BBDD')
        self.user = os.getenv('POSTGRESQL_USER')
        self.password = os.getenv('POSTGRESQL_PASS')
        self.port = os.getenv('POSTGRESQL_PORT', '5432')
        self.connection = None
        
        # Validar variables requeridas
        if not all([self.database, self.user, self.password]):
            raise ValueError(
                "Variables de entorno PostgreSQL requeridas: "
                "POSTGRESQL_BBDD, POSTGRESQL_USER, POSTGRESQL_PASS"
            )
    
    def get_connection_string(self) -> str:
        """
        Genera la cadena de conexión para PostgreSQL
        
        Returns:
            str: Cadena de conexión formateada
        """
        return f"host={self.host} port={self.port} dbname={self.database} user={self.user} password={self.password}"
    
    def connect(self) -> bool:
        """
        Establece conexión con la base de datos PostgreSQL
        
        Returns:
            bool: True si la conexión fue exitosa, False en caso contrario
        """
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            logging.info(f"Conexión exitosa a PostgreSQL: {self.database} en {self.host}:{self.port}")
            return True
            
        except psycopg2.Error as e:
            logging.error(f"Error al conectar a PostgreSQL: {e}")
            return False
    
    def disconnect(self):
        """
        Cierra la conexión con la base de datos
        """
        if self.connection:
            self.connection.close()
            self.connection = None
            logging.info("Conexión a PostgreSQL cerrada")
    
    def is_connected(self) -> bool:
        """
        Verifica si hay una conexión activa
        
        Returns:
            bool: True si está conectado, False en caso contrario
        """
        return self.connection is not None and not self.connection.closed
    
    @contextmanager
    def get_cursor(self, commit: bool = True):
        """
        Context manager para obtener un cursor de la base de datos
        
        Args:
            commit (bool): Si se debe hacer commit automático al finalizar
            
        Yields:
            psycopg2.extras.RealDictCursor: Cursor para ejecutar consultas
        """
        if not self.is_connected():
            if not self.connect():
                raise Exception("No se pudo establecer conexión con PostgreSQL")
        
        cursor = None
        try:
            cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            yield cursor
            if commit:
                self.connection.commit()
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            logging.error(f"Error en operación de base de datos: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Ejecuta una consulta SELECT y retorna los resultados
        
        Args:
            query (str): Consulta SQL a ejecutar
            params (tuple, optional): Parámetros para la consulta
            
        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con los resultados
        """
        try:
            with self.get_cursor(commit=False) as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()
                return [dict(row) for row in results]
                
        except Exception as e:
            logging.error(f"Error ejecutando consulta: {e}")
            logging.error(f"Query: {query}")
            if params:
                logging.error(f"Parámetros: {params}")
            return None
    
    def execute_command(self, command: str, params: Optional[tuple] = None) -> bool:
        """
        Ejecuta un comando INSERT, UPDATE, DELETE
        
        Args:
            command (str): Comando SQL a ejecutar
            params (tuple, optional): Parámetros para el comando
            
        Returns:
            bool: True si se ejecutó exitosamente, False en caso contrario
        """
        try:
            with self.get_cursor(commit=True) as cursor:
                cursor.execute(command, params)
                logging.info(f"Comando ejecutado exitosamente: {command}")
                return True
                
        except Exception as e:
            logging.error(f"Error ejecutando comando: {e}")
            logging.error(f"Comando: {command}")
            if params:
                logging.error(f"Parámetros: {params}")
            return False
    
    def execute_many(self, command: str, params_list: List[tuple]) -> bool:
        """
        Ejecuta múltiples comandos con diferentes parámetros
        
        Args:
            command (str): Comando SQL a ejecutar
            params_list (List[tuple]): Lista de parámetros para cada ejecución
            
        Returns:
            bool: True si se ejecutaron exitosamente, False en caso contrario
        """
        try:
            with self.get_cursor(commit=True) as cursor:
                cursor.executemany(command, params_list)
                logging.info(f"Ejecutados {len(params_list)} comandos exitosamente")
                return True
                
        except Exception as e:
            logging.error(f"Error ejecutando múltiples comandos: {e}")
            logging.error(f"Comando: {command}")
            return False
    
    def table_exists(self, table_name: str) -> bool:
        """
        Verifica si una tabla existe en la base de datos
        
        Args:
            table_name (str): Nombre de la tabla a verificar
            
        Returns:
            bool: True si la tabla existe, False en caso contrario
        """
        query = """
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = %s
            );
        """
        result = self.execute_query(query, (table_name,))
        return result[0]['exists'] if result else False
    
    def get_table_info(self, table_name: str) -> Optional[List[Dict[str, Any]]]:
        """
        Obtiene información sobre las columnas de una tabla
        
        Args:
            table_name (str): Nombre de la tabla
            
        Returns:
            List[Dict[str, Any]]: Información de las columnas
        """
        query = """
            SELECT 
                column_name,
                data_type,
                is_nullable,
                column_default
            FROM information_schema.columns 
            WHERE table_schema = 'public' 
            AND table_name = %s
            ORDER BY ordinal_position;
        """
        return self.execute_query(query, (table_name,))
    
    def get_database_info(self) -> Dict[str, Any]:
        """
        Obtiene información general de la base de datos
        
        Returns:
            Dict[str, Any]: Información de la base de datos
        """
        return {
            'host': self.host,
            'port': self.port,
            'database': self.database,
            'user': self.user,
            'connected': self.is_connected()
        }
    
    def __enter__(self):
        """
        Context manager entry
        """
        if not self.connect():
            raise Exception("No se pudo conectar a PostgreSQL")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit
        """
        self.disconnect() 