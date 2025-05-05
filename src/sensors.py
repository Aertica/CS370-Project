import math
from datetime import datetime, timezone
from gpiozero import Button
import adafruit_dht
import threading

class Anemometer:
    def __init__(self, pin):
        self.pin = pin
        self.current_speed = 0

    def start(self):
        print(threading.current_thread())
        self.button = Button(self.pin)
        self.button.when_pressed = self.on_spin
        self.button.when_activated
        self.last_spin = None
        self.current_spin = None
        self.current_speed = 0

    def on_spin(self):
        self.last_spin = self.current_spin
        self.current_spin = datetime.now(timezone.utc)
        if self.last_spin is not None:
            time = self.current_spin - self.last_spin
            if time.seconds == 0 and time.microseconds < 1000:
                return
            seconds = time.seconds + (time.microseconds / 1000000.0)
            radius = 0.092
            self.current_speed = math.pi * radius / seconds

class Temp:
    def __init__(self, pin):
        self.dht_device = adafruit_dht.DHT11(pin)

    def temp_c(self):
        return self.dht_device.temperature
    
    def temp_f(self):
        return self.temp_c() * (9 / 5) + 32
    
    def humidity(self):
        return self.dht_device.humidity
