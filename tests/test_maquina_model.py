

import unittest
from datetime import date
from decimal import Decimal

from models.clase_maquina import Maquina


class TestMaquinaModel(unittest.TestCase):
    """
    Comprueba el funcionamiento del modelo Maquina,
    incluyendo sus propiedades y validaciones.
    """

    def crear_maquina(self):
        """
        Crea una máquina con datos válidos para reutilizar
        en las distintas pruebas.
        """

        return Maquina(
            id_maquina=1,
            codigo="TEST-001",
            nombre="Press de pecho",
            marca="Iron Gym",
            modelo="Modelo A",
            descripcion="Máquina para trabajar pectorales.",
            carga_minima=5,
            carga_maxima=100,
            imagen="press_pecho.jpg",
            estado="ACTIVA",
            fecha_alta=date.today()
        )

    # --------------------------------------------------
    # PRUEBAS DE CREACIÓN
    # --------------------------------------------------

    def test_crear_maquina_correctamente(self):
        # Comprobamos que se pueda crear una máquina válida.
        maquina = self.crear_maquina()

        self.assertIsInstance(maquina, Maquina)
        self.assertEqual(maquina.nombre, "Press de pecho")
        self.assertEqual(maquina.estado, "ACTIVA")

    # --------------------------------------------------
    # PRUEBAS DE NOMBRE
    # --------------------------------------------------

    def test_nombre_obligatorio(self):
        # El nombre no puede ser None ni una cadena vacía.
        with self.assertRaises(ValueError):
            Maquina(codigo="TEST-002", nombre=None)

        with self.assertRaises(ValueError):
            Maquina(codigo="TEST-003", nombre="   ")

    def test_modificar_nombre(self):
        maquina = self.crear_maquina()

        # Comprobamos que la propiedad permita modificar el nombre.
        maquina.nombre = "Press inclinado"

        self.assertEqual(maquina.nombre, "Press inclinado")

    # --------------------------------------------------
    # PRUEBAS DE CÓDIGO
    # --------------------------------------------------

    def test_codigo_obligatorio(self):
        with self.assertRaises(ValueError):
            Maquina(codigo="", nombre="Máquina de prueba")

    # --------------------------------------------------
    # PRUEBAS DE CARGAS
    # --------------------------------------------------

    def test_cargas_no_negativas(self):
        with self.assertRaises(ValueError):
            Maquina(
                codigo="TEST-004",
                nombre="Máquina de prueba",
                carga_minima=-5
            )

        with self.assertRaises(ValueError):
            Maquina(
                codigo="TEST-005",
                nombre="Máquina de prueba",
                carga_maxima=-10
            )

    def test_cargas_admiten_valores_decimales(self):
        maquina = self.crear_maquina()

        maquina.carga_minima = 2.5
        maquina.carga_maxima = 75.5

        self.assertEqual(maquina.carga_minima, Decimal("2.5"))
        self.assertEqual(maquina.carga_maxima, Decimal("75.5"))

    def test_cargas_rechazan_valores_no_numericos(self):
        maquina = self.crear_maquina()

        with self.assertRaises(ValueError):
            maquina.carga_minima = "pesado"

        with self.assertRaises(ValueError):
            maquina.carga_maxima = "mucho"

    # --------------------------------------------------
    # PRUEBAS DE ESTADO
    # --------------------------------------------------

    def test_estado_valido(self):
        maquina = self.crear_maquina()

        for estado in ("ACTIVA", "INACTIVA", "REPARACION"):
            maquina.estado = estado
            self.assertEqual(maquina.estado, estado)

    def test_estado_invalido(self):
        maquina = self.crear_maquina()

        with self.assertRaises(ValueError):
            maquina.estado = "FUERA_DE_SERVICIO"

    # --------------------------------------------------
    # PRUEBAS DE FECHA
    # --------------------------------------------------

    def test_fecha_alta_valida(self):
        maquina = self.crear_maquina()

        self.assertIsInstance(maquina.fecha_alta, date)

    def test_fecha_alta_invalida(self):
        maquina = self.crear_maquina()

        with self.assertRaises(ValueError):
            maquina.fecha_alta = "15/11/2026"

    # --------------------------------------------------
    # PRUEBAS DE ATRIBUTOS OPCIONALES
    # --------------------------------------------------

    def test_atributos_opcionales_admiten_none(self):
        maquina = self.crear_maquina()

        maquina.marca = None
        maquina.modelo = None
        maquina.descripcion = None
        maquina.imagen = None

        self.assertIsNone(maquina.marca)
        self.assertIsNone(maquina.modelo)
        self.assertIsNone(maquina.descripcion)
        self.assertIsNone(maquina.imagen)


if __name__ == "__main__":
    unittest.main(verbosity=2)
