

class Maquina:
    """
    Representa una máquina de musculación del gimnasio.

    Esta clase contiene los atributos correspondientes
    a la tabla maquinas de nuestra base de datos.
    """

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
        # Identificador único generado automáticamente por MySQL.
        self.id_maquina = id_maquina

        # Código interno que identifica a cada máquina.
        self.codigo = codigo

        # Información descriptiva de la máquina.
        self.nombre = nombre
        self.marca = marca
        self.modelo = modelo
        self.descripcion = descripcion

        # Rango de carga permitido para la máquina.
        self.carga_minima = carga_minima
        self.carga_maxima = carga_maxima

        # Ruta o nombre del archivo de imagen.
        self.imagen = imagen

        # Estado actual de la máquina.
        self.estado = estado

        # Fecha en la que se incorporó al gimnasio.
        self.fecha_alta = fecha_alta
