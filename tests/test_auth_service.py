

# Importamos las herramientas para realizar pruebas.
import unittest

# Importamos herramientas para simular el repositorio.
from unittest.mock import patch

# Importamos las funciones para generar hashes de contraseñas.
from werkzeug.security import generate_password_hash

# Importamos el modelo Usuario.
from models.clase_usuario import Usuario

# Importamos el servicio que vamos a probar.
from services.auth_service import AuthService


class TestAuthService(unittest.TestCase):
    """
    Prueba las reglas de negocio del servicio de autenticación.

    El repositorio se simula para evitar depender de MySQL.
    """

    def setUp(self):
        # Reemplazamos el repositorio real por uno simulado.
        self.parche = patch("services.auth_service.UsuarioRepository")

        # Activamos la simulación.
        self.repositorio_mock = self.parche.start()

        # Obtenemos la instancia simulada del repositorio.
        self.repositorio = self.repositorio_mock.return_value

        # Creamos el servicio que utilizaremos en las pruebas.
        self.servicio = AuthService()

        # Generamos un hash para utilizarlo en las pruebas.
        self.password = "Prueba2026!"
        self.password_hash = generate_password_hash(self.password)

        # Creamos un usuario de prueba activo.
        self.usuario = Usuario(
            dni="99999999",
            nombre="Usuario",
            apellido="Prueba",
            telefono="1100000000",
            email="prueba@irongym.com",
            password_hash=self.password_hash,
            rol="SOCIO",
            activo=True
        )

    def tearDown(self):
        # Desactivamos la simulación después de cada prueba.
        self.parche.stop()

    def test_autenticar_sin_email(self):
        # No debe autenticar si el correo está vacío.
        resultado = self.servicio.autenticar("", self.password)

        self.assertIsNone(resultado)

        # No debería consultar el repositorio.
        self.repositorio.obtener_por_email.assert_not_called()

    def test_autenticar_sin_password(self):
        # No debe autenticar si la contraseña está vacía.
        resultado = self.servicio.autenticar(
            "prueba@irongym.com",
            ""
        )

        self.assertIsNone(resultado)

        # No debería consultar el repositorio.
        self.repositorio.obtener_por_email.assert_not_called()

    def test_autenticar_usuario_inexistente(self):
        # Simulamos que el repositorio no encuentra al usuario.
        self.repositorio.obtener_por_email.return_value = None

        resultado = self.servicio.autenticar(
            "desconocido@irongym.com",
            self.password
        )

        self.assertIsNone(resultado)

    def test_autenticar_usuario_inactivo(self):
        # Creamos un usuario cuya cuenta está desactivada.
        usuario_inactivo = Usuario(
            dni="99999999",
            nombre="Usuario",
            apellido="Prueba",
            telefono="1100000000",
            email="prueba@irongym.com",
            password_hash=self.password_hash,
            rol="SOCIO",
            activo=False
        )

        self.repositorio.obtener_por_email.return_value = usuario_inactivo

        resultado = self.servicio.autenticar(
            "prueba@irongym.com",
            self.password
        )

        self.assertIsNone(resultado)

    def test_autenticar_password_incorrecta(self):
        # Simulamos que el usuario existe.
        self.repositorio.obtener_por_email.return_value = self.usuario

        resultado = self.servicio.autenticar(
            "prueba@irongym.com",
            "ContraseñaIncorrecta"
        )

        self.assertIsNone(resultado)

    def test_autenticar_correctamente(self):
        # Simulamos que el usuario existe.
        self.repositorio.obtener_por_email.return_value = self.usuario

        resultado = self.servicio.autenticar(
            "prueba@irongym.com",
            self.password
        )

        # Debe devolver el mismo usuario encontrado.
        self.assertIs(resultado, self.usuario)

    def test_autenticar_elimina_espacios_del_email(self):
        # Simulamos que el usuario existe.
        self.repositorio.obtener_por_email.return_value = self.usuario

        resultado = self.servicio.autenticar(
            "  prueba@irongym.com  ",
            self.password
        )

        self.assertIs(resultado, self.usuario)

        # Comprobamos que el correo se envió sin espacios.
        self.repositorio.obtener_por_email.assert_called_once_with(
            "prueba@irongym.com"
        )

    def test_obtener_por_dni_correctamente(self):
        # Simulamos que el repositorio encuentra al usuario.
        self.repositorio.obtener_por_dni.return_value = self.usuario

        resultado = self.servicio.obtener_por_dni("99999999")

        self.assertIs(resultado, self.usuario)

    def test_obtener_por_dni_usuario_inexistente(self):
        # Simulamos que el usuario no existe.
        self.repositorio.obtener_por_dni.return_value = None

        resultado = self.servicio.obtener_por_dni("99999999")

        self.assertIsNone(resultado)

    def test_obtener_por_dni_usuario_inactivo(self):
        # Creamos un usuario desactivado.
        usuario_inactivo = Usuario(
            dni="99999999",
            nombre="Usuario",
            apellido="Prueba",
            telefono="1100000000",
            email="prueba@irongym.com",
            password_hash=self.password_hash,
            rol="SOCIO",
            activo=False
        )

        self.repositorio.obtener_por_dni.return_value = usuario_inactivo

        resultado = self.servicio.obtener_por_dni("99999999")

        self.assertIsNone(resultado)


# Permite ejecutar las pruebas directamente desde este archivo.
if __name__ == "__main__":
    unittest.main()
