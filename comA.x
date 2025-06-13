# Odocoileus virginianus v1.0
#
# odoco-web.service
#

[Unit]
Description=Odoco Web Interface
After=network.target

[Service]
User=rpi
WorkingDirectory=/home/rpi/Odoco/www
ExecStart=/home/rpi/Odoco/venv/bin/gunicorn --bind 0.0.0.0:8080 --workers 1 app:app
Restart=always
Environment="PYTHONPATH=/home/rpi/Odoco/www"