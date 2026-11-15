

import mysql.connector

# Importamos la configuración centralizada.
from config import Config


def obtener_conexion():
    """
    Establece una conexión con la base de datos Iron Gym.

    Retorna:
        Una conexión activa con MySQL.
    """

    try:
        conexion = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,

            # Utilizamos Python puro para evitar el componente C
            # y obtener errores de conexión más descriptivos.
            use_pure=True
        )

        return conexion

    except mysql.connector.Error as error:
        print(f"Error al conectar con MySQL: {error}")

        return None


'''
1. Importa la configuración.
2. Establece la conexión.
3. Devuelve la conexión a quien la solicita.



El funcionamiento sería el siguiente:

        .env
 (Almacena las variables)
          ⬇️
        config.py
 (Lee y centraliza la configuración)
          ⬇️
      connection.py
 (Utiliza la configuración y conecta con MySQL)
          ⬇️
    Base de datos iron_gy
   (Conexión establecida)

'''