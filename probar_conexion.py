
# Importamos nuestra función de conexión.
from connection import obtener_conexion

# Permite mostrar información detallada cuando ocurre un error.
import traceback


def probar_conexion():
    """
    Comprueba la conexión entre Python y MySQL
    y verifica que podamos consultar la base de datos.
    """

    conexion = None
    cursor = None

    try:
        # Intentamos establecer la conexión.
        conexion = obtener_conexion()

        if conexion is None:
            print("No se pudo establecer la conexión.")
            return

        print("¡Conexión con MySQL establecida correctamente!")

        # Creamos un cursor para ejecutar consultas SQL.
        cursor = conexion.cursor()

        # Consultamos qué base de datos está seleccionada.
        cursor.execute("SELECT DATABASE()")

        resultado = cursor.fetchone()

        print(f"Base de datos seleccionada: {resultado[0]}")

    except Exception:
        print("Se produjo un error durante la prueba:")
        traceback.print_exc()

    finally:
        # Cerramos el cursor si llegó a crearse.
        if cursor is not None:
            cursor.close()

        # Cerramos la conexión si llegó a establecerse.
        if conexion is not None and conexion.is_connected():
            conexion.close()
            print("Conexión cerrada correctamente.")


if __name__ == "__main__":
    probar_conexion()
