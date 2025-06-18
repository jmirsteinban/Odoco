#!/usr/bin/env python3
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return """
    <h1>¡Odoco funciona!</h1>
    <p>Demo básica en puerto 80</p>
    <p><a href="/status">Ver estado</a></p>
    """

@app.route('/status')
def status():
    return {"status": "active", "service": "odoco-web"}

if __name__ == '__main__':
    # Ejecución directa (usando authbind para puerto 80)
    os.system('authbind --deep python3 ' + __file__ + ' debug')
    app.run(host='0.0.0.0', port=80)