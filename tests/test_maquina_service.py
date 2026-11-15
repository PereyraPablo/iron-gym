

import unittest
from datetime import date
from decimal import Decimal
from unittest.mock import patch

from models.clase_maquina import Maquina
from services.maquina_service import MaquinaService


class TestMaquinaService(unittest.TestCase):
    """
    Pruebas unitarias del servicio de máquinas.

    Utilizamos mocks para simular el repositorio y evitar
    depender de una conexión real con MySQL.
    """

    def setUp(self):
        # Simulamos el repositorio que utiliza el servicio.
        self.patch_repositorio = patch(
            "services.maquina_service.MaquinaRepository"
        )

        self.mock_repositorio = self.patch_repositorio.start()

        # Creamos el servicio utilizando el repositorio simulado.
        self.servicio = MaquinaService()

        self.repositorio = self.servicio._MaquinaService__repositorio

        # Creamos una máquina válida para utilizar en las pruebas.
        self.maquina = Maquina(
            id_maquina=1,
            codigo="MAQ-001",
            nombre="Press de pecho",
            marca="Iron Gym",
            modelo="PX-100",
            descripcion="Máquina para trabajar pectorales.",
            carga_minima=Decimal("5.00"),
            carga_maxima=Decimal("100.00"),
            imagen="press_pecho.jpg",
            estado="ACTIVA",
            fecha_alta=date.today()
        )

    def tearDown(self):
        # Restauramos el comportamiento original del repositorio.
        self.patch_repositorio.stop()

    # --------------------------------------------------
    # CONSULTAS
    # --------------------------------------------------

    def test_listar_activas(self):
        self.repositorio.listar_activas.return_value = [self.maquina]

        resultado = self.servicio.listar_activas()

        self.assertEqual(len(resultado), 1)
        self.repositorio.listar_activas.assert_called_once()

    def test_obtener_por_id_invalido(self):
        with self.assertRaises(ValueError):
            self.servicio.obtener_por_id(0)

        self.repositorio.obtener_por_id.assert_not_called()

    def test_obtener_por_id_inexistente(self):
        self.repositorio.obtener_por_id.return_value = None

        with self.assertRaises(ValueError):
            self.servicio.obtener_por_id(999)

    def test_obtener_por_id_correcto(self):
        self.repositorio.obtener_por_id.return_value = self.maquina

        resultado = self.servicio.obtener_por_id(1)

        self.assertEqual(resultado.codigo, "MAQ-001")

    # --------------------------------------------------
    # VALIDACIONES DE CARGAS
    # --------------------------------------------------

    def test_cargas_ambas_vacias(self):
        self.servicio._validar_cargas(None, None)

    def test_cargas_correctas(self):
        self.servicio._validar_cargas(
            Decimal("5.00"),
            Decimal("100.00")
        )

    def test_cargas_incompletas(self):
        with self.assertRaises(ValueError):
            self.servicio._validar_cargas(
                Decimal("5.00"),
                None
            )

    def test_carga_maxima_menor_que_minima(self):
        with self.assertRaises(ValueError):
            self.servicio._validar_cargas(
                Decimal("100.00"),
                Decimal("50.00")
            )

    # --------------------------------------------------
    # REGISTRO
    # --------------------------------------------------

    def test_registrar_codigo_existente(self):
        self.repositorio.existe_codigo.return_value = True

        with self.assertRaises(ValueError):
            self.servicio.registrar(self.maquina)

        self.repositorio.registrar.assert_not_called()

    def test_registrar_error_al_verificar_codigo(self):
        self.repositorio.existe_codigo.return_value = None

        with self.assertRaises(RuntimeError):
            self.servicio.registrar(self.maquina)

        self.repositorio.registrar.assert_not_called()

    def test_registrar_correctamente(self):
        self.repositorio.existe_codigo.return_value = False
        self.repositorio.registrar.return_value = 25

        resultado = self.servicio.registrar(self.maquina)

        self.assertEqual(resultado, 25)
        self.repositorio.registrar.assert_called_once_with(self.maquina)

    # --------------------------------------------------
    # ACTUALIZACIÓN
    # --------------------------------------------------

    def test_actualizar_sin_identificador(self):
        maquina = Maquina(
            codigo="MAQ-002",
            nombre="Press de hombros",
            fecha_alta=date.today()
        )

        with self.assertRaises(ValueError):
            self.servicio.actualizar(maquina)

    def test_actualizar_codigo_pertenece_a_otra_maquina(self):
        self.repositorio.obtener_por_id.return_value = self.maquina
        self.repositorio.existe_codigo.return_value = True

        with self.assertRaises(ValueError):
            self.servicio.actualizar(self.maquina)

        self.repositorio.actualizar.assert_not_called()

    def test_actualizar_correctamente(self):
        self.repositorio.obtener_por_id.return_value = self.maquina
        self.repositorio.existe_codigo.return_value = False
        self.repositorio.actualizar.return_value = True

        resultado = self.servicio.actualizar(self.maquina)

        self.assertTrue(resultado)
        self.repositorio.actualizar.assert_called_once_with(self.maquina)

    # --------------------------------------------------
    # CAMBIO DE ESTADO
    # --------------------------------------------------

    def test_cambiar_estado_invalido(self):
        with self.assertRaises(ValueError):
            self.servicio.cambiar_estado(1, "EN MANTENIMIENTO")

        self.repositorio.cambiar_estado.assert_not_called()

    def test_cambiar_estado_correctamente(self):
        self.repositorio.obtener_por_id.return_value = self.maquina
        self.repositorio.cambiar_estado.return_value = True

        resultado = self.servicio.cambiar_estado(1, "REPARACION")

        self.assertTrue(resultado)
        self.repositorio.cambiar_estado.assert_called_once_with(
            1,
            "REPARACION"
        )


if __name__ == "__main__":
    unittest.main()
