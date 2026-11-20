

# Importamos las herramientas necesarias para manejar las rutas.
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

# Importamos las funciones de Flask-Login.
from flask_login import login_user, logout_user, login_required

# Importamos el servicio de autenticación.
from services.auth_service import AuthService

# Importamos el administrador de sesiones.
from extensions import login_manager


# Creamos el Blueprint de autenticación.
auth_bp = Blueprint("auth", __name__)

# Creamos una instancia del servicio.
servicio_auth = AuthService()


# ---------------------------------------------------------
# RECUPERACIÓN DEL USUARIO
# ---------------------------------------------------------

@login_manager.user_loader
def cargar_usuario(dni):
    """
    Recupera un usuario mediante su DNI.

    Flask-Login ejecuta esta función cuando necesita
    recuperar al usuario almacenado en una sesión.
    """

    return servicio_auth.obtener_por_dni(dni)


# ---------------------------------------------------------
# INICIO DE SESIÓN
# ---------------------------------------------------------

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    # Si el usuario ya inició sesión, lo enviamos al inicio.
    from flask_login import current_user

    if current_user.is_authenticated:
        return redirect(url_for("inicio"))

    # Procesamos los datos cuando se envía el formulario.
    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        # Solicitamos al servicio que valide las credenciales.
        usuario = servicio_auth.autenticar(email, password)

        if usuario is not None:

            # Iniciamos la sesión del usuario.
            login_user(usuario)

            flash(
                f"¡Bienvenido/a, {usuario.nombre}!",
                "exito"
            )

            return redirect(url_for("inicio"))

        # Mostramos un mensaje si las credenciales son incorrectas.
        flash(
            "El correo electrónico o la contraseña son incorrectos.",
            "error"
        )

    # Mostramos el formulario de inicio de sesión.
    return render_template("auth/login.html")


# ---------------------------------------------------------
# CIERRE DE SESIÓN
# ---------------------------------------------------------

@auth_bp.route("/logout")
@login_required
def logout():

    # Cerramos la sesión del usuario actual.
    logout_user()

    flash("Cerraste sesión correctamente.", "exito")

    return redirect(url_for("inicio"))
