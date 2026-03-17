from picamera2 import Picamera2
import time
import cv2
import numpy as np
from logwrite import MyLogging   # 追加

class CameraModule:
    def __init__(self):
        self.log = MyLogging()   # ログ初期化
        self.log.write("Camera Init Start", "INFO")

        try:
            self.picam2 = Picamera2()
            self.picam2.configure(
                self.picam2.create_still_configuration(
                    main={"size": (1280, 720)}
                )
            )
            self.cnt = 0
            self.picam2.start()
            self.log.write("Camera Startup Success", "INFO")

        except Exception as e:
            self.log.write(f"Camera Init Failed: {e}", "ERROR")
            raise

    def cap(self):
        try:
            time.sleep(1)
            img = self.picam2.capture_array()
            img = cv2.flip(img, -1)

            self.cnt += 1

            img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            self.save_bgr(img_bgr)

            self.log.write(f"Shooting Success, count:{self.cnt}", "DEBUG")

            return img_bgr

        except Exception as e:
            self.log.write(f"Sooting Error: {e}", "ERROR")
            return None

    def save_bgr(self, img_bgr):
        try:
            path = f"/home/pi/cansat_2026/img/{self.cnt}.jpg"
            cv2.imwrite(path, img_bgr)
            self.log.write(f"Save Success", "DEBUG")
        except Exception as e:
            self.log.write(f"Save Failed: {e}", "ERROR")

    def end(self):
        try:
            self.picam2.stop()
            self.picam2.close()
            self.log.write("Camera Close", "INFO")
        except Exception as e:
            self.log.write(f"Camera Close Eroor: {e}", "ERROR")


def main():
    log = MyLogging()
    log.write("CameraModule テスト開始", "INFO")

    camera = CameraModule()

    try:
        while True:
            img = camera.cap()

            if img is None:
                log.write("画像取得失敗", "WARNING")

            a = int(input("もう一度:1、終了:ctrl+c"))
            if a == 1:
                continue

    except KeyboardInterrupt:
        log.write("KeyboardInterrupt により終了", "INFO")

    except Exception as e:
        log.write(f"予期せぬエラー: {e}", "CRITICAL")

    finally:
        camera.end()
        log.write("プログラム終了", "INFO")


if __name__ == "__main__":
    main()