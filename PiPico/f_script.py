from machine import Pin
import time

pin = Pin(25, Pin.OUT)
but = Pin(28, Pin.IN)
old_but = but.value()
while True:
    if old_but != but.value():
        pin.toggle()
    time.sleep_ms(10)