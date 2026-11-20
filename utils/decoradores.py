

from functools import wraps

from flask import abort
from flask_login import current_user, login_required


def requiere_rol(*roles_permitidos):
    """
    Restringe el acceso a una ruta según el rol del usuario.

    Primero comprueba que el usuario haya iniciado sesión.
    Después verifica si su rol está autorizado.

    Ejemplo:
        @requiere_rol("ADMIN")
        def panel_administracion():
            ...
    """

    # Normalizamos los roles para evitar diferencias entre mayúsculas
    # y minúsculas al definir los permisos.
    roles = {rol.upper() for rol in roles_permitidos}

    # No tiene sentido crear una autorización sin roles.
    if not roles:
        raise ValueError("Debe especificarse al menos un rol permitido.")

    def decorador(funcion):

        # login_required exige que el usuario esté autenticado.
        @wraps(funcion)
        @login_required
        def envoltura(*args, **kwargs):

            # Comprobamos si el rol del usuario está autorizado.
            if current_user.rol.upper() not in roles:

                # HTTP 403: el usuario está autenticado,
                # pero no tiene permisos para acceder.
                abort(403)

            return funcion(*args, **kwargs)

        return envoltura

    return decorador
