

# Importamos las herramientas necesarias de Flask.
from flask import Blueprint, render_template

# Importamos el decorador que controla los permisos.
from utils.decoradores import requiere_rol


# Creamos el Blueprint del panel de administración.
admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin")
@requiere_rol("ADMIN")
def panel_administracion():
    """
    Muestra el panel de administración.

    Solamente pueden ingresar los usuarios
    que tengan el rol ADMIN.
    """

    return render_template("admin/panel.html")
