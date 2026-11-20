

import unittest
from datetime import date
from uuid import uuid4

from connection import obtener_conexion
from repositories.socio_repository import SocioRepository
from models.clase_socio import Socio


class TestSocioRepository(unittest.TestCase):
    """
    Comprueba las operaciones del repositorio de socios
    utilizando la base de datos MySQL.
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
        cls.repositorio = SocioRepository()

    def generar_dni(self):
        """
        Genera un DNI temporal de ocho dígitos.

        Utilizamos valores aleatorios para evitar conflictos
        con otros registros de la base de datos.
        """

        return str(uuid4().int % 100_000_000).zfill(8)

    def setUp(self):
        """
        Prepara usuarios y socios temporales para las pruebas.

        Creamos tres socios:
        - Dos activos.
        - Uno inactivo.

        También creamos un usuario que todavía no tiene
        un registro asociado en la tabla socios.
        """

        conexion = obtener_conexion()

        if conexion is None:
            self.fail("No se pudo conectar con la base de datos de prueba.")

        cursor = None

        try:
            cursor = conexion.cursor()

            # Generamos cuatro DNI diferentes para las pruebas.
            self.dnis = []

            while len(self.dnis) < 4:
                dni = self.generar_dni()

                if dni not in self.dnis:
                    self.dnis.append(dni)

            # Los tres primeros DNI tendrán un socio registrado.
            # El cuarto DNI se utilizará para probar registrar().
            self.dni_activo_1 = self.dnis[0]
            self.dni_activo_2 = self.dnis[1]
            self.dni_inactivo = self.dnis[2]
            self.dni_sin_socio = self.dnis[3]

            # Primero creamos los usuarios porque la tabla socios
            # tiene una clave foránea que depende de usuarios.
            consulta_usuario = """
                INSERT INTO usuarios (
                    dni,
                    nombre,
                    apellido,
                    telefono,
                    email,
                    password_hash,
                    rol,
                    activo
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            for i, dni in enumerate(self.dnis):
                cursor.execute(
                    consulta_usuario,
                    (
                        dni,
                        f"Usuario{i}",
                        "Prueba",
                        "1100000000",
                        f"usuario{i}_{dni}@test.com",
                        "hash_temporal_pruebas",
                        "SOCIO",
                        True
                    )
                )

            # Preparamos los tres socios con diferentes estados.
            consulta_socio = """
                INSERT INTO socios (
                    dni,
                    fecha_alta,
                    activo
                )
                VALUES (%s, %s, %s)
            """

            socios_prueba = [
                (self.dni_activo_1, date.today(), True),
                (self.dni_activo_2, date.today(), True),
                (self.dni_inactivo, date.today(), False)
            ]

            for socio in socios_prueba:
                cursor.execute(consulta_socio, socio)

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

        Primero eliminamos los socios y después los usuarios,
        respetando el orden de las claves foráneas.
        """

        conexion = obtener_conexion()

        if conexion is None:
            self.fail("No se pudo conectar para limpiar los datos de prueba.")

        cursor = None

        try:
            cursor = conexion.cursor()

            # Eliminamos los socios temporales.
            for dni in self.dnis:
                cursor.execute(
                    """
                    DELETE FROM socios
                    WHERE dni = %s
                    """,
                    (dni,)
                )

            # Eliminamos los usuarios temporales.
            for dni in self.dnis:
                cursor.execute(
                    """
                    DELETE FROM usuarios
                    WHERE dni = %s
                    """,
                    (dni,)
                )

            conexion.commit()

        except Exception:
            conexion.rollback()
            raise

        finally:
            if cursor is not None:
                cursor.close()

            conexion.close()

    def test_obtener_por_dni(self):
        # Buscamos uno de los socios activos creados para la prueba.
        socio = self.repositorio.obtener_por_dni(self.dni_activo_1)

        self.assertIsInstance(socio, Socio)
        self.assertEqual(socio.dni, self.dni_activo_1)
        self.assertTrue(socio.activo)

    def test_obtener_por_dni_inexistente(self):
        # Buscamos un DNI que no corresponde a nuestros socios.
        socio = self.repositorio.obtener_por_dni("00000000")

        self.assertIsNone(socio)

    def test_listar_todos(self):
        # Recuperamos todos los socios registrados.
        socios = self.repositorio.listar_todos()

        self.assertIsInstance(socios, list)

        # Cada elemento debe ser un objeto Socio.
        for socio in socios:
            self.assertIsInstance(socio, Socio)

        # Comprobamos que aparezcan nuestros tres socios temporales.
        dnis_encontrados = {socio.dni for socio in socios}

        self.assertTrue(
            {
                self.dni_activo_1,
                self.dni_activo_2,
                self.dni_inactivo
            }.issubset(dnis_encontrados)
        )

    def test_listar_activos(self):
        # Recuperamos solamente los socios activos.
        socios = self.repositorio.listar_activos()

        self.assertIsInstance(socios, list)

        # Todos los resultados deben ser objetos Socio activos.
        for socio in socios:
            self.assertIsInstance(socio, Socio)
            self.assertTrue(socio.activo)

        # Nuestros dos socios activos deben aparecer.
        dnis_encontrados = {socio.dni for socio in socios}

        self.assertIn(self.dni_activo_1, dnis_encontrados)
        self.assertIn(self.dni_activo_2, dnis_encontrados)

        # El socio inactivo no debe aparecer.
        self.assertNotIn(self.dni_inactivo, dnis_encontrados)

    def test_registrar(self):
        # Creamos un socio para el usuario que todavía no tiene socio.
        socio_nuevo = Socio(
            dni=self.dni_sin_socio,
            fecha_alta=date.today(),
            activo=True
        )

        # Registramos el socio en la base de datos.
        resultado = self.repositorio.registrar(socio_nuevo)

        self.assertTrue(resultado)

        # Comprobamos que el registro se haya guardado correctamente.
        socio_recuperado = self.repositorio.obtener_por_dni(
            self.dni_sin_socio
        )

        self.assertIsInstance(socio_recuperado, Socio)
        self.assertEqual(socio_recuperado.dni, self.dni_sin_socio)
        self.assertTrue(socio_recuperado.activo)

    def test_registrar_socio_duplicado(self):
        # Intentamos registrar nuevamente un socio que ya existe.
        socio_duplicado = Socio(
            dni=self.dni_activo_1,
            fecha_alta=date.today(),
            activo=True
        )

        resultado = self.repositorio.registrar(socio_duplicado)

        # La base de datos debe rechazar el DNI duplicado.
        self.assertFalse(resultado)


if __name__ == "__main__":
    unittest.main(verbosity=2)
