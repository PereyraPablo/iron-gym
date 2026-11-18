

# Importamos el conector de MySQL para manejar sus excepciones.
import mysql.connector

# Importamos la función encargada de establecer la conexión.
from connection import obtener_conexion

# Importamos el modelo que representa una máquina.
from models.clase_maquina import Maquina


class MaquinaRepository:
    """
    Repositorio encargado de realizar las operaciones
    de acceso a datos correspondientes a la tabla maquinas.

    Se comunica directamente con MySQL y utiliza
    la clase Maquina para representar los registros.
    """


    def listar_todas(self):
        """
        Obtiene todas las máquinas registradas.

        Retorna:
            Una lista de objetos Maquina.
        """

        conexion = None
        cursor = None
        maquinas = []

        try:
            # Solicitamos una conexión con la base de datos.
            conexion = obtener_conexion()

            # Comprobamos que la conexión se haya establecido.
            if conexion is None:
                return maquinas

            # Creamos un cursor que devuelve los resultados como diccionarios.
            cursor = conexion.cursor(dictionary=True)

            # Consultamos todas las máquinas.
            consulta = """
                SELECT *
                FROM maquinas
                ORDER BY nombre ASC
            """

            cursor.execute(consulta)

            # Recuperamos todos los registros encontrados.
            resultados = cursor.fetchall()

            # Convertimos cada registro en un objeto Maquina.
            for registro in resultados:
                maquina = Maquina(**registro)
                maquinas.append(maquina)

            return maquinas

        except mysql.connector.Error as error:
            print(f"Error al listar las máquinas: {error}")
            return []

        finally:
            # Liberamos los recursos utilizados.
            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()


    def listar_activas(self):
        """
        Obtiene únicamente las máquinas disponibles
        para el catálogo público.

        Retorna:
            Una lista de objetos Maquina activas.
        """

        conexion = None
        cursor = None
        maquinas = []

        try:
            conexion = obtener_conexion()

            if conexion is None:
                return maquinas

            cursor = conexion.cursor(dictionary=True)

            # Filtramos las máquinas cuyo estado sea ACTIVA.
            consulta = """
                SELECT *
                FROM maquinas
                WHERE estado = %s
                ORDER BY nombre ASC
            """

            cursor.execute(consulta, ("ACTIVA",))

            resultados = cursor.fetchall()

            for registro in resultados:
                maquina = Maquina(**registro)
                maquinas.append(maquina)

            return maquinas

        except mysql.connector.Error as error:
            print(f"Error al listar las máquinas activas: {error}")
            return []

        finally:
            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()

    
    def listar_grupos_activos(self):
        """
        Obtiene los grupos musculares que están activos.

        Retorna:
            Una lista de diccionarios con los datos de cada grupo.
            Una lista vacía si no hay grupos o ocurre un error.
        """

        conexion = None
        cursor = None
        grupos = []

        try:
            # Solicitamos una conexión con la base de datos.
            conexion = obtener_conexion()

            if conexion is None:
                return grupos

            # Utilizamos un cursor que devuelve los resultados como diccionarios.
            cursor = conexion.cursor(dictionary=True)

            # Consultamos únicamente los grupos musculares activos.
            consulta = """
                SELECT id_grupo, nombre, descripcion
                FROM grupos_musculares
                WHERE activo = TRUE
                ORDER BY nombre ASC
            """

            cursor.execute(consulta)

            # Recuperamos todos los grupos encontrados.
            grupos = cursor.fetchall()

            return grupos

        except mysql.connector.Error as error:
            print(f"Error al listar los grupos musculares: {error}")
            return []

        finally:
            # Liberamos los recursos utilizados.
            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()


    def listar_activas_por_grupo(self, id_grupo):
        """
        Obtiene las máquinas activas asociadas a un grupo muscular.

        Parámetros:
            id_grupo: identificador del grupo muscular.

        Retorna:
            Una lista de diccionarios con los datos de las máquinas
            y el tipo de trabajo muscular.
            Una lista vacía si no hay resultados o ocurre un error.
        """

        conexion = None
        cursor = None
        maquinas = []

        try:
            # Solicitamos una conexión con la base de datos.
            conexion = obtener_conexion()

            if conexion is None:
                return maquinas

            # Utilizamos un cursor que devuelve los resultados como diccionarios.
            cursor = conexion.cursor(dictionary=True)

            # Relacionamos las máquinas con sus grupos musculares.
            # También verificamos que ambos registros estén activos.
            consulta = """
                SELECT
                    m.*,
                    mgm.tipo_trabajo
                FROM maquinas AS m
                INNER JOIN maquina_grupo_muscular AS mgm
                    ON m.id_maquina = mgm.id_maquina
                INNER JOIN grupos_musculares AS gm
                    ON mgm.id_grupo = gm.id_grupo
                WHERE m.estado = %s
                AND gm.id_grupo = %s
                AND gm.activo = TRUE
                ORDER BY m.nombre ASC
            """

            cursor.execute(consulta, ("ACTIVA", id_grupo))

            # Recuperamos las máquinas encontradas.
            maquinas = cursor.fetchall()

            return maquinas

        except mysql.connector.Error as error:
            print(f"Error al listar máquinas por grupo muscular: {error}")
            return []

        finally:
            # Liberamos los recursos utilizados.
            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()
            

    def obtener_por_id(self, id_maquina):
        """
        Busca una máquina mediante su identificador.

        Parámetros:
            id_maquina: identificador de la máquina.

        Retorna:
            Un objeto Maquina si existe.
            None si no se encuentra.
        """

        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()

            if conexion is None:
                return None

            cursor = conexion.cursor(dictionary=True)

            consulta = """
                SELECT *
                FROM maquinas
                WHERE id_maquina = %s
            """

            cursor.execute(consulta, (id_maquina,))

            registro = cursor.fetchone()

            if registro is not None:
                return Maquina(**registro)

            return None

        except mysql.connector.Error as error:
            print(f"Error al buscar la máquina: {error}")
            return None

        finally:
            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()


    def registrar(self, maquina):
        """
        Registra una nueva máquina en la base de datos.

        Parámetros:
            maquina: objeto de la clase Maquina.

        Retorna:
            El identificador generado por MySQL.
            None si ocurre un error.
        """

        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()

            if conexion is None:
                return None

            cursor = conexion.cursor()

            consulta = """
                INSERT INTO maquinas (
                    codigo,
                    nombre,
                    marca,
                    modelo,
                    descripcion,
                    carga_minima,
                    carga_maxima,
                    imagen,
                    estado,
                    fecha_alta
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            valores = (
                maquina.codigo,
                maquina.nombre,
                maquina.marca,
                maquina.modelo,
                maquina.descripcion,
                maquina.carga_minima,
                maquina.carga_maxima,
                maquina.imagen,
                maquina.estado,
                maquina.fecha_alta
            )

            cursor.execute(consulta, valores)

            # Confirmamos el registro en la base de datos.
            conexion.commit()

            # Recuperamos el ID generado automáticamente por MySQL.
            return cursor.lastrowid

        except mysql.connector.Error as error:
            print(f"Error al registrar la máquina: {error}")

            # Deshacemos la operación si ocurrió algún error.
            if conexion is not None:
                conexion.rollback()

            return None

        finally:
            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()


    def actualizar(self, maquina):
        """
        Actualiza los datos de una máquina existente.

        Parámetros:
            maquina: objeto Maquina con los datos modificados.

        Retorna:
            True si la operación se ejecutó correctamente.
            False si ocurrió un error.
        """

        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()

            if conexion is None:
                return False

            cursor = conexion.cursor()

            consulta = """
                UPDATE maquinas
                SET
                    codigo = %s,
                    nombre = %s,
                    marca = %s,
                    modelo = %s,
                    descripcion = %s,
                    carga_minima = %s,
                    carga_maxima = %s,
                    imagen = %s,
                    estado = %s,
                    fecha_alta = %s
                WHERE id_maquina = %s
            """

            valores = (
                maquina.codigo,
                maquina.nombre,
                maquina.marca,
                maquina.modelo,
                maquina.descripcion,
                maquina.carga_minima,
                maquina.carga_maxima,
                maquina.imagen,
                maquina.estado,
                maquina.fecha_alta,
                maquina.id_maquina
            )

            cursor.execute(consulta, valores)

            conexion.commit()

            return True

        except mysql.connector.Error as error:
            print(f"Error al actualizar la máquina: {error}")

            if conexion is not None:
                conexion.rollback()

            return False

        finally:
            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()
                

    def cambiar_estado(self, id_maquina, nuevo_estado):
        """
        Modifica el estado de una máquina.

        Permite establecer los estados:
            ACTIVA, INACTIVA o REPARACION.

        Parámetros:
            id_maquina: identificador de la máquina.
            nuevo_estado: nuevo estado que se desea establecer.

        Retorna:
            True si la operación se ejecutó correctamente.
            False si ocurrió un error.
        """

        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()

            if conexion is None:
                return False

            cursor = conexion.cursor()

            consulta = """
                UPDATE maquinas
                SET estado = %s
                WHERE id_maquina = %s
            """

            cursor.execute(
                consulta,
                (nuevo_estado, id_maquina)
            )

            conexion.commit()

            return True

        except mysql.connector.Error as error:
            print(f"Error al cambiar el estado de la máquina: {error}")

            if conexion is not None:
                conexion.rollback()

            return False

        finally:
            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()


    def existe_codigo(self, codigo, excluir_id=None):
        """
        Comprueba si un código ya está registrado.

        Parámetros:
            codigo: código que se desea verificar.
            excluir_id: identificador que se excluye de la búsqueda.
                        Se utiliza al actualizar una máquina.

        Retorna:
            True si el código ya existe.
            False si el código está disponible.
            None si ocurre un error de conexión o consulta.
        """

        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()

            if conexion is None:
                return None

            cursor = conexion.cursor()

            # Si estamos modificando una máquina, excluimos su propio ID.
            if excluir_id is not None:
                consulta = """
                    SELECT 1
                    FROM maquinas
                    WHERE codigo = %s
                    AND id_maquina <> %s
                    LIMIT 1
                """

                cursor.execute(consulta, (codigo, excluir_id))

            else:
                consulta = """
                    SELECT 1
                    FROM maquinas
                    WHERE codigo = %s
                    LIMIT 1
                """

                cursor.execute(consulta, (codigo,))

            # Si fetchone devuelve un registro, el código ya existe.
            return cursor.fetchone() is not None

        except mysql.connector.Error as error:
            print(f"Error al verificar el código de la máquina: {error}")
            return None

        finally:
            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()
