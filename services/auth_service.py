

# Importamos el repositorio encargado de consultar los usuarios.
from repositories.usuario_repository import UsuarioRepository

# Importamos las herramientas de Werkzeug para verificar contraseñas.
from werkzeug.security import check_password_hash


class AuthService:
    """
    Contiene las reglas de negocio relacionadas
    con la autenticación de los usuarios.
    """

    def __init__(self):
        # Creamos el repositorio que utilizaremos para buscar usuarios.
        self.__repositorio = UsuarioRepository()

    def autenticar(self, email, password):
        """
        Verifica las credenciales de acceso de un usuario.

        Retorna:
            Un objeto Usuario si las credenciales son correctas.
            None si los datos son incorrectos o la cuenta está inactiva.
        """

        # Validamos que se hayan ingresado ambos datos.
        if not email or not password:
            return None

        # Buscamos al usuario mediante su correo electrónico.
        usuario = self.__repositorio.obtener_por_email(email.strip())

        # Si el usuario no existe, no permitimos el acceso.
        if usuario is None:
            return None

        # Impedimos el acceso de cuentas desactivadas.
        if not usuario.activo:
            return None

        # Comparamos la contraseña ingresada con el hash almacenado.
        if not check_password_hash(usuario.password_hash, password):
            return None

        # Si todas las validaciones son correctas, devolvemos el usuario.
        return usuario

    def obtener_por_dni(self, dni):
        """
        Recupera un usuario mediante su DNI.

        Flask-Login utilizará este método para restaurar
        la sesión de un usuario autenticado.
        """

        # Buscamos al usuario en el repositorio.
        usuario = self.__repositorio.obtener_por_dni(dni)

        # No permitimos recuperar cuentas desactivadas.
        if usuario is None or not usuario.activo:
            return None

        return usuario
