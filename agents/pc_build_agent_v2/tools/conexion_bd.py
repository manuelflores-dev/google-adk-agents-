"""
Herramienta de Conexión a Base de Datos
Maneja la conexión a MariaDB
"""

import os
import mysql.connector
from dotenv import load_dotenv

# Cargar variables de entorno
# Cargar variables de entorno
# Construir ruta absoluta al archivo .env (un nivel arriba de tools)
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)


def conectar_bd():
    """
    Establece conexión con la base de datos MariaDB de Zegucom
    
    Returns:
        connection: Objeto de conexión a MariaDB
        
    Raises:
        mysql.connector.Error: Si hay error en la conexión
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error conectando a la base de datos: {err}")
        raise


if __name__ == "__main__":
    # Test de conexión
    print("Probando conexión a MariaDB...")
    try:
        conn = conectar_bd()
        if conn.is_connected():
            print("Conexión exitosa!")
            conn.close()
    except Exception as e:
        print(f"Error: {e}")
