from picamera2_camera import CameraModule
from img_dtc import Detect
from motor_t1 import MotorController
from logwrite import MyLogging  # 追加
import config
import time


class CameraPhase:
    def __init__(self):
        self.camera = CameraModule()
        self.detector = Detect()
        self.motor = MotorController()
        self.log = MyLogging()  # ログ機能の初期化

    def run(self):
        self.log.write("CameraPhaseを開始します", "INFO")
        try:
            while True:
                # ===== 撮影 =====
                img = self.camera.cap()

                # ===== 画像判定 =====
                result = self.detector.dtc_img(img)
                
                # コンソールとログの両方に出力
                log_msg = f"判定結果: {result}"
                self.log.write(log_msg, "INFO")

                # ===== モータ制御（config使用）=====
                if result in ["left", "forward", "right"]:
                    active_time = 2.0 if result == "forward" else 0.5
                    
                    self.log.write(f"モータ動作: {result} (時間: {active_time}s)", "DEBUG")
                    
                    self.motor.move(
                        mode=result,
                        active_time=active_time,
                        duty=config.MOTOR_DUTY
                    )
                
                elif result == "goal":
                    msg = "ゴールに到達しました"
                    self.log.write(msg, "INFO")
                    # 必要に応じてここで break して終了させることも検討してください
                    break

                elif result=="not find":
                    self.log.write("not find error","WARNING")

                    self.motor.move(
                        mode=result,
                        active_time=0.5,
                        duty=50)

                else:
                    self.log.write(f"不明な判定結果: {result}", "WARNING")
                    self.motor.stop()
                    # time.sleepをスキップせずに一定時間待機するためcontinueは削除、または調整
                
                time.sleep(config.SLEEP_TIME)

        except KeyboardInterrupt:
            msg = "キーボード割り込みにより終了します"
            self.log.write(msg, "WARNING")

        except Exception as e:
            err_msg = f"致命的なエラーが発生しました: {e}"
            self.log.write(err_msg, "ERROR")

        finally:
            self.camera.end()
            self.motor.cleanup()
            self.log.write("プロセスを正常にクリーンアップしました", "INFO")


def main():
    phase = CameraPhase()
    phase.run()


if __name__ == "__main__":
    main()