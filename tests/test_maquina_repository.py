

import unittest

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


if __name__ == "__main__":
    unittest.main(verbosity=2)
