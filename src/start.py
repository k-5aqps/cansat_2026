#gpio 19.26
import time
from logwrite import MyLogging

import RPi.GPIO as GPIO

st_pin=19
in_pin=26

log = MyLogging()

def awaiting():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(st_pin,GPIO.OUT)
    GPIO.setup(in_pin,GPIO.IN)
    GPIO.output(st_pin,GPIO.HIGH)

    while True:
        value=GPIO.input(in_pin)
        if value==0:
            log.write("Start Program","INFO")
            break
        print("waiting")
        time.sleep(1)
    time.sleep(25)
    return

def main():
    awaiting()

if __name__=='__main__':
    main()
