"""
Raspberry Pi モーターコントローラー
2モーター制御用のクラス（前進、右折、左折機能付き）
"""

import time
import RPi.GPIO as GPIO


# デフォルトのGPIOピン設定
IN1, ENA1 = 20, 21  # 左モーター
IN2, ENA2 = 12, 16  # 右モーター

PWM_FREQ = 1000  # PWM周波数 (Hz)


class MotorController:
    """2輪モーターコントローラークラス"""
    
    def __init__(self, in_left=IN1, ena_left=ENA1, in_right=IN2, ena_right=ENA2, pwm_freq=PWM_FREQ):
        """
        モーターコントローラーの初期化
        
        Args:
            in_left: 左モーターの方向制御ピン
            ena_left: 左モーターのPWMピン
            in_right: 右モーターの方向制御ピン
            ena_right: 右モーターのPWMピン
            pwm_freq: PWM周波数
        """
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        # GPIOピンの設定
        GPIO.setup(in_left, GPIO.OUT)
        GPIO.setup(ena_left, GPIO.OUT)
        GPIO.setup(in_right, GPIO.OUT)
        GPIO.setup(ena_right, GPIO.OUT)

        # PWMオブジェクトの作成と開始
        self.pwm_left = GPIO.PWM(ena_left, pwm_freq)
        self.pwm_right = GPIO.PWM(ena_right, pwm_freq)
        self.pwm_left.start(0)
        self.pwm_right.start(0)

        self.in_left = in_left
        self.in_right = in_right
        
        # 現在のデューティサイクルを保持
        self.duty_left = 0
        self.duty_right = 0
        
        # 動作中フラグ
        self.is_moving = False

    def move(self, mode, active_time, duty):
        """
        指定されたモードでモーターを動かす
        
        Args:
            mode: 動作モード ("forward", "right", "left")
            active_time: 動作時間（秒）
            duty: デューティサイクル (0-100)
        """
        self.is_moving = True
        self._set_dutycycle(mode, duty)

        stop_time = time.time() + active_time
        try:
            while time.time() < stop_time:
                if not self.is_moving:  # 強制停止チェック
                    break
                self.pwm_right.ChangeDutyCycle(self.duty_right)
                self.pwm_left.ChangeDutyCycle(self.duty_left)
                time.sleep(0.01)  # CPU負荷軽減
        finally:
            # 動作終了後は必ず停止
            self.pwm_right.ChangeDutyCycle(0)
            self.pwm_left.ChangeDutyCycle(0)
            self.duty_left = 0
            self.duty_right = 0
            self.is_moving = False
            time.sleep(0.5)  # 停止後の待機時間を短縮

    def _set_dutycycle(self, mode, duty):
        """
        モードに応じてデューティサイクルを設定（内部メソッド）
        
        Args:
            mode: 動作モード
            duty: 基準デューティサイクル
        """
        # 方向制御ピンの設定（前進方向）
        GPIO.output(self.in_left, GPIO.LOW)
        GPIO.output(self.in_right, GPIO.HIGH)
        
        if mode == "forward":
            # 前進：両輪同じ速度
            self.duty_right = duty
            self.duty_left = duty
        elif mode == "right":
            # 右折：左輪を速く、右輪を遅く
            self.duty_right = duty * 0.5
            self.duty_left = duty
        elif mode == "left":
            # 左折：右輪を速く、左輪を遅く
            self.duty_right = duty
            self.duty_left = duty * 0.4
        else:
            # 不明なモードの場合は停止
            self.duty_right = 0
            self.duty_left = 0

    def stop(self):
        """
        モーターを強制停止する
        """
        self.is_moving = False
        self.pwm_right.ChangeDutyCycle(0)
        self.pwm_left.ChangeDutyCycle(0)
        self.duty_left = 0
        self.duty_right = 0
        print("モーター停止")

    def set_speed(self, left_speed, right_speed):
        """
        左右のモーターの速度を個別に設定
        
        Args:
            left_speed: 左モーターの速度 (0-100)
            right_speed: 右モーターの速度 (0-100)
        """
        self.duty_left = max(0, min(100, left_speed))
        self.duty_right = max(0, min(100, right_speed))
        self.pwm_left.ChangeDutyCycle(self.duty_left)
        self.pwm_right.ChangeDutyCycle(self.duty_right)

    def cleanup(self):
        """
        GPIOリソースのクリーンアップ
        """
        self.stop()
        self.pwm_left.stop()
        self.pwm_right.stop()
        GPIO.cleanup()
        print("クリーンアップ完了")


def main():
    """メイン関数"""
    motor = MotorController()
    print("=" * 50)
    print("モーターコントローラー起動")
    print("=" * 50)
    print("コマンド:")
    print("  forward - 前進")
    print("  right   - 右折")
    print("  left    - 左折")
    print("  stop    - 強制停止")
    print("  quit    - 終了")
    print("=" * 50)
    
    try:
        while True:
            mode = input("\nモード: ").strip().lower()
            
            if mode == "quit" or mode == "q":
                print("プログラムを終了します")
                break
            elif mode == "stop" or mode == "s":
                motor.stop()
            elif mode in ["forward", "right", "left"]:
                # デフォルト: 2秒間、デューティサイクル40%で動作
                motor.move(mode, 2, 40)
            else:
                print(f"不明なコマンド: {mode}")
                print("forward, right, left, stop, quit のいずれかを入力してください")
    
    except KeyboardInterrupt:
        print("\n\nキーボード割り込みを検出")
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")
    finally:
        motor.cleanup()


if __name__ == '__main__':
    main()