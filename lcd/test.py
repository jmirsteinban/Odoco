#!/usr/bin/env python3
import time
import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# Configuración específica para tu pantalla 0.91" 128x32
OLED_WIDTH = 128
OLED_HEIGHT = 32
OLED_ADDRESS = 0x3C  # La mayoría de estas pantallas usan 0x3C

def initialize_display():
    try:
        # Inicializar I2C usando los pines correctos (8 y 10)
        i2c = board.I2C()
        
        # Crear objeto OLED
        oled = adafruit_ssd1306.SSD1306_I2C(
            OLED_WIDTH, 
            OLED_HEIGHT, 
            i2c, 
            addr=OLED_ADDRESS
        )
        return oled
    except Exception as e:
        print(f"Error al inicializar: {e}")
        return None

def main():
    print("Iniciando prueba para pantalla 0.91\" 128x32...")
    
    oled = initialize_display()
    if not oled:
        print("No se pudo inicializar la pantalla")
        print("Verifique:")
        print("1. Conexiones físicas (pines 8 y 10)")
        print("2. Resistencia pull-up (4.7KΩ en SDA/SCL)")
        print("3. Voltaje entre Pin 2 (3.3V) y Pin 6 (GND)")
        return
    
    try:
        # Limpiar pantalla
        oled.fill(0)
        oled.show()
        
        # Crear imagen
        image = Image.new("1", (oled.width, oled.height))
        draw = ImageDraw.Draw(image)
        
        # Cargar fuente (tamaño adecuado para 32px de altura)
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", 12)
        except:
            font = ImageFont.load_default()
        
        # Texto centrado
        text = "0.91\" OLED OK!"
        text_width = draw.textlength(text, font=font)
        x_pos = (oled.width - text_width) // 2
        
        draw.text((x_pos, 5), text, font=font, fill=255)
        draw.text((10, 20), "KICKPI-K2B", font=font, fill=255)
        
        # Mostrar imagen
        oled.image(image)
        oled.show()
        
        print("¡Pantalla funcionando correctamente!")
        time.sleep(5)
        
    except Exception as e:
        print(f"Error durante operación: {e}")

if __name__ == "__main__":
    main()
