import socket
import time
from rpi_ws281x import PixelStrip, Color
from multiprocessing import Process, Value



LED_COUNT = 30        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def rainbow_leds(led_count, led_pin, run_flag):
    
    strip = PixelStrip(led_count, led_pin, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    def wheel(pos):
        if pos < 0 or pos > 255:
            return Color(0, 0, 0)
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        if pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

    while run_flag.value:
        for j in range(led_count):
            strip.setPixelColor(j, wheel((int(j * 256 / led_count) + int(time.time() * 10)) & 255))
        strip.show()
        time.sleep(10/1000.0)

def flash_red(led_count, led_pin):

    strip = PixelStrip(led_count, led_pin, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    for i in range(led_count):
        strip.setPixelColor(i, Color(255, 0, 0))
    strip.show()

    time.sleep(5)

def run_leds(led_count, led_pin):
    host = ''
    port = 12345
    buf = 1024

    addr = (host, port)
    UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPSock.bind(addr)

    run_flag = Value('i', 1)
    p = Process(target=rainbow_leds, args=(led_count, led_pin, run_flag,))
    p.start()

    print("Running rainbow_leds by default... Waiting for commands...")

    while True:
        (data, addr) = UDPSock.recvfrom(buf)
        data = data.decode()
        if data == "flash":
            run_flag.value = 0
            flash_red(led_count, led_pin)
            run_flag.value = 1
            p = Process(target=rainbow_leds, args=(led_count, led_pin, run_flag,))
            p.start()

run_leds(30,18)
