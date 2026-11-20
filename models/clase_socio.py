

from datetime import date


class Socio:
    """
    Representa a un socio del gimnasio.

    Esta clase contiene los atributos correspondientes
    a la tabla socios de nuestra base de datos.

    Los datos personales y de acceso se encuentran
    en la clase Usuario y no se repiten aquí.

    Utiliza encapsulamiento mediante propiedades
    para controlar el acceso y la modificación de sus datos.
    """

    def __init__(
        self,
        dni=None,
        fecha_alta=None,
        activo=True
    ):
        # Utilizamos las propiedades para asignar los valores.
        self.dni = dni
        self.fecha_alta = fecha_alta
        self.activo = activo

    # --------------------------------------------------
    # DNI
    # --------------------------------------------------

    @property
    def dni(self):
        return self.__dni

    @dni.setter
    def dni(self, valor):
        # El DNI debe ser un texto de exactamente 8 dígitos.
        # Lo almacenamos como texto para conservar posibles ceros iniciales.
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El DNI del socio es obligatorio.")

        valor = valor.strip()

        if len(valor) != 8 or not valor.isdigit():
            raise ValueError("El DNI debe contener exactamente 8 dígitos.")

        self.__dni = valor

    # --------------------------------------------------
    # FECHA DE ALTA
    # --------------------------------------------------

    @property
    def fecha_alta(self):
        return self.__fecha_alta

    @fecha_alta.setter
    def fecha_alta(self, valor):
        # La fecha de alta es obligatoria en la base de datos.
        if not isinstance(valor, date):
            raise ValueError("La fecha de alta debe ser una fecha válida.")

        self.__fecha_alta = valor

    # --------------------------------------------------
    # ESTADO
    # --------------------------------------------------

    @property
    def activo(self):
        return self.__activo

    @activo.setter
    def activo(self, valor):
        # Comprobamos que el estado sea un booleano real.
        # Excluimos otros valores como 0, 1 o None.
        if not isinstance(valor, bool):
            raise ValueError("El estado del socio debe ser True o False.")

        self.__activo = valor
