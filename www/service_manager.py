import subprocess
import os
from datetime import datetime

class ServiceManager:
    def __init__(self, service_name, service_file, system_service_file, backup_file):
        self.service_name = service_name
        self.service_file = service_file
        self.system_service_file = system_service_file
        self.backup_file = backup_file
        
        # Crear directorios si no existen
        os.makedirs(os.path.dirname(self.service_file), exist_ok=True)
        os.makedirs(os.path.dirname(self.backup_file), exist_ok=True)

    def get_service_content(self):
        try:
            with open(self.service_file, 'r') as f:
                return f.read()
        except FileNotFoundError:
            # Si el archivo no existe, devolver contenido por defecto
            return """[Unit]
Description=Odoco Web Interface
After=network.target

[Service]
User=rpi
WorkingDirectory=/home/rpi/Odoco/www
ExecStart=/usr/bin/gunicorn --bind 0.0.0.0:80 --workers 1 app:app
Restart=always
Environment="PYTHONPATH=/home/rpi/Odoco/www"

[Install]
WantedBy=multi-user.target"""

    def save_service_file(self, content):
        # Crear backup antes de guardar
        if os.path.exists(self.service_file):
            with open(self.backup_file, 'w') as f:
                f.write(self.get_service_content())
        
        with open(self.service_file, 'w') as f:
            f.write(content)

    def apply_changes(self, content):
        # Guardar el archivo
        self.save_service_file(content)
        
        # Copiar al directorio systemd
        self._copy_to_systemd()
        
        # Recargar daemon
        self.reload_daemon()
        
        # Reiniciar el servicio
        self.restart_service()

    def _copy_to_systemd(self):
        # Copiar el archivo de servicio al directorio systemd
        subprocess.run(['sudo', 'cp', self.service_file, self.system_service_file], check=True)
        subprocess.run(['sudo', 'chmod', '644', self.system_service_file], check=True)
        
        # Habilitar el servicio para que se inicie al arrancar
        subprocess.run(['sudo', 'systemctl', 'enable', self.service_name], check=True)

    def get_service_status(self):
        try:
            result = subprocess.run(['systemctl', 'status', self.service_name], 
                                  capture_output=True, text=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return e.output

    def stop_service(self):
        subprocess.run(['sudo', 'systemctl', 'stop', self.service_name], check=True)

    def start_service(self):
        subprocess.run(['sudo', 'systemctl', 'start', self.service_name], check=True)

    def restart_service(self):
        subprocess.run(['sudo', 'systemctl', 'restart', self.service_name], check=True)

    def reload_daemon(self):
        subprocess.run(['sudo', 'systemctl', 'daemon-reload'], check=True)

    def get_service_logs(self, lines=100):
        try:
            result = subprocess.run(['journalctl', '-u', self.service_name, '-n', str(lines), '--no-pager'], 
                                  capture_output=True, text=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return e.output