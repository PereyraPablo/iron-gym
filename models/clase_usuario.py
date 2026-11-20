

# Importamos UserMixin para integrar nuestro modelo
# con el sistema de autenticación Flask-Login.
from flask_login import UserMixin


class Usuario(UserMixin):
    """
    Representa un usuario registrado en Iron Gym.

    Cada usuario tiene una cuenta de acceso y un rol
    que determina los permisos dentro del sistema.
    """

    def __init__(
        self,
        dni,
        nombre,
        apellido,
        telefono,
        email,
        password_hash,
        rol,
        activo=True
    ):
        # El DNI identifica de manera única al usuario.
        self.__dni = dni

        # Datos personales y de contacto.
        self.__nombre = nombre
        self.__apellido = apellido
        self.__telefono = telefono
        self.__email = email

        # Almacenamos el hash, nunca la contraseña original.
        self.__password_hash = password_hash

        # El rol determina el nivel de acceso del usuario.
        self.__rol = rol

        # Indica si la cuenta está habilitada.
        self.__activo = activo

    # Flask-Login utiliza este método para identificar
    # al usuario durante la sesión.
    def get_id(self):
        return self.__dni

    # -------------------------
    # PROPIEDADES
    # -------------------------

    @property
    def dni(self):
        return self.__dni

    @property
    def nombre(self):
        return self.__nombre

    @property
    def apellido(self):
        return self.__apellido

    @property
    def telefono(self):
        return self.__telefono

    @property
    def email(self):
        return self.__email

    @property
    def password_hash(self):
        return self.__password_hash

    @property
    def rol(self):
        return self.__rol

    @property
    def activo(self):
        return self.__activo
