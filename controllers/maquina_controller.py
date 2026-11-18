

# Importamos las herramientas necesarias de Flask.
from flask import Blueprint, render_template, request, abort

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

    # Obtenemos el identificador del grupo muscular enviado por la URL.
    # Si el parámetro no existe o llega vacío, mostramos todas las máquinas.
    id_grupo = request.args.get("id_grupo") or None

    # Obtenemos los grupos musculares activos para mostrarlos en el filtro.
    grupos = servicio_maquinas.listar_grupos_activos()

    # Si no se seleccionó un grupo, mostramos todas las máquinas activas.
    if id_grupo is None:

        maquinas = servicio_maquinas.listar_activas()

    else:

        # Convertimos el identificador recibido desde la URL a entero.
        # Los parámetros de una URL siempre llegan inicialmente como texto.
        try:
            id_grupo = int(id_grupo)

        except ValueError:
            # Rechazamos identificadores que no sean números enteros.
            abort(400)

        # Consultamos las máquinas activas asociadas al grupo seleccionado.
        # El servicio se encarga de validar el identificador.
        try:
            maquinas = servicio_maquinas.listar_activas_por_grupo(id_grupo)

        except ValueError:
            # Si el identificador no es válido, respondemos con error 400.
            abort(400)

    # Enviamos los datos necesarios a la plantilla HTML.
    return render_template(
        "maquinas/catalogo.html",
        maquinas=maquinas,
        grupos=grupos,
        id_grupo=id_grupo
    )
