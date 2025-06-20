from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import time

try:
    # Usar el bus I2C correcto (I2C2)
    i2c = I2C(2)  # Corresponde a los pines 8 (SCL) y 10 (SDA)
    
    # Detección automática de dirección
    addresses = [0x3C, 0x3D]
    oled = None
    
    for addr in addresses:
        try:
            oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=addr)
            print(f"¡Pantalla encontrada en 0x{addr:02X}!")
            break
        except Exception as e:
            print(f"Intento con 0x{addr:02X} falló: {e}")
    
    if not oled:
        raise RuntimeError("No se encontró la pantalla OLED en ninguna dirección")
    
    # Limpiar y mostrar mensaje
    oled.fill(0)
    oled.show()
    
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 16)
    except:
        font = ImageFont.load_default()
    
    draw.text((0, 0), "¡Conexión Correcta!", font=font, fill=255)
    draw.text((0, 16), "K2B I2C2 Funciona", font=font, fill=255)
    
    oled.image(image)
    oled.show()
    time.sleep(5)

except Exception as e:
    print(f"Error crítico: {e}")
    print("Verifica:")
    print("1. Conexiones físicas (pines 8 y 10)")
    print("2. Soldaduras y contactos")
    print("3. Alimentación 3.3V (pin 2)")