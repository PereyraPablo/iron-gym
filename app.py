

# Importamos Flask para crear nuestra aplicación web.
from flask import Flask, render_template

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

    # Renderiza la plantilla principal del sitio web.
    # inicio.html hereda la estructura de base.html.
    return render_template("inicio.html")


# ---------------------------------------------------------
# INICIO DEL SERVIDOR
# ---------------------------------------------------------

if __name__ == "__main__":

    # Activamos el servidor en modo desarrollo.
    app.run(debug=True)
