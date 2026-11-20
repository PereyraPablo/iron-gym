

# Importamos el conector de MySQL para manejar sus excepciones.
import mysql.connector

# Importamos la función encargada de establecer la conexión.
from connection import obtener_conexion

# Importamos el modelo que representa a un socio.
from models.clase_socio import Socio


class SocioRepository:
    """
    Repositorio encargado de realizar las operaciones
    de acceso a datos correspondientes a la tabla socios.

    Se comunica directamente con MySQL y utiliza
    la clase Socio para representar los registros.
    """

    def _crear_socio(self, registro):
        """
        Convierte un registro de MySQL en un objeto Socio.
    
        MySQL Connector puede devolver los valores BOOLEAN
        como enteros (0 o 1). Los convertimos a booleanos
        reales antes de construir el objeto.
        """
    
        registro["activo"] = bool(registro["activo"])
        return Socio(**registro) 


    def obtener_por_dni(self, dni):
        """
        Busca un socio mediante su DNI.

        Parámetros:
            dni: DNI del socio que se desea buscar.

        Retorna:
            Un objeto Socio si existe.
            None si no se encuentra u ocurre un error.
        """

        conexion = None
        cursor = None

        try:
            # Solicitamos una conexión con la base de datos.
            conexion = obtener_conexion()

            # Comprobamos que la conexión se haya establecido.
            if conexion is None:
                return None

            # Creamos un cursor que devuelve los resultados como diccionarios.
            cursor = conexion.cursor(dictionary=True)

            # Consultamos el socio mediante su DNI.
            consulta = """
                SELECT *
                FROM socios
                WHERE dni = %s
            """

            cursor.execute(consulta, (dni,))

            # Recuperamos el registro encontrado.
            registro = cursor.fetchone()

            # Si existe, convertimos el registro en un objeto Socio.
            if registro is not None:
                return self._crear_socio(registro)

            return None

        except mysql.connector.Error as error:
            print(f"Error al buscar el socio: {error}")
            return None

        finally:
            # Liberamos los recursos utilizados.
            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()


    def listar_todos(self):
        """
        Obtiene todos los socios registrados.

        Retorna:
            Una lista de objetos Socio.
            Una lista vacía si no hay resultados o ocurre un error.
        """

        conexion = None
        cursor = None
        socios = []

        try:
            # Solicitamos una conexión con la base de datos.
            conexion = obtener_conexion()

            if conexion is None:
                return socios

            # Creamos un cursor que devuelve los resultados como diccionarios.
            cursor = conexion.cursor(dictionary=True)

            # Consultamos todos los socios.
            consulta = """
                SELECT *
                FROM socios
                ORDER BY fecha_alta DESC
            """

            cursor.execute(consulta)

            # Recuperamos todos los registros encontrados.
            resultados = cursor.fetchall()

            # Convertimos cada registro en un objeto Socio.
            for registro in resultados:
                socio = self._crear_socio(registro)
                socios.append(socio)

            return socios

        except mysql.connector.Error as error:
            print(f"Error al listar los socios: {error}")
            return []

        finally:
            # Liberamos los recursos utilizados.
            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()


    def listar_activos(self):
        """
        Obtiene únicamente los socios activos.

        Retorna:
            Una lista de objetos Socio activos.
            Una lista vacía si no hay resultados o ocurre un error.
        """

        conexion = None
        cursor = None
        socios = []

        try:
            # Solicitamos una conexión con la base de datos.
            conexion = obtener_conexion()

            if conexion is None:
                return socios

            cursor = conexion.cursor(dictionary=True)

            # Filtramos los socios cuyo estado sea activo.
            consulta = """
                SELECT *
                FROM socios
                WHERE activo = TRUE
                ORDER BY fecha_alta DESC
            """

            cursor.execute(consulta)

            # Recuperamos los registros encontrados.
            resultados = cursor.fetchall()

            # Convertimos cada registro en un objeto Socio.
            for registro in resultados:
                socio = self._crear_socio(registro)
                socios.append(socio)

            return socios

        except mysql.connector.Error as error:
            print(f"Error al listar los socios activos: {error}")
            return []

        finally:
            # Liberamos los recursos utilizados.
            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()


    def registrar(self, socio):
        """
        Registra un nuevo socio en la base de datos.

        Parámetros:
            socio: objeto de la clase Socio.

        Retorna:
            True si el registro se realizó correctamente.
            False si ocurrió un error.
        """

        conexion = None
        cursor = None

        try:
            # Solicitamos una conexión con la base de datos.
            conexion = obtener_conexion()

            if conexion is None:
                return False

            cursor = conexion.cursor()

            # Insertamos únicamente los datos correspondientes a socios.
            consulta = """
                INSERT INTO socios (
                    dni,
                    fecha_alta,
                    activo
                )
                VALUES (%s, %s, %s)
            """

            valores = (
                socio.dni,
                socio.fecha_alta,
                socio.activo
            )

            cursor.execute(consulta, valores)

            # Confirmamos el registro en la base de datos.
            conexion.commit()

            return True

        except mysql.connector.Error as error:
            print(f"Error al registrar el socio: {error}")

            # Deshacemos la operación si ocurrió algún error.
            if conexion is not None:
                conexion.rollback()

            return False

        finally:
            # Liberamos los recursos utilizados.
            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()


             
