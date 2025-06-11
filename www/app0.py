from flask import Flask, render_template, request, redirect, url_for
import socket
import psutil  # Necesitarás instalar esta librería: pip install psutil

app = Flask(__name__)

def get_public_ip():
    try:
        # Método simple para obtener IP pública (puedes usar otro método si prefieres)
        return socket.gethostbyname(socket.gethostname())
    except:
        return "No disponible"

def get_cpu_temp():
    try:
        # Método para Raspberry Pi (puede variar según tu sistema)
        temp = psutil.sensors_temperatures()['cpu_thermal'][0].current
        return f"{temp}°C"
    except:
        return "No disponible"

@app.route('/')
def home():
    # Datos de WiFi
    wifi_data = {
        'mode': 'AP',
        'nic': 'wlan0',
        'ssid': 'MAOW 2.4G',
        'ip': '172.16.1.220'
    }
    
    # Datos de DNS
    dns_data = {
        'dnss_01': 'play.galaxite.net:19132',
        'dnss_02': 'play.craftersmc.net:19132'
    }
    
    # Datos de Raspberry Pi
    rpi_data = {
        'cpu': 'ARMv6',
        'ram': '512MB',
        'tmp': get_cpu_temp()
    }
    
    # Datos de RackNet
    rack_data = {
        'rack_01': 'play.galaxite.net:19132'
    }
    
    # Datos de Ethernet
    eth_data = {
        'mode': 'Cliente',
        'nic': 'eth0',
        'ip': '172.16.1.220'
    }
    
    # Datos de Internet
    internet_data = {
        'pub_ip': get_public_ip()
    }
    
    return render_template('index.html',
                         wifi_mode=wifi_data['mode'],
                         wifi_nic=wifi_data['nic'],
                         wifi_ssid=wifi_data['ssid'],
                         wifi_ip=wifi_data['ip'],
                         dnss_01=dns_data['dnss_01'],
                         dnss_02=dns_data['dnss_02'],
                         rpi_cpu=rpi_data['cpu'],
                         rpi_ram=rpi_data['ram'],
                         rpi_tmp=rpi_data['tmp'],
                         rack_01=rack_data['rack_01'],
                         eth_mode=eth_data['mode'],
                         eth_nic=eth_data['nic'],
                         eth_ip=eth_data['ip'],
                         pub_ip=internet_data['pub_ip'])

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        wifi_ssid = request.form.get('wifi_ssid')
        wifi_pass = request.form.get('wifi_password')
        # Aquí guardarías los datos en un archivo o base de datos
        return render_template('config.html', message="¡Configuración WiFi guardada!")
    return render_template('config.html')

@app.route('/wifi', methods=['GET', 'POST'])
def wifi():
    if request.method == 'POST':
        wifi_ssid = request.form.get('wifi_ssid')
        wifi_pass = request.form.get('wifi_password')
        # Aquí guardarías los datos en un archivo o base de datos
        return render_template('wifi.html', message="¡Configuración WiFi guardada!")
    return render_template('wifi.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)