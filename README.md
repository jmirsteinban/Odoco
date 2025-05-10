# 🦌 Odocoileus - Minecraft Bedrock Server Redirector

**Transforma una Raspberry Pi en un proxy inteligente para servidores Minecraft Bedrock Edition**  
*Controla y redirige tráfico de Minecraft mediante una interfaz web moderna*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-green.svg)](https://www.python.org/)
[![Platform: Raspberry Pi](https://img.shields.io/badge/Platform-Raspberry%20Pi-red.svg)](https://www.raspberrypi.org/)

## 🚀 Características Principales
- **Proxy RakNet Completo**: Intercepta y redirige paquetes de Minecraft Bedrock
- **Gestión Avanzada de Red**:
  - **NAT con iptables**: Redirección de puertos y enmascaramiento de IP
  - **Reglas de Firewall Persistente**: Configuración sobrevive a reinicios
- **Interfaz Web de Control**: Configuración en tiempo real desde cualquier dispositivo
- **Gestión Integrada de DNS**:  
  ```play.galaxite.net``` → ```tuserver.com```
- **Hotspot WiFi Automático**: Crea tu propia red para dispositivos móviles

## ⚙️ Arquitectura del Sistema
```mermaid
graph TD
    A[Dispositivo] -->|Conexión WiFi| B(RPi: Hotspot 192.168.50.1)
    B -->|DNS Manipulation| C{Proxy RakNet}
    C -->|iptables NAT| D[Servidor Real]
    C -->|Reglas Personalizadas| E[Opciones Avanzadas]
    F[Web Interface] -->|Control| C
    G[iptables] -->|Redirección| C
