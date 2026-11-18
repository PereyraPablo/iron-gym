

import unittest
from datetime import date
from uuid import uuid4

from connection import obtener_conexion
from repositories.maquina_repository import MaquinaRepository
from models.clase_maquina import Maquina


class TestMaquinaRepository(unittest.TestCase):
    """
    Comprueba las operaciones de lectura del repositorio
    de máquinas utilizando la base de datos MySQL.
    """

    @classmethod
    def setUpClass(cls):
        # Verificamos que MySQL esté disponible antes de probar.
        conexion = obtener_conexion()

        if conexion is None:
            raise RuntimeError(
                "No se pudo conectar con la base de datos Iron Gym."
            )

        conexion.close()

        # Creamos el repositorio que vamos a probar.
        cls.repositorio = MaquinaRepository()

    def setUp(self):
        """
        Prepara registros temporales para las pruebas de filtros.

        Creamos grupos y máquinas con distintos estados para
        comprobar que las consultas apliquen correctamente
        las condiciones establecidas.
        """

        conexion = obtener_conexion()

        if conexion is None:
            self.fail("No se pudo conectar con la base de datos de prueba.")

        cursor = None

        try:
            cursor = conexion.cursor()

            # Generamos un identificador único para evitar
            # conflictos con otros registros de la base de datos.
            sufijo = uuid4().hex[:8]

            # Creamos tres grupos musculares:
            # uno activo con máquinas, uno inactivo y uno vacío.
            consulta_grupo = """
                INSERT INTO grupos_musculares (
                    nombre,
                    descripcion,
                    activo
                )
                VALUES (%s, %s, %s)
            """

            cursor.execute(
                consulta_grupo,
                (f"Grupo activo {sufijo}", "Grupo para pruebas", True)
            )
            self.id_grupo_activo = cursor.lastrowid

            cursor.execute(
                consulta_grupo,
                (f"Grupo inactivo {sufijo}", "Grupo para pruebas", False)
            )
            self.id_grupo_inactivo = cursor.lastrowid

            cursor.execute(
                consulta_grupo,
                (f"Grupo vacío {sufijo}", "Grupo para pruebas", True)
            )
            self.id_grupo_vacio = cursor.lastrowid

            # Preparamos los identificadores de las máquinas creadas.
            self.ids_maquinas = []

            # Creamos dos máquinas activas y una inactiva.
            consulta_maquina = """
                INSERT INTO maquinas (
                    codigo,
                    nombre,
                    estado,
                    fecha_alta
                )
                VALUES (%s, %s, %s, %s)
            """

            maquinas_prueba = [
                (
                    f"TEST-A-{sufijo}",
                    f"Máquina activa principal {sufijo}",
                    "ACTIVA"
                ),
                (
                    f"TEST-B-{sufijo}",
                    f"Máquina activa secundaria {sufijo}",
                    "ACTIVA"
                ),
                (
                    f"TEST-C-{sufijo}",
                    f"Máquina inactiva {sufijo}",
                    "INACTIVA"
                )
            ]

            for codigo, nombre, estado in maquinas_prueba:
                cursor.execute(
                    consulta_maquina,
                    (codigo, nombre, estado, date.today())
                )

                self.ids_maquinas.append(cursor.lastrowid)

            # Relacionamos las tres máquinas con el grupo activo.
            consulta_relacion = """
                INSERT INTO maquina_grupo_muscular (
                    id_maquina,
                    id_grupo,
                    tipo_trabajo
                )
                VALUES (%s, %s, %s)
            """

            cursor.execute(
                consulta_relacion,
                (
                    self.ids_maquinas[0],
                    self.id_grupo_activo,
                    "PRINCIPAL"
                )
            )

            cursor.execute(
                consulta_relacion,
                (
                    self.ids_maquinas[1],
                    self.id_grupo_activo,
                    "SECUNDARIO"
                )
            )

            cursor.execute(
                consulta_relacion,
                (
                    self.ids_maquinas[2],
                    self.id_grupo_activo,
                    "PRINCIPAL"
                )
            )

            # Relacionamos una máquina activa con el grupo inactivo.
            cursor.execute(
                consulta_relacion,
                (
                    self.ids_maquinas[0],
                    self.id_grupo_inactivo,
                    "SECUNDARIO"
                )
            )

            # Confirmamos los registros temporales.
            conexion.commit()

        except Exception:
            # Si falla la preparación, deshacemos los cambios.
            conexion.rollback()
            raise

        finally:
            if cursor is not None:
                cursor.close()

            conexion.close()

    def tearDown(self):
        """
        Elimina los registros temporales creados por cada prueba.

        Respetamos el orden de las claves foráneas:
        primero las relaciones, después las máquinas y los grupos.
        """

        conexion = obtener_conexion()

        if conexion is None:
            self.fail("No se pudo conectar para limpiar los datos de prueba.")

        cursor = None

        try:
            cursor = conexion.cursor()

            # Eliminamos las relaciones de las máquinas temporales.
            for id_maquina in self.ids_maquinas:
                cursor.execute(
                    """
                    DELETE FROM maquina_grupo_muscular
                    WHERE id_maquina = %s
                    """,
                    (id_maquina,)
                )

            # Eliminamos las máquinas temporales.
            for id_maquina in self.ids_maquinas:
                cursor.execute(
                    """
                    DELETE FROM maquinas
                    WHERE id_maquina = %s
                    """,
                    (id_maquina,)
                )

            # Eliminamos los grupos musculares temporales.
            for id_grupo in (
                self.id_grupo_activo,
                self.id_grupo_inactivo,
                self.id_grupo_vacio
            ):
                cursor.execute(
                    """
                    DELETE FROM grupos_musculares
                    WHERE id_grupo = %s
                    """,
                    (id_grupo,)
                )

            conexion.commit()

        except Exception:
            conexion.rollback()
            raise

        finally:
            if cursor is not None:
                cursor.close()

            conexion.close()

    def test_listar_todas(self):
        # Recuperamos todas las máquinas registradas.
        maquinas = self.repositorio.listar_todas()

        # El resultado debe ser una lista.
        self.assertIsInstance(maquinas, list)

        # Cada elemento debe ser un objeto Maquina.
        for maquina in maquinas:
            self.assertIsInstance(maquina, Maquina)

        print(f"\nMáquinas encontradas: {len(maquinas)}")

    def test_listar_activas(self):
        # Recuperamos solamente las máquinas activas.
        maquinas = self.repositorio.listar_activas()

        self.assertIsInstance(maquinas, list)

        for maquina in maquinas:
            self.assertIsInstance(maquina, Maquina)
            self.assertEqual(maquina.estado, "ACTIVA")

        print(f"\nMáquinas activas: {len(maquinas)}")

    def test_obtener_por_id(self):
        # Primero recuperamos todas las máquinas.
        maquinas = self.repositorio.listar_todas()

        # Si hay registros, comprobamos la búsqueda individual.
        if maquinas:
            primera_maquina = maquinas[0]

            resultado = self.repositorio.obtener_por_id(
                primera_maquina.id_maquina
            )

            self.assertIsInstance(resultado, Maquina)
            self.assertEqual(
                resultado.id_maquina,
                primera_maquina.id_maquina
            )

        else:
            print("\nNo hay máquinas registradas para probar la búsqueda.")

    def test_listar_grupos_activos(self):
        # Recuperamos los grupos musculares activos.
        grupos = self.repositorio.listar_grupos_activos()

        self.assertIsInstance(grupos, list)

        # Cada resultado debe ser un diccionario.
        for grupo in grupos:
            self.assertIsInstance(grupo, dict)
            self.assertTrue(grupo["id_grupo"])
            self.assertTrue(grupo["nombre"])

        # Nuestro grupo activo debe aparecer.
        ids_grupos = [grupo["id_grupo"] for grupo in grupos]

        self.assertIn(self.id_grupo_activo, ids_grupos)

        # El grupo inactivo no debe aparecer.
        self.assertNotIn(self.id_grupo_inactivo, ids_grupos)

    def test_listar_activas_por_grupo(self):
        # Recuperamos las máquinas asociadas al grupo activo.
        maquinas = self.repositorio.listar_activas_por_grupo(
            self.id_grupo_activo
        )

        self.assertIsInstance(maquinas, list)

        # Solamente deben aparecer las dos máquinas activas.
        ids_encontrados = {
            maquina["id_maquina"] for maquina in maquinas
        }

        self.assertEqual(
            ids_encontrados,
            {self.ids_maquinas[0], self.ids_maquinas[1]}
        )

        # Comprobamos que se recupere el tipo de trabajo muscular.
        tipos_trabajo = {
            maquina["tipo_trabajo"] for maquina in maquinas
        }

        self.assertEqual(
            tipos_trabajo,
            {"PRINCIPAL", "SECUNDARIO"}
        )

    def test_listar_activas_por_grupo_inactivo(self):
        # Aunque tenga una máquina relacionada, el grupo está inactivo.
        maquinas = self.repositorio.listar_activas_por_grupo(
            self.id_grupo_inactivo
        )

        self.assertEqual(maquinas, [])

    def test_listar_activas_por_grupo_sin_maquinas(self):
        # Un grupo activo sin máquinas relacionadas debe devolver
        # una lista vacía.
        maquinas = self.repositorio.listar_activas_por_grupo(
            self.id_grupo_vacio
        )

        self.assertEqual(maquinas, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
