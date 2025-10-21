import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

IN1 = 20
ENA1 = 21

IN2 = 12
ENA2 = 16

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(ENA1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA2, GPIO.OUT)

pwm1 = GPIO.PWM(ENA1, 1000)
pwm2 = GPIO.PWM(ENA2, 1000)
pwm1.start(0)
pwm2.start(0)

dy=float(input("Duty:"))

def forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.HIGH)
    pwm1.ChangeDutyCycle(dy)
    pwm2.ChangeDutyCycle(dy)

def backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm1.ChangeDutyCycle(dy)
    pwm2.ChangeDutyCycle(dy)

def stop():
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(0)

try:
    while True:
        cmd = input("Command [f: forward, b: backward, s: stop, q: quit] > ").strip().lower()

        if cmd == "f":
            forward()
        elif cmd == "b":
            backward()
        elif cmd == "s":
            stop()
        elif cmd == "q":
            break
        else:
            print("Unknown command")

except KeyboardInterrupt:
    pass

finally:
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()