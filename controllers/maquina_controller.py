

# Importamos Blueprint para agrupar las rutas relacionadas con máquinas.
from flask import Blueprint, render_template

# Importamos el servicio que contiene las reglas de negocio.
from services.maquina_service import MaquinaService


# Creamos un Blueprint para organizar las rutas del módulo de máquinas.
# El nombre "maquinas" identifica este grupo de rutas dentro de Flask.
maquinas_bp = Blueprint("maquinas", __name__)

# Creamos una instancia del servicio que utilizará el controlador.
servicio_maquinas = MaquinaService()


# ---------------------------------------------------------
# CATÁLOGO PÚBLICO DE MÁQUINAS
# ---------------------------------------------------------

@maquinas_bp.route("/maquinas")
def catalogo():

    # Solicitamos al servicio únicamente las máquinas activas.
    # El controlador no realiza consultas SQL directamente.
    maquinas = servicio_maquinas.listar_activas()

    # Enviamos las máquinas obtenidas a la plantilla HTML.
    return render_template(
        "maquinas/catalogo.html",
        maquinas=maquinas
    )
