

import os

# Importamos load_dotenv para cargar las variables del archivo .env.
from dotenv import load_dotenv

# Cargamos las variables de entorno.
load_dotenv()


class Config:
    """
    Clase encargada de centralizar la configuración
    general de la aplicación Iron Gym.
    """

    # Clave secreta utilizada por Flask.
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Configuración de conexión con MySQL.
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_NAME = os.getenv("DB_NAME", "iron_gym")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")


'''
1. Carga las variables del .env.
2. Centraliza los datos de configuración.
3. Define la clase Config.

'''