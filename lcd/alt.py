#!/usr/bin/env python3
import time
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_ssd1306

def main():
    try:
        print("Iniciando prueba de pantalla OLED...")
        
        # Intenta con ambos buses posibles
        for bus_num in [3, 5]:
            try:
                print(f"\nProbando bus I2C-{bus_num}...")
                i2c = I2C(bus_num)
                
                # Prueba ambas direcciones comunes para OLED
                for addr in [0x3C, 0x3D]:
                    try:
                        print(f"Intentando dirección 0x{addr:02X}...")
                        oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=addr)
                        
                        # Prueba de visualización
                        oled.fill(0)
                        oled.text("¡Conectado!", 0, 0, 1)
                        oled.text(f"Bus:{bus_num} 0x{addr:02X}", 0, 16, 1)
                        oled.show()
                        
                        print("¡Pantalla OLED funciona correctamente!")
                        print(f"Usando bus I2C-{bus_num}, dirección 0x{addr:02X}")
                        time.sleep(5)
                        return
                        
                    except Exception as e:
                        print(f"No respuesta en 0x{addr:02X}: {str(e)}")
                        
            except Exception as e:
                print(f"Error en bus {bus_num}: {str(e)}")
        
        print("\nNo se pudo inicializar la pantalla OLED")
        
    except Exception as e:
        print(f"Error crítico: {str(e)}")
    
    print("\nSolución recomendada:")
    print("1. Verifica conexiones físicas (pines 8-SCL, 10-SDA)")
    print("2. Añade resistencias pull-up (4.7KΩ en SDA y SCL a 3.3V)")
    print("3. Mide voltaje entre Pin 2 (3.3V) y Pin 6 (GND)")
    print("4. Prueba con otra pantalla OLED si es posible")

if __name__ == "__main__":
    main()