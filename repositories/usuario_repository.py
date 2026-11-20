

# Importamos la función que centraliza la conexión con MySQL.
from connection import obtener_conexion

# Importamos el modelo Usuario.
from models.clase_usuario import Usuario


class UsuarioRepository:
    """
    Gestiona las consultas a la tabla usuarios.

    Esta clase se encarga exclusivamente del acceso
    a los datos, sin implementar reglas de negocio.
    """

    def obtener_por_email(self, email):
        """
        Busca un usuario mediante su correo electrónico.

        Retorna:
            Un objeto Usuario si existe.
            None si no existe o ocurre un error.
        """

        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()

            # Comprobamos que se haya establecido la conexión.
            if conexion is None:
                return None

            cursor = conexion.cursor(dictionary=True)

            consulta = """
                SELECT dni, nombre, apellido, telefono,
                       email, password_hash, rol, activo
                FROM usuarios
                WHERE email = %s
            """

            cursor.execute(consulta, (email,))

            resultado = cursor.fetchone()

            # Si no encontramos el correo, no existe el usuario.
            if resultado is None:
                return None

            # Convertimos el resultado de MySQL en un objeto Usuario.
            return Usuario(
                dni=resultado["dni"],
                nombre=resultado["nombre"],
                apellido=resultado["apellido"],
                telefono=resultado["telefono"],
                email=resultado["email"],
                password_hash=resultado["password_hash"],
                rol=resultado["rol"],
                activo=resultado["activo"]
            )

        except Exception as error:
            print(f"Error al buscar usuario por email: {error}")
            return None

        finally:
            # Liberamos los recursos utilizados.
            if cursor is not None:
                cursor.close()

            if conexion is not None and conexion.is_connected():
                conexion.close()

    def obtener_por_dni(self, dni):
        """
        Busca un usuario mediante su DNI.

        Este método será utilizado por Flask-Login
        para recuperar al usuario durante una sesión.
        """

        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()

            if conexion is None:
                return None

            cursor = conexion.cursor(dictionary=True)

            consulta = """
                SELECT dni, nombre, apellido, telefono,
                       email, password_hash, rol, activo
                FROM usuarios
                WHERE dni = %s
            """

            cursor.execute(consulta, (dni,))

            resultado = cursor.fetchone()

            if resultado is None:
                return None

            return Usuario(
                dni=resultado["dni"],
                nombre=resultado["nombre"],
                apellido=resultado["apellido"],
                telefono=resultado["telefono"],
                email=resultado["email"],
                password_hash=resultado["password_hash"],
                rol=resultado["rol"],
                activo=resultado["activo"]
            )

        except Exception as error:
            print(f"Error al buscar usuario por DNI: {error}")
            return None

        finally:
            if cursor is not None:
                cursor.close()

            if conexion is not None and conexion.is_connected():
                conexion.close()
