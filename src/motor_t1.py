import time
import pigpio

IN1, ENA1 = 20, 21
IN2, ENA2 = 12, 16

PWM_FREQ = 1000  # Hz

class MotorController:
    def __init__(self, in_left=IN1, ena_left=ENA1, in_right=IN2, ena_right=ENA2, pwm_freq=PWM_FREQ):
        self.pi = pigpio.pi()
        if not self.pi.connected:
            raise RuntimeError("pigpioデーモンに接続できません")

        self.in_left = in_left
        self.in_right = in_right
        self.ena_left = ena_left
        self.ena_right = ena_right

        # ピンを出力設定
        self.pi.set_mode(self.in_left, pigpio.OUTPUT)
        self.pi.set_mode(self.in_right, pigpio.OUTPUT)
        self.pi.set_mode(self.ena_left, pigpio.OUTPUT)
        self.pi.set_mode(self.ena_right, pigpio.OUTPUT)

        # PWM周波数設定
        self.pi.set_PWM_frequency(self.ena_left, pwm_freq)
        self.pi.set_PWM_frequency(self.ena_right, pwm_freq)

        # 初期停止
        self.pi.set_PWM_dutycycle(self.ena_left, 0)
        self.pi.set_PWM_dutycycle(self.ena_right, 0)

    def move(self, mode, active_time, duty):
        self.dutycycle(mode, duty)

        stop_time = time.time() + active_time
        while time.time() < stop_time:
            self.pi.set_PWM_dutycycle(self.ena_right, self.duty_right)
            self.pi.set_PWM_dutycycle(self.ena_left, self.duty_left)
            time.sleep(0.01)

        start_time=time.time()

        while time.time()-start_time<1:
            if mode == "forward":
                boost_duty = int(75)

                self.pi.write(self.in_left, 0)
                self.pi.write(self.in_right, 0)

                self.pi.set_PWM_dutycycle(self.ena_right, boost_duty)
                self.pi.set_PWM_dutycycle(self.ena_left, boost_duty)

        self.stop()
        time.sleep(1)

    def dutycycle(self, mode, duty,):
        self.pi.write(self.in_left, 0)
        self.pi.write(self.in_right, 0)

        # pigpioは0-255
        duty = int(duty * 255 / 100)

        if mode == "forward":
            self.duty_right = duty
            self.duty_left = duty
        elif mode == "right":
            self.duty_right = duty
            self.duty_left = int(duty * 0.8)
        elif mode == "left":
            self.duty_right = int(duty * 0.8)
            self.duty_left = duty
        else:
            self.duty_right = 0
            self.duty_left = 0

    def stop(self):
        self.pi.set_PWM_dutycycle(self.ena_left, 0)
        self.pi.set_PWM_dutycycle(self.ena_right, 0)

    def cleanup(self):
        self.stop()
        self.pi.stop()


def main():
    motor = MotorController()
    print("forward,right,left")

    try:
        while True:
            mode = input("mode:")
            motor.move(mode, 3, 50)

    except KeyboardInterrupt:
        print("終了")

    finally:
        motor.cleanup()


if __name__ == '__main__':
    main()
