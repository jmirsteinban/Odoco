#!/bin/bash
# Odoco AP Config v3.2 - Versión Final

# --- Configuración ---
AP_NAME="OdocoAP"
AP_SSID="Odoco"
AP_PASSWORD="Odoco2024"
AP_IP="192.168.4.1/24"
AP_CHANNEL="6"

# --- 1. Detener servicios y limpiar ---
sudo systemctl stop dhcpcd dnsmasq hostapd
sudo systemctl mask dhcpcd dnsmasq hostapd
sudo systemctl enable --now NetworkManager

# --- 2. Liberar interfaz wlan0 ---
sudo nmcli con down "preconfigured" 2>/dev/null
sudo nmcli con del "preconfigured" 2>/dev/null
sudo nmcli con del "$AP_NAME" 2>/dev/null
sudo ip addr flush dev wlan0
sudo rfkill unblock wlan

# --- 3. Configurar AP ---
sudo nmcli con add type wifi ifname wlan0 con-name "$AP_NAME" \
  ipv4.method shared \
  ipv4.addresses "$AP_IP" \
  wifi.mode ap wifi.ssid "$AP_SSID" \
  wifi.band bg wifi.channel "$AP_CHANNEL" \
  wifi-sec.key-mgmt wpa-psk wifi-sec.psk "$AP_PASSWORD"

# --- 4. Configurar NAT y forwarding ---
sudo sysctl -w net.ipv4.ip_forward=1
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf

sudo iptables -t nat -F
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT

sudo apt-get install -y iptables-persistent
sudo netfilter-persistent save

# --- 5. Activar conexión ---
sudo systemctl restart NetworkManager
sudo nmcli con up "$AP_NAME"

echo -e "\n✔ Access Point configurado correctamente"
echo -e "SSID: $AP_SSID"
echo -e "IP: $AP_IP"
echo -e "Contraseña: $AP_PASSWORD"