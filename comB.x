[Unit]
Description=Odoco Web Interface
After=network.target

[Service]
User=rpi
WorkingDirectory=/home/rpi/Odoco/www
ExecStart=/usr/bin/authbind --deep /home/rpi/Odoco/venv/bin/python3 /home/rpi/Odoco/www/app.py
Restart=always
Environment="PYTHONPATH=/home/rpi/Odoco/www"

[Install]
WantedBy=multi-user.target