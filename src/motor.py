import time
import RPi.GPIO as GPIO

IN1, ENA1 = 20, 21
IN2, ENA2 = 12, 16

PWM_FREQ     = 1000  # Hz

class MotorController:
    def __init__(self, in_left=IN1, ena_left=ENA1, in_right=IN2, ena_right=ENA2, pwm_freq=PWM_FREQ):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(in_left,  GPIO.OUT)
        GPIO.setup(ena_left, GPIO.OUT)
        GPIO.setup(in_right, GPIO.OUT)
        GPIO.setup(ena_right,GPIO.OUT)

        self.pwm_left  = GPIO.PWM(ena_left,  pwm_freq)
        self.pwm_right = GPIO.PWM(ena_right, pwm_freq)
        self.pwm_left.start(0)
        self.pwm_right.start(0)

        self.in_left  = in_left
        self.in_right = in_right

    def move(self,mode,active_time,duty):
        self.dutycycle(mode,duty)

        stop_time = time.time() + active_time
        while time.time() < stop_time:
            self.right.ChangeDutyCycle(self.right_duty)
            self.left.ChangeDutyCycle(self.left_duty)

        self.right.ChangeDutyCycle(0)
        self.left.ChangeDutyCycle(0)
        time.sleep(1)

    def dutycycle(self,mode,duty):
        GPIO.output(self.in_left,  GPIO.HIGH)
        GPIO.output(self.in_right, GPIO.HIGH)
        if mode=="forward":
            self.duty_right=duty
            self.duty_left=duty
        elif mode=="right":
            self.duty_right=duty*0.5
            self.duty_left=duty
        elif mode=="left":
            self.duty_right=duty
            self.duty_left=duty*0.5
        else:
            self.duty_right=self.duty_left=0

    def cleanup(self):
        GPIO.cleanup()

def main():
    motor=MotorController()
    print("forward,right,left")
    try:
        while True:
            mode=input("mode:")
            motor.move(mode,3,100)
    except KeyboardInterrupt:
        motor.cleanup()

if __name__=='__main__':
    main()