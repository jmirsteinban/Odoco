#!/usr/bin/env python3
import smbus
import time

# Configuración
I2C_BUS = 5  # Cambia a 3 si es necesario
OLED_ADDRESS = 0x3C  # Prueba también con 0x3D

# Comandos básicos para OLED SSD1306
OLED_DISPLAY_OFF = 0xAE
OLED_DISPLAY_ON = 0xAF
OLED_NORMAL_DISPLAY = 0xA6
OLED_ENTIRE_DISPLAY_ON = 0xA4
OLED_SET_CONTRAST = 0x81
OLED_SET_PAGE_ADDR = 0x22
OLED_SET_COL_ADDR = 0x21

def write_command(bus, cmd):
    bus.write_byte_data(OLED_ADDRESS, 0x00, cmd)

def initialize_oled(bus):
    write_command(bus, OLED_DISPLAY_OFF)
    write_command(bus, OLED_SET_CONTRAST)
    write_command(bus, 0xCF)  # Valor de contraste
    write_command(bus, OLED_NORMAL_DISPLAY)
    write_command(bus, OLED_ENTIRE_DISPLAY_ON)
    write_command(bus, OLED_DISPLAY_ON)

def clear_screen(bus):
    write_command(bus, OLED_SET_COL_ADDR)
    write_command(bus, 0)     # Columna inicio
    write_command(bus, 127)    # Columna fin
    write_command(bus, OLED_SET_PAGE_ADDR)
    write_command(bus, 0)      # Página inicio
    write_command(bus, 7)      # Página fin
    
    # Limpiar toda la pantalla
    for _ in range(0, 128*8):
        bus.write_byte_data(OLED_ADDRESS, 0x40, 0x00)

def main():
    try:
        bus = smbus.SMBus(I2C_BUS)
        initialize_oled(bus)
        clear_screen(bus)
        
        # Escribir texto simple (modo gráfico básico)
        # Esta es una implementación muy simple para prueba
        write_command(bus, OLED_SET_COL_ADDR)
        write_command(bus, 0)
        write_command(bus, 127)
        write_command(bus, OLED_SET_PAGE_ADDR)
        write_command(bus, 0)
        write_command(bus, 0)
        
        # Patrón de prueba (primeras 16 columnas)
        for i in range(16):
            bus.write_byte_data(OLED_ADDRESS, 0x40, 0xFF if i % 2 else 0x00)
        
        print("¡Prueba de pantalla OLED completada!")
        time.sleep(2)
        clear_screen(bus)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Soluciones posibles:")
        print("1. Verifica el número de bus I2C (actual: {I2C_BUS})")
        print("2. Prueba con otra dirección OLED (0x3C o 0x3D)")
        print("3. Asegúrate de tener los permisos I2C (sudo usermod -aG i2c $USER)")
        print("4. Verifica las conexiones físicas")

if __name__ == "__main__":
    main()