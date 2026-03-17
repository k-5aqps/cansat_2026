import pigpio
import time

BUZZER_PIN = 18

class BUZZER:
    def __init__(self):
        self.pi = pigpio.pi()
        if not self.pi.connected:
            print("pigpio接続失敗")
            exit()

    def beep(self, buzzer_time, buzzer_hz):
        # self.pi.set_PWM_frequency(BUZZER_PIN, buzzer_hz)
        # self.pi.set_PWM_dutycycle(BUZZER_PIN, 250)
        self.pi.hardware_PWM(BUZZER_PIN,buzzer_hz,500000)
        time.sleep(buzzer_time)
        self.pi.set_PWM_dutycycle(BUZZER_PIN, 0)

    def cleanup(self):
        self.pi.stop()