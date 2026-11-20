

import unittest
from datetime import date

from models.clase_socio import Socio


class TestSocioModel(unittest.TestCase):
    """
    Contiene las pruebas unitarias del modelo Socio.
    """

    # --------------------------------------------------
    # CREACIÓN DEL SOCIO
    # --------------------------------------------------

    def test_crear_socio_correctamente(self):
        socio = Socio(
            dni="12345678",
            fecha_alta=date(2026, 11, 20),
            activo=True
        )

        self.assertEqual(socio.dni, "12345678")
        self.assertEqual(socio.fecha_alta, date(2026, 11, 20))
        self.assertTrue(socio.activo)

    # --------------------------------------------------
    # DNI
    # --------------------------------------------------

    def test_dni_obligatorio(self):
        with self.assertRaises(ValueError):
            Socio(
                dni=None,
                fecha_alta=date(2026, 11, 20)
            )

    def test_dni_debe_tener_ocho_digitos(self):
        with self.assertRaises(ValueError):
            Socio(
                dni="1234567",
                fecha_alta=date(2026, 11, 20)
            )

    def test_dni_no_acepta_letras(self):
        with self.assertRaises(ValueError):
            Socio(
                dni="1234567A",
                fecha_alta=date(2026, 11, 20)
            )

    def test_dni_elimina_espacios(self):
        socio = Socio(
            dni=" 12345678 ",
            fecha_alta=date(2026, 11, 20)
        )

        self.assertEqual(socio.dni, "12345678")

    # --------------------------------------------------
    # FECHA DE ALTA
    # --------------------------------------------------

    def test_fecha_alta_obligatoria(self):
        with self.assertRaises(ValueError):
            Socio(
                dni="12345678",
                fecha_alta=None
            )

    def test_fecha_alta_valida(self):
        fecha = date(2026, 11, 20)

        socio = Socio(
            dni="12345678",
            fecha_alta=fecha
        )

        self.assertEqual(socio.fecha_alta, fecha)

    def test_fecha_alta_invalida(self):
        with self.assertRaises(ValueError):
            Socio(
                dni="12345678",
                fecha_alta="20/11/2026"
            )

    # --------------------------------------------------
    # ESTADO
    # --------------------------------------------------

    def test_estado_activo(self):
        socio = Socio(
            dni="12345678",
            fecha_alta=date(2026, 11, 20),
            activo=True
        )

        self.assertTrue(socio.activo)

    def test_estado_inactivo(self):
        socio = Socio(
            dni="12345678",
            fecha_alta=date(2026, 11, 20),
            activo=False
        )

        self.assertFalse(socio.activo)

    def test_estado_invalido(self):
        with self.assertRaises(ValueError):
            Socio(
                dni="12345678",
                fecha_alta=date(2026, 11, 20),
                activo="ACTIVO"
            )

    # --------------------------------------------------
    # MODIFICACIÓN DE ATRIBUTOS
    # --------------------------------------------------

    def test_modificar_estado(self):
        socio = Socio(
            dni="12345678",
            fecha_alta=date(2026, 11, 20)
        )

        socio.activo = False

        self.assertFalse(socio.activo)

    def test_modificar_dni_invalido(self):
        socio = Socio(
            dni="12345678",
            fecha_alta=date(2026, 11, 20)
        )

        with self.assertRaises(ValueError):
            socio.dni = "123"

    def test_modificar_fecha_invalida(self):
        socio = Socio(
            dni="12345678",
            fecha_alta=date(2026, 11, 20)
        )

        with self.assertRaises(ValueError):
            socio.fecha_alta = "fecha incorrecta"


if __name__ == "__main__":
    unittest.main()
