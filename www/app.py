from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        wifi_ssid = request.form.get('wifi_ssid')
        wifi_pass = request.form.get('wifi_password')
        # Aquí guardarías los datos en un archivo o base de datos
        return render_template('config.html', message="¡Configuración WiFi guardada!")
    return render_template('config.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)