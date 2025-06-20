#!/usr/bin/env python3
import time
import smbus2
from PIL import Image

# Configuración para KICKPI-K2B
I2C_BUS = 5  # Usar bus 5 (pines 8 y 10)
OLED_ADDR = 0x3C  # Prueba también con 0x3D si no funciona
OLED_WIDTH = 128
OLED_HEIGHT = 32

# Comandos básicos SSD1306
OLED_SET_CONTRAST = 0x81
OLED_DISPLAY_ON = 0xAF
OLED_DISPLAY_OFF = 0xAE
OLED_SET_PAGE_ADDR = 0x22
OLED_SET_COL_ADDR = 0x21

class OLED_SSD1306:
    def __init__(self, bus, address):
        self.bus = bus
        self.address = address
        self._initialize()
    
    def _write_command(self, cmd):
        try:
            self.bus.write_byte_data(self.address, 0x00, cmd)
        except Exception as e:
            print(f"Error escribiendo comando: {e}")

    def _initialize(self):
        self._write_command(OLED_DISPLAY_OFF)
        self._write_command(OLED_SET_CONTRAST)
        self._write_command(0xCF)  # Contraste
        self._write_command(OLED_DISPLAY_ON)
        self.clear()
    
    def clear(self):
        self._write_command(OLED_SET_COL_ADDR)
        self._write_command(0)
        self._write_command(OLED_WIDTH - 1)
        self._write_command(OLED_SET_PAGE_ADDR)
        self._write_command(0)
        self._write_command(3)  # 32px = 4 páginas (0-3)
        
        for _ in range(0, OLED_WIDTH * 4):
            self.bus.write_byte_data(self.address, 0x40, 0x00)
    
    def show_image(self, image):
        if image.size != (OLED_WIDTH, OLED_HEIGHT):
            raise ValueError("Imagen debe ser 128x32 pixeles")
        
        self._write_command(OLED_SET_COL_ADDR)
        self._write_command(0)
        self._write_command(OLED_WIDTH - 1)
        self._write_command(OLED_SET_PAGE_ADDR)
        self._write_command(0)
        self._write_command(3)
        
        pixels = list(image.getdata())
        for i in range(0, len(pixels), OLED_WIDTH):
            page = pixels[i:i+OLED_WIDTH]
            packed_data = []
            for j in range(0, OLED_WIDTH, 8):
                byte = 0
                for k in range(8):
                    if j+k < OLED_WIDTH and page[j+k]:
                        byte |= (1 << k)
                packed_data.append(byte)
            
            self.bus.write_i2c_block_data(self.address, 0x40, packed_data)

def main():
    try:
        bus = smbus2.SMBus(I2C_BUS)
        oled = OLED_SSD1306(bus, OLED_ADDR)
        
        # Crear imagen de prueba
        image = Image.new("1", (OLED_WIDTH, OLED_HEIGHT))
        draw = ImageDraw.Draw(image)
        draw.text((10, 5), "KICKPI-K2B", fill=1)
        draw.text((20, 20), "OLED 0.91\"", fill=1)
        
        oled.show_image(image)
        print("¡Pantalla OLED funcionando correctamente!")
        time.sleep(5)
        oled.clear()
        
    except Exception as e:
        print(f"Error: {e}")
        print("Soluciones posibles:")
        print("1. Verifica conexiones (SCL=Pin8, SDA=Pin10)")
        print("2. Añade resistencias pull-up de 4.7KΩ")
        print("3. Prueba con dirección 0x3D")
        print("4. Verifica voltaje de 3.3V en la pantalla")

if __name__ == "__main__":
    from PIL import ImageDraw  # Import aquí para evitar error si fallan imports previos
    main()