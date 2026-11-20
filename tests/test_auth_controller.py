

# Importamos las herramientas para realizar pruebas.
import unittest

# Importamos herramientas para simular objetos.
from unittest.mock import patch

# Importamos Flask y las funciones para generar hashes.
from flask import Flask
from werkzeug.security import generate_password_hash

# Importamos el modelo Usuario.
from models.clase_usuario import Usuario

# Importamos el sistema de autenticación.
from controllers.auth_controller import auth_bp
from controllers.admin_controller import admin_bp

# Importamos el Blueprint de máquinas porque la plantilla base
# utiliza sus rutas en la navegación principal.
from controllers.maquina_controller import maquinas_bp

# Importamos el administrador de sesiones.
from extensions import login_manager


class TestAuthController(unittest.TestCase):
    """
    Prueba las rutas de autenticación y el acceso
    al panel de administración.
    """

    def setUp(self):
        # Creamos la aplicación indicando dónde están las plantillas
        # y los archivos estáticos del proyecto.
        self.app = Flask(
            __name__,
            template_folder="../templates",
            static_folder="../static"
        )

        # Configuramos una clave secreta para las sesiones.
        self.app.config["SECRET_KEY"] = "clave_pruebas_iron_gym"

        # Desactivamos las notificaciones de Flask durante las pruebas.
        self.app.config["TESTING"] = True

        # Inicializamos Flask-Login.
        login_manager.init_app(self.app)

        # Registramos los Blueprints necesarios para las pruebas
        # y para resolver los enlaces de las plantillas.
        self.app.register_blueprint(auth_bp)
        self.app.register_blueprint(admin_bp)
        self.app.register_blueprint(maquinas_bp)

        # Creamos una ruta de inicio para las redirecciones.
        @self.app.route("/")
        def inicio():
            return "Página de inicio"

        # Configuramos el cliente de pruebas.
        self.cliente = self.app.test_client()

        # Generamos el hash de la contraseña de prueba.
        self.password = "Prueba2026!"
        self.password_hash = generate_password_hash(self.password)

        # Creamos un administrador de prueba.
        self.administrador = Usuario(
            dni="11111111",
            nombre="Administrador",
            apellido="Prueba",
            telefono="1100000000",
            email="admin@irongym.com",
            password_hash=self.password_hash,
            rol="ADMIN",
            activo=True
        )

        # Creamos un socio de prueba.
        self.socio = Usuario(
            dni="22222222",
            nombre="Socio",
            apellido="Prueba",
            telefono="1100000000",
            email="socio@irongym.com",
            password_hash=self.password_hash,
            rol="SOCIO",
            activo=True
        )

        # Simulamos el servicio de autenticación.
        self.parche = patch(
            "controllers.auth_controller.servicio_auth"
        )

        self.servicio_mock = self.parche.start()

    def tearDown(self):
        # Restauramos el servicio original después de cada prueba.
        self.parche.stop()

    def test_login_get_muestra_formulario(self):
        # Solicitamos la página de inicio de sesión.
        respuesta = self.cliente.get("/login")

        self.assertEqual(respuesta.status_code, 200)

    def test_login_correcto(self):
        # Simulamos una autenticación exitosa.
        self.servicio_mock.autenticar.return_value = self.administrador

        respuesta = self.cliente.post(
            "/login",
            data={
                "email": "admin@irongym.com",
                "password": self.password
            }
        )

        # Debe redirigir al inicio.
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(respuesta.location, "/")

        # Comprobamos que la sesión se haya iniciado.
        with self.cliente.session_transaction() as sesion:
            self.assertIn("_user_id", sesion)

    def test_login_incorrecto(self):
        # Simulamos credenciales incorrectas.
        self.servicio_mock.autenticar.return_value = None

        respuesta = self.cliente.post(
            "/login",
            data={
                "email": "admin@irongym.com",
                "password": "Incorrecta"
            }
        )

        # Debe permanecer en el formulario de login.
        self.assertEqual(respuesta.status_code, 200)

        # Comprobamos que se muestre el mensaje de credenciales incorrectas.
        self.assertIn(
            b"incorrectos.",
            respuesta.data
        )

    def test_administrador_accede_al_panel(self):
        # Simulamos la recuperación del administrador por DNI.
        self.servicio_mock.obtener_por_dni.return_value = self.administrador

        # Iniciamos sesión directamente para esta prueba.
        with self.cliente.session_transaction() as sesion:
            sesion["_user_id"] = self.administrador.dni
            sesion["_fresh"] = True

        respuesta = self.cliente.get("/admin")

        self.assertEqual(respuesta.status_code, 200)
        # Verificamos que se muestre el título del panel.
        self.assertIn(
            "Panel de administración".encode("utf-8"),
            respuesta.data
        )

    def test_socio_no_accede_al_panel(self):
        # Simulamos la recuperación del socio por DNI.
        self.servicio_mock.obtener_por_dni.return_value = self.socio

        # Iniciamos sesión como socio.
        with self.cliente.session_transaction() as sesion:
            sesion["_user_id"] = self.socio.dni
            sesion["_fresh"] = True

        respuesta = self.cliente.get("/admin")

        # El socio está autenticado, pero no autorizado.
        self.assertEqual(respuesta.status_code, 403)

    def test_visitante_es_redirigido_al_login(self):
        # Intentamos acceder al panel sin iniciar sesión.
        respuesta = self.cliente.get("/admin")

        self.assertEqual(respuesta.status_code, 302)
        self.assertIn("/login", respuesta.location)

    def test_logout_cierra_sesion(self):
        # Simulamos la recuperación del administrador.
        self.servicio_mock.obtener_por_dni.return_value = self.administrador

        # Iniciamos sesión.
        with self.cliente.session_transaction() as sesion:
            sesion["_user_id"] = self.administrador.dni
            sesion["_fresh"] = True

        # Solicitamos el cierre de sesión.
        respuesta = self.cliente.get("/logout")

        self.assertEqual(respuesta.status_code, 302)

        # Comprobamos que la sesión haya sido eliminada.
        with self.cliente.session_transaction() as sesion:
            self.assertNotIn("_user_id", sesion)


# Permite ejecutar las pruebas directamente desde este archivo.
if __name__ == "__main__":
    unittest.main()
