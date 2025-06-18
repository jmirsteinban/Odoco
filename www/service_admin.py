#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import subprocess
from service_manager import ServiceManager

app = Flask(__name__)
app.secret_key = 'cambia_esta_clave_por_una_segura_y_unica'  # ¡Importante cambiar esto!

# Configuración
INSTALL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICE_NAME = "odoco-web.service"
SERVICE_FILE = f"{INSTALL_DIR}/etc/systemd/system/odoco-web.service"
SYSTEM_SERVICE_FILE = f"/etc/systemd/system/{SERVICE_NAME}"
BACKUP_FILE = f"{INSTALL_DIR}/etc/systemd/system/odoco-web.service.bak"

service_manager = ServiceManager(SERVICE_NAME, SERVICE_FILE, SYSTEM_SERVICE_FILE, BACKUP_FILE)

@app.route('/')
def home():
    """Redirige al panel de administración"""
    return redirect(url_for('service_admin'))

@app.route('/service-admin')
def service_admin():
    service_content = service_manager.get_service_content()
    service_status = service_manager.get_service_status()
    return render_template('service_manager.html',
                         service_content=service_content,
                         service_status=service_status,
                         service_name=SERVICE_NAME)

@app.route('/service-admin/save', methods=['POST'])
def save():
    new_content = request.form['service_content']
    service_manager.save_service_file(new_content)
    flash('Configuración guardada (no aplicada)', 'info')
    return redirect(url_for('service_admin'))

@app.route('/service-admin/apply', methods=['POST'])
def apply():
    new_content = request.form['service_content']
    service_manager.apply_changes(new_content)
    flash('Cambios aplicados y servicio reiniciado', 'success')
    return redirect(url_for('service_admin'))

@app.route('/service-admin/action/<action>')
def service_action(action):
    if action == 'stop':
        service_manager.stop_service()
        flash('Servicio detenido', 'info')
    elif action == 'start':
        service_manager.start_service()
        flash('Servicio iniciado', 'success')
    elif action == 'restart':
        service_manager.restart_service()
        flash('Servicio reiniciado', 'success')
    elif action == 'reload':
        service_manager.reload_daemon()
        flash('Daemon recargado', 'info')
    return redirect(url_for('service_admin'))

@app.route('/service-admin/logs')
def show_logs():
    logs = service_manager.get_service_logs()
    return render_template('service_manager.html',
                         service_content=service_manager.get_service_content(),
                         service_status=service_manager.get_service_status(),
                         service_name=SERVICE_NAME,
                         logs=logs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)