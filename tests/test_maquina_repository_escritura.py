

import unittest
import uuid
from datetime import date

import mysql.connector

from connection import obtener_conexion
from models.clase_maquina import Maquina
from repositories.maquina_repository import MaquinaRepository


class TestMaquinaRepositoryEscritura(unittest.TestCase):
    """
    Comprueba las operaciones de escritura del repositorio
    de máquinas utilizando registros temporales de prueba.
    """

    @classmethod
    def setUpClass(cls):
        # Verificamos que MySQL esté disponible antes de comenzar.
        conexion = obtener_conexion()

        if conexion is None:
            raise RuntimeError(
                "No se pudo conectar con la base de datos Iron Gym."
            )

        conexion.close()

        cls.repositorio = MaquinaRepository()

    def setUp(self):
        # Cada prueba tendrá su propio identificador de máquina.
        self.id_maquina = None

        # Generamos un código único para evitar conflictos.
        codigo_unico = f"TEST-{uuid.uuid4().hex[:10].upper()}"

        # Construimos una máquina temporal para las pruebas.
        self.maquina = Maquina(
            codigo=codigo_unico,
            nombre="Máquina de prueba",
            marca="Iron Gym",
            modelo="Modelo temporal",
            descripcion="Registro utilizado para pruebas automatizadas.",
            carga_minima=5,
            carga_maxima=100,
            imagen=None,
            estado="ACTIVA",
            fecha_alta=date.today()
        )

    def tearDown(self):
        """
        Elimina el registro temporal después de cada prueba.

        De esta manera no dejamos máquinas de prueba
        almacenadas en la base de datos real.
        """

        if self.id_maquina is None:
            return

        conexion = None
        cursor = None

        try:
            conexion = obtener_conexion()

            if conexion is None:
                self.fail("No se pudo conectar para limpiar la prueba.")

            cursor = conexion.cursor()

            consulta = """
                DELETE FROM maquinas
                WHERE id_maquina = %s
            """

            cursor.execute(consulta, (self.id_maquina,))
            conexion.commit()

        except mysql.connector.Error as error:
            self.fail(f"Error al limpiar la máquina de prueba: {error}")

        finally:
            if cursor is not None:
                cursor.close()

            if conexion is not None:
                conexion.close()

    def registrar_maquina_prueba(self):
        """
        Registra la máquina temporal y guarda su identificador
        para poder recuperarla y eliminarla posteriormente.
        """

        self.id_maquina = self.repositorio.registrar(self.maquina)

        self.assertIsNotNone(
            self.id_maquina,
            "No se pudo registrar la máquina de prueba."
        )

    def test_registrar(self):
        # Registramos la máquina temporal.
        self.registrar_maquina_prueba()

        # Recuperamos el registro utilizando su identificador.
        resultado = self.repositorio.obtener_por_id(
            self.id_maquina
        )

        # Comprobamos que se haya guardado correctamente.
        self.assertIsInstance(resultado, Maquina)
        self.assertEqual(resultado.codigo, self.maquina.codigo)
        self.assertEqual(resultado.nombre, self.maquina.nombre)

    def test_actualizar(self):
        # Primero registramos una máquina para poder modificarla.
        self.registrar_maquina_prueba()

        # Modificamos algunos de sus atributos.
        self.maquina.id_maquina = self.id_maquina
        self.maquina.nombre = "Máquina actualizada"
        self.maquina.descripcion = "Descripción modificada."
        self.maquina.carga_maxima = 120

        # Ejecutamos la actualización.
        resultado = self.repositorio.actualizar(self.maquina)

        self.assertTrue(resultado)

        # Volvemos a consultar el registro para comprobar los cambios.
        maquina_actualizada = self.repositorio.obtener_por_id(
            self.id_maquina
        )

        self.assertEqual(
            maquina_actualizada.nombre,
            "Máquina actualizada"
        )

        self.assertEqual(
            maquina_actualizada.descripcion,
            "Descripción modificada."
        )

        self.assertEqual(
            float(maquina_actualizada.carga_maxima),
            120.0
        )

    def test_cambiar_estado(self):
        # Registramos una máquina inicialmente activa.
        self.registrar_maquina_prueba()

        # Cambiamos su estado a REPARACION.
        resultado = self.repositorio.cambiar_estado(
            self.id_maquina,
            "REPARACION"
        )

        self.assertTrue(resultado)

        # Consultamos nuevamente la máquina.
        maquina_actualizada = self.repositorio.obtener_por_id(
            self.id_maquina
        )

        # Verificamos que el nuevo estado se haya guardado.
        self.assertEqual(
            maquina_actualizada.estado,
            "REPARACION"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
