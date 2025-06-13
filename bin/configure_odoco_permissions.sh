#!/bin/bash
# Odoco Service Permissions v1.0
# Configura permisos sudo para el servicio odoco-web sin contraseña

# --- Configuración ---
USER="rpi"
SERVICE="odoco-web.service"
SUDOERS_FILE="/etc/sudoers.d/odoco-web-permissions"
LOG_FILE="/var/log/odoco-permissions-setup.log"

# --- Funciones ---
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

check_root() {
    if [ "$(id -u)" -ne 0 ]; then
        log "ERROR: Este script debe ejecutarse como root"
        exit 1
    fi
}

verify_service() {
    if ! systemctl list-unit-files | grep -q "^$SERVICE"; then
        log "ERROR: El servicio $SERVICE no existe"
        exit 1
    fi
}

verify_user() {
    if ! id "$USER" &>/dev/null; then
        log "ERROR: El usuario $USER no existe"
        exit 1
    fi
}

configure_permissions() {
    log "Configurando permisos para $USER en $SERVICE"
    
    # Crear contenido para archivo sudoers
    SUDOERS_CONTENT="$USER ALL=(ALL) NOPASSWD: /bin/systemctl start $SERVICE, /bin/systemctl stop $SERVICE, /bin/systemctl restart $SERVICE, /bin/systemctl status $SERVICE"
    
    log "Creando archivo $SUDOERS_FILE"
    echo "$SUDOERS_CONTENT" > temp_sudoers
    
    log "Validando sintaxis sudoers"
    if ! visudo -c -f temp_sudoers; then
        log "ERROR: Sintaxis incorrecta en configuración sudoers"
        rm -f temp_sudoers
        exit 1
    fi
    
    mv temp_sudoers $SUDOERS_FILE
    chmod 440 $SUDOERS_FILE
    
    log "Permisos configurados correctamente"
}

test_permissions() {
    log "Probando permisos..."
    sudo -u $USER sudo -n systemctl status $SERVICE
    if [ $? -ne 0 ]; then
        log "ERROR: La prueba de permisos falló"
        exit 1
    fi
    log "Prueba de permisos exitosa"
}

# --- Ejecución principal ---
main() {
    check_root
    verify_user
    verify_service
    
    log "Iniciando configuración de permisos para $SERVICE"
    
    configure_permissions
    test_permissions
    
    log "Configuración completada exitosamente"
    echo "Los permisos se han configurado correctamente para el usuario $USER"
    echo "Detalles registrados en $LOG_FILE"
}

main