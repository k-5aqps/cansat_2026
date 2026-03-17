from picamera2 import CameraModule
from img_dtc import Detect
from motor_t1 import MotorController
import config
import time


class CameraPhase:
    def __init__(self):
        self.camera = CameraModule()
        self.detector = Detect()
        self.motor = MotorController()

    def run(self):
        try:
            while True:
                # ===== 撮影 =====
                img = self.camera.cap()

                # ===== 画像判定 =====
                result = self.detector.dtc_img(img)
                print("判定結果:", result)

                # ===== モータ制御（config使用）=====
                if result in ["left", "forward", "right"]:
                    self.motor.move(
                        mode=result,
                        active_time=2.0 if result == "forward" else 0.5,
                        duty=config.MOTOR_DUTY
                    )
                else:
                    self.motor.stop()
                    continue

                if result=="end":
                    print("ゴール")
                    pass

                time.sleep(config.SLEEP_TIME)

        except KeyboardInterrupt:
            print("終了します")

        except Exception as e:
            print("エラー:", e)

        finally:
            self.camera.end()
            self.motor.cleanup()


def main():
    phase = CameraPhase()
    phase.run()


if __name__ == "__main__":
    main()