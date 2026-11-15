

# Importamos Flask para crear nuestra aplicación web.
from flask import Flask

# Importamos la configuración centralizada del proyecto.
from config import Config


# Creamos la instancia principal de nuestra aplicación Flask.
app = Flask(__name__)

# Incorporamos las configuraciones definidas en config.py.
app.config.from_object(Config)


# ---------------------------------------------------------
# RUTA PRINCIPAL
# ---------------------------------------------------------

@app.route("/")
def inicio():
    """
    Ruta principal de Iron Gym.

    Por ahora devuelve un mensaje sencillo para comprobar
    que el servidor Flask funciona correctamente.
    Posteriormente mostraremos nuestra página de inicio.
    """

    return """
        <h1>IRON GYM</h1>
        <h2>¡Bienvenido a nuestro gimnasio!</h2>
        <p>La aplicación Flask está funcionando correctamente.</p>
    """


# ---------------------------------------------------------
# INICIO DEL SERVIDOR
# ---------------------------------------------------------

if __name__ == "__main__":

    # Activamos el servidor en modo desarrollo.
    app.run(debug=True)
