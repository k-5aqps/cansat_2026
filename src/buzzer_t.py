import RPi.GPIO as GPIO
import time

BUZZER_PIN = 18  # GPIO18（物理ピン12）

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# PWM開始（周波数262Hz）
pwm = GPIO.PWM(BUZZER_PIN, 262)
pwm.start(50)  # デューティ比50%

time.sleep(1)  # 1秒鳴らす

pwm.stop()
GPIO.cleanup()