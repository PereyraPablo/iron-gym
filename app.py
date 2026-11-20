

# Importamos Flask para crear nuestra aplicación web.
from flask import Flask, render_template

# Importamos la configuración centralizada del proyecto.
from config import Config

# Importamos los Blueprints de los controladores.
from controllers.maquina_controller import maquinas_bp
from controllers.auth_controller import auth_bp
from controllers.admin_controller import admin_bp

# Importamos el administrador de sesiones de Flask-Login.
from extensions import login_manager



# ---------------------------------------------------------
# CONFIGURACIÓN DE LA APLICACIÓN
# ---------------------------------------------------------

# Creamos la instancia principal de nuestra aplicación Flask.
app = Flask(__name__)

# Incorporamos las configuraciones definidas en config.py.
app.config.from_object(Config)

# Inicializamos Flask-Login con nuestra aplicación.
# Esto permite administrar las sesiones de los usuarios.
login_manager.init_app(app)


# ---------------------------------------------------------
# REGISTRO DE BLUEPRINTS
# ---------------------------------------------------------

# Registramos el Blueprint del catálogo de máquinas.
app.register_blueprint(maquinas_bp)

# Registramos el Blueprint de autenticación.
# Incorpora las rutas de inicio y cierre de sesión.
app.register_blueprint(auth_bp)

# Registramos el Blueprint de Admin.
app.register_blueprint(admin_bp)


# ---------------------------------------------------------
# RUTA PRINCIPAL
# ---------------------------------------------------------

@app.route("/")
def inicio():

    # Renderiza la plantilla principal del sitio web.
    # inicio.html hereda la estructura de base.html.
    return render_template("inicio.html")


@app.errorhandler(403)
def acceso_denegado(error):
    """
    Muestra una página personalizada cuando un usuario
    intenta acceder a una sección sin los permisos necesarios.
    """

    return render_template("403.html"), 403


# ---------------------------------------------------------
# INICIO DEL SERVIDOR
# ---------------------------------------------------------

if __name__ == "__main__":

    # Activamos el servidor en modo desarrollo.
    app.run(debug=True)
