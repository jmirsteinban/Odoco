#!/usr/bin/env python3
import time
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

def main():
    try:
        print("Iniciando prueba OLED 0.91\" 128x32...")
        
        # 1. Intentar inicializar I2C
        try:
            i2c = board.I2C()
            print("Bus I2C inicializado correctamente")
        except Exception as e:
            print(f"Error al iniciar I2C: {e}")
            return
        
        # 2. Probar ambas direcciones posibles
        for addr in [0x3C, 0x3D]:
            try:
                print(f"\nProbando dirección 0x{addr:02X}...")
                oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=addr)
                
                # Prueba de funcionamiento
                oled.fill(0)
                oled.text("OLED Funciona!", 0, 0, 1)
                oled.text(f"Addr: 0x{addr:02X}", 0, 16, 1)
                oled.show()
                
                print("¡Pantalla OLED detectada correctamente!")
                time.sleep(5)
                return
                
            except Exception as e:
                print(f"Error en 0x{addr:02X}: {str(e)}")
        
        print("\nNo se detectó la pantalla OLED")
        
    except Exception as e:
        print(f"Error crítico: {str(e)}")
    
    print("\nSolución recomendada:")
    print("1. Verifica conexiones (SCL=Pin8, SDA=Pin10)")
    print("2. Añade resistencias pull-up (4.7KΩ en SDA/SCL a 3.3V)")
    print("3. Mide voltaje entre Pin2 (3.3V) y Pin6 (GND)")
    print("4. Prueba con otra pantalla OLED si es posible")

if __name__ == "__main__":
    main()