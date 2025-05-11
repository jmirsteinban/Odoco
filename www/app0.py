#!/usr/bin/env python3
from flask import Flask, render_template, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = '4f70f9289673603338c2dc055180c9235139bf5ab7139e3c52f2276950bd8532'  # Tu clave segura

# Ruta demo principal
@app.route('/')
def home():
    return """
    <h1>¡Odoco funciona!</h1>
    <p>Interfaz temporal en puerto 80</p>
    <p><a href="/service-admin">Ir al panel</a></p>
    """

# Ruta temporal para pruebas
@app.route('/service-admin')
def service_admin():
    return render_template('service_manager.html',
                         service_content="Demo funcionando",
                         service_status="Active (Demo Mode)",
                         service_name="odoco-web.service")

if __name__ == '__main__':
    # Ejecución con authbind para puerto 80
    os.system('authbind --deep python3 ' + __file__ + ' debug')
    app.run(host='0.0.0.0', port=80, debug=True)