

# Importamos el modelo y el repositorio de socios.
from models.clase_socio import Socio
from repositories.socio_repository import SocioRepository


class SocioService:
    """
    Servicio encargado de gestionar las reglas de negocio
    relacionadas con los socios del gimnasio.

    Recibe solicitudes del controlador, valida los datos
    y utiliza el repositorio para acceder a MySQL.
    """

    def __init__(self):
        # Creamos el repositorio que utilizará el servicio.
        self.__repositorio = SocioRepository()

    # --------------------------------------------------
    # CONSULTAS
    # --------------------------------------------------

    def obtener_por_dni(self, dni):
        """
        Busca un socio mediante su DNI.

        Retorna:
            El objeto Socio si existe.
            None si no se encuentra.
        """

        # Validamos que el DNI sea un texto de 8 dígitos.
        if (
            not isinstance(dni, str)
            or len(dni.strip()) != 8
            or not dni.strip().isdigit()
        ):
            raise ValueError("El DNI del socio no es válido.")

        # Buscamos al socio mediante su DNI.
        return self.__repositorio.obtener_por_dni(dni.strip())

    def listar_todos(self):
        """
        Obtiene todos los socios registrados.

        Esta operación será utilizada principalmente
        por el administrador.
        """

        return self.__repositorio.listar_todos()

    def listar_activos(self):
        """
        Obtiene únicamente los socios activos.

        Esta consulta permitirá trabajar con los socios
        que actualmente tienen su membresía activa.
        """

        return self.__repositorio.listar_activos()

    # --------------------------------------------------
    # VALIDACIONES DE NEGOCIO
    # --------------------------------------------------

    def _validar_socio(self, socio):
        """
        Comprueba que el objeto recibido sea un socio válido
        y que sus datos respeten las reglas de negocio.
        """

        # Verificamos que el objeto corresponda al modelo Socio.
        if not isinstance(socio, Socio):
            raise ValueError("Los datos recibidos no corresponden a un socio.")

        # Comprobamos que el DNI tenga el formato esperado.
        if (
            not isinstance(socio.dni, str)
            or len(socio.dni) != 8
            or not socio.dni.isdigit()
        ):
            raise ValueError("El DNI del socio no es válido.")

        # Comprobamos que la fecha de alta sea una fecha válida.
        from datetime import date

        if not isinstance(socio.fecha_alta, date):
            raise ValueError("La fecha de alta del socio no es válida.")

        # Comprobamos que el estado sea booleano.
        if not isinstance(socio.activo, bool):
            raise ValueError("El estado del socio no es válido.")

    # --------------------------------------------------
    # REGISTRO
    # --------------------------------------------------

    def registrar(self, socio):
        """
        Valida y registra un nuevo socio.

        Retorna:
            True si el registro se realizó correctamente.
        """

        # Validamos los datos del socio antes de continuar.
        self._validar_socio(socio)

        # Comprobamos si el DNI ya se encuentra registrado.
        existente = self.__repositorio.obtener_por_dni(socio.dni)

        if existente is not None:
            raise ValueError(
                "Ya existe un socio registrado con ese DNI."
            )

        # Si todas las validaciones pasan, registramos el socio.
        resultado = self.__repositorio.registrar(socio)

        if not resultado:
            raise RuntimeError("No se pudo registrar el socio.")

        return resultado
