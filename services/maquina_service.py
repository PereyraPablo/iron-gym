

from datetime import date
from decimal import Decimal

# Importamos el modelo y el repositorio de máquinas.
from models.clase_maquina import Maquina
from repositories.maquina_repository import MaquinaRepository


class MaquinaService:
    """
    Servicio encargado de gestionar las reglas de negocio
    relacionadas con las máquinas de musculación.

    Recibe solicitudes del controlador, valida los datos
    y utiliza el repositorio para acceder a MySQL.
    """

    def __init__(self):
        # Creamos el repositorio que utilizará el servicio.
        self.__repositorio = MaquinaRepository()

    # --------------------------------------------------
    # CONSULTAS
    # --------------------------------------------------

    def listar_todas(self):
        """
        Obtiene todas las máquinas registradas.

        Esta operación será utilizada principalmente
        por el administrador.
        """

        return self.__repositorio.listar_todas()

    def listar_activas(self):
        """
        Obtiene únicamente las máquinas activas.

        Esta operación será utilizada para el catálogo público.
        """

        return self.__repositorio.listar_activas()

    def listar_grupos_activos(self):
        """
        Obtiene los grupos musculares que se encuentran activos.

        Esta consulta permitirá mostrar los grupos disponibles
        para que el usuario pueda filtrar el catálogo de máquinas.
        """

        return self.__repositorio.listar_grupos_activos()

    def listar_activas_por_grupo(self, id_grupo):
        """
        Obtiene las máquinas activas asociadas a un grupo muscular.

        Recibe:
            id_grupo: identificador del grupo muscular.

        Retorna:
            Una lista de diccionarios con los datos de las máquinas
            y el tipo de trabajo muscular correspondiente.

        Si el grupo no existe, está inactivo o no tiene máquinas
        asociadas, el repositorio devolverá una lista vacía.
        """

        # Validamos que el identificador sea un entero positivo.
        # También rechazamos bool, aunque en Python sea un subtipo de int.
        if (
            not isinstance(id_grupo, int)
            or isinstance(id_grupo, bool)
            or id_grupo <= 0
        ):
            raise ValueError("El identificador del grupo muscular no es válido.")

        # Solicitamos al repositorio las máquinas activas del grupo.
        return self.__repositorio.listar_activas_por_grupo(id_grupo)

    def obtener_por_id(self, id_maquina):
        """
        Busca una máquina mediante su identificador.
        """

        if not isinstance(id_maquina, int) or isinstance(id_maquina, bool) or id_maquina <= 0:
            raise ValueError("El identificador de la máquina no es válido.")

        maquina = self.__repositorio.obtener_por_id(id_maquina)

        if maquina is None:
            raise ValueError("No se encontró la máquina solicitada.")

        return maquina

    # --------------------------------------------------
    # VALIDACIONES DE NEGOCIO
    # --------------------------------------------------

    def _validar_cargas(self, carga_minima, carga_maxima):
        """
        Comprueba que las cargas mínima y máxima
        respeten las reglas del gimnasio.

        Ambas deben informarse juntas o dejarse vacías.
        La carga máxima nunca puede ser inferior a la mínima.
        """

        # No permitimos informar solamente una de las cargas.
        if (carga_minima is None) != (carga_maxima is None):
            raise ValueError(
                "Debe indicar ambas cargas o dejar las dos vacías."
            )

        # Si ambas están vacías, no hay nada más que validar.
        if carga_minima is None:
            return

        # Convertimos los valores a Decimal para trabajar
        # con números decimales de manera precisa.
        try:
            minima = Decimal(str(carga_minima))
            maxima = Decimal(str(carga_maxima))
        except Exception:
            raise ValueError("Las cargas deben ser valores numéricos.")

        if not minima.is_finite() or not maxima.is_finite():
            raise ValueError("Las cargas deben ser valores numéricos válidos.")

        if minima < 0 or maxima < 0:
            raise ValueError("Las cargas no pueden ser negativas.")

        if maxima < minima:
            raise ValueError(
                "La carga máxima no puede ser inferior a la mínima."
            )

    def _validar_maquina(self, maquina):
        """
        Comprueba que el objeto recibido sea una máquina válida
        y que sus datos respeten las reglas de negocio.
        """

        if not isinstance(maquina, Maquina):
            raise ValueError("Los datos recibidos no corresponden a una máquina.")

        # Verificamos que ambas cargas sean coherentes.
        self._validar_cargas(
            maquina.carga_minima,
            maquina.carga_maxima
        )

        # Comprobamos que el estado sea uno de los permitidos.
        if maquina.estado not in Maquina.ESTADOS_VALIDOS:
            raise ValueError("El estado de la máquina no es válido.")

        # La fecha de alta debe estar informada.
        if not isinstance(maquina.fecha_alta, date):
            raise ValueError("La fecha de alta es obligatoria.")

    # --------------------------------------------------
    # REGISTRO
    # --------------------------------------------------

    def registrar(self, maquina):
        """
        Valida y registra una nueva máquina.

        Retorna:
            El identificador generado por MySQL.
        """

        self._validar_maquina(maquina)

        # Comprobamos si el código ya está registrado.
        existe = self.__repositorio.existe_codigo(maquina.codigo)

        if existe is None:
            raise RuntimeError(
                "No se pudo verificar la disponibilidad del código."
            )

        if existe:
            raise ValueError(
                "Ya existe una máquina registrada con ese código."
            )

        # Si todas las validaciones pasan, registramos la máquina.
        resultado = self.__repositorio.registrar(maquina)

        if resultado is None:
            raise RuntimeError("No se pudo registrar la máquina.")

        return resultado

    # --------------------------------------------------
    # ACTUALIZACIÓN
    # --------------------------------------------------

    def actualizar(self, maquina):
        """
        Valida y actualiza una máquina existente.
        """

        self._validar_maquina(maquina)

        if maquina.id_maquina is None:
            raise ValueError("La máquina no tiene un identificador asignado.")

        # Comprobamos que la máquina exista.
        existente = self.__repositorio.obtener_por_id(
            maquina.id_maquina
        )

        if existente is None:
            raise ValueError("No se encontró la máquina que desea actualizar.")

        # Verificamos que el código no pertenezca a otra máquina.
        existe = self.__repositorio.existe_codigo(
            maquina.codigo,
            excluir_id=maquina.id_maquina
        )

        if existe is None:
            raise RuntimeError(
                "No se pudo verificar la disponibilidad del código."
            )

        if existe:
            raise ValueError(
                "El código ingresado pertenece a otra máquina."
            )

        resultado = self.__repositorio.actualizar(maquina)

        if not resultado:
            raise RuntimeError("No se pudo actualizar la máquina.")

        return resultado

    # --------------------------------------------------
    # CAMBIO DE ESTADO
    # --------------------------------------------------

    def cambiar_estado(self, id_maquina, nuevo_estado):
        """
        Valida y modifica el estado de una máquina.
        """

        if nuevo_estado not in Maquina.ESTADOS_VALIDOS:
            raise ValueError("El nuevo estado de la máquina no es válido.")

        # Comprobamos que la máquina exista.
        self.obtener_por_id(id_maquina)

        resultado = self.__repositorio.cambiar_estado(
            id_maquina,
            nuevo_estado
        )

        if not resultado:
            raise RuntimeError("No se pudo modificar el estado de la máquina.")

        return resultado
