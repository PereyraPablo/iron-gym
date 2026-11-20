

import unittest
from datetime import date
from unittest.mock import patch

from models.clase_socio import Socio
from services.socio_service import SocioService


class TestSocioService(unittest.TestCase):
    """
    Comprueba las reglas de negocio del servicio de socios.

    Simulamos las respuestas del repositorio para probar
    el comportamiento del servicio sin acceder a MySQL.
    """

    def setUp(self):
        # Simulamos el repositorio antes de crear el servicio.
        self.parche = patch("services.socio_service.SocioRepository")
        self.repositorio_mock = self.parche.start()

        # Creamos el servicio y obtenemos su repositorio simulado.
        self.servicio = SocioService()
        self.repositorio = self.repositorio_mock.return_value

        # Creamos un socio válido para utilizar en las pruebas.
        self.socio = Socio(
            dni="12345678",
            fecha_alta=date.today(),
            activo=True
        )

    def tearDown(self):
        # Restauramos la clase original del repositorio.
        self.parche.stop()

    # --------------------------------------------------
    # CONSULTAS
    # --------------------------------------------------

    def test_obtener_por_dni(self):
        # Simulamos que el repositorio encuentra al socio.
        self.repositorio.obtener_por_dni.return_value = self.socio

        resultado = self.servicio.obtener_por_dni("12345678")

        self.assertIsInstance(resultado, Socio)
        self.assertEqual(resultado.dni, "12345678")

    def test_obtener_por_dni_invalido(self):
        # Un DNI con menos de 8 dígitos debe ser rechazado.
        with self.assertRaises(ValueError):
            self.servicio.obtener_por_dni("1234")

    def test_obtener_por_dni_vacio(self):
        # No se permite buscar utilizando un DNI vacío.
        with self.assertRaises(ValueError):
            self.servicio.obtener_por_dni("")

    def test_obtener_por_dni_inexistente(self):
        # Simulamos que el repositorio no encuentra al socio.
        self.repositorio.obtener_por_dni.return_value = None

        resultado = self.servicio.obtener_por_dni("12345678")

        self.assertIsNone(resultado)

    def test_listar_todos(self):
        # Simulamos una lista con un socio.
        self.repositorio.listar_todos.return_value = [self.socio]

        resultado = self.servicio.listar_todos()

        self.assertIsInstance(resultado, list)
        self.assertEqual(len(resultado), 1)
        self.repositorio.listar_todos.assert_called_once()

    def test_listar_activos(self):
        # Simulamos una lista de socios activos.
        self.repositorio.listar_activos.return_value = [self.socio]

        resultado = self.servicio.listar_activos()

        self.assertIsInstance(resultado, list)
        self.assertEqual(len(resultado), 1)
        self.repositorio.listar_activos.assert_called_once()

    # --------------------------------------------------
    # VALIDACIONES
    # --------------------------------------------------

    def test_validar_socio_correcto(self):
        # Un socio correctamente construido debe ser válido.
        self.servicio._validar_socio(self.socio)

    def test_validar_objeto_incorrecto(self):
        # El servicio debe rechazar objetos que no sean Socio.
        with self.assertRaises(ValueError):
            self.servicio._validar_socio("No soy un socio")

    # --------------------------------------------------
    # REGISTRO
    # --------------------------------------------------

    def test_registrar_socio(self):
        # Simulamos que el DNI todavía no está registrado.
        self.repositorio.obtener_por_dni.return_value = None

        # Simulamos que el registro se realiza correctamente.
        self.repositorio.registrar.return_value = True

        resultado = self.servicio.registrar(self.socio)

        self.assertTrue(resultado)

        # Comprobamos que se hayan realizado las consultas.
        self.repositorio.obtener_por_dni.assert_called_once_with(
            "12345678"
        )

        self.repositorio.registrar.assert_called_once_with(
            self.socio
        )

    def test_registrar_socio_duplicado(self):
        # Simulamos que ya existe un socio con ese DNI.
        self.repositorio.obtener_por_dni.return_value = self.socio

        with self.assertRaises(ValueError):
            self.servicio.registrar(self.socio)

        # No debe intentar registrar un socio duplicado.
        self.repositorio.registrar.assert_not_called()

    def test_registrar_objeto_incorrecto(self):
        # No se permite registrar un objeto que no sea Socio.
        with self.assertRaises(ValueError):
            self.servicio.registrar("Objeto incorrecto")

        # El repositorio no debe recibir ninguna solicitud.
        self.repositorio.registrar.assert_not_called()

    def test_error_al_registrar_socio(self):
        # Simulamos que el DNI está disponible.
        self.repositorio.obtener_por_dni.return_value = None

        # Simulamos que el repositorio no logra registrar.
        self.repositorio.registrar.return_value = False

        with self.assertRaises(RuntimeError):
            self.servicio.registrar(self.socio)


if __name__ == "__main__":
    unittest.main(verbosity=2)
