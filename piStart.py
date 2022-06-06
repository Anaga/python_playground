from machine import Pin
import time

pin10 = Pin(10, Pin.OUT)
pin11 = Pin(11, Pin.OUT)
pin12 = Pin(12, Pin.OUT)
pin13 = Pin(13, Pin.OUT)

pList = (pin10, pin11, pin12, pin13)
pList2 = (pin13, pin12, pin11, pin10)

def allOn():
    for p in pList:
        p.off()
        
def foo():
    for p in pList:
        p.toggle()
        print("pin %s have %d value"%(p, p.value()))
        time.sleep(1)

allOn()

while True:
    foo()
    time.sleep(1)