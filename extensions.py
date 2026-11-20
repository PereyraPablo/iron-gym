

# Importamos LoginManager para administrar las sesiones.
from flask_login import LoginManager


# Creamos una instancia que podrá reutilizar toda la aplicación.
login_manager = LoginManager()

# Indicamos la ruta a la que se redirigirá
# al usuario cuando intente acceder sin iniciar sesión.
login_manager.login_view = "auth.login"

# Configuramos el mensaje para los usuarios no autenticados.
login_manager.login_message = "Debés iniciar sesión para acceder a esta sección."

# Definimos la categoría del mensaje flash.
login_manager.login_message_category = "advertencia"
