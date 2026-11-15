
from datetime import date
from decimal import Decimal


class Maquina:
    """
    Representa una máquina de musculación del gimnasio.

    Esta clase contiene los atributos correspondientes
    a la tabla maquinas de nuestra base de datos.

    Utiliza encapsulamiento mediante propiedades
    para controlar el acceso y la modificación de sus datos.
    """

    # Estados permitidos para una máquina.
    ESTADOS_VALIDOS = ("ACTIVA", "INACTIVA", "REPARACION")

    def __init__(
        self,
        id_maquina=None,
        codigo=None,
        nombre=None,
        marca=None,
        modelo=None,
        descripcion=None,
        carga_minima=None,
        carga_maxima=None,
        imagen=None,
        estado="ACTIVA",
        fecha_alta=None
    ):
        # Utilizamos las propiedades para asignar los valores.
        self.id_maquina = id_maquina
        self.codigo = codigo
        self.nombre = nombre
        self.marca = marca
        self.modelo = modelo
        self.descripcion = descripcion
        self.carga_minima = carga_minima
        self.carga_maxima = carga_maxima
        self.imagen = imagen
        self.estado = estado
        self.fecha_alta = fecha_alta

    # --------------------------------------------------
    # IDENTIFICADOR
    # --------------------------------------------------

    @property
    def id_maquina(self):
        return self.__id_maquina

    @id_maquina.setter
    def id_maquina(self, valor):
        if valor is not None and (
            not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0
        ):
            raise ValueError("El identificador debe ser un entero positivo.")

        self.__id_maquina = valor

    # --------------------------------------------------
    # CÓDIGO
    # --------------------------------------------------

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El código de la máquina es obligatorio.")

        self.__codigo = valor.strip()

    # --------------------------------------------------
    # NOMBRE
    # --------------------------------------------------

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre de la máquina es obligatorio.")

        self.__nombre = valor.strip()

    # --------------------------------------------------
    # MARCA
    # --------------------------------------------------

    @property
    def marca(self):
        return self.__marca

    @marca.setter
    def marca(self, valor):
        if valor is not None and (
            not isinstance(valor, str) or not valor.strip()
        ):
            raise ValueError("La marca debe contener un texto válido.")

        self.__marca = valor.strip() if valor is not None else None

    # --------------------------------------------------
    # MODELO
    # --------------------------------------------------

    @property
    def modelo(self):
        return self.__modelo

    @modelo.setter
    def modelo(self, valor):
        if valor is not None and (
            not isinstance(valor, str) or not valor.strip()
        ):
            raise ValueError("El modelo debe contener un texto válido.")

        self.__modelo = valor.strip() if valor is not None else None

    # --------------------------------------------------
    # DESCRIPCIÓN
    # --------------------------------------------------

    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor):
        if valor is not None and not isinstance(valor, str):
            raise ValueError("La descripción debe ser un texto válido.")

        self.__descripcion = valor.strip() if valor is not None else None

    # --------------------------------------------------
    # CARGA MÍNIMA
    # --------------------------------------------------

    @property
    def carga_minima(self):
        return self.__carga_minima

    @carga_minima.setter
    def carga_minima(self, valor):
        if valor is not None:
            if isinstance(valor, bool):
                raise ValueError("La carga mínima debe ser numérica.")

            try:
                valor = Decimal(str(valor))
            except Exception:
                raise ValueError("La carga mínima debe ser numérica.")

            if not valor.is_finite() or valor < 0:
                raise ValueError("La carga mínima no puede ser negativa.")

        self.__carga_minima = valor

    # --------------------------------------------------
    # CARGA MÁXIMA
    # --------------------------------------------------

    @property
    def carga_maxima(self):
        return self.__carga_maxima

    @carga_maxima.setter
    def carga_maxima(self, valor):
        if valor is not None:
            if isinstance(valor, bool):
                raise ValueError("La carga máxima debe ser numérica.")

            try:
                valor = Decimal(str(valor))
            except Exception:
                raise ValueError("La carga máxima debe ser numérica.")

            if not valor.is_finite() or valor < 0:
                raise ValueError("La carga máxima no puede ser negativa.")

        self.__carga_maxima = valor

    # --------------------------------------------------
    # IMAGEN
    # --------------------------------------------------

    @property
    def imagen(self):
        return self.__imagen

    @imagen.setter
    def imagen(self, valor):
        if valor is not None and (
            not isinstance(valor, str) or not valor.strip()
        ):
            raise ValueError("La imagen debe contener una ruta válida.")

        self.__imagen = valor.strip() if valor is not None else None

    # --------------------------------------------------
    # ESTADO
    # --------------------------------------------------

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, valor):
        if valor not in self.ESTADOS_VALIDOS:
            raise ValueError(
                f"Estado inválido. Valores permitidos: {self.ESTADOS_VALIDOS}"
            )

        self.__estado = valor

    # --------------------------------------------------
    # FECHA DE ALTA
    # --------------------------------------------------

    @property
    def fecha_alta(self):
        return self.__fecha_alta

    @fecha_alta.setter
    def fecha_alta(self, valor):
        if valor is not None and not isinstance(valor, date):
            raise ValueError("La fecha de alta debe ser una fecha válida.")

        self.__fecha_alta = valor
